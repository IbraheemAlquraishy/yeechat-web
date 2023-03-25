let loginbtn = document.getElementById('loginbtn');
let signupbtn=document.getElementById('signup');
let username = document.getElementsByClassName('usern')[0].innerHTML;
let title = document.getElementsByClassName('title')
let pas=document.getElementById('password').innerHTML
function sign(){
    document.getElementById('showname').style.display='none';
    document.getElementById('confirm_password').style.display='none';
    document.getElementById("login").style.height="300px";
    document.getElementById('title').innerHTML="LOGIN";
    fetch("/../login",{
        body:({
            name:username,password:pas
        }),headers:({
            "Content-Type": "application/json"
        })
    })

}

function changer(){
    
}
function sbtn(){
    document.getElementById('showname').style.display='block';
    document.getElementById('confirm_password').style.display='block';
    document.getElementById("login").style.height="400px";
    document.getElementById('title').innerHTML="SIGN UP";

}