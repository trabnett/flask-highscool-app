
function tests(num, input){
    let x = document.getElementById(`row${num}`)
    let y = x.nextSibling
    if (y.id === "remove"){
        return y.remove()
    }
    let node = document.createElement('table')
    node.id = 'remove'
    node.classList.add('table')
    let str = '<thead><tr>Test Scores</tr></thead>'
    input.forEach(test => {
        str += `<tr><td>${test[0]}</td><td>${test[1]}</td></tr>`
    })
    node.innerHTML = `${str}`
    x.parentNode.insertBefore(node, x.nextSibling)
    // let z
    // if (x.childNodes[7]){
    //     z = x.childNodes[7]
    //     x.removeChild(z)
    // } else {
    // let y = document.createElement('div')
    // y.innerHTML = `
    //     <h2>Tests:</h2>
    //     <ul>
    //     </ul>
    // `
    // input.forEach(arr => {
    //     let node = document.createElement('li')
    //     node.innerHTML = `<li>${arr[0]}: <b>${arr[1]}%</b></li>`
    //     y.childNodes[3].appendChild(node)
    // })
    // x.appendChild(y)
    // }
}

function match(){
    let div = document.getElementById('new_password2')
    if (div.childNodes[5]){
        div.childNodes[5].remove()
    }
    let pwd1 = document.getElementById('Password2').value
    let pwd2 = document.getElementById('Password3').value
    if (pwd1 === "" || pwd2 === ""){
        return
    }
    if (pwd1 === pwd2){
        let button = document.getElementById('password_update_button')
        button.type = "submit"
        let warning = document.createElement('div')
        warning.innerHTML = `<p style="text-align:center;color:green;">&#10004; They Match</p>`
        div.appendChild(warning)
    } else {
        let button = document.getElementById('password_update_button')
        button.type = 'button'
        let warning = document.createElement('div')
        warning.innerHTML = `<p class="warning">&#10007 Please make sure your passwords match</p>`
        div.appendChild(warning)
    }
}
