let loginbtn = document.getElementsByClassName('subm');
let signupbtn = document.getElementsByClassName("change");
let username = document.getElementsByClassName('usern');
let title = document.getElementsByClassName("title")

signupbtn.onclick = function(){
    username.style.maxHieght = "0";
    title.innerHTML = "SIGN UP";
}