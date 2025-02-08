document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#order-date-data').value = formatDate(today);
    document.querySelector('#delivery-date-data').value = formatDate(futureDate);
    document.querySelector('#orderer-data').value = place;

    // 테이블 행 [상품 코드, 상품 명, 수량, 개당 단가, 총 금액] 10개 생성
    for(let i=0; i<itemRowCount; i++){
        createCell();
    }
});