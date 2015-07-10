$(function () {
  $(document).ready(function () {
    Highcharts.setOptions({
      global: {
        useUTC: false
      }
    });

    $('#container').highcharts('StockChart', {
      chart: {
        //type: 'spline',
        //animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
          load: function () {

            // set up the updating of the chart each second
            window.series = this.series[0];
          }
        }
      },
      xAxis: {
        type: 'datetime',
        tickPixelInterval: 150,
        minRange: 10000
      },
      yAxis: {
        //min: -0.5,
        //max: 0.5,
        title: {
          text: 'Value'
        },
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      },
      tooltip: {
        formatter: function () {
          return '<b>' + this.series.name + '</b><br/>' +
            Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
            Highcharts.numberFormat(this.y, 2);
        }
      },
      legend: {
        enabled: false
      },
      exporting: {
        enabled: false
      },
      series: [{
        name: 'Random data',
        data: (function () {
          // generate an array of random data
          var data = [];
          //time = (new Date()).getTime();
          return data;
        }()),
      }]
    });
  });
});
