document.addEventListener('DOMContentLoaded', () => {
    // [재고 물품 등록 및 정보] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#inventoryInfo').addEventListener('click', function() {
        window.location.href = '/admin_page/inventory_info';  
    });

    // [판매 내역] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#salesHistory').addEventListener('click', function() {
        window.location.href = '/admin_page/sales_history';
    });

    // [수요 예측] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#demandForecasting').addEventListener('click', function() {
        window.location.href = '/admin_page/predict_model_load';
    });

    // [발주서 작성] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#orderPage').addEventListener('click', function() {
        window.location.href = '/admin_page/order_page';
    });

    // [홈] 버튼을 눌렀을 때 홈 페이지 이동
    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    })

    // [←] 버튼을 눌렀을 때 이전 페이지 이동
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/';
    });
});