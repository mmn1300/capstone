const categoryKorenName = {
    beer : "맥주",
    icecream : "아이스크림",
    mask : "마스크",
    soda : "탄산음료",
    umbrella : "우산",
    water : "생수",
    snack : "과자"
}

// 배열을 입력받아 모든 값을 더해 반환하는 함수
const getArraySum = (arr) => {
    let sum = 0;
    arr.forEach(element => {
        sum += element;
    });
    
    // 소수점 2째 자리까지만 반환
    return parseFloat(sum.toFixed(2));
}

const requiredNum = getArraySum(predictData.slice(0, 7));

const ctx = document.querySelector('#myChart').getContext('2d');
const weekdays = ["일", "월", "화", "수", "목", "금", "토"];
const ylabel = [];
const today = new Date();
// ["26일(월)", "27일(화)", "28일(수)", ...] 형식으로 그래프의 레이블을 생성
for (let i = 0; i <= 7; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    ylabel.push(`${date.getDate()}일(${weekdays[date.getDay()]})`)
}


// Chart.js 차트 설정
const myChart = new Chart(ctx, {
    type: 'line', // 꺾은 선 그래프
    data: {
        labels: predictData.map((_, index) => `${ylabel[index]}`), // X축 레이블
        datasets: [{
            label: '데이터',
            data: predictData,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderWidth: 2,
            pointRadius: 5,
            pointBackgroundColor: 'rgba(75, 192, 192, 1)',
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: '날짜'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: '예상 판매량'
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `값: ${context.raw}`;
                    }
                }
            }
        }
    }
});

function setText(event){
    const i = parseInt(event.target.id.slice(10)) - 1;
    dayPredict = predictData[i];
    if(i===0){
        dayPredictPercent = parseFloat((dayPredict / (yesterdaySalesRate) * 100).toFixed(2));
    }else{
        dayPredictPercent = parseFloat((dayPredict / (predictData[i-1]) * 100).toFixed(2));
    }
    if(event.target.className === 'day-button'){
        const dayButtonClickedArray = document.querySelectorAll('.day-button-clicked');
        dayButtonClickedArray.forEach(element => {
            element.className = 'day-button';
        });
        event.target.className = 'day-button-clicked';
    }

    document.querySelector('#day-predict').textContent = `${ylabel[i]}의 ${categoryKorenName[categoryName]} 예상 판매량은 ${dayPredict}개`;
    document.querySelector('#span-text1').textContent = '전일 대비 ';
    document.querySelector('#span-text2').textContent =`${dayPredictPercent} % `;
    document.querySelector('#span-text3').textContent ='입니다.';

    if(dayPredictPercent>100){
        document.querySelector('#span-text2').className = 'highlight-red';
    }else if(dayPredictPercent<100){
        document.querySelector('#span-text2').className = 'highlight-blue';
    }else{
        document.querySelector('#span-text2').className = 'highlight-black';
    }
};

function setPredictData(event){
    if(event.target.textContent === '7일간 예상 수요량'){
        event.target.textContent = `${Math.ceil(requiredNum)} 개`;
        event.target.className = 'data-text-btn-clicked';
    }else{
        event.target.textContent = '7일간 예상 수요량';
        event.target.className = 'data-text-btn';
    }
};

function setRequiedNumber(event){
    const requiredQuantity = Math.ceil(requiredNum-categoryQuantity);
    if(event.target.textContent === '추가 필요 수량'){
        event.target.textContent = `${ requiredQuantity>0 ? requiredQuantity : 0 } 개`;
        event.target.className = 'data-text-btn-clicked';
    }else{
        event.target.textContent = '추가 필요 수량';
        event.target.className = 'data-text-btn';
    }
};