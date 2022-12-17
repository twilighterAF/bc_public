function getTheme(){
    let theme = localStorage.getItem('theme')
    if (theme){
        document.documentElement.className = theme
    }
}

getTheme()