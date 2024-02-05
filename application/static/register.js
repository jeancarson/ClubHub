const checkbox = document.querySelector("#register-show-password-input");
const pw = document.querySelector("#register-password-input");
const confirm_pw = document.querySelector("#register-confirm-password-input");

checkbox.addEventListener("change", () => {
    if (pw.type === "password") {
        pw.type = "text";
        confirm_pw.type = "text";
    } else if (pw.type === "text") {
        pw.type = "password";
        confirm_pw.type = "password";
    }
});
