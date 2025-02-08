document.addEventListener('DOMContentLoaded', () => {
    // [로그인/로그아웃] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#login').addEventListener('click', function(event) {
        if(event.target.textContent === '로그인'){
            window.location.href = '/login_form';
        }else{
            window.location.href = '/logout';
        }
    });

    // [일반 사용자] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#userButton').addEventListener('click', function() {
        window.location.href = '/place';
    });

    // [관리자] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#adminButton').addEventListener('click', function() {
        window.location.href = '/admin_page';
    });
});