function fetchAllBuses() {
  fetch(url, {
    method: 'PUT'
  })
  .then(
    function(response) {
    return response.json();
    }
  ).then(
    function(data) {
    // get the buses with JSON.parse(data.incomingBuses[70][0])
    busGroupsById = data.incomingBuses;

    // get all the div blocks from inside the 'table'
    var busPlaceHolders = document.getElementById("BusPlaceHolder").getElementsByTagName("div");

    for (index in busPlaceHolders){
      if (!isNaN(parseInt(index))){
        busNum = busPlaceHolders[index].id;
        div = busPlaceHolders[index];
        // modify the div only if it's present in the update
        if (busGroupsById[busNum]){
            busGroup = busGroupsById[busNum];
            var innerDiv = "<b> Incoming: " + busNum + " </b>";
            for (innerIndex = 0; innerIndex<busGroup.length; innerIndex++){
              // modify that div group to reflect the update
              innerDiv += "<p>ETA: " + JSON.parse(busGroup[innerIndex]).ETA +" minutes</p>";
            }
            div.innerHTML = innerDiv;
          }
        else{
            div.innerHTML = "<i> No "+busNum+" buses are inbound to Ericsson!</i>";
          }

      }

     }

    }
  );
}

//data.incomingBuses[X] for the corresponding array

url = "http://127.0.0.1:5000/bus/";

setInterval(fetchAllBuses, 30000);
