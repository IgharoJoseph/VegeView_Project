document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Basic validation (you might want to enhance this)
    if (email && password) {
        alert('Login successful!');
        // Here you can add code to handle the login process, e.g., send data to the server
    } else {
        alert('Please fill out all fields.');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.menu-button');
    const nav = document.querySelector('.nav');

    menuButton.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuButton.classList.toggle('active');
    });
});