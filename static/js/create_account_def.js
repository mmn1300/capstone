const checkedImgPath = "/static/img/checked.png";
const uncheckedImgPath = "/static/img/unchecked.png";

const checkFalg = {
    id : false,
    pw : false,
    place : false,
    name : false,
    apCode : false 
}

async function idredundancyCheck(id){
    return fetch('/account/id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id : id})
    })
    .then(response => response.json())
    .then(data => {
        if(data["idCheck"]){
            checkFalg["id"] = "true";
            return true;
        }else{
            return false;
        }
    })
    // 동작이 정상적으로 수행되지 못했을 경우 에러 메세지를 출력함
    .catch(error => {
        alert('동작 수행 중 에러가 발생했습니다.');
        console.error('Error:', error);
    });
}

async function nameCheck(nickname){
    return fetch('/account/nickname', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({nickname : nickname})
    })
    .then(response => response.json())
    .then(data => {
        if(data["nicknameCheck"]){
            checkFalg["name"] = true;
            return true;
        }else{
            return false;
        }
    })
    // 동작이 정상적으로 수행되지 못했을 경우 에러 메세지를 출력함
    .catch(error => {
        alert('동작 수행 중 에러가 발생했습니다.');
        console.error('Error:', error);
    });
}

async function placeCheck(place){
    return fetch('/account/place', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({place : place})
    })
    .then(response => response.json())
    .then(data => {
        if(data["placeCheck"]){
            checkFalg["place"] = true;
            return true;
        }else{
            return false;
        }
    })
    // 동작이 정상적으로 수행되지 못했을 경우 에러 메세지를 출력함
    .catch(error => {
        alert('동작 수행 중 에러가 발생했습니다.');
        console.error('Error:', error);
    });
}

async function apCodeCheck(apCode){
    return fetch('/account/code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({code : apCode})
    })
    .then(response => response.json())
    .then(data => {
        if(data["codeCheck"]){
            checkFalg["apCode"] = true;
            return true;
        }else{
            return false;
        }
    })
    // 동작이 정상적으로 수행되지 못했을 경우 에러 메세지를 출력함
    .catch(error => {
        alert('동작 수행 중 에러가 발생했습니다.');
        console.error('Error:', error);
    });
}