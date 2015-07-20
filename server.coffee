http = require('http')
url  = require('url')
path = require('path')
fs   = require('fs')
express = require('express')
app = express()
bodyParser = require("body-parser")
pythonShell = require('python-shell')
pythonInstance = null
spawn = require('child_process').spawn


app.use express.static 'WebDrone'
app.use bodyParser.urlencoded(
  extended: false
)

app.post '/', (req, res) ->
  console.log req.body
  options = 
    scriptPath: '.'
    args: ['-s', 'simple']

  if 'action' not of req.body
    return

  if req.body.action == 'start'
    return if pythonInstance?
    console.log 'Python starting'
    #pythonInstance = new pythonShell 'main.py', options, (err, res) ->
      #console.log 'result = ' + res
      #return
    pythonInstance = spawn('python', ['main.py', '-s', 'simple'])
    console.log 'Python started'
    #pythonInstance.on 'message', (mes) ->
      #console.log 'Python says: ' + mes
    #pythonInstance.on 'error', (err) ->
      #console.log 'Python err: ' + err

  if req.body.action == 'stop'
    console.log 'stop'
    return if not pythonInstance?

    #pythonInstance.childProcess.kill()
    pythonInstance.kill('SIGKILL')
    pythonInstance = null

    console.log 'python closed'

server = app.listen 8080, () ->
  host = server.address().address
  port = server.address().port

  console.log 'host, port = ' + host + ', ' + port


