document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#main-text').textContent = `${categoryKorenName[categoryName]} 수요 예측 정보`;
    document.querySelector('#category-img').src = `/static/${imgPath}`;
    document.querySelector('#today-weather').textContent = weatherTextData;

    let dayPredict = predictData[0];
    let dayPredictPercent = parseFloat((dayPredict / (yesterdaySalesRate) * 100).toFixed(2));

    document.querySelector('#day-predict').textContent = `${ylabel[0]}의 ${categoryKorenName[categoryName]} 예상 판매량은 ${dayPredict}개`;
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


    document.querySelector('#temperature-data').textContent = `${weatherNumberData[0]} °C`;
    document.querySelector('#windspeed-data').textContent = `${weatherNumberData[1]} m/s`;
    document.querySelector('#humidity-data').textContent = `${weatherNumberData[2]} %`;

    if(typeof(weatherNumberData[3])==="number"){
        document.querySelector('#precipitation-data').textContent = `${weatherNumberData[3]} mm`;
    }else{
        document.querySelector('#precipitation-data').textContent = `0.0 mm`;
    }

    document.querySelector(`#${categoryName}-btn`).className = 'category-select-clicked';
});