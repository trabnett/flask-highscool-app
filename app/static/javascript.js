//workaround for styling wtforms quickforms buttons so that they match bootstrap buttons 
let quick_form = document.getElementById('quick_form')
if (quick_form){
    quick_form.childNodes.forEach(node => {
        if (node.type === 'submit'){
            node.classList.add('bootstrap-copy')
        }
    })
}

// scroll fade feature for homepage
let x = 0
function scroll(){
    let id1 = ''
    let id2 = ''
    let scroll_num = 0
    if (x < 644){
        scroll_num = x
        id1 = "school"
        id2 = "class"
    } else if (x < 1210) {
        scroll_num = x - 800
        id1 = "class"
        id2 = "sportpic"
    } else if (x < 2011) {
        scroll_num = x - 1550
        id1 = "sportpic"
        id2 = "cafeteria"
    } else {
        scroll_num = x - 2380
        id1 = "cafeteria"
        id2 = "test"
    }
    y = document.getElementById(id1)
    z = document.getElementById(id2)
    let opacity = 1 - (scroll_num / 500)
    if (window.scrollY > x) {
        x = window.scrollY
        y.style.opacity = opacity
        z.style.opacity = 1 - opacity
    } else {
        x = window.scrollY
        y.style.opacity = opacity
        z.style.opacity = 1 - opacity
    }
    x = window.scrollY
}

if (document.getElementById('school')){
    document.addEventListener("scroll", scroll)
}

// display test scores on student page
function tests(num, input){
    let x = document.getElementById(`row${num}`)
    let y = x.nextSibling
    if (y.id === "remove"){
        return y.remove()
    }
    let node = document.createElement('table')
    node.id = 'remove'
    node.classList.add('test_scores', 'table-striped')
    let str = '<thead><tr>Test Scores:</tr></thead>'
    input.forEach(test => {
        str += `<tr><td>${test[0]}</td><td>${test[1]}%</td></tr>`
    })
    node.innerHTML = `${str}`
    x.parentNode.insertBefore(node, x.nextSibling)
}

// check if password and new password match in password modal
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
