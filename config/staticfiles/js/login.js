document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.login-form');
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');

    // Clear the fields immediately when the page loads
    emailField.value = '';
    passwordField.value = '';

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = emailField.value;
        const password = passwordField.value;

        // Basic validation for email and password
        if (!validateEmail(email)) {
            alert('Please enter a valid email address!');
            return;
        }

        if (!password) {
            alert('Password cannot be empty!');
            return;
        }

        // Proceed with form submission after validation
        form.submit(); // This will actually submit the form
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
