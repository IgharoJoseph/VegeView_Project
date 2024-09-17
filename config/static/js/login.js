document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.login-form');
    
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Basic validation for email and password
        if (!validateEmail(email)) {
            alert('Please enter a valid email address!');
            return;
        }

        if (!password) {
            alert('Password cannot be empty!');
            return;
        }

    });
});

document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.menu-button');
    const nav = document.querySelector('.nav');

    menuButton.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuButton.classList.toggle('active');
    });
});

// Function to validate email format
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
