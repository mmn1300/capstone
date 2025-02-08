document.addEventListener('DOMContentLoaded', () => {
    
    // [홈] 버튼을 눌렀을 때 홈 페이지 이동
    document.querySelector('#home').addEventListener('click', ()=>{
        window.location.href = '/';
    });

    // [←] 버튼을 눌렀을 때 이전 페이지 이동
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/admin_page/inventory_info';
    });


    // 카테고리 버튼들을 눌렀을 때 해당 질의 결과 페이지로 이동
    for (let i=0;i<categoryArray.length;i++){
        document.querySelector(`#${categoryArray[i]}`).addEventListener('click', ()=>{
            const queryString = new URLSearchParams({ category: categoryArray[i] }).toString();
            window.location.href = `/admin_page/inventory_info/products?${queryString}`;
        });
    }

    // [3일] 버튼 클릭시 예측된 3일치 판매량보다 재고가 적은 물품들을 이미지로 표시해주는 이벤트 함수
    document.querySelector('#predict-btn-left').addEventListener('click', (event) => {
        if(Object.values(sumOfThreeDaysPredictSales).every(value => value === 0)){
            alert('수요예측을 먼저 실행해 주세요.');
        }else{
            if(threeBtnFlag){
                removeIcon();
                threeBtnFlag = false;
                event.target.className = 'predict-btn';
            }else{
                createIcon(sumOfThreeDaysPredictSales, sumOfCategoryQuantity);
                const clickedBtn = document.querySelector('.predict-btn-clicked');
                threeBtnFlag = true;
                sevenBtnFlag = false;
                if(clickedBtn){
                    clickedBtn.className = 'predict-btn';
                }
                event.target.className = 'predict-btn-clicked';
            }
        }
    });
    
    // [7일] 버튼 클릭시 예측된 7일치 판매량보다 재고가 적은 물품들을 이미지로 표시해주는 이벤트 함수
    document.querySelector('#predict-btn-right').addEventListener('click', (event) => {
        if(Object.values(sumOfSevenDaysPredictSales).every(value => value === 0)){
            alert('수요예측을 먼저 실행해 주세요.');
        }else{
            if(sevenBtnFlag){
                removeIcon();
                sevenBtnFlag = false;
                event.target.className = 'predict-btn';
            }else{
                createIcon(sumOfSevenDaysPredictSales, sumOfCategoryQuantity);
                const clickedBtn = document.querySelector('.predict-btn-clicked');
                threeBtnFlag = false;
                sevenBtnFlag = true;
                if(clickedBtn){
                    clickedBtn.className = 'predict-btn';
                }
                event.target.className = 'predict-btn-clicked';
            }
        }
    });

    // 페이지를 이전으로 넘기는 이벤트.
    document.querySelector('#previous-page-btn').addEventListener('click', () => {
        const pn = Number(document.querySelector('#page-number').value);
        if(pn>1){
            document.querySelector('#page-number').value = pn - 1;
            showData(pn-1,false);
        }
        
        if(threeBtnFlag){
            createIcon(sumOfThreeDaysPredictSales, sumOfCategoryQuantity);
        }else if(sevenBtnFlag){
            createIcon(sumOfSevenDaysPredictSales, sumOfCategoryQuantity);
        }
    });

    // 페이지를 다음으로 넘기는 이벤트.
    document.querySelector('#next-page-btn').addEventListener('click', () => {
        const pn = Number(document.querySelector('#page-number').value);
        const maxPageNum = Math.floor((queryData.length-1) / pageIdx) + 1;
        if(pn===maxPageNum-1){
            document.querySelector('#page-number').value = pn + 1;
            showData(pn+1,true);
        }else if(pn<maxPageNum){
            document.querySelector('#page-number').value = pn + 1;
            showData(pn+1,false);
        }

        if(threeBtnFlag){
            createIcon(sumOfThreeDaysPredictSales, sumOfCategoryQuantity);
        }else if(sevenBtnFlag){
            createIcon(sumOfSevenDaysPredictSales, sumOfCategoryQuantity);
        }
    });

    // 페이지 번호를 직접 입력하여 해당 페이지에 맞는 정보를 화면에 출력해주는 함수.
    document.querySelector('#page-number').addEventListener('change', () => {
        const pn = Number(document.querySelector('#page-number').value);
        const maxPageNum = Math.floor((queryData.length-1) / pageIdx) + 1;
        if(pn<1){
            document.querySelector('#page-number').value = 1;
            showFirstData();
        }else if(pn>=maxPageNum){
            document.querySelector('#page-number').value = maxPageNum;
            showData(maxPageNum, true);
        }else{
            showData(pn, false);
        }
    });

    // 변경하기 버튼을 눌렀을 때 재고 정보 변경사항을 app.py에 보낸 다음에 데이터베이스에 반영시킴
    document.querySelector('.update-item-button').addEventListener('click', () => {
        if(confirm("입력하신 내용으로 재고 정보를 수정 하시겠습니까?")){
            const productCodeArray = document.querySelectorAll('[cid=product-code-cell]');
            const quantityArray = document.querySelectorAll('[cid=product-quantity-cell]');
            const priceArray = document.querySelectorAll('[cid=product-price-cell]');

            const productCodes = [];
            const quantitys = [];
            const prices = [];
            productCodeArray.forEach(element => {
                productCodes.push(element.textContent)
            });
            quantityArray.forEach(element => {
                quantitys.push(element.value)
            });
            priceArray.forEach(element => {
                prices.push(element.value)
            });

            requestData = {
                productCodes:productCodes,
                quantitys:quantitys,
                prices:prices
            }

            fetch('/admin_page/inventory_info_update', {
                method: 'PUT',
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
                alert('재고 정보가 수정되었습니다.');
                const queryString = new URLSearchParams({ category: 'all' }).toString();
                window.location.href = `/admin_page/inventory_info/products?${queryString}`;
            })
            .catch((error) => {
                alert(`요청 중 에러가 발생했습니다.\n\n${error.message}`);
                window.location.href = `/admin_page/inventory_info/db_query`;
            });
        }
    });
});