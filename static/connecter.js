        // get the URL of the current page
        var url = window.location.href;

        // split the URL by '/'
        var parts = url.split('/');
        
        // get the last path
        var lastPath = parts[parts.length - 1];
        
        // log the last path
                console.log(lastPath);
                var socketio=io();
                socketio.on('connect', function() {
                console.log('Connected to server');
          
          // Send data to the server
                socketio.emit('connect_chat', {'chat_id':lastPath});
        
                socketio.on("chat_members",function(data) {
                        console.log('Received data:', data);})
        
          
        
        });
        ocketio.on('disconnect', function() {
            // Create a JSON object
            var data = {"chat_id": lastPath};
            
            // Send the JSON object to the server
            socketio.emit('client_message', data);
        });
        function sendmessage(){
            let te=document.getElementById("test")
            socketio.emit('message',{'data':te.value})
        }