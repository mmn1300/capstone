document.addEventListener('DOMContentLoaded', () => {
    
    // [홈] 버튼을 눌렀을 때 홈 페이지 이동
    document.querySelector('#home').addEventListener('click', ()=>{
        window.location.href = '/';
    });


    // 페이지를 이전으로 넘기는 이벤트.
    document.querySelector('#previous-page-btn').addEventListener('click', () => {
        const pn = Number(document.querySelector('#page-number').value);
        if(pn>1){
            document.querySelector('#page-number').value = pn - 1;
            showData(pn-1,false);
        }
        
        if(threeBtnFlag){
            createIcon(sumOfThreeDaysPredictSales);
        }else if(sevenBtnFlag){
            createIcon(sumOfSevenDaysPredictSales);
        }
    });

    // 페이지를 다음으로 넘기는 이벤트.
    document.querySelector('#next-page-btn').addEventListener('click', () => {
        const pn = Number(document.querySelector('#page-number').value);
        const maxPageNum = Math.floor((queryData.length-1) / pageIdx) + 1;
        if(pn===maxPageNum-1){
            document.querySelector('#page-number').value = pn + 1;
            showData(pn+1,true);
        }else if(pn<maxPageNum){
            document.querySelector('#page-number').value = pn + 1;
            showData(pn+1,false);
        }

        if(threeBtnFlag){
            createIcon(sumOfThreeDaysPredictSales);
        }else if(sevenBtnFlag){
            createIcon(sumOfSevenDaysPredictSales);
        }
    });

    // 페이지 번호를 직접 입력하여 해당 페이지에 맞는 정보를 화면에 출력해주는 함수.
    document.querySelector('#page-number').addEventListener('change', () => {
        const pn = Number(document.querySelector('#page-number').value);
        const maxPageNum = Math.floor((queryData.length-1) / pageIdx) + 1;
        if(pn<1){
            document.querySelector('#page-number').value = 1;
            showFirstData();
        }else if(pn>=maxPageNum){
            document.querySelector('#page-number').value = maxPageNum;
            showData(maxPageNum, true);
        }else{
            showData(pn, false);
        }
    });


});