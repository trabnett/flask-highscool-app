function expand(idx){
    event.preventDefault()
    let button = document.getElementById(idx)
    if (button.parentNode.innerText === "more info"){
        button.parentNode.parentNode.childNodes[5].style = "visibility: visible"
        button.parentNode.innerHTML = `<button id=${idx} class="btn btn-primary" onclick="expand(${idx})">less info</button>`

    } else {
        button.parentNode.parentNode.childNodes[5].style = "visibility: hidden"
        button.parentNode.innerHTML = `<button id=${idx} class="btn btn-primary" onclick="expand(${idx})">more info</button>`
    }
    
}

