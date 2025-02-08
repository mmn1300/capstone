const pageIdx = 8;
let cnt = 1;

// 상품들의 정보를 담을 배열
const foodData = [];
const drinkData = [];
const sanitaryProductsData = [];
const etcData = [];

// 각 카테고리별 상품들의 이름을 알맞는 배열에 삽입
for(let i=0; i<inventoryData.length; i++){
    if(inventoryData[i][0] === '식품'){
        foodData.push([inventoryData[i][0], inventoryData[i][1], inventoryData[i][2]]);
    }else if(inventoryData[i][0] === '음료'){
        drinkData.push([inventoryData[i][0], inventoryData[i][1], inventoryData[i][2]]);
    }else if(inventoryData[i][0] === '위생용품'){
        sanitaryProductsData.push([inventoryData[i][0], inventoryData[i][1], inventoryData[i][2]]);
    }else{
        etcData.push([inventoryData[i][0], inventoryData[i][1], inventoryData[i][2]]);
    }
}

const categoryToArray = {
    '식품' : foodData,
    '음료' : drinkData,
    '위생용품' : sanitaryProductsData,
    '기타' : etcData
}

const categoryArray = [
    ["food", "식품"],
    ["drink", "음료"],
    ["sanitary-products", "위생용품"],
    ["etc", "기타"]
];


// 행을 생성하는 함수 
const createRow = () =>{

    // 새로 추가할 행 div 생성
    const newRow = document.createElement('div');
    newRow.className = 'input-row-add';

    // input 태그 생성 (텍스트 값)
    const textSelect = document.createElement('select');
    textSelect.name = 'texts';
    textSelect.className = 'select';
    const options = [
        { value: '과자', text: '과자' },
        { value: '라면', text: '라면' },
        { value: '마스크', text: '마스크' },
        { value: '맥주', text: '맥주' },
        { value: '면도기', text: '면도기' },
        { value: '생리대', text: '생리대' },
        { value: '생수', text: '생수' },
        { value: '숙취해소제', text: '숙취해소제' },
        { value: '스타킹', text: '스타킹' },
        { value: '아이스크림', text: '아이스크림' },
        { value: '우산', text: '우산' },
        { value: '탄산음료', text: '탄산음료' }
    ];
    options.forEach(optionData => {
        const option = document.createElement('option');
        option.value = optionData.value;
        option.textContent = optionData.text;
        textSelect.appendChild(option);
    });
    newRow.appendChild(textSelect);

    // input 태그 생성 (문자열 값)
    const textInput = document.createElement('input');
    textInput.type = 'text';
    textInput.name = 'texts2';
    textInput.value = '';
    textInput.className = 'text2';
    newRow.appendChild(textInput);

    // input 태그 생성 (정수 값)
    const numberInput = document.createElement('input');
    numberInput.type = 'number';
    numberInput.name = 'numbers';
    numberInput.value = '0';
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

    // 수량 입력란에 정수값이 아닌 다른 값이 입력되었을 경우의 처리
    numberInput.addEventListener('keydown', () => {
        const number = parseInt(numberInput.value, 10);
        if ((numberInput.value !=='') && (isNaN(number) || number.toString() !== numberInput.value)) {
            alert("정수만 입력할 수 있습니다.");
            numberInput.value = numberInput.value.slice(0, -1);
        }
    });

    // 수량 입력칸을 공백으로 두었을 경우의 처리
    numberInput.addEventListener('change', () => {
        if (numberInput.value === ''){
            numberInput.value = 0;
        }
    });

    // + 버튼을 클릭했을 때의 이벤트 (input태그 값 하나 증가)
    incrementButton.addEventListener('click', () => {
        numberInput.value = String(parseInt(numberInput.value) + 1);
    });

    // - 버튼을 클릭했을 때의 이벤트 (input태그 값 하나 감소)
    decrementButton.addEventListener('click', () => {
        numberInput.value = String(parseInt(numberInput.value) - 1);
    });

    return newRow;
}


// 재고 목록들을 화면에 출력하기 위한 태그를 생성하는 함수
const printInventory = (category, itemtype, itemname) => {
    const newRow = document.createElement('div');
    newRow.className = 'inventory-list';

    const text1 = document.createElement('span');
    text1.textContent = category;
    text1.className = 'left-span';
    newRow.appendChild(text1);
    
    const text2 = document.createElement('span');
    text2.textContent = itemtype;
    text2.className = 'middle-span';
    newRow.appendChild(text2);

    const btn = document.createElement('button');
    btn.textContent = itemname;
    btn.className = 'right-btn';
    newRow.appendChild(btn);

    // 상품 이름이 쓰여진 버튼을 눌렀을 때, 장바구니 맨 마지막 행에 상품 형태와 상품명을 자동 기입해주는 이벤트
    btn.addEventListener('click', ()=>{
        const textArray = document.querySelectorAll('.text2');
        const lastText = textArray[textArray.length-1];
        lastText.value = btn.textContent;
        
        const selectArray = document.querySelectorAll('.select');
        const lastSelect = selectArray[selectArray.length-1];
        lastSelect.text = text2.textContent;
        lastSelect.value = text2.textContent;

    });
    
    return newRow;
}


// 재고 목록들을 제거하는 함수
const deleteInventoryList = () => {
    const ivL = document.querySelectorAll('.inventory-list');
    for(let i=0; i<ivL.length; i++){
        ivL[i].remove();
    }
}


// 해당 카테고리에 맞는 재고들을 재고 목록에 추가하는 함수
const setItemList = (category, pn=1) => {
    const iL = document.querySelector('.item-list');
    const setDataArray = categoryToArray[category];
    const maxPageNum = Math.floor((setDataArray.length-1) / pageIdx) + 1;
    if (setDataArray.length < pageIdx){
        for(let i=0; i<setDataArray.length; i++){
            iL.appendChild(printInventory(category, setDataArray[i+pageIdx*(pn-1)][1], setDataArray[i+pageIdx*(pn-1)][2]));
        }
    }else if(pn===maxPageNum){
        for(let i=0; i<setDataArray.slice(pageIdx*(pn-1)).length; i++){
            iL.appendChild(printInventory(category, setDataArray[i+pageIdx*(pn-1)][1], setDataArray[i+pageIdx*(pn-1)][2]));
        }
    }else{
        for(let i=0; i<pageIdx; i++){
            iL.appendChild(printInventory(category, setDataArray[i+pageIdx*(pn-1)][1], setDataArray[i+pageIdx*(pn-1)][2]));
        }
    }
}