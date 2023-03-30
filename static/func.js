let loginbtn = document.getElementById('loginbtn');
let signupbtn=document.getElementById('signup');
let title = document.getElementsByClassName('title')
function login() {
    // Get the values of the name and password input fields
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;

    // Create an object to represent the JSON body of the POST request
    const body = { name, password };
    
    // Make the POST request using the Fetch API
    fetch('/../login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if(data["message"]=="ok"){
            window.location.href="/chats"
        }else{
            console.log(data);
        }
    })
}
function sign() {
    if (document.getElementById('password').value==document.getElementById('confirm_password').value){
    // Get the values of the name and password input fields
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    const username = document.getElementById('showname').value;
    
    // Create an object to represent the JSON body of the POST request
    const body = { name,username, password };
    
    // Make the POST request using the Fetch API
    fetch('/../signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if(data["message"]=="done"){
            window.location.href="/chats"
        }else{
            document.write("taken")
        }
    })
    }
    else {
        alert("تسرسح")
    }
}
function create(){
    const name = document.getElementById('name').value;
    const user = document.getElementById('user').value;
    
    const body = { name, user };
    fetch('/../chats/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      .then(response => response.json())
      .then(data => {
          if(data["message"]=="done"){
              console.log("done")
              document.location.reload();
            }else{
              document.getElementById("error").innerHTML="no such user";
          }
      })
}

function switch1(){
    document.getElementById('showname').style.display='block';
    document.getElementById('confirm_password').style.display='block';
    document.getElementById('login').style.height="500px";
    document.getElementById('title').innerHTML="SIGN UP";
    document.getElementById('confirm_passwordl').style.display='block';
    document.getElementById('shownamel').style.display='block';
    document.getElementById('btn1').style.display='none';
    document.getElementById('btn2').style.display='block';
}
function switch2(){
    document.getElementById('confirm_passwordl').style.display='none';
    document.getElementById('shownamel').style.display='none';
    document.getElementById('showname').style.display='none';
    document.getElementById('confirm_password').style.display='none';
    document.getElementById('login').style.height="380px";
    document.getElementById('title').innerHTML="LOGIN";
    document.getElementById('btn1').style.display='block';
    document.getElementById('btn2').style.display='none';

}
