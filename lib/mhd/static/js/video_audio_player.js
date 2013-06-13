jQuery(document).ready(function () {  



	$('#bg_images img').slideshowify({ 
		
		randomize    : true,
		fadeInSpeed  : 1000,
		fadeOutSpeed : 1000,
		aniSpeedMin  : 2000,
		aniSpeedMax  : 7000,

		
		faterFadeIn : function(curImage){
        	// do something else
        	//alert(curImage);
    	},
	});


});