document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelector('#back_page').addEventListener('click', ()=>{
        window.location.href = '/admin_page';
    });

    document.querySelector('#beer').addEventListener('click',()=>{
        window.location.href = '/admin_page/demand_forecasting/beer';
    });

    document.querySelector('#icecream').addEventListener('click',()=>{
        window.location.href = '/admin_page/demand_forecasting/icecream';
    });

    document.querySelector('#mask').addEventListener('click',()=>{
        window.location.href = '/admin_page/demand_forecasting/mask';
    });

    document.querySelector('#soda').addEventListener('click',()=>{
        window.location.href = '/admin_page/demand_forecasting/soda';
    });
    
    document.querySelector('#umbrella').addEventListener('click',()=>{
        window.location.href = '/admin_page/demand_forecasting/umbrella';
    });

    document.querySelector('#water').addEventListener('click',()=>{
        window.location.href = '/admin_page/demand_forecasting/water';
    });

});