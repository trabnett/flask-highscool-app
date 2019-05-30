
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