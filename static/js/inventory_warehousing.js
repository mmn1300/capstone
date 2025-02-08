document.addEventListener('DOMContentLoaded', () => {

    // 맨 처음 실행시 디폴트 값으로 먼저 식품 카테고리에 대한 재고 정보를 재고 목록에 나열함
    setItemList('식품');
    document.querySelector('#food-btn').className = 'category-btn-clicked';
    
    // 행을 생성하여 새로 추가
    const container = document.querySelector('#input-container');
    container.appendChild(createRow());
});