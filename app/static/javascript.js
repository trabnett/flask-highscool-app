
$(document).ready(function(){
    // adjustments for various mobile views
    $('#school').height($(window).height() - $('.first').height()).css({'background-repeat': 'no-repeat', 'background-attachment': 'fixed', 'background-size': 'cover'}).attr("class","")
    $('.card-backdrop').css('min-height', $(window).height())
    $('.last').css('top', $('.navbar').height())


    // scroll fade feature for homepage
    let scroll = 0
    $(window).scroll(function(){
        let id1 = ''
        let id2 = ''
        let scroll_num = 0
        if (scroll < 644){
            scroll_num = scroll
            id1 = "school"
            id2 = "class"
        } else if (scroll < 1210) {
            scroll_num = scroll - 800
            id1 = "class"
            id2 = "sportpic"
        } else if (scroll < 2011) {
            scroll_num = scroll - 1500
            id1 = "sportpic"
            id2 = "cafeteria"
        } else {
            scroll_num = scroll - 2080
            id1 = "cafeteria"
            id2 = "test"
        }
        let opacity = 1 - (scroll_num / 500)
        scroll = $(this).scrollTop()
        $(`#${id1}`).css('opacity', `${opacity}`)
        $(`#${id2}`).css('opacity', `${1 - opacity}`)
    });

    //workaround for styling wtforms quickforms buttons so that they match bootstrap buttons 
    $('#quick_form').find(':submit').addClass('bootstrap-copy')


  })

  
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

// check if password and new password match in settings modal
function match(){
    if ($('#Password2').val() === "" || $('#Password3').val() === ""){
        return $('#password-match').html('')
    }
    if ($('#Password2').val() === $('#Password3').val()){
        $('#password_update_button').prop('type', 'submit')
        $('#password-match').html('&#10004; They Match').css('color', 'green')
    } else {
        $('#password_update_button').prop('type', 'button')
        $('#password-match').html('&#10007 Please make sure your passwords match').css('color', 'red')
    }
}
