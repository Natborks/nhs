

        // Create a function that will cause the bar to load at a speed of 50 ms
        function load_bar(fill){

           // Call the "load()" function every 50 ms
           window.setInterval(function(){
            // Add 10% for each iteration of the function (should be 10 iterations in total)
            fill += 10;

            // If the percentage of the progress bar that is loaded === 100, stop the iteration
            if(fill === 5000){
                clearInterval();
            }
            // Continue the iteration as long as the value of fill < 100
            else{
                document.getElementById("progress_one").style.width = fill + "%";
            }

           }, 50);
	}

document.addEventListener('DOMContentLoaded', () => {
		//alert("loaded");
	 // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	socket.on('connect', () => {
		while(true) {
			socket.emit('submit', {'selection': "yes"});
		}
		 //document.getElementById('button').onclick = () => {
				//socket.emit('submit', {'selection': "yes"});
				//alert("clicked");
		//}
       
    });

    socket.on('announce', data => {
	fill = data.selection;
	load_bar(fill);
    });

		
});
