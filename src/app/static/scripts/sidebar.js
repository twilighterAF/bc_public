import {URL} from "./main.js"


 let inputPairs = document.querySelector('.input-pairs')
 let tables = document.querySelector('.tables-content')


const eventHandler = {

    moveSidebar(sideButton){
        let sideBar = document.querySelector('.sidebar')
        let arrow = sideButton.querySelector('i')
        let buttonID = sideButton.id

        if (buttonID === 'hide-button'){
            sideBar.id = "sidebar-hide"
            sideButton.id = 'show-button'
            arrow.className = 'fa fa-chevron-right'

        }   
        else if (buttonID === 'show-button'){
            sideBar.id = "sidebar-show"
            sideButton.id = 'hide-button'
            arrow.className = 'fa fa-chevron-left'
        }
    },

    allowDrop(event){
        event.preventDefault()
    },

    dragStart(event){
        let target = event.target
        event.dataTransfer.setData('name', event.target.innerHTML)
    },

    drop(event){
        let name = event.dataTransfer.getData('name')
        event.target.value = name
    },

    addNewPair(event){
        let allInputs = document.querySelectorAll('.input-pairs [class*="input"]')
        let target = event.target
        let parent = target.parentNode.parentNode
        let newNode = parent.cloneNode(true)
    
        newNode.className = 'input' + (allInputs.length + 1)
        let inputs = newNode.querySelectorAll('input')
        inputs[0].className = 'give' + (allInputs.length + 1)
        inputs[0].value = ''
        inputs[1].className = 'take' + (allInputs.length + 1)
        inputs[1].value = ''
        inputPairs.append(newNode)
    },

    deleteThisPair(event){
        let allInputs = document.querySelectorAll('.input-pairs [class*="input"]')
        let target = event.target
        let parent = target.parentNode.parentNode

        if (allInputs.length > 1){
            parent.remove()
            let allInputs = document.querySelectorAll('.input-pairs [class*="input"]')

            for (let counter = 0; counter < allInputs.length; counter++){
                let thisNode = allInputs[counter]
                thisNode.className = 'input' + (counter + 1)
                let inputs = thisNode.querySelectorAll('input')
                inputs[0].className = 'give' + (counter + 1)
                inputs[1].className = 'take' + (counter + 1)
            }
        }
    },

    inputPairsButtons(event){
        let target = event.target

        switch(target.parentElement.className){
            case 'add-new-pair':
                eventHandler.addNewPair(event)
                break

            case 'delete-this-pair':
                eventHandler.deleteThisPair(event)
                break
        }
    },

    cityInputButtons(event){
        let target = event.target
        let input = target.parentElement.parentElement.querySelector('input')
    
        switch(target.parentElement.id){
            case 'city-show-button':
                input.id = 'city-showed'
                target.parentElement.id = 'city-hide-button'
                target.className = 'fa fa-arrow-left'
                break

            case 'city-hide-button':
                input.id = 'city-hided'
                target.parentElement.id = 'city-show-button'
                target.className = 'fa fa-arrow-right'
                break
        }
    },

    logoutUser(){
        const url = URL.logout
        window.location.href = url
    },
}


const dataHandler = {
    CURRENCIES: [],

    parseCurrencies(data){
        let container = document.querySelector('.pairs-list')
        let currList = document.querySelectorAll('[class*="currency"]')
        let currLength = currList.length
        let currCount = 1
        let currNumber = Object.keys(data).length
        this.CURRENCIES = data
    
        for (let currency in data){
            let curr = container.querySelector('.currency' + currency)

            if (currNumber > currLength){ 
                curr.innerHTML = data[currency]
                let newCurr = curr.cloneNode(true)
                newCurr.className = 'currency' + currCount++
                container.append(newCurr)
            } 
            else {
                curr.innerHTML = data[currency]
            }
        }
    },

    currStatus(response){
        if (response.status >= 200 && response.status < 300){  
            return Promise.resolve(response)
          } 
          else {  
            return Promise.reject(new Error(response.statusText))  
          }
    },

    currJSON(response){
        return response.json()
    },

    fetchCurrencies(){
        const url = URL.currencies
        fetch(url)
        .then(this.currStatus)
        .then(this.currJSON)
        .then(result => this.parseCurrencies(result))
    },

    pairsValidator(pair){
        let result = (this.CURRENCIES.indexOf(pair[0].value) != -1 &&
        this.CURRENCIES.indexOf(pair[1].value) != -1) ? true : false
        return result
    },

    parsePairs(pairsList){
        // parse before send to backend
        let result = []
        let pairs = []
        let tablesHeaders = []
        let list = pairsList.querySelectorAll('div')
        let tablesList = tables.querySelectorAll('table')

        for (let table of tablesList){
            let cityInput = table.querySelector('input').value
            let tablePair = table.querySelector('span').innerHTML
            let firstCurrency = tablePair.slice(0, tablePair.indexOf('-') - 1)
            let secondCurrency = ''
            let remainString = tablePair.slice(tablePair.indexOf('-') + 2, tablePair.length)
            let city = ''

            if (remainString.indexOf('/') != -1){
                secondCurrency = remainString.slice(0, remainString.indexOf('/') - 1)
                city = remainString.slice(remainString.indexOf('/') + 2)
            }
            else{
                secondCurrency = remainString
            }

            if (cityInput){
                city = cityInput == '-' ? '' : cityInput
            }
            tablesHeaders.push([firstCurrency, secondCurrency, city])
        }

        for (let inputPair of list){
            let inputs = inputPair.querySelectorAll('input')

            if (this.pairsValidator(inputs)){
                pairs.push([inputs[0].value, inputs[1].value])
            }
        }

        for (let pair in pairs){
            let thisHeader = tablesHeaders.shift()
            
            if (thisHeader){
                if (pairs[pair][0] == thisHeader[0] && pairs[pair][1] == thisHeader[1] && pairs[pair].length == 2){
                    pairs[pair].push(thisHeader[2])
                    thisHeader = null
                }
            }
            result.push(pairs[pair])
        }
        return result
    },
    
    sendData(){
        const url = URL.sendToServer
        let limitInput = document.querySelector('.input-limit')
        let exchangerMarkerInput = document.querySelector('.input-exchanger')
        let pairsResult = this.parsePairs(inputPairs)

        let data = {
            limit: limitInput.value,
            exchanger: exchangerMarkerInput.value,
            pairs: pairsResult
        }
        
        let send = fetch(url, 
            {
            method: 'POST',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: JSON.stringify(data)
            }
        )
    },

    buildupInputPairs(pairs){
        // buildup at the start of the page
        let counter = 0
    
        for (let pair in pairs){
            let allInputs = document.querySelectorAll('.input-pairs [class*="input"]')

            if (allInputs.length < Object.keys(pairs).length){
                let newNode = allInputs[counter].cloneNode(true)
                newNode.className = 'input' + (allInputs.length + 1)
                let inputs = newNode.querySelectorAll('input')
                inputs[0].className = 'give' + (allInputs.length + 1)
                inputs[1].className = 'take' + (allInputs.length + 1)
                inputPairs.append(newNode)
            }
            
            let thisNode = allInputs[counter]
            let fields = thisNode.querySelectorAll('input')
            fields[0].value = pairs[pair][0]
            fields[1].value = pairs[pair][1]
            counter++
        }
    },

    ParseUserSettings(settings){
        // parse settings from backend
        let cookie = document.cookie.split('=')[1]
        let user = cookie.substring(1, cookie.length - 1)
        let limitInput = document.querySelector('.input-limit')
        let exchangerMarkerInput = document.querySelector('.input-exchanger')
        let arraySettings = settings[user]

        limitInput.value = arraySettings['limit']
        exchangerMarkerInput.value = arraySettings['exchanger']

        this.buildupInputPairs(arraySettings['pairs'])
    },

    getUserSettings(){
        const url = URL.getSettings
        fetch(url)
            .then((response) => response.json())
            .then((json) => this.ParseUserSettings(json))
    },
}


const sideButton = document.querySelector('.side-button')
sideButton.onclick = () => eventHandler.moveSidebar(sideButton)

const updatePairsButton = document.querySelector('.update-pairs-list')
updatePairsButton.onclick = () => dataHandler.fetchCurrencies()

const logoutButton = document.querySelector('.logout')
logoutButton.onclick = () => eventHandler.logoutUser()

const saveButton = document.querySelector('.sidebar-save')
saveButton.onclick = () => dataHandler.sendData()

const currenciesList = document.querySelector('.pairs-list')

currenciesList.addEventListener('dragstart', eventHandler.dragStart)
inputPairs.addEventListener('dragover', eventHandler.allowDrop)
inputPairs.addEventListener('drop', eventHandler.drop)
inputPairs.addEventListener('click', eventHandler.inputPairsButtons)
tables.addEventListener('click', eventHandler.cityInputButtons)

dataHandler.getUserSettings()
dataHandler.fetchCurrencies()