document.addEventListener('DOMContentLoaded', () => {

    // [추가]버튼을 클릭했을 때의 이벤트
    document.querySelector('#addRow').addEventListener('click', () => {

        if(cnt<8){
            // 줄바꿈을 위한 태그
            const container = document.querySelector('#input-container');
            const br = document.createElement('br');
            container.appendChild(br);

            // 생성한 태그 들을 담은 div 태그를 추가함 
            container.appendChild(createRow());

            cnt+=1;

        }else{
            alert('더이상 추가하실 수 없습니다');
        }
    });

    // [홈] 버튼을 눌렀을 때 홈 페이지 이동
    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    });

    // [←] 버튼을 눌렀을 때 이전 페이지 이동
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/admin_page/inventory_info';
    });

    // [등록] 버튼을 눌렀을 때 서버에 데이터를 전송함.
    document.querySelector('#submitData').addEventListener('click', () => {
        if(confirm('입력하신 내용을 재고에 등록하겠습니까?')){
            const allData = document.querySelectorAll('.text2');
            let shouldSubmit = true;

            // 상품명을 입력하지 않은 요소가 존재하는지 확인
            for (let i = 0; i < allData.length; i++) {
                const element = allData[i];
                if (element.value === '') {
                    // 취소 누르면 동작
                    if (!confirm('입력하신 내용중 공백인 요소가 존재합니다.\n\n이대로 등록하시겠습니까?')) {
                        shouldSubmit = false; 
                        break;
                    }
                }
            }
    
            if (shouldSubmit) {
                document.querySelector('#inputForm').submit();
                alert('해당 내용이 재고에 정상적으로 등록되었습니다.');
            }
        }
    });

    // 페이지를 이전으로 넘기는 이벤트.
    document.querySelector('#previous-page-btn').addEventListener('click', () => {
        const pn = Number(document.querySelector('#page-number').value);
        const category = document.querySelector('.left-span').textContent;

        // 1번 페이지 이전 페이지는 존재 하지 않으므로 동작을 제한함
        if(pn>1){
            document.querySelector('#page-number').value = pn - 1;
            deleteInventoryList();
            setItemList(category, pn-1);
        }
    });

    // 페이지를 다음으로 넘기는 이벤트.
    document.querySelector('#next-page-btn').addEventListener('click', () => {
        const pn = Number(document.querySelector('#page-number').value);
        const category = document.querySelector('.left-span').textContent;
        const maxPageNum = Math.floor((categoryToArray[category].length-1) / pageIdx) + 1;

        // 최대로 넘길 수 있는 마지막 페이지이므로 동작을 제한함.
        if(pn<maxPageNum){
            document.querySelector('#page-number').value = pn + 1;
            deleteInventoryList();
            setItemList(category, pn+1);
        }
    });
    
    // 페이지 번호 변경 이벤트
    document.querySelector('#page-number').addEventListener('change', (event) => {
        let pn = Number(event.target.value);
        if (pn === '') {
            pn = 1;
        }
    
        const category = document.querySelector('.left-span').textContent;
        const maxPageNum = Math.floor((categoryToArray[category].length - 1) / pageIdx) + 1;
    
        deleteInventoryList();
        if (pn < 1) {
            document.querySelector('#page-number').value = 1;
            setItemList(category);
        } else if (pn >= maxPageNum) {
            document.querySelector('#page-number').value = maxPageNum;
            setItemList(category, maxPageNum);
        } else {
            setItemList(category, pn);
        }
    });
    


    // 각 카테고리 버튼을 누르면 해당 카테고리에 속한 상품들을 출력하는 이벤트 함수
    for(let i=0; i<categoryArray.length; i++){
        document.querySelector(`#${categoryArray[i][0]}-btn`).addEventListener('click', (event) => {
            deleteInventoryList();
            document.querySelector('#page-number').value = 1;
            setItemList(`${categoryArray[i][1]}`);
            document.querySelectorAll('.category-btn-clicked').forEach(element => {
                element.className = 'category-btn';
            });
            event.target.className = 'category-btn-clicked';
        });
    }

    // 테스트용 코드
    document.addEventListener("keydown", (event) => {
        if(event.key === 's' || event.key === 'S'){
            const testsAll = document.querySelectorAll('[name=texts]');
            const tests2All = document.querySelectorAll('[name=texts2]');
            const numbersAll = document.querySelectorAll('[name=numbers]');

            testsAll.forEach(e => {
                console.log(typeof(e.value));
            });
            tests2All.forEach(e => {
                console.log(typeof(e.value));
            });
            numbersAll.forEach(e => {
                console.log(typeof(e.value));
            });
        }
    })
});