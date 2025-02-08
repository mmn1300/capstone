let captureImageFlag = false;
let cnt = 0;

const container = document.querySelector('#input-group');


// 장바구니에 있는 모든 상품 개수와 가격의 합을 화면에 표시하는 함수
const handleEvent = () => {
    const total = document.querySelector('#right-bottom-span');
    const shoppingBagQuantityArray = document.querySelectorAll('.input');
    const shoppingBagPriceArray = document.querySelectorAll('.result-price');
    
    let count=0;
    for(let i=0; i<shoppingBagQuantityArray.length; i++){
        count += Number(shoppingBagQuantityArray[i].value);
    }

    let sum=0;
    for(let i=0; i<shoppingBagPriceArray.length; i++){
        sum += Number(shoppingBagPriceArray[i].textContent.slice(0,-2));
    }

    total.textContent = `전체 ${count} 개, ${sum} 원`;
}


// 스캔하기 동작을 수행하는 함수. app.py파일의 capture_image()함수에 요청
const captureImage = () => {
    // 삐 효과음 동작
    const soundEffect = document.querySelector('#soundEffect');
    soundEffect.currentTime = 0; // 소리 시작 지점 초기화
    soundEffect.play(); // 소리 재생

    fetch('/capture_image', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // 요청에 대한 응답으로 받아온 상품 인식 정보를 화면에 표시
        document.querySelector('#recognized-item-category').innerText = `카테고리: ${data.category}`;
        document.querySelector('#recognized-item-name').innerText = `제품 명: ${data.itemName}`;
        document.querySelector('#recognized-item-price').innerText = `가격: ${data.price} 원`;
        document.querySelector('#recognized-item-image').src = data.imagePath;
    })
    .catch(error => console.error('Error:', error));
}


// 장바구니에 새로운 상품 줄을 추가하는 함수
const createRow = () => {
    
    // 새로 추가할 행 div 생성
    const newRow = document.createElement('div');
    newRow.className = 'item-row-add';
    
    // 버튼 태그 생성 (x)
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'remove';
    removeButton.textContent = 'x';
    newRow.appendChild(removeButton);
    
    // 상품의 이름을 나타낼 span 태그 생성
    const textInput = document.createElement('input');
    textInput.type = 'text';
    textInput.name = 'text[]';
    textInput.className = 'item-name';
    textInput.value = document.querySelector('#recognized-item-name').textContent.slice(6);
    textInput.setAttribute('readonly', true);
    newRow.appendChild(textInput);
    
    // input 태그 생성 (정수 값)
    const numberInput = document.createElement('input');
    numberInput.type = 'number';
    numberInput.name = 'number[]';
    numberInput.value = '1';
    numberInput.className = 'input';
    newRow.appendChild(numberInput);
    
    // 버튼 태그 생성 (+)
    const incrementButton = document.createElement('button');
    incrementButton.type = 'button';
    incrementButton.className = 'increment';
    incrementButton.textContent = '+';
    newRow.appendChild(incrementButton);
    
    // 버튼 태그 생성 (-)
    const decrementButton = document.createElement('button');
    decrementButton.type = 'button';
    decrementButton.className = 'decrement';
    decrementButton.textContent = '-';
    newRow.appendChild(decrementButton);
    
    // 가격 정보를 나타낼 span 태그 생성
    const resultPrice = document.createElement('span');
    resultPrice.className = 'result-price';
    resultPrice.textContent = `${document.querySelector('#recognized-item-price').textContent.slice(4,-2)} 원`;
    newRow.appendChild(resultPrice);
    
    // x 버튼을 클릭했을때 해당 줄을 삭제하는 이벤트
    removeButton.addEventListener('click', () => {
        document.querySelector('.item-br').remove();
        newRow.remove();
        cnt-=1;
        handleEvent();
    })
    
    // 해당 줄의 상품 가격에 개수를 곱한 값을 가격 정보 span태그에 나타내는 익명 함수
    const setResultPrice = () => {
        const itemPrice = parseInt(document.querySelector('#recognized-item-price').textContent.slice(4,-2));
        const quantity = parseInt(numberInput.value);
        resultPrice.textContent = `${itemPrice*quantity} 원`;
    }

    // + 버튼을 클릭했을 때의 이벤트 (input태그 값 하나 증가)
    incrementButton.addEventListener('click', () => {
        numberInput.value = parseInt(numberInput.value) + 1;
        setResultPrice();
        handleEvent();
    });
    
    // - 버튼을 클릭했을 때의 이벤트 (input태그 값 하나 감소)
    decrementButton.addEventListener('click', () => {
        numberInput.value = parseInt(numberInput.value) - 1;
        setResultPrice();
        handleEvent();
    });
    
    return newRow;
}


// 서버에 데이터를 전송하는 함수. 비동기 요청으로 수행하므로 동작 정상 수행시 페이지 상태 초기화를 수행함
const submitData = () => {

    // 서버로 보낼 데이터를 배열에 담아 가공함
    const textInputs = document.querySelectorAll('.item-name');
    const textValues = Array.from(textInputs).map(input => input.value);
    const numberInputs = document.querySelectorAll('.input');
    const numberValues = Array.from(numberInputs).map(input => input.value);

    // 가공된 데이터를 객체에 담음
    const data = {
        texts: textValues,
        numbers: numberValues
    };

    // 비동기 방식으로 서버에 JSON 데이터를 보냄.
    // 상품 결제는 데이터베이스 안의 데이터를 변경시키므로 PUT을 사용
    fetch('/user_page/payment', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {

        // 정상적으로 동작이 완료되었을 때 페이지 상태 초기화를 수행함
        if(data.result === 'good'){
            const itemdivArray = document.querySelectorAll('.item-row-add');
            const itembrArray = document.querySelectorAll('.item-br');
            for (let i=0;i<itemdivArray.length;i++){
                itemdivArray[i].remove();
                itembrArray[i].remove();
            }
            captureImageFlag = false;
            document.querySelector('#recognized-item-category').innerText = `카테고리`;
            document.querySelector('#recognized-item-name').innerText = `제품 명`;
            document.querySelector('#recognized-item-price').innerText = `가격`;
            document.querySelector('#right-bottom-span').textContent = `전체 0 개, 0 원`;
            document.querySelector('#recognized-item-image').src = '/static/img/noimage.png';
        }
    })

    // 동작이 정상적으로 수행되지 못했을 경우 에러 메세지를 출력함
    .catch(error => {
        alert('동작 수행 중 에러가 발생했습니다.');
        console.error('Error:', error);
    });
}