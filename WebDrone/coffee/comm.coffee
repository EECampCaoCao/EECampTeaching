root = window.App

regex = /http[s]?:\/\/([^/:]*):/
url = regex.exec(document.URL)[1]

root.wsuri = "ws://" + url +  ":3000/ws/"
root.ws = null

root.connect = () ->
  options = 
    automaticOpen: false
    reconnectInterval: 500
    maxReconnectInterval: 5000
    reconnectDecay: 1.0

  ws = new ReconnectingWebSocket(root.wsuri, null, options)

  ws.onopen = () ->
    console.log "connected to", root.wsurl

  ws.onmessage = (evt) ->
    reader = new FileReader()
    reader.onload = (evt) ->
      data = JSON.parse evt.target.result
      root.scene.updateStatus data
    reader.readAsText evt.data

  ws.onerror = (e) ->
    console.log e

  ws.onclose = () ->
    console.log "closed"

  ws.sendJSON = (obj) ->
    @send JSON.stringify obj

  root.ws = ws




