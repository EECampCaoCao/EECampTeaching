

wsuri = "ws://localhost:3000/ws/"
@ws = null

@connect = () ->
  try
    @ws = new WebSocket(wsuri)
    @ws.onopen = () ->
      console.log "connected to", wsuri
    
    @ws.onmessage = (evt) ->
      reader = new FileReader()
      reader.onload = (evt) ->
        data = JSON.parse evt.target.result
        updateStatus data

      reader.readAsText evt.data
    @ws.onclose = () ->
      console.log("closed");
    
  catch err 
    console.log("can't connect to", wsuri);
    console.log("error message:", err.message);
  


