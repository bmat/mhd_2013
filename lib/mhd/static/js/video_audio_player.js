jQuery(document).ready(function () {  

	window.lines = [
		{time: 14.49, text: "It's not time to make a change"},
		{time: 16.02, text: 'Just relax, take it easy'},
		{time: 19.53, text: "You're still young, that's your fault"},
		{time: 23.07, text: "There's so much you have to know"},
		{time: 26.24, text: 'Find a girl, settle down'},
		{time: 29.57, text: 'If you want, you can marry'},
		{time: 33.04, text: 'Look at me, I am old'},
		{time: 36.55, text: "But I'm happy"},
		{time: 39.71, text: "I was once like you are now"},
		{time: 43.01, text: "And I know that it's not easy"},
	];

	window.next_line_idx = 0;
	window.next_line = lines[next_line_idx];

	$('#bg_images img').slideshowify({ 
		
		randomize    : false,
		fadeInSpeed  : 1500,
		fadeOutSpeed : 1500,
		aniSpeedMin  : 10000,
		aniSpeedMax  : 15000,
	});


});