window.App = {}
root = window.App

document.addEventListener "DOMContentLoaded", (event) ->

  root.connect()
  root.scene.start()

  $ '#start-btn'
    .click () ->
      root.ws.send JSON.stringify
          action: 'start'

  $ '#reset-btn'
    .click () ->
      root.scene.controls.reset()

  
