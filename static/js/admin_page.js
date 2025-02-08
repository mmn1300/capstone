document.addEventListener('DOMContentLoaded', () => {
    if(username.trim() != ''){
        document.querySelector('#login-info').textContent = `${username}님 | ${place} 지점`;
    }
});