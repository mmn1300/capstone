document.addEventListener('DOMContentLoaded', () => {
    // 페이지가 로드되면 renderCalendar 함수를 실행하여 초기 캘린더를 표시한다.
    renderCalendar();

    // 초기 화면 판매 수량 카운트
    const srArray = document.querySelectorAll('[column=sales_rate]');
    let sum = 0;
    srArray.forEach(e => {
        sum+=Number(e.textContent);
    });
    document.querySelector('#sales_rate').textContent = `총 판매 수량 : ${sum} 개`;
});

