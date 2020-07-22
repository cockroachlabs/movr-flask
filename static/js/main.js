jQuery(document).ready(function($){
    $('form #submit').removeClass('btn-default').addClass('btn-primary');

    $('.formatTime').each(function(key, e){
        $(e).text(
            new Date($(e).text())
            .toLocaleDateString("en-US")
        );
    })

    $('.formatDuration').each(function(key, e){
        var duration = $(e).text().split(":");
        $(e).text(`${
            //hours
            duration[0] > 0 ? duration[0]+":" : ""
        }${
            //minutes
            duration[1]
        }:${
            //seconds without mili
            duration[2].split(".")[0]
        }`);
    })

    $('.avatar').each(function(key, e){
        $(e).text(
             $(e).text().charAt(0)
        );
    })
})


function initMap() {
    $('.map').each(function(key, e){
        const addr = $(e).text().split('|')[0];
        const apikey = $(e).text().split('|')[1];
        const type = $(e).text().split('|')[2];
        const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${addr}&key=${apikey}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const pos = data.results[0].geometry.location
                let map = new google.maps.Map(e, {
                    center: {...pos},
                    fullscreenControl: false,
                    styles: [
                        {
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#212121"
                            }
                          ]
                        },
                        {
                          "elementType": "labels.icon",
                          "stylers": [
                            {
                              "visibility": "off"
                            }
                          ]
                        },
                        {
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#757575"
                            }
                          ]
                        },
                        {
                          "elementType": "labels.text.stroke",
                          "stylers": [
                            {
                              "color": "#212121"
                            }
                          ]
                        },
                        {
                          "featureType": "administrative",
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#757575"
                            }
                          ]
                        },
                        {
                          "featureType": "administrative.country",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#9e9e9e"
                            }
                          ]
                        },
                        {
                          "featureType": "administrative.land_parcel",
                          "stylers": [
                            {
                              "visibility": "off"
                            }
                          ]
                        },
                        {
                          "featureType": "administrative.locality",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#bdbdbd"
                            }
                          ]
                        },
                        {
                          "featureType": "poi",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#757575"
                            }
                          ]
                        },
                        {
                          "featureType": "poi.park",
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#181818"
                            }
                          ]
                        },
                        {
                          "featureType": "poi.park",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#616161"
                            }
                          ]
                        },
                        {
                          "featureType": "poi.park",
                          "elementType": "labels.text.stroke",
                          "stylers": [
                            {
                              "color": "#1b1b1b"
                            }
                          ]
                        },
                        {
                          "featureType": "road",
                          "elementType": "geometry.fill",
                          "stylers": [
                            {
                              "color": "#2c2c2c"
                            }
                          ]
                        },
                        {
                          "featureType": "road",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#8a8a8a"
                            }
                          ]
                        },
                        {
                          "featureType": "road.arterial",
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#373737"
                            }
                          ]
                        },
                        {
                          "featureType": "road.highway",
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#3c3c3c"
                            }
                          ]
                        },
                        {
                          "featureType": "road.highway.controlled_access",
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#4e4e4e"
                            }
                          ]
                        },
                        {
                          "featureType": "road.local",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#616161"
                            }
                          ]
                        },
                        {
                          "featureType": "transit",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#757575"
                            }
                          ]
                        },
                        {
                          "featureType": "water",
                          "elementType": "geometry",
                          "stylers": [
                            {
                              "color": "#000000"
                            }
                          ]
                        },
                        {
                          "featureType": "water",
                          "elementType": "labels.text.fill",
                          "stylers": [
                            {
                              "color": "#3d3d3d"
                            }
                          ]
                        }
                      ],
                    zoom: 16
                });

                new google.maps.Marker({
                    position: new google.maps.LatLng(...Object.values(pos)),
                    icon: {
                        url: `/static/img/pin/${type}.png`,
                        scaledSize: new google.maps.Size(100, 100),
                        anchor: new google.maps.Point(50, 50),
                    },
                    map: map
                  });
            });
    })
}