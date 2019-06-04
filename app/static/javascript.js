
function tests(num, input){
    let x = document.getElementById(num).parentNode.parentNode
    let z
    if (x.childNodes[7]){
        z = x.childNodes[7]
        x.removeChild(z)
    } else {
    let y = document.createElement('div')
    y.innerHTML = `
        <h1>Tests:</h2>
        <ul>
        </ul>
    `
    input.forEach(arr => {
        let node = document.createElement('li')
        node.innerHTML = `<li>${arr[0]}: <b>${arr[1]}%</b></li>`
        y.childNodes[3].appendChild(node)
    })
    x.appendChild(y)
    }
}

function match(e){
    let div = document.getElementById('new_password2')
    if (div.childNodes[5]){
        div.childNodes[5].remove()
    }
    console.log(div.childNodes, "<====")
    let pwd1 = document.getElementById('Password2').value
    let pwd2 = document.getElementById('Password3').value
    if (pwd1 === "" && pwd2 === ""){
        return
    }
    if (pwd1 === pwd2){
        let warning = document.createElement('div')
        warning.innerHTML = `<p style="text-align:center;color:green;">They Match</p>`
        div.appendChild(warning)
        console.log('yes sir')
    } else {
        let warning = document.createElement('div')
        warning.innerHTML = `<p style="text-align:center;color:red;">Please make sure your passwords match</p>`
        div.appendChild(warning)
        console.log('no match')
    }
}