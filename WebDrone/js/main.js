// Generated by CoffeeScript 1.9.3
(function() {
  var root;

  window.App = {};

  root = window.App;

  $(function(event) {
    var c, i, len, ref, results;
    root.connect();
    root.scene.start();
    $('#start-btn').click(function() {
      return root.ws.sendJSON({
        action: 'start',
        args: []
      });
    });
    $('#reset-btn').click(function() {
      return root.scene.controls.reset();
    });
    ref = ['P', 'I', 'D'];
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      c = ref[i];
      results.push((function(cc) {
        return $('#range-' + c).change(function() {
          console.log(cc, $(this).val());
          root.ws.sendJSON({
            action: 'tweak',
            args: [cc, parseFloat($(this).val()) * 0.01]
          });
        });
      })(c));
    }
    return results;
  });

}).call(this);
