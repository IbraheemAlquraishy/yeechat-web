let loginbtn = document.getElementsByClassName('subm');
let signupbtn = document.getElementsByClassName("change");
let username = document.getElementsByClassName('usern')[0].innerHTML;
let title = document.getElementsByClassName("title")
let pas=document.getElementById('password').innerHTML
function sign(){
    fetch("/../login",{
        body:({
            name:username,password:pas
        }),headers:({
            "Content-Type": "application/json"
        })
    })
}