document.addEventListener('DOMContentLoaded', () => {
    if(username.trim() !== ''){
        if(place.trim() !== ''){
            document.querySelector('#login-info').textContent = `${username}님 | ${place}지점`;
        }else{
            document.querySelector('#login-info').textContent = `${username}님`;
        }
        const btn = document.querySelector('#login');
        btn.textContent = '로그아웃';
    }
});