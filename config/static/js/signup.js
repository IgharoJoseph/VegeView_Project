document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.signup-form');
    
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const fullName = document.getElementById('full-name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        // Handle form submission (e.g., send data to server)
        alert('Form submitted successfully!');
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

