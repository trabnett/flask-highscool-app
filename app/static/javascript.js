console.log("hhhhheeeeey")

function hello(idx){
    let moreInfo = document.getElementById(idx)
    if (moreInfo.parentNode.childNodes[3].innerText === "more info"){
        moreInfo.style = "visibility: visible;"
        moreInfo.parentNode.childNodes[3].innerText = "less info"
    } else {
        moreInfo.style = "visibility: hidden;"
        moreInfo.parentNode.childNodes[3].innerText = "more info"
    }
}
