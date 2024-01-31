const alert_message = document.querySelector(".alert-dialog");
const alert_message_button = document.querySelector(".alert-dialog-button");

// Hides any active dialog error or message.
alert_message_button.addEventListener("click", () => {
    alert_message.style.display = "none";
})
