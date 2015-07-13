document.addEventListener('keydown', function(event) {
		if(event.keyCode == 37) {
			console.log('left');
		}
		else if(event.keyCode == 39) {
			console.log('right');
		}
		else if(event.keyCode == 38) {
			console.log('up');
		}
		else if(event.keyCode == 40) { 	
			console.log('down');
		}                              	
});

document.addEventListener('keyup', function(event) {
		if(event.keyCode == 37) {
			console.log('left is up');           
		}
		else if(event.keyCode == 39) {         
			console.log('right is up');
		}
		else if(event.keyCode == 38) { 	
			console.log('up is up');
		}
		else if(event.keyCode == 40) { 
			console.log('down is up');
		}                              	
});
