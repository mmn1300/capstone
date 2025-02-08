document.addEventListener('DOMContentLoaded', () => {
    // [재고 등록] 버튼을 눌렀을 때 이동
    document.querySelector('#registerButton').addEventListener('click', function() {
        window.location.href = '/admin_page/inventory_info/inventory_warehousing';
    });

    // [재고 정보 출력] 버튼을 눌렀을 때 이동
    document.querySelector('#searchButton').addEventListener('click', function() {
        const queryString = new URLSearchParams({ category: 'all' }).toString();
        window.location.href = `/admin_page/inventory_info/products?${queryString}`;
    });

    // [홈] 버튼을 눌렀을 때 홈 페이지 이동
    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    });

    // [←] 버튼을 눌렀을 때 이전 페이지 이동
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/admin_page';
    });
});