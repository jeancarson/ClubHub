/**
 * Toggles the hamburger icon on the navigation bar.
 */
function toggleHamburger() {
    let x = document.getElementById("navbar");

    if (x.className === "responsive") {
        x.className = ""
    } else {
        x.className = "responsive";
    }
}

/*
 * Removes (hides) the error message on the login page.
 */
function removeLoginErrorMessage() {
    document.getElementById("input-error-msg").style.display = "none";
}

document.getElementById("username-input").addEventListener("click", removeLoginErrorMessage)
document.getElementById("password-input").addEventListener("click", removeLoginErrorMessage)
