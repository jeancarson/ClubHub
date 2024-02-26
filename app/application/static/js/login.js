const checkbox = document.querySelector("#login-show-password-input");
const pw = document.querySelector("#login-password-input");

checkbox.addEventListener("change", () => {
    if (checkbox.checked) {
        pw.type = "text";
    } else {
        pw.type = "password";
    }
});
