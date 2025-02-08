const calendarDates = document.getElementById("calendarDates");
const currentMonthElement = document.getElementById("currentMonth");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

const today = new Date(); // 현재 날짜를 나타내는 Date 객체를 저장한다.

let currentMonth = today.getMonth();
/* 현재 월을 나타내는 값을 저장한다. getMonth() 메서드는 0부터 시작하는 월을 반환하므로
1월이면 0, 2월이면 1을 반환한다. */
let currentYear = today.getFullYear(); // 변수에 현재 연도를 나타내는 값을 저장한다.

function renderCalendar() {
    /* renderCalendar 함수는 월별 캘랜더를 생성하고 표시하는 함수이다. */
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    /* firstDayOfMonth 변수에 현재 월의 첫 번째 날짜를 나타내는 Date 객체를 저장한다.
    해당 월의 첫 번째 날짜에 대한 정보를 얻는다. */
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    /* daysInMonth 변수에 현재 월의 총 일 수를 나타내는 값을 저장한다. 
    해당 월이 몇 일까지 있는지 알 수 있다. */
    const startDayOfWeek = firstDayOfMonth.getDay();
    /* 변수에 현재 월의 첫 번째 날짜의 요일을 나타내는 값을 저장한다.
    해당 월의 첫 번째 날짜가 무슨 요일인지 알 수 있다. */
    currentMonthElement.textContent = `${currentYear}년 ${currentMonth + 1}월`;
    // 월을 나타내는 요소에 현재 월과 연도를 설정하여 표시한다.

    calendarDates.innerHTML = ""; // 일자를 표시하는 그리드 컨테이너를 비운다.

    // 빈 날짜(이전 달)
    for (let i = 0; i < startDayOfWeek; i++) {
        const emptyDate = document.createElement("div");
        //  빈 날짜를 나타내는 div 요소를 생성한다.
        emptyDate.classList.add("date", "empty");
        // 생성한 div 요소에 "date"와 "empty" 클래스를 추가한다.
        calendarDates.appendChild(emptyDate);
        // 생성한 빈 날짜 요소를 캘린더 그리드에 추가한다.
    }

    // 현재 달의 날짜
    for (let i = 1; i <= daysInMonth; i++) {
        const dateElement = document.createElement("button");
        dateElement.classList.add("date");
        dateElement.textContent = i;
        dateElement.id = 'day-button'+String(i);
        calendarDates.appendChild(dateElement);

        // 해당 날짜를 클릭했을 때, 해당 날짜를 YYYY-MM-DD형식으로 만들어 서버에 날짜 정보를 넘기는 이벤트
        document.querySelector('#day-button'+String(i)).addEventListener('click', () => {
            const year = currentYear
            const month = ('0' + (currentMonth + 1)).slice(-2);
            const day = ('0' + String(i)).slice(-2);
            const date = `${year}-${month}-${day}`;
            const selectDate = new Date(date);

            // 판매기록은 현재 시점까지만 볼 수 있기에
            if(selectDate<today){
                const queryString = new URLSearchParams({ date: date }).toString();
                fetch(`/admin_page/sales_history/select_date?${queryString}`, {
                    method: 'GET'
                })
                .then(response => response.json())
                .then(responseData => {
                    document.querySelector('#date').textContent = `${responseData[0][0]} 편의점 판매 내역`;
                    const dateArray = document.querySelectorAll('[column=date]');
                    const codeArray = document.querySelectorAll('[column=code]');
                    const categoryArray = document.querySelectorAll('[column=category]');
                    const nameArray = document.querySelectorAll('[column=name]');
                    const srArray = document.querySelectorAll('[column=sales_rate]');
                    const elementArray = [dateArray, codeArray, categoryArray, nameArray, srArray];

                    for(let i=0; i<responseData.length; i++){
                        for(let j=0; j<responseData[i].length; j++){
                            elementArray[j][i].textContent = responseData[i][j];
                        }
                    }

                    let sum = 0;
                    srArray.forEach(e => {
                        sum+=Number(e.textContent);
                    });
                    document.querySelector('#sales_rate').textContent = `총 판매 수량 : ${sum} 개`;
                })
                .catch(error => console.error('Error:', error));
            }else{
                alert('해당 날짜는 선택하실 수 없습니다.');
            }
        });
    }
    /* 
    1. for 문을 이용하여 현재 월의 총 일 수만큼 반복하여 월의 날짜를 순서대로 표시한다.
    2. const dateElement = document.createElement("div");를 통해 날짜를 나타내는 div 요소를 생성한다.
    3. dateElement.classList.add("date");를 통해 생성한 div 요소에 "date" 클래스를 추가한다.
    4. dateElement.textContent = i;를 통해 해당 날짜 값을 div 요소의 텍스트로 설정한다.
    5. calendarDates.appendChild(dateElement);를 통해 생성한 날짜 요소를 캘린더 그리드에 추가한다.
    */

}

// 캘린더 소스코드 출처 : https://velog.io/@eungbi/Javascript-%EC%BA%98%EB%A6%B0%EB%8D%94-%EB%A7%8C%EB%93%A4%EA%B8%B0-1
