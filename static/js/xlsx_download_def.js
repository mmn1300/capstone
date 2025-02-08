async function downloadCSV() {
    const fileName = document.querySelector('#download').getAttribute('fn');

    // POST 요청을 보내서 문자열 데이터를 서버로 전송
    const response = await fetch(`/admin_page/order_page/create_xlsx/download/${fileName}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })

    // 서버 응답으로부터 파일을 다운로드
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName; // 다운로드할 파일 이름
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}