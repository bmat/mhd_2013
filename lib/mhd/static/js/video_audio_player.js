jQuery(document).ready(function () {  


	// Show loading gif
	
	// Get info from JSON, load all the info needed
	var query = $('#query').text()
	$.getJSON('search?q='+query, function(data) {
		window.data_videoclipr = data;

		// add images
		$.each(data.images, function(key, val) {
		    var img_src = '<img id="img_'+key+'" src="' + val + '" />';
		    $('#bg_images').append(img_src);
		});

		window.lyrics = window.data_videoclipr.lyrics;
		window.next_line_idx = 0;
		window.next_line = window.lyrics[next_line_idx];
		//alert(window.next_line);

		// create player and autostart
		var myPlayer = $("#jplayer_1"),
			myPlayerData,
			fixFlash_mp4, // Flag: The m4a and m4v Flash player gives some old currentTime values when changed.
			fixFlash_mp4_id, // Timeout ID used with fixFlash_mp4
			options = {
				ready: function (event) {
					// Determine if Flash is being used and the mp4 media type is supplied. BTW, Supplying both mp3 and mp4 is pointless.
					fixFlash_mp4 = event.jPlayer.flash.used && /m4a|m4v/.test(event.jPlayer.options.supplied);
					// Setup the player with media.
					$(this).jPlayer("setMedia", {
						mp3: window.data_videoclipr.audio,
					});
					$(this).jPlayer("play");
					// Set track, artist, isrc, label
					$('#current_line_text').text(window.data_videoclipr.artist+' - '+window.data_videoclipr.title);
					$('#current_line_text').fadeIn('slow');
				},
				timeupdate: function(event) {
					var indicator_position = event.jPlayer.status.currentTime;
					$('#info').text(indicator_position);

					// Check next line, and update, if needed
					if (indicator_position >= window.next_line[0]){

						//$('#current_line_text').fadeOut('fast');
						// TODO, smooth transition
						$('#current_line_text').text(window.next_line[1]);
						//$('#current_line_text').fadeIn('fast');

						window.next_line_idx = window.next_line_idx + 1;
						window.next_line = window.lyrics[next_line_idx];
					}

				},
				swfPath: "/static/js",
				solution:"html, flash",
				solution:"html",
				supplied: "mp3",
				cssSelectorAncestor: "#jplayer_1",
				wmode: "window",
			};
		// Instance jPlayer
		myPlayer.jPlayer(options);
		//$("#jplayer_1").jPlayer("play");
		// A pointer to the jPlayer data object
		myPlayerData = myPlayer.data("jPlayer");



		// Remove loading gif

		// Start slideshow
		$('#bg_images img').slideshowify({ 
			randomize    : false,
			fadeInSpeed  : 1500,
			fadeOutSpeed : 1500,
			aniSpeedMin  : 10000,
			aniSpeedMax  : 15000,
		});


		});

});