http = require('http')
url  = require('url')
path = require('path')
fs   = require('fs')
express = require('express')
app = express()
bodyParser = require("body-parser")
pythonShell = require('python-shell')
WebSocketServer = require('ws').Server

wss = new WebSocketServer port: 4000
wss.broadcast = (data) ->
  wss.clients.forEach (cl) ->
    cl.send data


pythonInstance = null
pythonStarted = false


app.use express.static 'WebDrone'
app.use bodyParser.urlencoded(
  extended: false
)

startPython = () ->
  if pythonStarted
    pythonInstance.childProcess.kill('SIGKILL')
  pythonStarted = true
  console.log 'Python starting'
  options =
    pythonPath: 'python3'
    scriptPath: '.'
    args: ['-s', 'simple']
  pythonInstance = new pythonShell 'main.py', options
  console.log 'Python started'
  pythonInstance.on 'message', (mes) ->
    console.log 'Python says: ' + mes
  pythonInstance.on 'error', (err) ->
    errString = "" + err
    if errString != 'Error: process exited with code null'
      wss.broadcast JSON.stringify
        action: 'error'
        data: "" + err
        isError: true
    else
      wss.broadcast JSON.stringify
        action: 'error'
        data: "Your program successfully finished."
        isError: false

app.post '/', (req, res) ->
  console.log req.body

  if 'action' not of req.body
    res.sendStatus 404
    return

  if req.body.action == 'start'
    startPython()
    res.sendStatus 200
    return

  if req.body.action == 'stop'
    console.log 'stop'
    return if not pythonStarted

    pythonInstance.childProcess.kill('SIGKILL')
    pythonStarted = false

    console.log 'python closed'
    res.sendStatus 200
    return
  res.sendStatus 404

app.post '/runCode', (req, res) ->
  fs.writeFile (__dirname+'/mymath/mypid.py'), req.body.code, (err) ->
    return console.log(err) if err
    startPython()
  res.sendStatus 200

app.get '/mypid.py', (req, res) ->
  res.sendFile __dirname + '/mymath/mypid.py'

server = app.listen 8080, () ->
  host = server.address().address
  port = server.address().port

  console.log 'host, port = ' + host + ', ' + port



