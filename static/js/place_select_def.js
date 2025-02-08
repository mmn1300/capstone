function user_page_load(){
    let selectedOption = select[select.selectedIndex];
    let selectedText = selectedOption.text;
    const userIpAdress = document.querySelector('#user-ip-address');
    data = {
        "place" : selectedText,
        "IP-URL" : userIpAdress.value
    }
    if(selectedText.trim() !== ''){
        if(userIpAdress.value.trim() !== ''){
            fetch('/create_user_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if(data.message){
                    window.location.href = '/user_page';
                }else{
                    alert('처리 중 오류가 발생했습니다');
                }
            });
        }else{
            alert('IP주소가 입력되지 않았습니다.');
        }
    }else{
        alert('해당 지점은 선택할 수 없습니다.');
    }
}