$(document).ready(function(){

	/*
	 * jQuery UI ThemeRoller
	 *
	 * Includes code to hide GUI volume controls on mobile devices.
	 * ie., Where volume controls have no effect. See noVolume option for more info.
	 *
	 * Includes fix for Flash solution with MP4 files.
	 * ie., The timeupdates are ignored for 1000ms after changing the play-head.
	 * Alternative solution would be to use the slider option: {animate:false}
	 */

	//var recording = $('.audio_path').text()
	var recording = 'http://audio.bmat.com/audio/32/8/8/5/107885.mp3'
	recording = 'http://audio.bmat.com/audio/32/7/8/8/111788.mp3'
	recording = 'http://audio.bmat.com/audio/117/0/9/0/gbaan700004200602498112090.mp3'


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
					mp3: recording,
				});
				$(this).jPlayer("play");
			},
			timeupdate: function(event) {
				var indicator_position = event.jPlayer.status.currentTime;
				$('#info').text(indicator_position);

				// Check next line, and update, if needed
				if (indicator_position >= window.next_line.time){

					// TODO, smooth transition
					$('#current_line_text').text(window.next_line.text);

					window.next_line_idx = window.next_line_idx + 1;
					window.next_line = lines[next_line_idx];
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

	$.jPlayer.timeFormat.showHour = true;

	// A pointer to the jPlayer data object
	myPlayerData = myPlayer.data("jPlayer");

});