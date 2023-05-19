        // get the URL of the current page
        var url = window.location.href;

        // split the URL by '/'
        var parts = url.split('/');
        
        // get the last path
        var lastPath = parts[parts.length - 1];
        console.log(lastPath);
        var socketio=io();
        socketio.on('connect', function() {
                console.log('Connected to server');
            });
          
        socketio.emit('connect_chat', {'chat_id':lastPath});
        
        socketio.on("chat_members",function(data) {
            console.log('Received data:', data);
            console.log(data.messages)
            message=JSON.parse(data.messages)
            for(let i=0;i<message.length;i++){
                let chat=document.getElementById("chat")
                let mes=document.createElement('p')
                mes.innerText=message[i].name+"      "+message[i].data+"      "+message[i].time
                chat.appendChild(mes)
            }
        })
        
        socketio.on('message',function(m){
            message=JSON.parse(m)
            let chat=document.getElementById("chat")
            let mes=document.createElement('p')
            mes.innerText=message.name+"      "+message.data+"      "+message.time
            chat.appendChild(mes)
        })
        socketio.on('disconnect', function() {
            
        });
        function sendmessage(){
            let te=document.getElementById("test")
            socketio.emit('message',{'room':lastPath,'data':te.value})
        }