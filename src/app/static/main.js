
function updateTimer(data){
    let timer = document.querySelector('.update_time');
    timer.innerHTML = data['update_time']['update_time'];
    delete data['update_time'];
}


function constructTables(ratesCount){
    let tables = document.querySelectorAll('table');
    let mainbox = document.querySelector('.maindiv');

    if (tables.length < ratesCount){
        let classCount = 1;

        for (let tablesCount = ratesCount - tables.length; tablesCount > 0; tablesCount--){
            let table = tables[0].cloneNode(true);  // first table always exists for a bluprint
            table.className = 'table' + classCount++;
            mainbox.append(table);
        }
    }
}


function markExchanger(exchange, row){
    const BTC24PRO = 'BTC24pro';
    let exchanger = exchange.indexOf(BTC24PRO) != -1 ? true : false;

    if (exchanger){
        row.childNodes[0].id = 'exchangerBTC24pro';
        row.childNodes[1].id = 'rateBTC24pro';
        row.childNodes[2].id = 'reserveBTC24pro';

    }else if (!exchanger && row.childNodes[0].getAttribute('id')){
        row.childNodes[0].removeAttribute('id')
        row.childNodes[1].removeAttribute('id')
        row.childNodes[2].removeAttribute('id')
    }
}


// main content function
function updateTables(table, array){
    let rowsList = table.querySelectorAll('[class*="exchanger"]');
    let rowLength = rowsList.length -1;  // length - 1 because of first header row
    let rowNumber = Object.keys(array).length;
    

    for (let counter = 0; counter < rowNumber; counter++){
        let exchanger = array[counter]['exchange_name'];

        if (rowLength < rowNumber){
            let newRow = table.insertRow();
            let nameCell = newRow.insertCell();
            let rateCell = newRow.insertCell();
            let reserveCell = newRow.insertCell();

            nameCell.innerHTML = array[counter]['exchange_name'];
            rateCell.innerHTML = array[counter]['receive_amount'];
            reserveCell.innerHTML = array[counter]['reserve'];

            nameCell.className = 'exchanger' + counter;
            rateCell.className = 'rate' + counter;
            reserveCell.className = 'reserve' + counter;
            markExchanger(exchanger, newRow);

        } else if(rowLength > rowNumber){
            console.log('Table rows counter feels bad');
            break

        } else {
            let nameCell = table.querySelector('.exchanger' + counter);
            let rateCell = table.querySelector('.rate' + counter);
            let reserveCell = table.querySelector('.reserve' + counter);

            nameCell.innerHTML = array[counter]['exchange_name'];
            rateCell.innerHTML = array[counter]['receive_amount'];
            reserveCell.innerHTML = array[counter]['reserve'];
            markExchanger(exchanger, nameCell.parentNode);
        }
    }
}


// main data processor
function parseData(data, timer){
    updateTimer(data, timer);
    
    const dataLength = Object.keys(data).length;
    constructTables(dataLength);
    let allTables = document.querySelectorAll('table');
    let currentTable = 0;

    for (let pair in data){
        let array = data[pair];
        let tableSelector = '.table' + currentTable;
        let pairCount = 0;

        for (table of allTables.values()){
            let tableHead = document.querySelector(tableSelector + ' thead tr th');
            tableHead.innerHTML = array[0]['give_name'] + ' - ' + array[0]['receive_name'];
            pairCount++;
        }
        
        let tableBody = document.querySelector(tableSelector + ' tbody');
        updateTables(tableBody, array);
        currentTable++;
    }
}


function promiseStatus(response){
    if (response.status >= 200 && response.status < 300) {  
      return Promise.resolve(response)  

    } else {  
      return Promise.reject(new Error(response.statusText))  
    }
}

function getJSON(response){
    return response.json()  
}

function fetchData(){
    const url = 'http://127.0.0.1:5000/api/rates:2000';
    fetch(url)
    .then(promiseStatus)
    .then(getJSON)
    .then(result => parseData(result))
}


setInterval(() => {fetchData();}, 30000);
