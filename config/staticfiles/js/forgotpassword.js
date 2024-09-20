// Toggle the mobile menu
document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.menu-button');
    const nav = document.querySelector('.nav');

    menuButton.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuButton.classList.toggle('active');
    });
});

// Form submission (optional: handle form submission)
document.querySelector('.forgot-password-form').addEventListener('submit', function (event) {
    event.preventDefault();
    alert('Password reset link has been sent to your email.');
});

