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
    //console.log(busGroupsById);

    // get all the div blocks from inside the 'table'
    var busPlaceHolders = document.getElementById("BusPlaceHolder").getElementsByTagName("div");

//    console.log(busPlaceHolders);
//    console.log(busGroupsById);

    // how to iterate over the divs
    for (index in busPlaceHolders){
      if (!isNaN(parseInt(index))){
        busNum = busPlaceHolders[index].id;
        div = busPlaceHolders[index];
        // modify the div only if it's present in the update
        if (busGroupsById[busNum]){
            //console.log(busGroupsById[busNum]);
            busGroup = busGroupsById[busNum];
            console.log("BUSGROUP")
            console.log(busGroup)
            var innerDiv = "<b> Incoming: " + busNum + " </b>";
            for (innerIndex = 0; innerIndex<busGroup.length; innerIndex++){
            //for (innerIndex of busGroup.entries()){
              // modify that div group to reflect the update
              console.log("innerIndex");
              console.log(innerIndex);
              console.log(busGroup[innerIndex]);
              innerDiv += "<p>ETA: " + JSON.parse(busGroup[innerIndex]).ETA +" minutes</p>";
            }
            div.innerHTML = innerDiv;
          }
        else{
            //console.log(busNum + " is not present!");
            div.innerHTML = "<p> No "+busNum+" buses are inbound to Ericsson!</p>";
          }

      }

     }

    }
  );
}

//data.incomingBuses[X] for the corresponding array

url = "http://127.0.0.1:5000/bus/";

setInterval(fetchAllBuses, 10000);
//fetchAllBuses();



// SyntaxError: await is only valid in async functions and async generators

//// Fetch from Rest API
//  const response = await fetch(url, {
//    headers: {
//      'Accept': 'application/json',
//      'Content-Type': 'application/json'
//    },
//    method: PUT,
//    body: jsonBody
//  });
//  // Wait the response and parse it as json, you can use the json as an object
//  const json = await response.json() as T;
//
//
