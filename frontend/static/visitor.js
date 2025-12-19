// Core functions for Mulan Zoofari website
document.addEventListener('DOMContentLoaded', function() {
    // Initialize navigation
    initNavigation();
    
    // Initialize back to top button
    initBackToTop();
    
    // Initialize animal data
    initAnimalData();
    
    // Initialize ticket calculation
    initTicketCalculation();
    
    // Initialize countdown for events
    initCountdown();
    
    // Initialize map interactions
    initMapInteractions();
    
    // Initialize animated hero elements
    initAnimatedHero();
});

// Animated hero function with emojis removed
function initAnimatedHero() {
    const heroContent = document.querySelector('.hero-content');
    if (!heroContent) return;
    
    // Create style element for animations (keeping text glow but removing emojis)
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        @keyframes textGlow {
            0% { text-shadow: 0 0 15px rgba(164, 214, 94, 0.3), 0 0 5px rgba(255,255,255,0.3); }
            100% { text-shadow: 0 0 25px rgba(164, 214, 94, 0.7), 0 0 15px rgba(255,255,255,0.5); }
        }
        
        .welcome-text-glow {
            animation: textGlow 3s infinite alternate;
        }
    `;
    document.head.appendChild(styleElement);
    
    // Apply text glow effect to welcome text (if it exists)
    const welcomeText = document.querySelector('.mega-welcome');
    if (welcomeText) {
        welcomeText.classList.add('welcome-text-glow');
    }
    
    // Add animation to tagline
    const tagline = document.querySelector('.hero p');
    if (tagline) {
        tagline.style.animation = 'fadeIn 1.5s ease-out';
    }
}

// Navigation functions
function initNavigation() {
    const mainNav = document.querySelector('.main-nav');
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    // Scroll effect for navigation
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            mainNav.classList.add('scrolled');
        } else {
            mainNav.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    navLinks.classList.remove('active');
                }
            }
        });
    });
}

// Back to top button
function initBackToTop() {
    const backToTopButton = document.getElementById('back-to-top');
    
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.classList.add('active');
            } else {
                backToTopButton.classList.remove('active');
            }
        });
        
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Animal data initialization
function initAnimalData() {
    const animalsGrid = document.querySelector('.animals-grid');
    if (!animalsGrid) return;
    
    // Sample animal data - in a real app, this would come from your backend
    const animals = [
        {
            name: 'African Elephant',
            scientificName: 'Loxodonta africana',
            type: 'mammals',
            origin: 'Africa',
            imageUrl: 'elephant.png',
            description: 'The largest land animal, known for its intelligence and social behavior.'
        },
        {
            name: 'Bengal Tiger',
            scientificName: 'Panthera tigris tigris',
            type: 'mammals',
            origin: 'India',
            imageUrl: 'tiger.png',
            description: 'A majestic big cat with distinctive orange coat and black stripes.'
        },
        {
            name: 'Red Macaw',
            scientificName: 'Ara macao',
            type: 'birds',
            origin: 'Central and South America',
            imageUrl: 'macaw.jpg',
            description: 'Known for its vibrant red, yellow, and blue feathers.'
        },
        {
            name: 'Lion',
            scientificName: 'Panthera leo',
            type: 'mammals',
            origin: 'Africa',
            imageUrl: 'lion.png',
            description: 'Known as the "king of the jungle", lions are apex predators.'
        },
        {
            name: 'Giant Panda',
            scientificName: 'Ailuropoda melanoleuca',
            type: 'mammals',
            origin: 'China',
            imageUrl: 'panda.png',
            description: 'Beloved for its distinct black and white coloring.'
        },
        {
            name: 'Giraffe',
            scientificName: 'Giraffa camelopardalis',
            type: 'mammals',
            origin: 'Africa',
            imageUrl: 'Giraffe.png',
            description: 'The tallest living terrestrial animal.'
        },
        {
            name: 'Western Lowland Gorilla',
            scientificName: 'Gorilla gorilla gorilla',
            type: 'mammals',
            origin: 'Central Africa',
            imageUrl: 'Gorilla.png',
            description: 'The most numerous and widespread of all gorilla subspecies.'
        }
    ];
    
    // Display all animals at once
    displayAnimals(animals, animalsGrid);
}

// Display animals function
function displayAnimals(animals, container) {
    animals.forEach(animal => {
        const animalCard = document.createElement('div');
        animalCard.className = 'animal-card';
        animalCard.dataset.type = animal.type;
        
        animalCard.innerHTML = `
            <div class="animal-image">
                <img src="${window.STATIC_URLS.imageBase + animal.imageUrl}" alt="${animal.name}">
                <div class="animal-type">${animal.type}</div>
            </div>
            <div class="animal-info">
                <h3>${animal.name}</h3>
                <div class="animal-scientific-name">${animal.scientificName}</div>
                <div class="animal-origin"><i class="fas fa-globe-africa"></i> ${animal.origin}</div>
                <p class="animal-facts">${animal.description}</p>
            </div>
        `;
        
        container.appendChild(animalCard);
        
        // Add click event for modal
        animalCard.addEventListener('click', function() {
            showAnimalModal(animal);
        });
    });
}

// Show animal modal
function showAnimalModal(animal) {
    // Create modal if it doesn't exist
    let modal = document.querySelector('.animal-modal');
    
    if (!modal) {
        modal = document.createElement('div');
        modal.className = 'animal-modal';
        document.body.appendChild(modal);
    }
    
    modal.innerHTML = `
        <div class="animal-modal-content">
            <span class="close-modal">&times;</span>
            <div class="animal-modal-header">
                <h2>${animal.name}</h2>
                <div>${animal.scientificName}</div>
            </div>
            <div class="animal-modal-body">
                <div class="animal-modal-image">
                    <img src="${window.STATIC_URLS.imageBase + animal.imageUrl}" alt="${animal.name}">
                </div>
                <div class="animal-modal-info">
                    <div class="info-item">
                        <strong>Type:</strong> ${animal.type}
                    </div>
                    <div class="info-item">
                        <strong>Origin:</strong> ${animal.origin}
                    </div>
                    <div class="info-item">
                        <strong>Description:</strong> ${animal.description}
                    </div>
                    <div class="conservation-status">
                        <strong>Conservation Status:</strong>
                        <div class="status-indicator">Vulnerable</div>
                    </div>
                </div>
            </div>
            <div class="animal-modal-footer">
                <button class="btn btn-primary">Learn More</button>
            </div>
        </div>
    `;
    
    modal.classList.add('show');
    
    // Close modal functionality
    const closeModal = modal.querySelector('.close-modal');
    closeModal.addEventListener('click', function() {
        modal.classList.remove('show');
    });
    
    // Close when clicking outside the modal
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });
}

// Map interactions
function initMapInteractions() {
    const mapPoints = document.querySelectorAll('.map-point');
    
    mapPoints.forEach(point => {
        // Show tooltip on hover
        point.addEventListener('mouseenter', function() {
            const tooltip = this.querySelector('.map-tooltip');
            if (tooltip) {
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateY(0)';
            }
        });
        
        // Hide tooltip when mouse leaves
        point.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.map-tooltip');
            if (tooltip) {
                tooltip.style.opacity = '0';
                tooltip.style.transform = 'translateY(10px)';
            }
        });
        
        // Show info on click
        point.addEventListener('click', function() {
            const tooltip = this.querySelector('.map-tooltip');
            const title = tooltip.querySelector('h4').textContent;
            const description = tooltip.querySelector('p').textContent;
            
            showLocationInfo(title, description, this.getBoundingClientRect());
        });
    });
    
    function showLocationInfo(title, description, rect) {
        // Create or update location info popup
        let infoPopup = document.querySelector('.location-info-popup');
        
        if (!infoPopup) {
            infoPopup = document.createElement('div');
            infoPopup.className = 'location-info-popup';
            document.body.appendChild(infoPopup);
        }
        
        infoPopup.innerHTML = `
            <div class="info-popup-header">
                <h3>${title}</h3>
                <span class="close-popup">&times;</span>
            </div>
            <div class="info-popup-content">
                <p>${description}</p>
                <button class="btn btn-sm">See Photos</button>
            </div>
        `;
        
        // Position popup near the clicked point
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        infoPopup.style.top = (rect.top + scrollTop - 120) + 'px';
        infoPopup.style.left = (rect.left + rect.width / 2 - 150) + 'px';
        
        infoPopup.classList.add('show');
        
        // Close popup functionality
        const closePopup = infoPopup.querySelector('.close-popup');
        closePopup.addEventListener('click', function() {
            infoPopup.classList.remove('show');
        });
        
        // Close when clicking outside
        document.addEventListener('click', function closeOutside(e) {
            if (!infoPopup.contains(e.target) && !e.target.closest('.map-point')) {
                infoPopup.classList.remove('show');
                document.removeEventListener('click', closeOutside);
            }
        });
    }
}

// Ticket calculation
function initTicketCalculation() {
    const ticketForm = document.getElementById('ticket-booking-form');
    const ticketInputs = document.querySelectorAll('.ticket-quantity');
    const totalPriceElement = document.getElementById('total-price');
    
    if (ticketForm && ticketInputs.length > 0 && totalPriceElement) {
        // Update total price when quantities change
        ticketInputs.forEach(input => {
            input.addEventListener('change', updateTotalPrice);
        });
        
        // Form submission
        ticketForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const visitDate = document.getElementById('visit-date').value;
            const adultTickets = parseInt(document.getElementById('adult-tickets').value) || 0;
            const childTickets = parseInt(document.getElementById('child-tickets').value) || 0;
            const seniorTickets = parseInt(document.getElementById('senior-tickets').value) || 0;
            
            const totalTickets = adultTickets + childTickets + seniorTickets;
            
            if (!visitDate) {
                alert('Please select a visit date.');
                return;
            }
            
            if (totalTickets === 0) {
                alert('Please select at least one ticket.');
                return;
            }
            
            // Show booking confirmation (in a real app, this would submit to server)
            showBookingConfirmation();
        });
        
        function updateTotalPrice() {
            let total = 0;
            
            document.querySelectorAll('.ticket-type').forEach(ticketType => {
                const price = parseFloat(ticketType.dataset.price);
                const quantity = parseInt(ticketType.querySelector('.ticket-quantity').value) || 0;
                total += price * quantity;
            });
            
            totalPriceElement.textContent = '$' + total.toFixed(2);
        }
        
        function showBookingConfirmation() {
            const ticketBooking = document.querySelector('.ticket-booking');
            
            // Generate random booking reference
            const bookingRef = 'MZ-' + Math.random().toString(36).substring(2, 8).toUpperCase();
            
            ticketBooking.innerHTML = `
                <div class="booking-confirmation">
                    <div class="confirmation-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h3>Booking Confirmed!</h3>
                    <p>Your tickets have been booked successfully. A confirmation email will be sent shortly.</p>
                    <div class="booking-reference">
                        Booking Reference: ${bookingRef}
                    </div>
                    <button class="btn btn-primary" onclick="location.reload()">Book More Tickets</button>
                </div>
            `;
        }
    }
}

// Countdown timer for events
function initCountdown() {
    const countdownElements = document.querySelectorAll('.countdown');
    
    countdownElements.forEach(countdown => {
        const targetDate = new Date(countdown.dataset.date).getTime();
        
        // Calculate initial values based on current date (including the mocked date if provided)
        // Using the current date from the page metadata if available (May 11, 2025)
        const currentDate = new Date('2025-05-11T21:27:37');
        const now = currentDate.getTime();
        const initialDistance = targetDate - now;
        updateCountdownDisplay(initialDistance, countdown);
        
        // Update the countdown every 1 second
        const countdownTimer = setInterval(function() {
            // In real environment, this would use new Date().getTime()
            // But for demo, we'll increment from our mocked date
            const updatedTime = currentDate.setSeconds(currentDate.getSeconds() + 1);
            const distance = targetDate - updatedTime;
            
            updateCountdownDisplay(distance, countdown);
            
            // If the countdown is finished
            if (distance < 0) {
                clearInterval(countdownTimer);
                countdown.innerHTML = '<div class="event-happening-now">Happening Now!</div>';
            }
        }, 1000);
    });
    
    function updateCountdownDisplay(distance, countdown) {
        // Time calculations
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        // Display the result
        countdown.querySelector('#countdown-days').textContent = days.toString().padStart(2, '0');
        countdown.querySelector('#countdown-hours').textContent = hours.toString().padStart(2, '0');
        countdown.querySelector('#countdown-minutes').textContent = minutes.toString().padStart(2, '0');
        countdown.querySelector('#countdown-seconds').textContent = seconds.toString().padStart(2, '0');
    }
}