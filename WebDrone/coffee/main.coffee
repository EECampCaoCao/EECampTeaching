window.App = {}
root = window.App

$ (event) ->

  root.connect()
  root.scene.start()

  $ '#start-btn'
    .click () ->
      root.ws.sendJSON
        action: 'start'
        args: []

  $ '#reset-btn'
    .click () ->
      root.scene.controls.reset()

  
