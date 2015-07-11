
document.addEventListener "DOMContentLoaded", (event) -> 
  connect();
  $ '#start-btn' 
    .click () ->
      ws.send JSON.stringify
          data: 'test'

  
