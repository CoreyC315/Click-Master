let clickCount = 0;
const clicker = document.getElementById("main-clicker");
const clickCounterDisplay = document.getElementById("click-counter");
const Submit = document.getElementById("submit")

clicker.addEventListener("click", () => {
    clickCount++;
    clickCounterDisplay.textContent = `Clicks: ${clickCount}`;
    console.log(clickCount);
});

