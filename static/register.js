var form = document.getElementById('reg-user');

form.addEventListener('submit', function(event) {
    var username = document.getElementById('username').value;
    var name = document.getElementById('name').value;
    var subname = document.getElementById('subname').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    if (username === '' || name === '' || subname === '' || email === '' || password === '' || confirmPassword === '') {
        alert('Por favor, complete todos los campos');
        event.preventDefault();
    }

    // Validar la estructura del correo electrónico
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Por favor, ingrese un correo electrónico válido');
        event.preventDefault();
    }

    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        event.preventDefault();
    }
});