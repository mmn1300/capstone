document.addEventListener('DOMContentLoaded', () => {
    
    // [홈] 버튼을 눌렀을 때 이동할 URL 이벤트
    document.querySelector('#home').addEventListener('click', ()=>{
        window.location.href = '/';
    });

    // [←] 버튼을 눌렀을 때 이전 페이지로 이동할 URL 이벤트
    document.querySelector('#backPage').addEventListener('click', ()=>{
        window.location.href = '/admin_page';
    });

    // 각 카테고리에 해당하는 버튼을 누르면 해당 카테고리의 수요 예측 정보 페이지로 이동함
    const categoryArray = ["beer", "icecream", "soda", "umbrella", "water", "snack"]

    for(let i = 0; i < categoryArray.length; i++){
        document.querySelector(`#${categoryArray[i]}-btn`).addEventListener('click', () => {
            const queryString = new URLSearchParams({ category: categoryArray[i] }).toString();
            window.location.href = `/admin_page/demand_forecasting?${queryString}`;
        });
    }

    // n일차 버튼을 누르면 해당 날짜의 예상 판매량과 퍼센트 수치를 텍스트로 나타내주는 이벤트 함수
    for(let i = 0; i < 8; i++) {
        document.querySelector(`#day-button${i+1}`).addEventListener('click', setText);
    }

    
    document.querySelector('#inventory-quantity-btn').addEventListener('click', (event) =>{
        if(event.target.textContent === '현재 재고 수량'){
            event.target.textContent = `${categoryQuantity} 개`;
            event.target.className = 'data-text-btn-clicked';
        }else{
            event.target.textContent = '현재 재고 수량';
            event.target.className = 'data-text-btn';
        }
    });

    document.querySelector('#demand-forecasting-btn').addEventListener('click', setPredictData);

    document.querySelector('#required-number-btn').addEventListener('click', setRequiedNumber);

    document.addEventListener('keydown', (event) => {
        if(event.ctrlKey && event.altKey && (event.key === 'd' || event.key === 'D')){
            const predictDay = prompt(
                "특정 날짜의 과거 예측 데이터를 확인하시려면\n"+
                "YYYY-MM-DD 형식으로 날짜를 입력하셔야합니다.\n\n"+
                "예를 들어, 광복절을 원하시면 2024-08-15를 입력해 주세요\n"+
                "날짜는 2024-01-01부터 오늘 날짜까지 입력 가능합니다."
            );
            const today = new Date();
            const formattedDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
            if(predictDay === formattedDate){
                location.reload();
                return;
            }
            const regex = /^\d{4}-\d{2}-\d{2}$/;
            if (!regex.test(predictDay)) {
                alert('올바르지 않은 형식입니다.')
                return;
            }
            const date = new Date(predictDay);
            const [year, month, day] = predictDay.split('-').map(Number);
            if((date.getFullYear() === year && date.getMonth() + 1 === month && date.getDate() === day && date.getFullYear() === 2024) === false){
                alert('올바르지 않은 날짜입니다.')
                return;
            }
            if(today<date){
                alert('미래 날짜의 예측 데이터는 확인하실 수 없습니다.');
                return;
            }

            const requestData = {
                category: categoryName,
                date : predictDay
            }
            const queryString = new URLSearchParams(requestData).toString();
            fetch(`/admin_page/demand_forecasting/date?${queryString}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(response => {
                if (!response.ok) {
                  throw new Error('Network response was not ok');
                }
                return response.json();  // 응답을 JSON 형식으로 변환
            })
            .then(data => {
                // 데이터 업데이트
                myChart.data.datasets[0].data = data.newPredictData;

                const weekdays = ["일", "월", "화", "수", "목", "금", "토"];
                const ylabel = [];
                const day = new Date(predictDay);
                // ["26일(월)", "27일(화)", "28일(수)", ...] 형식으로 그래프의 레이블을 생성
                for (let i = 0; i <= 7; i++) {
                    const date = new Date(day);
                    date.setDate(day.getDate() + i);
                    ylabel.push(`${date.getDate()}일(${weekdays[date.getDay()]})`)
                }
                myChart.data.labels = ylabel;

                // 차트 업데이트
                myChart.update();

                // 날씨 정보 업데이트
                if(data.weatherData !== false){
                    document.querySelector('#temperature-data').textContent = `${data.weatherData[0]} °C`;
                    document.querySelector('#windspeed-data').textContent = `${data.weatherData[1]} m/s`;
                    document.querySelector('#humidity-data').textContent = `${data.weatherData[2]} %`;
                    document.querySelector('#precipitation-data').textContent = `${data.weatherData[3]} mm`;
                    document.querySelector('#today-weather').textContent = '과거 예측 데이터 확인 중입니다.';
                }else{
                    console.error('요청 중 오류가 발생했습니다\n\n오류 종류 : 날씨 정보 로딩 오류');
                }

                alert('수요 예측 정보가 해당 날짜로 변경되었습니다.');
                document.querySelector('#main-text').textContent = `${categoryKorenName[categoryName]} 수요 예측 정보 (${predictDay})`;

                for(let i = 0; i < 8; i++) {
                    document.querySelector(`#day-button${i+1}`).removeEventListener('click', setText);
                    document.querySelector(`#day-button${i+1}`).addEventListener('click', () => {
                        alert('과거 예측량에서는 이 기능을 지원하지 않습니다.\n'+
                            '이 기능을 다시 사용하고 싶으시면 페이지를 새로고침 해주세요.');
                    });
                }
                const parentElement = document.querySelector('#text-7');
                while (parentElement.firstChild) {
                    parentElement.removeChild(parentElement.firstChild);
                }
                parentElement.appendChild(document.createElement('span'));
                parentElement.firstChild.textContent = '과거 예측 데이터 확인 중입니다.';

                idArr = ['#demand-forecasting-btn', '#required-number-btn'];
                document.querySelector(idArr[0]).removeEventListener('click', setPredictData);
                document.querySelector(idArr[1]).removeEventListener('click', setRequiedNumber);
                for(let i=0; i<idArr.length; i++){
                    document.querySelector(idArr[i]).addEventListener('click', () => {
                        alert('과거 예측량에서는 이 기능을 지원하지 않습니다.\n'+
                            '이 기능을 다시 사용하고 싶으시면 페이지를 새로고침 해주세요.');
                    });
                    document.querySelector(idArr[i]).className = 'data-text-btn';
                }
                document.querySelector(idArr[0]).textContent = '7일간 예상 수요량';
                document.querySelector(idArr[1]).textContent = '추가 필요 수량';
            })
            .catch(error => {
                console.error('요청 중 오류가 발생했습니다\n\n오류 종류 : ', error);
            });
        }
    })
});