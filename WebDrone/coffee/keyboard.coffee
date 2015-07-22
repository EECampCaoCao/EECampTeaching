root = window.App

keyFlag =
  37: false
  38: false
  39: false
  40: false
  72: false
  74: false
  75: false
  76: false

keyMap =
  37: 'left'
  38: 'up'
  39: 'right'
  40: 'down'
  72: 'h'
  74: 'j'
  75: 'k'
  76: 'l'

$ () ->
  root.sendControl = () ->
    C = 20.0 * Math.PI / 180
    D = 30.0 * Math.PI / 180
    E = 1
    thetaX = -C * keyFlag[38] + C * keyFlag[40]
    thetaY = -C * keyFlag[37] + C * keyFlag[39]
    omegaZ =  D * keyFlag[72] - D * keyFlag[76]
    vZ     = -E * keyFlag[74] + E * keyFlag[75]
    console.log thetaX
    @ws.sendJSON
      action: 'control'
      args: [vZ, thetaX, thetaY, omegaZ]
    

  document.addEventListener 'keydown', (event) ->
    k = event.keyCode
    return if k not of keyMap
    return if keyFlag[k]
    keyFlag[k] = true
    root.sendControl()

  document.addEventListener 'keyup', (event) ->
    k = event.keyCode
    return if k not of keyMap
    keyFlag[k] = false
    root.sendControl()
