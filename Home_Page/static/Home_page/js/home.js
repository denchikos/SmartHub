/* ================================
   SCROLL REVEAL
================================ */
const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {
    revealElements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 80) {
            el.classList.add("visible");
        }
    });
}

window.addEventListener("scroll", revealOnScroll);
revealOnScroll();


/* ================================
   THEME SWITCHER
================================ */
const themeToggle = document.getElementById("themeToggle");

function applySavedTheme() {
    const saved = localStorage.getItem("theme");
    if (saved === "light") {
        document.body.classList.add("light-theme");
        themeToggle.textContent = "☀️";
    }
}
applySavedTheme();

themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");

    const isLight = document.body.classList.contains("light-theme");
    themeToggle.textContent = isLight ? "☀️" : "🌙";

    localStorage.setItem("theme", isLight ? "light" : "dark");
});
