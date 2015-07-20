window.App = {}
root = window.App

$(window)
  .on 'beforeunload', () ->
    root.ws.close()

$ (event) ->

  root.connect()
  root.scene.start()

  $ '#ss-btn'
    .click () ->
      console.log 456
      $.post '/', {action: 'start'}
      root.ws.open()

  $ '#start-btn'
    .click () ->
      root.ws.sendJSON
        action: 'start'
        args: []
      root.clearChart()

  $ '#stop-btn'
    .click () ->
      console.log 123
      $.post '/',
        action: 'stop'
      root.ws.close()

  $ '#code-btn'
    .click () ->
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

  $.get '/mypid.py', (data) ->
    console.log data
    root.editor.setValue data


  $ '#return-btn'
    .click () ->
      console.log 123
      $ '#code-wrapper'
        .hide 200

  $ '#run-btn'
    .click () ->
      $.post '/runCode',
        code: root.editor.getValue()
      root.ws.open()
  
