async function sendMessage() {
    const userMessage = document.getElementById('user-input').value;

    // Clear previous recipes
    document.getElementById('chat').innerHTML = '';

    // Show loading indicator
    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('http://127.0.0.1:5000/recipes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage }),
        });

        // Hide loading indicator
        document.getElementById('loading').style.display = 'none';

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();

        // Check if data.response is an array
        if (Array.isArray(data.response)) {
            const botResponse = data.response.join('');  // Join the HTML strings
            document.getElementById('chat').innerHTML += `<div>${botResponse}</div>`;
        } else {
            // Handle the case where data.response is a string
            document.getElementById('chat').innerHTML += `<div><p>${data.response}</p></div>`;
        }
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('chat').innerHTML += `<div>Error: ${error.message}</div>`;
    }
}


document.getElementById('user-input').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        sendMessage(); // Call sendMessage when Enter is pressed
    }
});