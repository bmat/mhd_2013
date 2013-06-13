(function() { 
  window.onload = function() { 
    var mapDiv = document.getElementById('map'); 
    var latlng = new google.maps.LatLng(41.38, 2.17);
    var options = { 
      center: latlng,
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      mapTypeControl: true,
      mapTypeControlOptions: {
	    position: google.maps.ControlPosition.TOP_LEFT,
	    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
	    mapTypeIds: [ 
	      google.maps.MapTypeId.ROADMAP, 
	      google.maps.MapTypeId.HYBRID 
	    ]
	  },
	  disableDefaultUI: true,
	  navigationControl: true,
      navigationControlOptions: { 
	    style: google.maps.NavigationControlStyle.SMALL ,
	    position: google.maps.ControlPosition.TOP_RIGHT,
	  }
    }; 
     
    var map = new google.maps.Map(mapDiv, options);
  } 
})();