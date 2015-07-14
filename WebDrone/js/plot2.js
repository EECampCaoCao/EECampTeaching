window.onload = function () {

		var dps = []; // dataPoints

		var chart = new CanvasJS.Chart("plot-wrapper",{
			title :{
				text: "Live Random Data"
			},			
			data: [{
				type: "line",
				dataPoints: dps 
			}]
		});

		var xVal = 0;
		var yVal = 100;	
		var updateInterval = 20;
		var dataLength = 500; // number of dataPoints visible at any point
    var oops = 0;

		window.updateChart = function (y) {
			// count is number of times loop runs to generate random dataPoints.
			
				dps.push({
					x: oops,
					y: y
				});
        oops ++;

			if (dps.length > dataLength)
			{
				dps.shift();				
			}
			
			chart.render();		

		};

		// generates first set of dataPoints
		//updateChart(dataLength); 

		// update chart after specified time. 
		//setInterval(function(){updateChart()}, updateInterval); 

	}
