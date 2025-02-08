// 서버로부터 받는 데이터 예시
//
// const productTypeToCategory = {
//     "식품" : ["과자", "라면", "아이스크림"],
//     "음료" : ["맥주", "생수", "탄산음료"],
//     "위생용품" : ["마스크"],
//     "기타" : ["우산"]
// };
// const categoryToProductName = {
//     '과자': ['꼬깔콘', '꿀꽈배기', '다이제초코', '오레오'],
//     '라면': ['삼양라면', '신라면', '육개장컵', '진라면매운맛', '진라면순한맛'],
//     '아이스크림': ['메로나'],
//     '맥주': ['카스', '테라'],
//     '생수': ['삼다수', '아이시스'],
//     '탄산음료': ['밀키스', '코카콜라', '펩시', '핫식스', '환타'],
//     '마스크': ['KF94마스크'],
//     '우산': ['검정색우산', '청색접이식우산']
// };
// const productNameToCodeAndPrice = {
//     '아이시스': [1, 1000],
//     '메로나': [2, 1000],
//     '카스': [3, 1000],
//     '밀키스': [4, 1000],
//     '삼다수': [5, 1000],
//     '코카콜라': [6, 1000],
//     '테라': [7, 1000],
//     '환타': [8, 1000],
//     '오레오': [9, 1000],
//     '펩시': [10, 1000], 
//     '신라면': [11, 1000],
//     '삼양라면': [12, 1000],
//     '꼬깔콘': [13, 1000],
//     '검정색우산': [14, 1000],
//     '청색접이식우산': [15, 1000],
//     'KF94마스크': [16, 1000],
//     '진라면매운맛': [17, 1000],
//     '육개장컵': [18, 1000],
//     '진라면순한맛': [19, 1000],
//     '다이제초코': [20, 1000],
//     '꿀꽈배기': [21, 1000],
//     '핫식스': [22, 1000]
// };


let inputItemRowCount = 0; // 현재 행 개수 (좌측 항목)
const itemRowCount = 10; // 전체 행 개수 (우측 테이블)

const today = new Date();
const futureDate = new Date();
futureDate.setDate(today.getDate() + 7);

const tableBody = document.querySelector('.item-body');
const rowClassName = ['item-code-cell', 'item-name-cell', 'item-quantity-cell', 'item-price-cell', 'item-sum-price-cell']


// 날짜를 YYYY-MM-DD 형식으로 포맷팅하는 함수
const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 월은 0부터 시작하므로 +1
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 새 항목을 생성하는 함수. 항목의 데이터는 선택상자의 값임
const createRow = () => {
    const newRow = document.createElement('div');
    newRow.className = 'input-item-row';

    // 버튼 태그 생성 (x)
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'remove';
    removeButton.textContent = 'x';
    removeButton.id = 'remove' + inputItemRowCount;
    newRow.appendChild(removeButton);

    // 상품의 이름을 입력할 공간
    const inputText = document.createElement('input');
    inputText.className = 'input-item-name';
    inputText.id = 'input-item-name' + inputItemRowCount;
    inputText.type = 'text';
    const pname = document.querySelector('#productName');
    inputText.value = pname.options[pname.selectedIndex].text;
    newRow.appendChild(inputText);

    // 상품의 수량을 입력할 공간
    const inputNumber = document.createElement('input');
    inputNumber.className = 'input-item-quantity';
    inputNumber.id = 'input-item-quantity' + inputItemRowCount;
    inputNumber.type = 'number';
    inputNumber.value = '0';
    newRow.appendChild(inputNumber);

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

    // 상품 명과 상품 수량을 입력받아 테이블에 상품의 수량과 합계 금액을 띄우는 함수
    const inputSumPricecell = (inn) => {
        const index = parseInt(inn.id.slice(19));
        const allPrice = document.querySelectorAll('.item-price-cell');
        const price = allPrice[index].value;
        const quantity = inn.value;
        const sumPrice = parseInt(price)*parseInt(quantity);

        const allQuantity = document.querySelectorAll('.item-quantity-cell');
        allQuantity[index].value = String(quantity);
        const allSumPrice = document.querySelectorAll('.item-sum-price-cell');
        allSumPrice[index].value = String(sumPrice);
    }

    // 상품 명을 입력하면 테이블에 상품 정보들을 입력함.
    inputText.addEventListener('keyup', (event) => {
        const index = Number(event.target.id.slice(15));
        const allNameCell = document.querySelectorAll('.item-name-cell');
        allNameCell[index].value = String(event.target.value);

        const itemCodeCellArray = document.querySelectorAll('.item-code-cell');
        const itemQuantityCellArray = document.querySelectorAll('.item-quantity-cell');
        const itemPriceCellArray = document.querySelectorAll('.item-price-cell');
        const itemSumPriceCellArray = document.querySelectorAll('.item-sum-price-cell');

        // 입력된 상품명이 데이터베이스에 존재한다면 데이터베이스에 존재하는 정보대로 상품 정보를 입력
        if(inputText.value in productNameToCodeAndPrice){
            itemCodeCellArray[index].value = productNameToCodeAndPrice[inputText.value][0];
            itemPriceCellArray[index].value = productNameToCodeAndPrice[inputText.value][1];
            itemSumPriceCellArray[index].value = String(Number(itemPriceCellArray[index].value)*Number(itemQuantityCellArray[index].value));
        }else{ // 데이터베이스에 존재하지 않는 상품일 경우 상품 명을 제외한 다른 셀은 공백으로 함
            itemCodeCellArray[index].value = '';
            itemPriceCellArray[index].value = '';
            itemSumPriceCellArray[index].value = '';
        }
    });

    // 상품 수량을 변경하면 테이블의 수량, 합계 금액을 변경하는 이벤트 함수
    inputNumber.addEventListener('keyup', (event) => {
        const index = Number(event.target.id.slice(19));
        const allQuantityCell = document.querySelectorAll('.item-quantity-cell');
        allQuantityCell[index].value = String(event.target.value);

        const PriceCell = productNameToCodeAndPrice[document.querySelector(`#input-item-name${index}`).value][1];
        const allSumPriceCell = document.querySelectorAll('.item-sum-price-cell');
        allSumPriceCell[index].value = String(Number(event.target.value)*Number(PriceCell));
    });

    // 삭제 버튼을 누르면 해당 항목과 매칭되는 테이블의 값을 지움
    // 해당 항목의 이후 항목들이 존재할 시 이후 항목들의 id를 하나 차감함
    removeButton.addEventListener('click', (event) => {
        const index = Number(event.target.id.slice(6));

        const inputItemRowArray = document.querySelectorAll('.input-item-row');

        const itemInputCodeArray = document.querySelectorAll('.item-code-cell');
        const itemInputNameArrayArray = document.querySelectorAll('.item-name-cell');
        const itemInputQuantityArray = document.querySelectorAll('.item-quantity-cell');
        const itemInputPriceArray = document.querySelectorAll('.item-price-cell');
        const itemInputSumPriceArray = document.querySelectorAll('.item-sum-price-cell');
        
        const cells = [itemInputCodeArray, itemInputNameArrayArray, itemInputQuantityArray, itemInputPriceArray, itemInputSumPriceArray]

        cells.forEach(cell => {
            cell[index].value = '';
        });
        
        for(let i=index; i<itemRowCount-1; i++){
            cells.forEach(cell => {
                cell[i].value = cell[i+1].value;
            });
        }
        cells.forEach(cell => {
            cell[itemRowCount-1].value = '';
        });

        inputItemRowArray[index].remove();
        
        for(let i=index+1; i<inputItemRowArray.length; i++){
            const rv = inputItemRowArray[i].querySelector('.remove');
            const iin = inputItemRowArray[i].querySelector('.input-item-name');
            const iiq = inputItemRowArray[i].querySelector('.input-item-quantity');
            
            if(rv !== null){
                rv.id = 'remove'+String(Number(rv.id.slice(6))-1);
            }
            if(iin !== null){
                iin.id = 'input-item-name'+String(Number(iin.id.slice(15))-1);
            }
            if(iiq !== null){
                iiq.id = 'input-item-quantity'+String(Number(iiq.id.slice(19))-1);
            }
        }

        inputItemRowCount--;
    });

    // + 버튼을 클릭했을 때의 이벤트 (input태그 값 하나 증가)
    incrementButton.addEventListener('click', (event) => {
        inputNumber.value = String(parseInt(inputNumber.value) + 1);
        inputSumPricecell(inputNumber);
    });

    // - 버튼을 클릭했을 때의 이벤트 (input태그 값 하나 감소)
    decrementButton.addEventListener('click', () => {
        if(parseInt(inputNumber.value)<=0){
            return;
        }
        inputNumber.value = String(parseInt(inputNumber.value) - 1);
        inputSumPricecell(inputNumber);
    });

    return newRow;
}

// 우측 테이블의 셀을 생성하는 함수
const createCell = () => {
    const itemRow = document.createElement('tr');
    itemRow.className = 'item-row';
    
    const itemCell = [];
    const itemInput = [];
    for(let j=0; j<5; j++){
        itemCell[j] = document.createElement('td');
        itemCell[j].className = 'item-cell';
        itemInput[j] = document.createElement('input');
        itemInput[j].className = rowClassName[j];
        itemInput[j].type = 'text';
        itemInput[j].name = 'item_info';
        itemInput[j].value = '';
        itemCell[j].appendChild(itemInput[j]);
        itemRow.appendChild(itemCell[j]);
    }

    itemInput[0].addEventListener('keyup', () => {
        const itemCodeCellArray = document.querySelectorAll('.item-code-cell');
        const number = parseInt(itemInput[0].value, 10);
        let index = 0;
        for (let i=0; i<itemRowCount; i++){
            if(itemCodeCellArray[i]===itemInput[0]){
                index = i;
                break;
            }
        }
        if(inputItemRowCount<=index){
            alert('상품 추가는 좌측 기능을 이용해주십시오.');
            itemInput[0].value = '';
            return;
        }else if ((itemInput[0].value !=='') && (isNaN(number) || number.toString() !== itemInput[0].value)) {
            alert("정수만 입력할 수 있습니다.");
            itemInput[0].value = '';
            return;
        }else{
            for (let key in productNameToCodeAndPrice) {
                if (productNameToCodeAndPrice[key][0] === parseInt(itemInput[0].value)) {
                    itemInput[1].value = key;
                    document.querySelector(`#input-item-name`+index).value = key;
                    itemInput[3].value = String(productNameToCodeAndPrice[key][1]);
                    itemInput[4].value = String(parseInt(itemInput[2].value)*parseInt(itemInput[3].value));
                    break;
                }else{
                    document.querySelector(`#input-item-name`+index).value = '';
                    itemInput[1].value = '';
                    itemInput[3].value = 0;
                    itemInput[4].value = 0;
                }
            }
        }
    });

    // 테이블의 셀 데이터를 입력하면 좌측 항목의 값을 변경하는 이벤트 함수들
    itemInput[1].addEventListener('keyup', () => {
        const itemNameCellArray = document.querySelectorAll('.item-name-cell');
        let index = 0;
        for(let i=0; i<itemRowCount; i++){
            if(itemInput[1]===itemNameCellArray[i]){
                index = i;
                break;
            }
        }
        // 셀과 매칭되는 좌측 항목에 데이터 삽입
        const inputItemQuantity = document.querySelector(`#input-item-name`+index);
        if(inputItemQuantity !== null){
            inputItemQuantity.value = itemInput[1].value;
        }else{ // 좌측 항목과 매칭되지 않는 셀에 데이터 입력시 이벤트 함수 강제 종료
            alert('상품 추가는 좌측 기능을 이용해주십시오.');
            itemInput[1].value = '';
            return;
        }

        if(itemInput[1].value in productNameToCodeAndPrice){
            itemInput[0].value = productNameToCodeAndPrice[itemInput[1].value][0];
            itemInput[3].value = String(productNameToCodeAndPrice[itemInput[1].value][1]);
            itemInput[4].value = String(parseInt(itemInput[2].value)*parseInt(itemInput[3].value));
        }else{
            itemInput[0].value = '';
            itemInput[3].value = '';
            itemInput[4].value = '';
        }
    });

    itemInput[2].addEventListener('keyup', () => {
        const number = parseInt(itemInput[2].value, 10);
        const itemQuantityCellArray = document.querySelectorAll('.item-quantity-cell');
        let index = 0;
        for(let i=0; i<itemRowCount; i++){
            if(itemInput[2]===itemQuantityCellArray[i]){
                index = i;
                break;
            }
        }
        if(inputItemRowCount<=index){
            alert('상품 추가는 좌측 기능을 이용해주십시오.');
            itemInput[2].value = '';
            return;
        }else if((itemInput[2].value !=='') && (isNaN(number) || number.toString() !== itemInput[2].value)) {
            alert("정수만 입력할 수 있습니다.");
            itemInput[2].value = '';
            return;
        }else if(itemInput[3].value !== ''){ 
            const inputItemQuantityArray = document.querySelectorAll('.input-item-quantity');
            if(index < inputItemQuantityArray.length){
                if(itemInput[2].value === ''){
                    inputItemQuantityArray[index].value = 0;
                }else{
                    inputItemQuantityArray[index].value = itemInput[2].value;
                }
            }
            itemInput[4].value = String(parseInt(itemInput[2].value)*parseInt(itemInput[3].value));
        }
    });
    
    itemInput[3].addEventListener('keyup', () => {
        const number = parseInt(itemInput[3].value, 10);
        const itemPriceCellArray = document.querySelectorAll('.item-price-cell');
        let index = 0;
        for(let i=0; i<itemRowCount; i++){
            if(itemInput[3]===itemPriceCellArray[i]){
                index = i;
                break;
            }
        }
        if(inputItemRowCount<=index){
            alert('상품 추가는 좌측 기능을 이용해주십시오.');
            itemInput[3].value = '';
            return;
        }else if((itemInput[3].value !=='') && (isNaN(number) || number.toString() !== itemInput[3].value)) {
            alert("정수만 입력할 수 있습니다.");
            itemInput[3].value = '';
            return;
        }else if(itemInput[2].value !== ''){
            itemInput[4].value = String(parseInt(itemInput[2].value)*parseInt(itemInput[3].value));
        }
    });

    itemInput[4].addEventListener('keyup', () => {
        const number = parseInt(itemInput[4].value, 10);
        const itemSumPriceCellArray = document.querySelectorAll('.item-sum-price-cell');
        let index = 0;
        for(let i=0; i<itemRowCount; i++){
            if(itemInput[4]===itemSumPriceCellArray[i]){
                index = i;
                break;
            }
        }
        if(inputItemRowCount<=index){
            alert('상품 추가는 좌측 기능을 이용해주십시오.');
            itemInput[4].value = '';
            return;
        }else if((itemInput[4].value !=='') && (isNaN(number) || number.toString() !== itemInput[4].value)) {
            alert("정수만 입력할 수 있습니다.");
            itemInput[4].value = '';
            return;
        }
    })

    tableBody.appendChild(itemRow);
}

const orderSettingToPredictData = (inputs, data) => {
    const distributedQuantityDict = data['distributedQuantityDict'];

    const inputItemQuantityArray = document.querySelectorAll('.input-item-quantity');
    const itemQuantityCellArray = document.querySelectorAll('.item-quantity-cell');
    const itemPriceCellArray = document.querySelectorAll('.item-price-cell');
    const itemSumPriceCellArray = document.querySelectorAll('.item-sum-price-cell');

    let cnt = 0;
    inputs.forEach(element => {
        const itemName = element.value;
        if(itemName in distributedQuantityDict){
            inputItemQuantityArray[cnt].value = distributedQuantityDict[itemName];
            itemQuantityCellArray[cnt].value = distributedQuantityDict[itemName];
            itemSumPriceCellArray[cnt].value = parseInt(itemQuantityCellArray[cnt].value) * parseInt(itemPriceCellArray[cnt].value);
        }
        cnt++;
    });
}