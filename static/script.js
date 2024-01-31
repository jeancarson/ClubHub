const hamburger = document.querySelector("#hamburger");
const navbar_divs = document.querySelectorAll(".navbar-center");
const page_name = window.location.pathname;
const height = "2.75rem";
let hamburger_expanded = false;

// Give the "active" class to the link that is the current webpage.
for (let div of navbar_divs) {
    for (let anchor of div.children) {
        if (page_name === anchor.pathname) {
            if (!anchor.parentElement.classList.contains("active"))
                anchor.parentElement.classList.add("active");
        } else {
            if (anchor.parentElement.classList.contains("active"))
                anchor.parentElement.classList.remove("active");
        }
    }
}

// Toggle dropdown menu for smaller screens.
hamburger.addEventListener("click", () => {
    if (hamburger_expanded) {
        for (let div of navbar_divs) {
            div.style.height = 0;
        }
        hamburger_expanded = false;
    } else {
        for (let div of navbar_divs) {
            div.style.height = height;
        }
        hamburger_expanded = true;
    }
});
