document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const googleLoginBtn = document.getElementById('googleLoginBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    // Registro
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());

            const response = await fetch('http://localhost:3000/login/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            alert(result.msg);
        });
    }

    // Login
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            const response = await fetch('http://localhost:3000/login/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.token) {
                localStorage.setItem('token', result.token);
                window.location.href = 'dashboard.html';
            } else {
                alert(result.msg);
            }
        });
    }

    // Google Login
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener('click', function() {
            window.location.href = 'http://localhost:3000/login/auth/google';
        });
    }

    // Logout
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('token');
            window.location.href = 'http://localhost:3000';
        });
    }
});
