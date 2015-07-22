angular.module('judge', [])
  .controller 'problemController', ($scope, $http) ->
    $http.get '/getProblems'
      .success (res) -> 
        $scope.controller.problems = res

    return
  .controller 'codeController', ($scope) ->
    @name = $scope.problem.id
    console.log @name+'-editor'
    #editor = ace.edit(@name+'-editor')
    return
  .directive 'afterRender', () ->
    return link: (scope, ele, attr) ->
      editor = ace.edit(ele[0])
      $ ele
        .height(400)
      editor.setTheme "ace/theme/tomorrow_night_bright"
      editor.getSession().setMode "ace/mode/python"
      $.get 'code/' + scope.problem.id, (data) ->
        editor.setValue data
        editor.gotoLine(0)
        editor.setOptions fontSize: '18px'
      return

