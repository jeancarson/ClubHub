const checkbox = document.querySelector("#register-show-password-input");
const pw = document.querySelector("#register-password-input");
const confirm_pw = document.querySelector("#register-confirm-password-input");
const student_radio = document.querySelector("#register-student-input");
const coordinator_radio = document.querySelector("#register-coordinator-input");
const label_elements = document.querySelectorAll(".unknown-label-num");
const club_name = document.querySelector("#register-club-name-input");
const club_name_label = document.querySelector("#register-club-name-input-label");
const club_desc = document.querySelector("#register-club-description-input");
const club_desc_label = document.querySelector("#register-club-description-input-label");

const showClubNameInput = () => {
    club_name_label.style.display = "block";
    club_name.style.display = "block";
    club_name.required = true;

    club_desc_label.style.display = "block";
    club_desc.style.display = "block";
    club_desc.required = true;

    for (let label of label_elements) {
        label.innerHTML = (parseInt(label.innerHTML.substring(0, 1)) + 2) + label.innerHTML.substring(1);
    }
}

const hideClubNameInput = () => {
    club_name_label.style.display = "none";
    club_name.style.display = "none";
    club_name.required = false;
    club_name.value = "";

    club_desc_label.style.display = "none";
    club_desc.style.display = "none";
    club_desc.required = false;
    club_desc.innerHTML = "";

    for (let label of label_elements) {
        label.innerHTML = (parseInt(label.innerHTML.substring(0, 1)) - 2) + label.innerHTML.substring(1);
    }
}

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
    if (student_radio.checked) {
        coordinator_radio.checked = false;
        hideClubNameInput();
    }
});

coordinator_radio.addEventListener("change", () => {
    if (coordinator_radio.checked) {
        student_radio.checked = false;
        showClubNameInput();
    }
});
