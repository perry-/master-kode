$(document).ready(function(){
	var container = $('#target');
	
	$('.ajaxtrigger').click(function(){
		doAjax($(this).attr('href'));
		return false;
	});

	function doAjax(url){
		// if it is an external URI
		if(url.match('^http')){
			// call YQL
			$.getJSON("http://query.yahooapis.com/v1/public/yql?"+"q=select%20*%20from%20html%20where%20url%3D%22"+encodeURIComponent(url)+"%22&format=xml'&callback=?",

				// this function gets the data from the successful
				// JSON-P call
				function(data){
				// if there is data, filter it and render it out
					if(data.results[0]){
						var data = filterData(data.results[0]);
						container.html(data);
					// otherwise tell the world that something went wrong
					} else {
						var errormsg = '<p>Error: could not load the page.</p>';
						container.html(errormsg);
					}
				}
			);
		// if it is not an external URI, use Ajax load()
		} else {
			$('#target').load(url);
		}
	}

	// filter out some nasties
	function filterData(data){
		data = data.replace(/<?/body[^>]*>/g,'');
		data = data.replace(/[r|n]+/g,'');
		data = data.replace(/<--[Ss]*?-->/g,'');
		data = data.replace(/<noscript[^>]*>[Ss]*?</noscript>/g,'');
		data = data.replace(/<script[^>]*>[Ss]*?</script>/g,'');
		data = data.replace(/<script.*/>/,'');
		return data;
	}
});