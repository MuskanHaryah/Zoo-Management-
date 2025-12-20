// Scroll Indicator - Hide when user scrolls
document.addEventListener('DOMContentLoaded', function() {
  const scrollIndicator = document.getElementById('scrollIndicator');
  
  if (!scrollIndicator) {
    return;
  }
  
  // Hide scroll indicator when user scrolls
  window.addEventListener('scroll', function() {
    const scrollY = window.scrollY || window.pageYOffset;
    
    if (scrollY > 20) {
      scrollIndicator.classList.add('hidden');
    } else {
      scrollIndicator.classList.remove('hidden');
    }
  });
  
  // Optional: Click on indicator to scroll smoothly
  scrollIndicator.addEventListener('click', function() {
    window.scrollTo({
      top: window.innerHeight * 0.6,
      behavior: 'smooth'
    });
  });
});
