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
    console.log "connected to", root.wsuri
    root.onSocketConnected()

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
    root.onSocketClosed()

  ws.sendJSON = (obj) ->
    @send JSON.stringify obj

  root.ws = ws

root.connectPythonErrSocket = () ->
  ws2 = new WebSocket('ws://localhost:4000/ws/')

  ws2.onopen = () ->
    console.log "connected to 4000"

  ws2.onmessage = (evt) ->
    data = evt.data
    data = JSON.parse(data)
    errMesg = data.data
    root.onPythonError errMesg, data.isError

  ws2.onerror = (e) ->
    console.log e

  ws2.onclose = () ->
    console.log "closed"


