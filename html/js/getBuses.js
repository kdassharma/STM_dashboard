function fetchAllBuses() {
  request.open('PUT', url);
  request.send();
  request.onload = function(){
    alert(this.response["70"]);
  }

}
var request = new XMLHttpRequest();
url = "http://127.0.0.1:5000/bus/";

fetchAllBuses();
