root = window.App

keyFlag =
  37: false
  38: false
  39: false
  40: false

keyMap =
  37: 'left'
  38: 'up'
  39: 'right'
  40: 'down'

$ () ->
  root.sendControl = () ->
    C = 20.0 * Math.PI / 180
    thetaX = -C * keyFlag[38] + C * keyFlag[40]
    thetaY = -C * keyFlag[37] + C * keyFlag[39]
    console.log thetaX
    @ws.sendJSON
      action: 'control'
      args: [0, thetaX, thetaY, 0]
    

  document.addEventListener 'keydown', (event) ->
    k = event.keyCode
    return if keyFlag[k]
    keyFlag[k] = true
    root.sendControl()

  document.addEventListener 'keyup', (event) ->
    k = event.keyCode
    keyFlag[k] = false
    root.sendControl()
