document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#download').addEventListener('click', () => {
        downloadCSV();
    });

    
    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    });

    document.querySelector('#backPage').addEventListener('click', () => {
        window.location.href = '/admin_page';
    });
});