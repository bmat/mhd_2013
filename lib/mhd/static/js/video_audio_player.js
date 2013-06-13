jQuery(document).ready(function () {  



	$.slideshowify({
		dataUrl  : "http://www.gallerama.com/services/gallery/get.php?gid=2925&versions[]=9",
		dataType : "jsonp",
		filterFn : function(imgs){
			var fixedImgs = [];
			$.each(imgs, function(i, img){ fixedImgs.push($.extend(img.versions["9"], {id:img.id})); });
			return fixedImgs;
		},
		randomize    : true,
		fadeInSpeed  : 1500,
		fadeOutSpeed : 1500,
		aniSpeedMin  : 13000,
		aniSpeedMax  : 17000
	});


});