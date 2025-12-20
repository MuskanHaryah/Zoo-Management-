// Copy to Clipboard Function (must be global for inline onclick)
function copyToClipboard(text, button) {
  navigator.clipboard.writeText(text).then(function() {
    // Show success feedback
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i>';
    button.classList.add('copied');
    
    // Reset after 2 seconds
    setTimeout(function() {
      button.innerHTML = originalHTML;
      button.classList.remove('copied');
    }, 2000);
  }).catch(function(err) {
    console.error('Failed to copy:', err);
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i>';
    button.classList.add('copied');
    
    setTimeout(function() {
      button.innerHTML = originalHTML;
      button.classList.remove('copied');
    }, 2000);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  // Get the selection cards
  const visitorCard = document.getElementById('visitor-card');
  const caretakerCard = document.getElementById('caretaker-card');
  
  // Add click event listeners to the cards (with null checks)
  if (visitorCard) {
    visitorCard.addEventListener('click', function() {
      // Add clicked animation class
      visitorCard.classList.add('card-clicked');
      
      // After animation completes, redirect to visitor page
      setTimeout(() => {
        window.location.href = '/visitor/';
      }, 700);
    });
  } else {
    console.error('Visitor card element not found');
  }
  
  if (caretakerCard) {
    caretakerCard.addEventListener('click', function() {
      // Add clicked animation class
      caretakerCard.classList.add('card-clicked');
      
      // After animation completes, redirect to caretaker login
      setTimeout(() => {
        window.location.href = '/caretaker/login/';
      }, 700);
    });
  } else {
    console.error('Caretaker card element not found');
  }

  
  // Create silhouette images as needed
  createSilhouetteImages();
  
  // Add floating bubbles
  createFloatingElements();
});

function createSilhouetteImages() {
  // If the silhouette images don't exist yet, you'd create them here 
  // This is just a placeholder function
  console.log("Silhouette images would be created if needed");
}

function createFloatingElements() {
  const container = document.querySelector('.background-elements');
  const numBubbles = 15;
  
  for (let i = 0; i < numBubbles; i++) {
    const bubble = document.createElement('div');
    bubble.className = 'floating-bubble';
    
    // Random sizing and positioning
    const size = Math.floor(Math.random() * 30) + 10;
    const left = Math.floor(Math.random() * 100);
    const animDuration = Math.floor(Math.random() * 15) + 10;
    const delay = Math.floor(Math.random() * 10);
    
    bubble.style.width = size + 'px';
    bubble.style.height = size + 'px';
    bubble.style.left = left + '%';
    bubble.style.animationDuration = animDuration + 's';
    bubble.style.animationDelay = delay + 's';
    
    container.appendChild(bubble);
  }
}

// Add CSS styles for the card-clicked class
const style = document.createElement('style');
style.textContent = `
  @keyframes cardClick {
    0% { transform: scale(1); }
    50% { transform: scale(0.9); }
    100% { transform: scale(1.1); opacity: 0; }
  }
  
  .card-clicked {
    animation: cardClick 0.7s forwards;
  }
  
  .floating-bubble {
    position: absolute;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    bottom: -100px;
    animation: floatUp linear infinite;
  }
  
  @keyframes floatUp {
    0% { 
      transform: translateY(0) rotate(0);
      opacity: 0;
    }
    10% { 
      opacity: 0.5;
    }
    90% {
      opacity: 0.5;
    }
    100% { 
      transform: translateY(-100vh) rotate(360deg);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
