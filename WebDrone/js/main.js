// Generated by CoffeeScript 1.9.3
(function() {
  document.addEventListener("DOMContentLoaded", function(event) {
    connect();
    $('#start-btn').click(function() {
      ws.send(JSON.stringify({
        action: 'start'
      }));
    });
	$('#reset-btn').click(function() {
		controls.reset();
    });
  });

}).call(this);
