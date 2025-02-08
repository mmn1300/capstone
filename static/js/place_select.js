const options = [];
const select = document.querySelector('#place-select');

for(let i=0; i<placeList.length; i++){
options.push({text : placeList[i]});
}
options.forEach(optionData => {
const option = document.createElement('option');
option.textContent = optionData.text;
select.appendChild(option);
});