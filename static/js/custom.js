
const socket = io();
socket.on("connect", function () {
  console.log("Connected to server");
});
socket.on("disconnect", function () {
  console.log("Disconnected from server");
});
socket.on('from_server', function (data) {
  console.log('Received message from server:', data);
  let element = document.getElementById(data.id);
  if (element) {
    element.innerText = data.value;
  }
});
socket.on('update-content', function (data) {
  console.log('Received update-content message from server:', data);
  let element = document.getElementById(data.id);
  if (element) {
    element.outerHTML = data.value;
  }
});
socket.on('navigate_to', function (data) {
  console.log('Received navigate message from server:', data);
  window.location = "/" + data.value;
});
function clientEmit(id, event_name) {
  console.log(id, event_name)
  socket.emit('from_client', { id: id, event_name: event_name });
}