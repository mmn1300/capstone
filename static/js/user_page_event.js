document.addEventListener('DOMContentLoaded', () => {
    
    // [홈] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#home').addEventListener('click', ()=>{
        window.location.href = '/user_page/logout';
    });

    // [←] 버튼을 눌렀을 때 이전 페이지로 이동할 URL 이벤트
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/user_page/admin_page';
    });

    // 스캔하기 버튼을 눌렀을 때 스캔을 진행하는 이벤트
    document.querySelector('#capture-image').addEventListener('click', () => {
        captureImage();
        captureImageFlag = true;
    });  
    
    // 확인 버튼을 눌렀을 때, 스캔결과대로 장바구니에 상품을 추가하는 함수
    document.querySelector('#add-item').addEventListener('click', ()=>{
        const result = document.querySelector('#recognized-item-name').textContent.length;
        if(captureImageFlag == true){
            if(cnt<=12){
                // 줄바꿈을 위한 태그
                const br = document.createElement('br');
                br.className = 'item-br';
                container.appendChild(br);
                
                // 생성한 태그 들을 담은 div 태그를 추가함 
                container.appendChild(createRow());
                cnt +=1;
                
                handleEvent();
            }else{
                alert('더이상 추가하실 수 없습니다.');
            }
        }else{
            alert('먼저 스캔을 하십시오.');
        }
    });

    // 키보드 S키를 누를때 발동하는 함수. 스캔하기 버튼을 눌렀을때와 동일한 동작을 수행.
    document.addEventListener('keydown', (event) => {
        if (event.key === 's' || event.key === 'S') {
            captureImage();
            captureImageFlag = true;
        }
    });
    
    // [결제하기] 버튼을 누를때 발동. 서버에 결제할 상품들의 정보를 전송.
    document.querySelector('#payment').addEventListener('click', () => {
        submitData();
        alert('결제가 완료되었습니다.');
    });
});