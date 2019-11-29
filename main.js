$( window ).load(function() {

      mapboxgl.accessToken = 'pk.eyJ1IjoicnV0ZHJ1cCIsImEiOiJjazNnMGR0emIwYW8wM2tvZnc1aTR3NnJqIn0.ztUVnRKy3Rbpdyr8Xt1CWA';
        var map = new mapboxgl.Map({
            container: 'map',
            center: [-73.7279975, 45.4913029],
            zoom: 13,
            style: 'mapbox://styles/mapbox/streets-v11'
        });

    // https://docs.mapbox.com/help/tutorials/custom-markers-gl-js/
    // Can use this approach to add dynamic markers/buses to the map
    var geojson = {
        type: 'FeatureCollection',
        features: [{
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [-73.728, 45.491]
        },
        properties: {
            title: 'Mapbox',
            description: 'Ericsson Office.'
        }}]
    };

    // add the office marker to map
    geojson.features.forEach(function(marker) {
        // create a HTML element for each feature
        var el = document.createElement('div');
        el.className = 'office-marker';

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
        .setLngLat(marker.geometry.coordinates)
        .addTo(map);
    });

    setInterval(function(){ alert("Hello"); }, 3000); //we can define the function and the time in ms

});

