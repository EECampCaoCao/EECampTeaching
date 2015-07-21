http = require('http')
url  = require('url')
path = require('path')
fs   = require('fs')
express = require('express')
app = express()
bodyParser = require("body-parser")
pythonShell = require('python-shell')
pythonInstance = null
pythonStarted = false


app.use express.static 'WebDrone'
app.use bodyParser.urlencoded(
  extended: false
)

app.post '/', (req, res) ->
  console.log req.body
  options =
    pythonPath: 'python3'
    scriptPath: '.'
    args: ['-s', 'simple']

  if 'action' not of req.body
    res.sendStatus 404
    return

  if req.body.action == 'start'
    return if pythonStarted
    pythonStarted = true
    console.log 'Python starting'
    pythonInstance = new pythonShell 'main.py', options
    console.log 'Python started'
    pythonInstance.on 'message', (mes) ->
      console.log 'Python says: ' + mes
    pythonInstance.on 'error', (err) ->
      console.log 'Python err: ' + err
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
  #console.log req.body.code
  fs.writeFile (__dirname+'/mymath/mypid.py'), req.body.code, (err) ->
    return console.log(err) if err
    options =
      pythonPath: 'python3'
      scriptPath: '.'
      args: ['-s', 'simple']
    console.log 'Python starting'
    if pythonStarted
      pythonInstance.childProcess.kill('SIGKILL')
    pythonStarted = true
    pythonInstance = new pythonShell 'main.py', options
    console.log 'Python started'
    pythonInstance.on 'message', (mes) ->
      console.log 'Python says: ' + mes
    pythonInstance.on 'error', (err) ->
      console.log 'Python err: ' + err

  res.sendStatus 200

app.get '/mypid.py', (req, res) ->
  res.sendFile __dirname + '/mymath/mypid.py'

server = app.listen 8080, () ->
  host = server.address().address
  port = server.address().port

  console.log 'host, port = ' + host + ', ' + port



