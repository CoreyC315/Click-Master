// Wait until the entire HTML document is loaded before running the script.
document.addEventListener("DOMContentLoaded", () => {
    let clickCount = 0;
    let finalClickCount = 0;
    let finalPlayerName = ""
    
    // Get elements from the DOM
    const clicker = document.getElementById("main-clicker");
    const clickCounterDisplay = document.getElementById("click-counter");
    const submit = document.getElementById("submit"); 
    const playerName = document.getElementById("playerName");

    // Attach event listener to the main clicker button
    clicker.addEventListener("click", () => {
        clickCount++;
        clickCounterDisplay.textContent = `Clicks: ${clickCount}`;
        console.log(clickCount);
    });

    // Attach event listener to the submit button
    submit.addEventListener("click", (event) => {
        // Prevent the default form submission and page reload
        event.preventDefault(); 
        
        finalPlayerName = playerName.value;
        finalClickCount = clickCount;

        // This console log should now be visible
        console.log(JSON.stringify({name: finalPlayerName, clickTotal: finalClickCount}))
        
        // sending the JSON object to the database
        fetch('API-URL-HERE', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: finalPlayerName,
                clickTotal: finalClickCount
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            // Disable the buttons after the fetch call is complete, regardless of success or failure
            clicker.disabled = true;
            submit.disabled = true;
        });
    });
});
