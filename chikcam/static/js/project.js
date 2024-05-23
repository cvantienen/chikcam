document.addEventListener('DOMContentLoaded', function() {
  // Bounce effect for Title
  anime({
    targets: '#bounce_title', // Updated to match the ID in your HTML
    translateY: [-50, 0],
    opacity: [0, 1],
    easing: 'easeOutBounce',
    duration: 1100, // Adjust the duration as needed
    delay: 0 // Starts immediately
  });

  // Fizzle effect for content, starts 1 second after the title
  anime({
    targets: '#fizzle_title_1', // Updated to match the ID in your HTML
    opacity: [0, 1],
    scale: [0.95, 1],
    easing: 'easeInOutQuad',
    duration: 1500, // Adjust the duration as needed
    delay: 1000 // Starts 1 second after the title animation
  });

    // Fizzle effect for content, starts 1 second after the title
  anime({
    targets: '#fizzle_title_2', // Updated to match the ID in your HTML
    opacity: [0, 1],
    scale: [0.95, 1],
    easing: 'easeInOutQuad',
    duration: 1500, // Adjust the duration as needed
    delay: 2000 // Starts 1 second after the title animation
  });

  // Fizzle effect for buttons, starts 1 second after the content
  anime({
    targets: '.btn.rounded-pill',
    opacity: [0, 1],
    scale: [0.95, 1],
    easing: 'easeInOutQuad',
    duration: 1800, // Adjust the duration as needed
    delay: 2500 // Starts 1 second after the content animation
  });
});
