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

  
