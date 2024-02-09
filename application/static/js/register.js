const checkbox = document.querySelector("#register-show-password-input");
const pw = document.querySelector("#register-password-input");
const confirm_pw = document.querySelector("#register-confirm-password-input");
const student_radio = document.querySelector("#register-student-input");
const coordinator_radio = document.querySelector("#register-coordinator-input");

document.querySelector(
    "#gender-option-"
    + document.querySelector("#form-gender-value").dataset.value).selected = true;

checkbox.addEventListener("change", () => {
    if (checkbox.checked) {
        pw.type = "text";
        confirm_pw.type = "text";
    } else {
        pw.type = "password";
        confirm_pw.type = "password";
    }
});

student_radio.addEventListener("change", () => {
    if (student_radio.checked)
        coordinator_radio.checked = false;
});

coordinator_radio.addEventListener("change", () => {
    if (coordinator_radio.checked)
        student_radio.checked = false;
});
