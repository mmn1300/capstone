const noImgPath = '/static/img/noimage2.png';
const getIconImgPath = (categoryKoreanName, category) => {
    const entry = Object.entries(categoryKoreanName).find(([key, val]) => val === category);
    return `/static/img/bulb_icon_${entry ? entry[0] : undefined}.png`;
}

let threeBtnFlag = false;
let sevenBtnFlag = false;

const pageIdx = 10;


const categoryArray = ["all", "food", "drink", "sanitary_products", "etc"];

const categoryKoreanName = {
    "beer" : "맥주",
    "icecream" : "아이스크림",
    "mask" : "마스크",
    "soda" : "탄산음료",
    "umbrella" : "우산",
    "water" : "생수",
    "snack" : "과자",
    "ramen" : "라면",
    "razor" : "면도기",
    "hangover_cure" : "숙취해소제",
    "pad" : "생리대",
    "stockings" : "스타킹"
}


// 데이터를 표시할 행을 생성하는 함수
const createRow = () => {
    // 새로 추가할 행 div 생성
    const newRow = document.createElement('div');
    newRow.className = 'row';

    const span0 = document.createElement('span');
    span0.className = 'icon-cell-body';

    const img = document.createElement('img');
    img.src = '/static/img/noimage2.png';
    img.className = 'icon-img';
    img.width = '18';
    img.height = '18';
    span0.appendChild(img);
    newRow.appendChild(span0);

    const span1 = document.createElement('span');
    span1.className = 'code-cell';
    span1.setAttribute('cid', 'product-code-cell');
    newRow.appendChild(span1);

    const span2 = document.createElement('span');
    span2.className = 'cell-body-span';
    span2.setAttribute('cid', 'product-type-cell');
    newRow.appendChild(span2);

    const span3 = document.createElement('span');
    span3.className = 'cell-body-span';
    span3.setAttribute('cid', 'product-category-cell');
    newRow.appendChild(span3);

    const span4 = document.createElement('span');
    span4.className = 'cell-body-span';
    span4.setAttribute('cid', 'product-name-cell');
    newRow.appendChild(span4);

    const span5 = document.createElement('span');
    span5.className = 'cell-body';

    const quantityInput = document.createElement('input');
    quantityInput.type = 'text';
    quantityInput.name = 'quantity[]';
    quantityInput.id = 'quantity';
    quantityInput.value = '0';
    quantityInput.className = 'input';
    quantityInput.setAttribute('cid', 'product-quantity-cell');
    span5.appendChild(quantityInput);
    newRow.appendChild(span5);

    const span6 = document.createElement('span');
    span6.className = 'cell-body-last';

    const priceInput = document.createElement('input');
    priceInput.type = 'text';
    priceInput.name = 'price[]';
    priceInput.id = 'price';
    priceInput.value = '0';
    priceInput.className = 'input';
    priceInput.setAttribute('cid', 'product-price-cell');
    span6.appendChild(priceInput);
    newRow.appendChild(span6);

    const removeButton = document.createElement('button');
    removeButton.type = 'button'
    removeButton.textContent = 'x';
    newRow.appendChild(removeButton);

    quantityInput.addEventListener('keyup', () => {
        const number = parseInt(quantityInput.value, 10);
        if((quantityInput.value !=='') && (isNaN(number) || number.toString() !== quantityInput.value)) {
            alert("정수만 입력할 수 있습니다.");
            quantityInput.value = '';
            return;
        }
    });

    priceInput.addEventListener('keyup', () => {
        const number = parseInt(priceInput.value, 10);
        if((priceInput.value !=='') && (isNaN(number) || number.toString() !== priceInput.value)) {
            alert("정수만 입력할 수 있습니다.");
            priceInput.value = '';
            return;
        }
    });

    removeButton.addEventListener('click', (event) => {
        if(confirm('정말로 이 상품을 삭제하시겠습니까?')){
            const code = span1.textContent;
            const name = span4.textContent;
            requestData = {code: code, name: name};
            fetch('/admin_page/product/delete', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP 오류. 상태코드: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if(data.result){
                    alert('상품이 삭제되었습니다.');
                    location.reload();
                }else{
                    alert('처리 중 문제가 발생했습니다.')
                }
            })
            .catch((error) => {
                alert(`요청 중 에러가 발생했습니다.\n\n${error.message}`);
                window.location.href = `/admin_page`;
            });
        }
    });

    return newRow;
}


const queryResult = document.querySelector('#inventory');
    
// 출력된 데이터 요소들을 제거하는 함수
const deleteData = () => {
    const pageDataAll = document.querySelectorAll('.row');
    for (let i=0; i<pageDataAll.length; i++){
        pageDataAll[i].remove();
    }
}

// 화면에 데이터 요소들을 출력하는 함수. 페이지 번호와 해당 페이지의 정보(마지막 페이지인지 여부)를 입력받음
const showData = (pn, lastPage) => {
    deleteData();
    if(lastPage){ // 마지막 페이지를 생성할 경우
        const pageDataLength = queryData.slice((pn-1) * pageIdx).length;
        for(let i=0; i<pageDataLength; i++){
            queryResult.appendChild(createRow());
        }
    }else{ // 그외 페이지들을 생성할 경우
        for(let i=0; i<pageIdx; i++){
            queryResult.appendChild(createRow());
        }
    }

    const productCode = document.querySelectorAll("[cid='product-code-cell']");
    const productType = document.querySelectorAll("[cid='product-type-cell']");
    const productCategory = document.querySelectorAll("[cid='product-category-cell']");
    const productName = document.querySelectorAll("[cid='product-name-cell']");
    const productQuantity = document.querySelectorAll("[cid='product-quantity-cell']");
    const productPrice = document.querySelectorAll("[cid='product-price-cell']");

    let j = (pn-1) * pageIdx ;
    for (let i=0; i<productCode.length; i++){
        productCode[i].textContent = queryData[j][0];
        productType[i].textContent = queryData[j][1];
        productCategory[i].textContent = queryData[j][2];
        productName[i].textContent = queryData[j][3];
        productQuantity[i].value = queryData[j][4];
        productPrice[i].value = queryData[j][5];
        j++;
    }
}

// 첫 페이지를 출력하는 함수
const showFirstData = () => {
    if(queryData.length <= pageIdx){ // 데이터가 9개 이하인 경우 첫 페이지가 마지막 페이지임
        showData(1, true);
    }else{
        showData(1, false);
    }
}

// 전구 아이콘 이미지들을 전부 제거하는 함수
const removeIcon = () => {
    const allIcon = document.querySelectorAll('.icon-img');
    allIcon.forEach(icon => {
        icon.src = noImgPath;
    });
}

// 숫자를 입력 받아 입력값보다 작은 재고량 값을 가지는 요소에 전구 아이콘을 생성하는 함수
const createIcon = (daysPredictSalesObject, sumOfCategoryQuantity) => {
    removeIcon();
    const iconImgArray = document.querySelectorAll('.icon-img'); // img 태그
    const productCategoryArray = document.querySelectorAll("[cid='product-category-cell']"); // span 태그

    for(let i=0; i<productCategoryArray.length; i++){
        for(let key in sumOfCategoryQuantity){
            if(key === productCategoryArray[i].textContent){
                if(daysPredictSalesObject[key] > sumOfCategoryQuantity[key]){
                    iconImgArray[i].src = getIconImgPath(categoryKoreanName, key);
                }
            }
        }
    }
}