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
    console.log(JSON.parse(data.incomingBuses[70][0]));
    }
  );
}

//data.incomingBuses[X] for the corresponding array

url = "http://127.0.0.1:5000/bus/";

fetchAllBuses();


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
