document.addEventListener('DOMContentLoaded', () => {
    // [홈] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#home').addEventListener('click', ()=>{
        window.location.href = '/';
    });

    // [←] 버튼을 눌렀을 때 이전 페이지로 이동할 URL 이벤트
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/admin_page';
    });


    prevBtn.addEventListener("click", () => {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar();
    });
    /* 
    1. 이전 버튼(prevBtn)을 클릭하면 현재 월을 이전 월로 변경하고, 연도가 바뀌어야 한다면 연도를 변경한다.
    2. 변경된 월과 연도를 바탕으로 renderCalendar 함수를 호출하여 이전 월의 캘린더를 표시한다.
    */

    nextBtn.addEventListener("click", () => {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar();
    });
    /* 
    1. 다음 버튼(nextBtn)을 클릭하면 현재 월을 다음 월로 변경하고, 연도가 바뀌어야 한다면 연도를 변경한다.
    2. 변경된 월과 연도를 바탕으로 renderCalendar 함수를 호출하여 다음 월의 캘린더를 표시한다.
    */
    // 캘린더 소스코드 출처 : https://velog.io/@eungbi/Javascript-%EC%BA%98%EB%A6%B0%EB%8D%94-%EB%A7%8C%EB%93%A4%EA%B8%B0-1
});