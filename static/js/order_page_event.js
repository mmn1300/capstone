document.addEventListener('DOMContentLoaded', () => {

    // 첫번째 선택 상자(상품 형태)의 옵션이 변경되면 우측의 하위 선택상자의 옵션을 생성하는 이벤트 함수
    document.querySelector('#productType').addEventListener('change', (event) => {
        const selectCategory = document.querySelector('#category');
        while (selectCategory.firstChild) {
            selectCategory.removeChild(selectCategory.firstChild);
        }
        const selectProductName = document.querySelector('#productName');
        while (selectProductName.firstChild) {
            selectProductName.removeChild(selectProductName.firstChild);
        }

        // 선택된 옵션의 텍스트를 가져옴.
        let selectedOption = event.target.options[event.target.selectedIndex];
        let selectedText = selectedOption.text;

        if(selectedText === '새 물품 추가'){
            const option1 = document.createElement('option');
            option1.textContent = '';
            selectCategory.appendChild(option1)

            const option2 = document.createElement('option');
            option2.textContent = '';
            selectProductName.appendChild(option2)
        }else{ // 그 외 [식품, 음료, 위생용품, 기타] 옵션 선택 시
            const options = [];

            // 해당 옵션에 맞는 카테고리들을 오른쪽 select의 옵션으로 생성
            for(let i=0; i<productTypeToCategory[selectedText].length; i++){
                options.push({text : productTypeToCategory[selectedText][i]});
            }
            options.forEach(optionData => {
                const option = document.createElement('option');
                option.textContent = optionData.text;
                selectCategory.appendChild(option);
            });

            selectedOption = selectCategory.options[selectCategory.selectedIndex];
            selectedText = selectedOption.text;

            const pnOptions = [];

            for(let i=0; i<categoryToProductName[selectedText].length; i++){
                pnOptions.push({text : categoryToProductName[selectedText][i]});
            }
            pnOptions.forEach(optionData => {
                const option = document.createElement('option');
                option.textContent = optionData.text;
                selectProductName.appendChild(option);
            });
        }
    });

    // 두번째 선택 상자(카테고리)의 옵션이 변경되면 우측의 하위 선택상자의 옵션을 생성함
    document.querySelector('#category').addEventListener('change', (event) => {
        const selectProductName = document.querySelector('#productName');
        while (selectProductName.firstChild) {
            selectProductName.removeChild(selectProductName.firstChild);
        }
        const selectedOption = event.target.options[event.target.selectedIndex];
        const selectedText = selectedOption.text;

        const options = [];

        // 해당 옵션에 맞는 상품들을 오른쪽 select의 옵션으로 생성
        for(let i=0; i<categoryToProductName[selectedText].length; i++){
            options.push({text : categoryToProductName[selectedText][i]});
        }
        options.forEach(optionData => {
            const option = document.createElement('option');
            option.textContent = optionData.text;
            selectProductName.appendChild(option);
        });
    });
    
    // [항목 추가] 버튼 클릭시 선택상자에 선택된 값으로 항목을 생성함. 우측 테이블에 생성된 항목의 데이터를 삽입
    document.querySelector('#add-new-row').addEventListener('click', () => {
        if(inputItemRowCount<itemRowCount){
            const itemInputGroup = document.querySelector('.item-input-group');
            itemInputGroup.appendChild(createRow());
            const itemName = document.querySelector(`#input-item-name${inputItemRowCount}`)

            const itemInputCode = document.querySelectorAll('.item-code-cell');
            if(itemName.value in productNameToCodeAndPrice){
                itemInputCode[inputItemRowCount].value = productNameToCodeAndPrice[itemName.value][0];
            }

            const itemInputNameArray = document.querySelectorAll('.item-name-cell');
            itemInputNameArray[inputItemRowCount].value = itemName.value;

            const itemInputQuantityArray = document.querySelectorAll('.item-quantity-cell');
            const quantity = document.querySelector(`#input-item-quantity${inputItemRowCount}`).value;
            itemInputQuantityArray[inputItemRowCount].value = quantity;

            const itemInputPriceArray = document.querySelectorAll('.item-price-cell');
            let price = 0;
            if(itemName.value in productNameToCodeAndPrice){
                price =  productNameToCodeAndPrice[itemName.value][1];
            }
            itemInputPriceArray[inputItemRowCount].value = price;

            const itemInputSumPriceArray = document.querySelectorAll('.item-sum-price-cell');
            itemInputSumPriceArray[inputItemRowCount].value = 0;

            inputItemRowCount++;
        }else{
            alert('더이상 추가하실 수 없습니다.');
        }
    });

    // [AI 추천] 클릭시 예측 기간만큼의 AI 예측량을 받아옴. 예측량 만큼 발주서를 작성함
    document.querySelector('#add-ai-recommendation').addEventListener('click', () => {
        const predictDay = parseInt(prompt(
            "AI 예측 데이터를 기반으로 발주량을 추천받으시려면,\n"+
            "예측 기간(일 수)을 입력하셔야합니다.\n\n"+
            "예를 들어, 7일치를 원하시면 숫자로 7을 입력해 주세요\n"+
            "예측 기간은 1일치부터 7일치까지 입력 가능합니다."
        ));
        if(Number.isInteger(predictDay)){
            if(predictDay >= 1 && predictDay <= 7){
                const inputs = document.querySelectorAll('.input-item-name');
                const items = Array.from(inputs).map(input => input.value);
                const requestData = { day: predictDay, items: items }
                fetch(`/admin_page/order_page/predict`, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData),
                    })
                    .then(response => response.json())  // 서버의 응답을 JSON으로 처리
                    .then(data => {
                        if(confirm("발주 물품 수량을 예측 판매량만큼 변경합니다.")){
                            if(Object.values(data.distributedQuantityDict).every(value => value === 0)){
                                alert('해당 기능은 수요 예측을 실행해야만 사용하실 수 있습니다.');
                            }else{
                                orderSettingToPredictData(inputs, data);
                            }
                        }
                    })
                    .catch(error => {
                        console.error('요청 실패:', error);
                    });
            }else{
                alert("입력할 수 없는 범위의 일 수입니다.")
            }
        }else{
            alert("숫자만 입력할 수 있습니다.")
        }
    });

    // [파일 다운로드] 클릭시 서버에 테이블에 존재하는 데이터들을 전송
    document.querySelector('#file-download').addEventListener('click', () => {
        document.querySelector('#create_xlsx').submit();
    });

    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    });

    document.querySelector('#backPage').addEventListener('click', () => {
        window.location.href = '/admin_page';
    });

    // 좌측 상단 발주서 정보 입력 공간과 우측 발주서 정보 입력 공간 연결. 서로 같은 값을 가지도록 하는 이벤트 함수들 생성
    const infoData = document.querySelectorAll('.info-data');
    const infoInput = document.querySelectorAll('.info-input');
    for(let i=0; i<infoData.length; i++){
        infoInput[i].value = infoData[i].value;

        infoData[i].addEventListener('keyup', () => {
            infoInput[i].value = infoData[i].value; 
        });
        infoInput[i].addEventListener('keyup', () => {
            infoData[i].value = infoInput[i].value; 
        });
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 's' || event.key === 'S') {
            const allData = document.querySelectorAll("[name=item_info]");
            allData.forEach(element => {
                console.log(typeof(element.value));
            });
        }
    });
});