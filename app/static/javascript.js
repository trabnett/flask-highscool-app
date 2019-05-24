console.log("hhhhheeeeey")

function hello(x){
    let moreInfo = document.getElementById(x)
    if (moreInfo.parentNode.childNodes[3].innerText === "more info"){
        moreInfo.style = "visibility: visible;"
        moreInfo.parentNode.childNodes[3].innerText = "less info"
    } else {
        moreInfo.style = "visibility: hidden;"
        moreInfo.parentNode.childNodes[3].innerText = "more info"
    }


}