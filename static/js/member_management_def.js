let threeBtnFlag = false;
let sevenBtnFlag = false;

const pageIdx = 10;


// 데이터를 표시할 행을 생성하는 함수
const createRow = () => {
    // 새로 추가할 행 div 생성
    const newRow = document.createElement('div');
    newRow.className = 'member-data';

    const span1 = document.createElement('span');
    const button = document.createElement('button');
    button.className = 'member-delete';
    button.textContent = 'x';
    span1.appendChild(button);
    newRow.appendChild(span1)

    const list = ['level', 'code', 'id', 'name', 'place'];
    const input = [];
    for(let i=0; i<list.length; i++){
        const span = document.createElement('span');
        input.push(document.createElement('input'));
        input[i].className = list[i];
        input[i].id = list[i];
        input[i].type = 'text';
        input[i].value = '';
        if(i===0){
            input[i].readOnly = true;
        }
        span.appendChild(input[i]);
        newRow.appendChild(span);
    }

    button.addEventListener('click', () => {
        const level = input[0].value;
        if(parseInt(level) === 0){
            alert('이 회원은 삭제할 수 없습니다.');
            return;
        }

        const code = input[1].value;
        const id = input[2].value;
        requestData = {
            id:id,
            mcode:Number(code)
        };
        fetch('/member/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP 오류. 상태코드: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if(data.result){
                alert('맴버 정보가 수정되었습니다.');
                location.reload();
            }else{
                alert('처리 중 문제가 발생했습니다.')
            }
        })
        .catch((error) => {
            alert(`요청 중 에러가 발생했습니다.\n\n${error.message}`);
            window.location.href = `/admin_page`;
        });
    });

    return newRow;
}

const queryResult = document.querySelector('.member-data-container');
const showData = (pn, lastPage) => {
    deleteData();
    if(lastPage){ // 마지막 페이지를 생성할 경우
        const pageDataLength = queryData.slice((pn-1) * pageIdx).length;
        for(let i=0; i<pageDataLength; i++){
            queryResult.appendChild(createRow());
        }
    }else{ // 그외 페이지들을 생성할 경우
        for(let i=0; i<pageIdx; i++){
            queryResult.appendChild(createRow());
        }
    }

    const levelArray = document.querySelectorAll(".level");
    const codeArray = document.querySelectorAll(".code");
    const idArray = document.querySelectorAll(".id");
    const nameArray = document.querySelectorAll(".name");
    const placeArray = document.querySelectorAll(".place");

    let j = (pn-1) * pageIdx ;
    for (let i=0; i<levelArray.length; i++){
        levelArray[i].value = queryData[j][0];
        codeArray[i].value = queryData[j][1];
        idArray[i].value = queryData[j][2];
        nameArray[i].value = queryData[j][3];
        placeArray[i].value = queryData[j][4];
        j++;
    }
}


const showFirstData = () => {
    if(queryData.length <= pageIdx){ // 데이터가 9개 이하인 경우 첫 페이지가 마지막 페이지임
        showData(1, true);
    }else{
        showData(1, false);
    }
}

// 출력된 데이터 요소들을 제거하는 함수
const deleteData = () => {
    const pageDataAll = document.querySelectorAll('.member-data');
    for (let i=0; i<pageDataAll.length; i++){
        pageDataAll[i].remove();
    }
}