jQuery(document).ready(function () {  


	// Show loading gif
	$('#loading_img').fadeIn();
	window.next_is_ready = false;
	window.queryng_next_query = false;
	window.song_index_next = 1;
	window.next_query = '';
	window.current_moving = false;

	// hack for demo
	window.next_query = 'Don McLean American Pie';


	window.image_next_duration = 10000;

	
	// Get info from JSON, load all the info needed
	var query = $('#query').text()
	$.getJSON('search?q='+query, function(data) {
		window.data_videoclipr = data;
		$('#loading_img').fadeOut('fast');
		$('#courtain').fadeIn('slow');

		// Check bpm, and set fade times, CHECK!
		var bpm = window.data_videoclipr.bpm;
		if (bpm > 100){
			fade_time = 300;
		}
		else{
			fade_time = 1500;
		}

		window.images_bg = data.images;
		// add images
		$.each(data.images, function(key, val) {
			//alert(data.images[key][0]+'-'+data.images[key][1])
		    var img_src = '<img id="img_'+key+'" src="' + data.images[key][1] + '" />';
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
					cover = '<img style="opacity: 1; valign: baseline; height: 120px; weight: 120px;" src="'+window.data_videoclipr.cover+'" />';
					$('#current_line_text').html(cover+window.data_videoclipr.artist+' - '+window.data_videoclipr.title);
					$('#current_line_text').fadeIn('slow');
				},
				timeupdate: function(event) {
					var indicator_position = event.jPlayer.status.currentTime;
					$('#info').text(indicator_position);

					// Check next line, and update, if needed
					if (indicator_position+1 >= window.next_line[0]){
						if (!window.current_moving){
							$('#current_line_text').fadeOut();
							window.current_moving = true
						}
					}

					if (indicator_position >= window.next_line[0]){

						//$('#current_line_text').fadeOut('fast');
						// TODO, smooth transition
						$('#current_line_text').text(window.next_line[1]);
						$('#current_line_text').fadeIn('fast');
						//$('#current_line_text').fadeIn('fast');

						window.next_line_idx = window.next_line_idx + 1;
						window.next_line = window.lyrics[next_line_idx];
						window.current_moving = false;
					}

					//query the next one, check if it has audio (duration > 30s) and lyrics
					/* TODO
					if (indicator_position > 60 && !window.queryng_next_query && !window.next_is_ready){
						if (!window.next_is_ready){
							window.queryng_next_query = true;
							$.getJSON('search?q='+query+'&next='+window.song_index_next, function(next_data) {
								// Check duration and lyrics
								duration = next_data.duration;
								next_lyrics_lines = next_data.lyrics-length;
								if( next_lyrics_lines>0 && duration > 30){
									window.next_is_ready = true
									// alert new title
									// assign window.next_query
									window.next_query = 'Michael Jackson'
								}
								else{
									window.song_index_next = window.song_index_next + 1;
								}
								// At the end
								window.queryng_next_query = false;
								// Define if next is ready
							});
						}
					}
					*/

				},
				ended: function(event) {
					window.location = '/player?q='+window.next_query
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
			fadeInSpeed  : fade_time,
			fadeOutSpeed : fade_time,
			aniSpeedMin  : 10000,
			aniSpeedMax  : 15000,
		});


		});

});