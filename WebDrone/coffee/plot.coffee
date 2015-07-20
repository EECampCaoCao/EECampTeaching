root = window.App

$ () ->

    dps = [[], [], [], [], [], [], []]
    angleChart = new CanvasJS.Chart "plot0",
      data: [
        markerType: "none"
        type: "line"
        dataPoints: dps[0]
        legendText: "角度-x"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[1]
        legendText: "角度-y"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[2]
        legendText: "角度-z"
        showInLegend: true
      ]
      axisX:
        valueFormatString: "ss.fff"
      legend:
        fontSize: 20
        verticalAlign: "top"
        horizontalAlign: "right"

    motorChart = new CanvasJS.Chart "plot1",
      data: [
        markerType: "none"
        type: "line"
        dataPoints: dps[3]
        legendText: "馬達-1"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[4]
        legendText: "馬達-2"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[5]
        legendText: "馬達-3"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[6]
        legendText: "馬達-4"
        showInLegend: true
      ]
      axisX:
        valueFormatString: "ss.fff"
      legend:
        fontSize: 20
        verticalAlign: "top"
        horizontalAlign: "right"

    chartList = [angleChart, motorChart]
    xVal = 0
    yVal = 100
    updateInterval = 20
    dataLength = 500
    curChart = angleChart

    root.updateChart = (t, arr) ->
      cur = (new Date())
      for i in [0..6]
        dps[i].push(
          x: t
          y: arr[i]
        )
      curChart.render()

    root.changeChart = (type) ->
      type = parseInt(type)
      curChart = chartList[type]
      curChart.render()
      $('.plot-wrapper').hide()
      $('#plot' + type).show()

    root.clearChart = () ->
      for x in dps
        x.length = 0
      

