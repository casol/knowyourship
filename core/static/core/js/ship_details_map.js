function initMap() {
    var ship = {lat: latitude, lng: longitude};
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: ship
    });
    var marker = new google.maps.Marker({
      position: ship,
      map: map
    });

    var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 id="firstHeading" class="firstHeading">'+ ship_name +'</h1>'+
      '<div id="bodyContent">'+
      '<p>Looking for direction? Opening hours or more details?</p>'+
      '<a href="https://www.google.com/maps/search/?api=1&query=' + search + '">Open in Google Maps</a></p>'+
      '</div>'+
      '</div>';

    var infowindow = new google.maps.InfoWindow({
      content: contentString
    });

    var marker = new google.maps.Marker({
      position: ship,
      map: map,
      title: ship_name + ' ' + '(' + country + ')'
    });
      marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
}