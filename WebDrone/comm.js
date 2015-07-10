'use strict';
var wsuri = "ws://localhost:3000/ws/";
var ws = null;

var connect = function() {
  try {
    ws = new WebSocket(wsuri);
    ws.onopen = function(){
      console.log("connected to", wsuri);
    }
    ws.onmessage = function(evt){
      var reader = new FileReader();
      reader.onload = function(evt) {
        var data = JSON.parse(evt.target.result);
        updateStatus(data);
      }
      reader.readAsText(evt.data);
    }
    ws.onclose = function(){
      console.log("closed");
    }
  }
  catch (err) {
    console.log("can't connect to", wsuri);
    console.log("error message:", err.message);
  }
}


