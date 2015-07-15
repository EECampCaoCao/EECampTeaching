root = window.App

root.wsuri = "ws://localhost:3000/ws/"
root.ws = null

root.connect = () ->
  try
    ws = new WebSocket(root.wsuri)
  catch err
    console.log("can't connect to", root.wsuri)
    console.log("error message:", err.message)

  ws.onopen = () ->
    console.log "connected to", root.wsurl

  ws.onmessage = (evt) ->
    reader = new FileReader()
    reader.onload = (evt) ->
      data = JSON.parse evt.target.result
      root.scene.updateStatus data
    reader.readAsText evt.data

  ws.onclose = () ->
    console.log "closed"

  ws.sendJSON = (obj) ->
    @send JSON.stringify obj

  root.ws = ws




