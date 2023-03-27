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
function login() {
    // Get the values of the name and password input fields
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    //edit on css
    document.getElementById('showname').style.display='block';
    document.getElementById('confirm_password').style.display='block';
    document.getElementById("login").style.height="400px";
    document.getElementById('title').innerHTML="SIGN UP";
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
    // Get the values of the name and password input fields
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    
    // Create an object to represent the JSON body of the POST request
    const body = { name, password };
    
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
          }else{
              console.log("no such user")
          }
      })
}

