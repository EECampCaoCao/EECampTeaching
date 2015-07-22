http = require('http')
url  = require('url')
path = require('path')
fs   = require('fs')
express = require('express')
bodyParser = require("body-parser")
pythonShell = require('python-shell')

app = express()
app.use express.static 'judge'

app.get '/getProblems', (req, res) ->
  #res.send('123')
  fs.readFile __dirname+'/exercise/prob.json'
  , (err, data) ->
    console.log data.toString()
    if err
      console.log err

    res.send JSON.parse(data)

app.get '/code/:name', (req, res) ->
  console.log req.params
  res.sendFile __dirname + '/exercise/' + req.params.name + '/' +
    req.params.name + '.py'


server = app.listen 8000, () ->
  host = server.address().address
  port = server.address().port

  console.log 'host, port = ' + host + ', ' + port

