window.App = {}
root = window.App
Range = ace.require('ace/range').Range

$(window)
  .on 'beforeunload', () ->
    root.ws.close()

$ (event) ->

  root.connect()
  root.connectPythonErrSocket()
  root.scene.start()

  $ '#run-btn'
    .click () ->
      root.sendCodeAndRun()

  $ '#start-btn'
    .click () ->
      root.ws.sendJSON
        action: 'start'
        args: []
      root.clearChart()

  $ '#stop-btn'
    .click () ->
      $.post '/',
        action: 'stop'
      root.ws.close()

  $ '#code-btn'
    .click () ->
      return if not root.codeLoaded
      $ '#code-wrapper'
        .show 200, () ->
          $ '#code-area textarea'
            .focus()

  $ '#reset-btn'
    .click () ->
      root.scene.controls.reset()

  for c in ['P', 'I', 'D']
    ((cc) ->
      $ '#range-'+c
        .change () ->
          $(@).prev().text($(@).val() + '%')
          root.ws.sendJSON
            action: 'tweak'
            args: [cc, parseFloat($(@).val())*0.01]
          return
        .focus () ->
          $(@).blur()
    )(c)

  $ '#switch-panel>li'
    .click () ->
      me = $(@)
      $(@).siblings().removeClass('active')
      $(@).addClass('active')
      root.changeChart me.attr('data')

  editor = ace.edit 'code-area'
  editor.setTheme "ace/theme/tomorrow_night_bright"
  editor.getSession().setMode "ace/mode/python"
  root.editor = editor

  root.sendCodeAndRun = () ->
    $.post '/runCode',
      code: root.editor.getValue()
    root.ws.open()
    $ '#code-wrapper'
      .hide()
    root.clearMarkers()

    Materialize.toast 'The program is starting!', 2000

  root.showDronePanel = () ->
    $ '#drone-control-panel'
      .show()
      .removeClass('animated bounceOut')
      .addClass('animated bounceIn')

  root.hideDronePanel = () ->
    $ '#drone-control-panel'
      .removeClass('animated bounceIn')
      .addClass('animated bounceOut')
      .one 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', () ->
        me = $ '#drone-control-panel'
        if me.hasClass('bounceOut')
          me.hide()

  root.onSocketConnected = () ->
    root.showDronePanel()

  root.onSocketClosed = () ->
    root.hideDronePanel()

  root.clearMarkers = () ->
    markers = root.editor.session.getMarkers()
    window.a = markers
    Object.keys(markers)
      .map (x) -> markers[x]
      .filter (x) -> x.clazz == 'ace-editor-error'
      .forEach (x) ->
        console.log x
        root.editor.session.removeMarker x.id

  root.onPythonError = (err, flag) ->
    err = err.replace /\n/g, '<br>'
    $ '#error-text'
      .html(err)

    if not flag
      $ '#error-text'
        .removeClass('red').addClass('green')
      return

    $ '#error-text'
      .removeClass('green').addClass('red')
    pat = /mypid.py", line (\d+)/g
    mat = pat.exec(err)
    if mat
      ln = mat[1] - 1
      root.errorLine = ln
      root.editor.session.addMarker(
        new Range(ln, 0, ln, 100),
        "ace-editor-error",
        "fullLine",
        false
      )
    $ '#code-wrapper'
      .show 200

  $.get '/mypid.py', (data) ->
    root.editor.setValue data
    root.editor.gotoLine(0, 0, true)
    root.codeLoaded = true


  $ '#return-btn'
    .click () ->
      console.log 123
      $ '#code-wrapper'
        .hide 200

  $ '#code-run-btn'
    .click () ->
      root.sendCodeAndRun()
  
