const host = {
	url:'http://91.240.86.166',
    local: 'http://127.0.0.1:5000'
}
export const URL = {
    logout: host.url + '/logout',
    currencies: host.url + '/api/currencies',
    sendToServer: host.url + '/api/receive/sidebar',
    getSettings: host.url + '/api/filters',
    rates: host.url + '/api/rates',
}


const tablesHandler = {
    tablesBuild(ratesLength){
        // create and remove tables
        let mainbox = document.querySelector('.tables-content')
        let tables = mainbox.querySelectorAll('table')
        
        if (tables.length < ratesLength){
            
            for (let tablesCount = ratesLength - tables.length; tablesCount > 0; tablesCount--){
                let tablesLength = mainbox.querySelectorAll('table').length
                let table = tables[0].cloneNode(true)  // first table always exists for the bluprint
                table.className = 'table' + tablesLength
                let tableInput = table.querySelector('th input')
                tableInput.value = ''
                mainbox.append(table)
            }

        } else if (tables.length > ratesLength){
            let classCount = 1

            for (let tablesCount = tables.length - ratesLength; tablesCount > 0; tablesCount--){
                let table = mainbox.querySelector('.table' + classCount++)
                table.remove()
            }

            let remainTables = mainbox.querySelectorAll('table')
            for (let tableNumber = 0; tableNumber < remainTables.length; tableNumber++){
                remainTables[tableNumber].className = 'table' + tableNumber
            }
        }
    },

    markExchanger(exchangerName, row, markedExchanger){
        let mark = markedExchanger
        let exchanger = exchangerName.indexOf(mark) != -1 ? true : false

        if (exchanger){
            row.childNodes[0].id = 'markedExchanger'
            row.childNodes[1].id = 'markedExchanger'
            row.childNodes[2].id = 'markedExchanger'
            row.childNodes[3].id = 'markedExchanger'
        }
    },

    updateContent(table, array, markedExchanger){
        // tables content

        let rowsList = table.querySelectorAll('[class*="exchanger"]')
        let rowsLength = rowsList.length - 1  // length - 1 because of first header row
        let arrayLength = Object.keys(array).length

        for (let counter = rowsLength; counter > 0; counter--){
            table.deleteRow(counter)
        }

        for (let counter = 0; counter < arrayLength; counter++){
            
            let exchangerName = array[counter]['exchange_name']
            let existsRowsNumber = table.querySelectorAll('[class*="exchanger"]').length
            let classCounter = existsRowsNumber > 1 ? existsRowsNumber - 1 : 0

            let newRow = table.insertRow()
            let [nameCell, giveCell, receiveCell, reserveCell] = 
            [newRow.insertCell(), newRow.insertCell(), newRow.insertCell(), newRow.insertCell()]

            nameCell.innerHTML = array[counter]['exchange_name']
            giveCell.innerHTML = array[counter]['give_amount']
            receiveCell.innerHTML = array[counter]['receive_amount']
            reserveCell.innerHTML = array[counter]['reserve']

            nameCell.className = 'exchanger' + classCounter
            giveCell.className = 'give-amount' + classCounter
            receiveCell.className = 'receive-amount' + classCounter
            reserveCell.className = 'reserve' + classCounter

            this.markExchanger(exchangerName, newRow, markedExchanger)
        }

    },

    parseData(data){
        // main data processor

        let cities = data['city']
        let dataHeaders = data['headers']
        let markedExchanger = data['marked_exchanger']['marked_exchanger']
        let time = data['update_time']['update_time']
        utility.updateTimer(time)
        delete data['city']
        delete data['headers']
        delete data['marked_exchanger']
        delete data['update_time']
        
        let dataLength = Object.keys(data).length
        this.tablesBuild(dataLength)
        let allTables = document.querySelectorAll('table')
        let currentTable = 0

        for (let pair in data){
            let array = data[pair]
            let tableSelector = '.table' + currentTable
            let tableHeader = document.querySelector(tableSelector + ' thead tr th span')
            let cityButton = document.querySelector(tableSelector + ' thead tr th button')
            let thisCity = cities[currentTable]
            cityButton.className = 'button'+ currentTable

            if (thisCity){
                tableHeader.innerHTML = dataHeaders[currentTable][0] + ' - ' + dataHeaders[currentTable][1] + ' / ' +
                thisCity
            }
            else{
                tableHeader.innerHTML = dataHeaders[currentTable][0] + ' - ' + dataHeaders[currentTable][1]
            }

            let tableBody = document.querySelector(tableSelector + ' tbody')
            this.updateContent(tableBody, array, markedExchanger)
            currentTable++
        }
    },
}


const utility = {
    updateTimer(time){
        let timer = document.querySelector('.update-time')
        const strOffset = 2
        const lengthString = 8
        let timeStart = time.indexOf(':') - strOffset
        timer.innerHTML = time.slice(timeStart, timeStart + lengthString)
    },

    promiseStatus(response){
        if (response.status >= 200 && response.status < 300) {  
            return Promise.resolve(response)  
      
          } 
          else {  
            return Promise.reject(new Error(response.statusText))  
          }
    },

    getJSON(response){
        return response.json()
    },

    fetchData(){
        const url = URL.rates
        fetch(url)
        .then(this.promiseStatus)
        .then(this.getJSON)
        .then(result => tablesHandler.parseData(result))
    },

    setTheme(theme){
        let themeButton = document.querySelector('.theme-button')
        let themeIcon = themeButton.querySelector('i')
        let thisTheme = theme ? theme : themeButton.id
        document.documentElement.className = thisTheme
        localStorage.setItem('theme', thisTheme)

        switch(thisTheme){
            case 'light-mode':
                themeIcon.className = 'fa fa-moon-o'
                themeButton.id = 'dark-mode'
                themeButton.title = 'Тёмная тема'
                break
            case 'dark-mode':
                themeIcon.className = 'fa fa-sun-o'
                themeButton.id = 'light-mode'
                themeButton.title = 'Светлая тема'
                break
        }
    },

    getTheme(){
        let theme = localStorage.getItem('theme')
        if (theme){
            this.setTheme(theme)
        }
    },
}


let themeButton = document.querySelector('.theme-button')
themeButton.onclick = () => utility.setTheme()

utility.getTheme()
utility.fetchData()
setInterval(() => {utility.fetchData()}, 10000)
