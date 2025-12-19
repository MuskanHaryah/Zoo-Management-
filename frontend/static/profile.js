// Clock functionality
function updateTime() {
  const options = {
    timeZone: 'Asia/Karachi',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  };
  const formatter = new Intl.DateTimeFormat('en-GB', options);
  document.getElementById('current-time').textContent = formatter.format(new Date());
}



// Task management functionality
document.addEventListener('DOMContentLoaded', function () {
  // Initialize variables
  const popup = document.getElementById('taskPopup');
  const completeBtn = document.getElementById('completeTaskBtn');
  let currentTaskId = null;
  
  // Initialize clock
  updateTime();
  setInterval(updateTime, 1000);

  // Count and update pending tasks counter
  const updateActiveTaskCount = function() {
    // Reset counter
    let pendingCount = 0;
    
    // Look for tasks directly in the .task-list section instead of .task-container
    document.querySelectorAll('.task-list .task-card').forEach(card => {
      const statusElem = card.querySelector('.status');
      const computedStyle = window.getComputedStyle(card);
      
      // Only count visible pending tasks
      if (computedStyle.display !== 'none' && 
          statusElem && 
          statusElem.textContent.toLowerCase().includes('pending')) {
        pendingCount++;
      }
      });
    
    // Update the count in the UI
    const activeTaskCountElement = document.getElementById('activeTaskCount');
    if (activeTaskCountElement) {
      activeTaskCountElement.textContent = pendingCount;
    }
  };
  
  // Run the count update
  updateActiveTaskCount();

  // Hide all non-pending tasks
  document.querySelectorAll('.task-card').forEach(card => {
    const statusElem = card.querySelector('.status');
    if (statusElem && !statusElem.textContent.toLowerCase().includes('pending')) {
      card.style.display = 'none';
    }
  });

  // Call updateActiveTaskCount again after hiding tasks
  updateActiveTaskCount();

  // Add popup close button listener
  const taskCloseBtn = document.querySelector('#taskPopup .popup-close');
  if (taskCloseBtn) {
    taskCloseBtn.addEventListener('click', function() {
      popup.style.display = 'none';
    });
  }

  // Close popup when clicking outside of it
  // if (popup) {
  //   popup.addEventListener('click', function (e) {
  //     if (e.target === popup) {
  //       popup.style.display = 'none';
  //     }
  //   });
  // }

  // Add click event to all task cards
  document.querySelectorAll('.task-card').forEach(card => {
    card.addEventListener('click', function (e) {
      // Ignore clicks on action buttons
      if (e.target.closest('.action-button') || e.target.closest('.view-task-btn')) {
        return;
      }

      const taskCard = this;
      currentTaskId = taskCard.dataset.taskId;

      // Fetch task details from backend
      fetch(`/tasks/${currentTaskId}/`)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(task => {
          console.log("Task data:", task); // Debug log
          
          document.getElementById('popup-animal-name').textContent = task.animal.name;
          document.getElementById('popup-description').textContent = task.description;
          document.getElementById('popup-status').textContent = task.status;

          // Format assigned date
          const assignedDate = new Date(task.date_assigned);
          document.getElementById('popup-assigned').textContent = formatDateTime(assignedDate);

          // Format deadline if it exists
          if (task.deadline) {
            const deadlineDate = new Date(task.deadline);
            const deadlineElement = document.getElementById('popup-deadline');
            deadlineElement.textContent = formatDateTime(deadlineDate);

            // Add deadline styling based on urgency
            const now = new Date();
            const timeUntilDeadline = deadlineDate - now;
            const daysUntilDeadline = timeUntilDeadline / (1000 * 60 * 60 * 24);

            deadlineElement.classList.remove('deadline-normal', 'deadline-warning', 'deadline-danger');
            if (timeUntilDeadline < 0) {
              deadlineElement.classList.add('deadline-danger');
            } else if (daysUntilDeadline < 2) {
              deadlineElement.classList.add('deadline-warning');
            } else {
              deadlineElement.classList.add('deadline-normal');
            }
          } else {
            document.getElementById('popup-deadline').textContent = 'Not available';
          }

          // Disable complete button if task is already completed
          completeBtn.disabled = task.status.toLowerCase() === 'completed';

          // Add completion status class to popup
          const popupContainer = document.querySelector('.popup-container');
          popupContainer.classList.remove('status-pending', 'status-in-progress', 'status-completed');
          popupContainer.classList.add('status-' + task.status.toLowerCase());

          // Show popup with animation
          popup.style.display = 'flex';
          popup.style.opacity = '0';
          setTimeout(() => {
            popup.style.opacity = '1';
          }, 10);
        })
        .catch(error => {
          console.error('Error fetching task details:', error);

          // Fallback: Display data available in the card
          const animalName = taskCard.querySelector('h3').textContent;
          const description = taskCard.querySelector('.task-description').textContent;
          const status = taskCard.querySelector('.status') ?
            taskCard.querySelector('.status').textContent.trim() : 'Pending';
          const assigned = taskCard.querySelector('.assigned-date') ?
            taskCard.querySelector('.assigned-date').textContent.trim() : 'Not available';

          document.getElementById('popup-animal-name').textContent = animalName;
          document.getElementById('popup-description').textContent = description;
          document.getElementById('popup-status').textContent = status;
          document.getElementById('popup-assigned').textContent = assigned;
          document.getElementById('popup-deadline').textContent = 'Not available';

          completeBtn.disabled = status.toLowerCase().includes('completed');

          popup.style.display = 'flex';
        });
    });
  });

  // View task button functionality
  document.querySelectorAll('.view-task-btn').forEach(button => {
    button.addEventListener('click', function (e) {
      e.stopPropagation();
      const taskCard = this.closest('.task-card');
      taskCard.click();
    });
  });

  // Handle marking task as complete
  completeBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    if (!currentTaskId) return;

    // Get current date and time for submission
    const submissionTime = new Date();
    
    // Send request to mark task as complete
    fetch(`/tasks/${currentTaskId}/complete/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        submission_date: submissionTime.toISOString()
      })
    })
    .then(response => {
      if (response.ok) {
        // Update UI
        const taskCard = document.querySelector(`.task-card[data-task-id="${currentTaskId}"]`);
        const statusElement = taskCard.querySelector('.status');

         // In the complete task handler, after updating the status
if (statusElement) {
          statusElement.classList.remove('status-pending', 'status-in-progress');
          statusElement.classList.add('status-completed');
          statusElement.innerHTML = '<i class="fas fa-circle"></i> Completed';
          
          // Update submission date in the popup
          const submissionDateElement = document.createElement('div');
          submissionDateElement.className = 'task-detail';
          submissionDateElement.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span class="label">Submitted:</span>
            <span id="popup-submitted" class="datetime-value">${formatDateTime(submissionTime)}</span>
          `;
          
          // Add submission date to popup if not already present
          const popupBody = document.querySelector('.popup-body');
          if (!document.getElementById('popup-submitted')) {
            popupBody.appendChild(submissionDateElement);
          } else {
            document.getElementById('popup-submitted').textContent = formatDateTime(submissionTime);
          }
          
          // Hide the completed task since we're only showing pending tasks
          taskCard.style.display = 'none';
        }

        // Update the count
        updateActiveTaskCount();


           // Update popup
        document.getElementById('popup-status').textContent = 'Completed';
        completeBtn.disabled = true;

        // Update popup container class
        const popupContainer = document.querySelector('.popup-container');
        popupContainer.classList.remove('status-pending', 'status-in-progress');
        popupContainer.classList.add('status-completed');

        // Add visual feedback
        taskCard.style.animation = 'flash-success 1s';
        setTimeout(() => {
          taskCard.style.animation = '';
        }, 1000);
      } else {
        throw new Error('Failed to update task');
      }
    })
    .catch(error => {
      console.error('Error completing task:', error);
      alert('Could not mark task as complete. Please try again.');
    });
  });


  // Rejected Tasks Functionality
  const rejectedTasksPopup = document.getElementById('rejectedTasksPopup');
  const viewRejectedBtn = document.getElementById('viewRejectedBtn');
  const rejectedTasksList = document.getElementById('rejectedTasksList');
  const noRejectedTasks = document.getElementById('noRejectedTasks');

  // Open rejected tasks popup
  if (viewRejectedBtn) {
    viewRejectedBtn.addEventListener('click', function () {
      console.log('View rejected button clicked'); // Debug log
      
      // Show loading state
      rejectedTasksList.innerHTML = `
        <div class="loading-indicator">
          <div class="spinner"></div>
          <p>Loading rejected tasks...</p>
        </div>
      `;
      noRejectedTasks.style.display = 'none';

      // Display popup
      rejectedTasksPopup.style.display = 'flex';

      // Fetch rejected tasks
      console.log('Fetching rejected tasks'); // Debug log
      fetch('/tasks/rejected/')
        .then(response => {
          console.log('Response status:', response.status); // Debug log
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(tasks => {
          console.log('Received tasks:', tasks); // Debug log
          
          // Clear loading indicator
          rejectedTasksList.innerHTML = '';

          if (tasks.length === 0) {
            // Show no tasks message
            noRejectedTasks.style.display = 'block';
          } else {
            // Create task elements
            tasks.forEach(task => {
              const taskElement = createRejectedTaskElement(task);
              rejectedTasksList.appendChild(taskElement);
            });
          }
        })
        .catch(error => {
          console.error('Error fetching rejected tasks:', error);
          rejectedTasksList.innerHTML = `
            <div class="error-message">
              <i class="fas fa-exclamation-circle"></i>
              <p>Failed to load rejected tasks. Please try again.</p>
            </div>
          `;
        });
    });
  } else {
    console.error('View rejected button not found'); // Debug log
  }

  // Close rejected tasks popup
  const rejectedCloseBtn = document.querySelector('#rejectedTasksPopup .popup-close');
  if (rejectedCloseBtn) {
    rejectedCloseBtn.addEventListener('click', function () {
      rejectedTasksPopup.style.display = 'none';
    });
  }

  // Close popup when clicking outside of it
  if (rejectedTasksPopup) {
    rejectedTasksPopup.addEventListener('click', function (e) {
      if (e.target === rejectedTasksPopup) {
        rejectedTasksPopup.style.display = 'none';
      }
    });
  }
});

// Helper function to format date and time
function formatDateTime(date) {
  if (!date) return 'Not specified';

  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };

  return date.toLocaleString('en-US', options);
}

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Helper function to create rejected task element
function createRejectedTaskElement(task) {
  const taskElement = document.createElement('div');
  taskElement.className = 'rejected-task-item';

  const submissionDate = task.submission_date ?
    formatDateTime(new Date(task.submission_date)) : 'Not submitted';

  taskElement.innerHTML = `
    <h3>${task.animal.name}</h3>
    <p>${task.description}</p>
    <div class="reason">
      <strong>Rejected</strong>
    </div>
    <div class="rejected-task-meta">
      <span><i class="fas fa-calendar-check"></i> Submitted: ${submissionDate}</span>
    </div>
  `;

  return taskElement;
}

