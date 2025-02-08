document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#login').addEventListener('click', () => {
        login();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            login();
        }
    });

    document.querySelector('#home').addEventListener('click', () => {
        window.location.href = '/';
    });

    document.querySelector('#backPage').addEventListener('click', () => {
        window.location.href = '/';
    });

    const inputs = document.querySelectorAll('input');
    inputs.forEach((input, index) => {
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Tab') {
                event.preventDefault();
                const nextIndex = (index + 1) % inputs.length;
                inputs[nextIndex].focus();
            }
        });
    });
});