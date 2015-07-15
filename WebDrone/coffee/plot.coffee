root = window.App

$ () ->

    dps = [[], [], []]
    chart = new CanvasJS.Chart "plot-wrapper",
      data: [
        markerType: "none"
        type: "line"
        dataPoints: dps[0]
        legendText: "Angle-x"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[1]
        legendText: "Angle-y"
        showInLegend: true
      ,
        markerType: "none"
        type: "line"
        dataPoints: dps[2]
        legendText: "Angle-z"
        showInLegend: true
      ]
      axisX:
        valueFormatString: "ss.fff"

    xVal = 0
    yVal = 100
    updateInterval = 20
    dataLength = 500

    root.updateChart = (arr) ->
      cur = (new Date())
      for i in [0..2]
        dps[i].push(
          x: cur
          y: arr[i]
        )
      
      chart.render()

