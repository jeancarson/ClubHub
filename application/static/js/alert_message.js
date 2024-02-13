const alert_message = document.querySelector(".alert-dialog");
const alert_message_button = document.querySelector(".alert-dialog-button");

alert_message_button.addEventListener("click", () => alert_message.style.display = "none");

document.body.addEventListener('click', function( event ){
    if (" block".includes(alert_message.style.display) && !alert_message.contains(event.target))
		alert_message.style.display = "none";
});
