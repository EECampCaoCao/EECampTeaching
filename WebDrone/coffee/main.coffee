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

  
