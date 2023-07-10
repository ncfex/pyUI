window.event_handlers = window.event_handlers || {};
window.elements = window.elements || {};

// Establish socket connection
const socket = io();

socket.on("connect", () => console.log("Connected to server"));
socket.on("disconnect", () => console.log("Disconnected from server"));
socket.on('ping', data => console.log("pong", "Received ping:", data));

socket.on('from-server', handleServerMessage);

function clientEmit(id, event_name) {
  console.log(id, event_name)
  socket.emit('from-client', { id: id, event_name: event_name });
}

function handleServerMessage(data) {
  console.log("Payload Received ", data);

  if (data.event_name in window.event_handlers) {
    window.event_handlers[data.event_name](data.id, data.value, data.event_name);
    return;
  } else {
    console.log("no handler for", data.event_name);
  }

  const el = document.getElementById(data.id);

  if (!el) {
    console.log(`Element with id ${data.id} not found`);
    return;
  }

  switch (data.event_name) {
    case 'init-content':
      el.innerHTML = data.value;
      break;
    case 'update-content':
      el.outerHTML = data.value;
      break;
    case 'toggle-class':
      el.classList.toggle(data.value);
      break;
    default:
      handleComplexEvents(data, el);
      break;
  }
}

function handleComplexEvents(data, el) {
  const eventNameParts = data.event_name.split("-");
  const command = eventNameParts[0];
  const property = eventNameParts[1];

  switch (command) {
    case 'change':
      if (property === 'location') {
        window.location = data.value;
      } else if (property === 'value') {
        el[property] = data.value;
      }
      break;
    case 'set':
      el.style[property] = data.value;
      break;
    default:
      console.log("Unknown command:", command);
      break;
  }
}