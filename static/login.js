document.getElementById('login-form-id').addEventListener('submit', async (e) => {
    e.preventDefault();
    const userId = document.getElementById('user-id').value;
    const userPassword = document.getElementById('user-password').value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';
  
    
    const response = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({userId, userPassword}),
    });
    
    const data = await response.json();

    if (data.success) {
        // Başarılı giriş durumunda yönlendirme
        window.location.href = data.redirect_url;
    } else {
        errorMessage.textContent = data.message;
    }
});
