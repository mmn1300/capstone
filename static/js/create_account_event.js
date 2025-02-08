document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#id').addEventListener('change', () => {
        checkFalg["id"] = false;
        const iconImg = document.querySelectorAll('.icon-img');
        iconImg[0].src = uncheckedImgPath;
    });

    document.querySelector('#pw').addEventListener('change', (event) => {
        const pwCheck = document.querySelector('#pw-check');
        const pwCheckText = document.querySelector('#pw-check-text');
        const iconImg = document.querySelectorAll('.icon-img');
        checkFalg["pw"] = false;
        iconImg[1].src = uncheckedImgPath;
        iconImg[2].src = uncheckedImgPath;
        

        if(event.target.value.length >= 8){
            if(event.target.value.length <= 15){
                if(pwCheck.value.trim() === ''){
                    pwCheckText.textContent = '비밀번호 확인란을 입력해주세요.';
                    pwCheckText.className = 'highlight-black';
                    iconImg[1].src = checkedImgPath;
                }else if(event.target.value === pwCheck.value.trim()){
                    pwCheckText.textContent = '비밀번호가 일치합니다.';
                    pwCheckText.className = 'highlight-blue';
                    checkFalg["pw"] = true;
                    iconImg[1].src = checkedImgPath;
                    iconImg[2].src = checkedImgPath;
                }else{
                    pwCheckText.textContent = '비밀번호가 일치하지 않습니다.';
                    pwCheckText.className = 'highlight-red';
                    iconImg[1].src = checkedImgPath;
                }
            }else{
                pwCheckText.textContent = '비밀번호는 열다섯 글자까지만 입력할 수 있습니다.';
                pwCheckText.className = 'highlight-red';
            }
        }else{
            pwCheckText.textContent = '비밀번호는 여덟글자 이상이어야 합니다.';
            pwCheckText.className = 'highlight-red';
        }
    });

    document.querySelector('#pw-check').addEventListener('change', (event) => {
        const pw = document.querySelector('#pw');
        const pwCheckText = document.querySelector('#pw-check-text');
        const iconImg = document.querySelectorAll('.icon-img');
        checkFalg["pw"] = false;
        iconImg[2].src = uncheckedImgPath;
        
        if(pw.value.trim() === ''){
            pwCheckText.textContent = '비밀번호란을 입력해주세요.';
            pwCheckText.className = 'highlight-black';
        }else if(event.target.value === pw.value.trim()){
            if(pw.value.length >= 8){
                if(pw.value.length <= 15){
                    pwCheckText.textContent = '비밀번호가 일치합니다.';
                    pwCheckText.className = 'highlight-blue';
                    checkFalg["pw"] = true;
                    iconImg[1].src = checkedImgPath;
                    iconImg[2].src = checkedImgPath;
                }else{
                    pwCheckText.textContent = '비밀번호는 열다섯 글자까지만 입력할 수 있습니다.';
                    pwCheckText.className = 'highlight-red';
                }
            }else{
                pwCheckText.textContent = '비밀번호는 여덟글자 이상이어야 합니다.';
                pwCheckText.className = 'highlight-red';
            }
        }else{
            pwCheckText.textContent = '비밀번호가 일치하지 않습니다.';
            pwCheckText.className = 'highlight-red';
        }
    });

    document.querySelector('#nickname').addEventListener('change', () => {
        const iconImg = document.querySelectorAll('.icon-img');
        iconImg[3].src = uncheckedImgPath;
        checkFalg["name"] = false;
    });

    document.querySelector('#place').addEventListener('change', () => {
        const iconImg = document.querySelectorAll('.icon-img');
        iconImg[4].src = uncheckedImgPath;
        checkFalg["place"] = false;
    });

    document.querySelector('#approval-code').addEventListener('change', () => {
        const iconImg = document.querySelectorAll('.icon-img');
        iconImg[5].src = uncheckedImgPath;
        checkFalg["apCode"] = false;
    });


    document.querySelector('#id-redundancy-check').addEventListener('click', () => {
        const id = document.querySelector('#id');
        idredundancyCheck(id.value).then(result => {
            if(result){
                if(id.value.length > 15){
                    alert('아이디는 열다섯 글자까지만 입력할 수 있습니다.');
                }else if(id.value.trim() === ''){
                    alert('아이디를 입력해주세요.');
                }else{
                    alert('생성 가능한 아이디입니다!');
                    const iconImg = document.querySelectorAll('.icon-img');
                    iconImg[0].src = checkedImgPath;
                }
            }else{
                alert('이미 존재하는 아이디입니다!');
            }
        });
    });
    
    document.querySelector('#name-redundancy-check').addEventListener('click', () => {
        const nickname = document.querySelector('#nickname');
        nameCheck(nickname.value).then(result => {
            if(result){
                if(nickname.value.length > 10){
                    alert('닉네임은 열 글자까지만 입력할 수 있습니다.');
                }else if(nickname.value.trim() === ''){
                    alert('닉네임을 입력해주세요.');
                }else{
                    alert('생성 가능한 닉네임입니다!');
                    const iconImg = document.querySelectorAll('.icon-img');
                    iconImg[3].src = checkedImgPath;
                }
            }else{
                alert('이미 존재하는 닉네임입니다!');
            }
        });
    });

    document.querySelector('#place-redundancy-check').addEventListener('click', () => {
        const place = document.querySelector('#place');
        placeCheck(place.value).then(result => {
            if(result){
                if(place.value.length > 10){
                    alert('지점명은 열 글자까지만 입력할 수 있습니다.');
                }else if(place.value.trim() === ''){
                    alert('지점명을 입력해주세요.');
                }else{
                    alert('생성 가능한 지점입니다!');
                    const iconImg = document.querySelectorAll('.icon-img');
                    iconImg[4].src = checkedImgPath;
                }
            }else{
                alert('해당 지점의 계정이 이미 존재합니다!');
            }
        });
    });

    document.querySelector('#approval-code-check').addEventListener('click', () => {
        const approvalCode = document.querySelector('#approval-code');
        if(approvalCode.value.trim() !== ''){
            apCodeCheck(approvalCode.value).then(result => {
                if(result){
                    alert('승인 코드와 일치합니다!');
                    const iconImg = document.querySelectorAll('.icon-img');
                    iconImg[5].src = checkedImgPath;
                }else{
                    alert('승인 코드와 일치하지않습니다!');
                }
            });
        }else{
            alert('승인 코드와 일치하지않습니다!');
        }
    });


    document.querySelector('#approval-code-check').addEventListener('keyup', (event) => {
        const number = parseInt(event.target.value, 10);
        if((event.target.value !=='') && (isNaN(number) || number.toString() !== event.target.value)) {
            alert("정수만 입력할 수 있습니다.");
            event.target.value = '';
            return;
        }
    });


    const inputs = document.querySelectorAll('input');
    inputs.forEach((input, index) => {
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Tab') {
                event.preventDefault();
                const nextIndex = (index + 1) % inputs.length;
                inputs[nextIndex].focus();
            }
        });
    });


    document.querySelector('#sign-up').addEventListener('click', () => {
        if(!checkFalg["id"]){
            alert("아이디 중복 확인이 필요합니다.");
            return;
        }
        if(!checkFalg["pw"]){
            alert("생성할 수 없는 형태의 비밀번호입니다.");
            return;
        }
        if(!checkFalg["place"]){
            alert("지점명 중복 확인이 필요합니다.");
            return;
        }
        if(!checkFalg["name"]){
            alert("닉네임 중복 확인이 필요합니다.");
            return;
        }
        if(!checkFalg["apCode"]){
            alert("승인 코드 일치 확인이 필요합니다.");
            return;
        }

        data = {
            id : document.querySelector('#id').value,
            pw : document.querySelector('#pw').value,
            name : document.querySelector('#nickname').value,
            place : document.querySelector('#place').value
        }
        fetch('/account/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if(data["message"]==='good'){
                alert("회원가입이 완료되었습니다.");
                window.location.href = '/login_form';
            }else{
                alert("로그인 중 문제가 발생하였습니다.");
                return;
            }
        })
        // 동작이 정상적으로 수행되지 못했을 경우 에러 메세지를 출력함
        .catch(error => {
            alert('동작 수행 중 에러가 발생했습니다.');
            console.error('Error:', error);
        });
    });

    document.querySelector('#back-page').addEventListener('click', () => {
        const inputs = document.querySelectorAll('input');
        let allEmpty = true;

        inputs.forEach(input => {
            if (input.value.trim() !== '') {
                allEmpty = false;
            }
        });

        if(allEmpty){
            window.location.href = '/login_form';
        }else if(confirm('회원가입을 취소하시겠습니까?')){
            window.location.href = '/login_form';
        }
    });
});