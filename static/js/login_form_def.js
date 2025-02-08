async function isIdExist(id){
    return fetch('/login/id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id:id}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP 오류. 상태코드: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if(data["message"] === 'exists'){
            return true;
        }else{
            return false;
        }
    })
    .catch((error) => {
        alert(`요청 중 에러가 발생했습니다.\n\n${error.message}`);
    });
}

async function isPwMatched(id,pw){
    return fetch('/login/pw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id:id,pw:pw}),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP 오류. 상태코드: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if(data["message"] === 'exists'){
            return true;
        }else{
            return false;
        }
    })
    .catch((error) => {
        alert(`요청 중 에러가 발생했습니다.\n\n${error.message}`);
    });
}


function login(){
    const id = document.querySelector('#id');
    const pw = document.querySelector('#password');

    if(id.value.trim() === ''){
        alert('아이디를 입력해주세요');
    }else if(pw.value.trim() === ''){
        alert('비밀번호를 입력해주세요');
    }else{
        isIdExist(id.value).then(result => {
            if(result){
                isPwMatched(id.value, pw.value).then(result => {
                    if(result){
                        document.querySelector('#login-form').submit();
                        alert('로그인 되었습니다.')
                    }else{
                        alert('비밀번호 입력이 잘못되었습니다.\n다시 입력해주세요.');
                        return;
                    }
                });
            }else{
                alert('입력하신 아이디가 존재하지 않습니다.');
                return;
            }
        });
    }
}