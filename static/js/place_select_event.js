document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#select-btn').addEventListener('click', user_page_load);

    document.addEventListener('keydown', (event) => {
        if(event.key === 'Enter'){
            user_page_load();
        }
    })

    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    });
});