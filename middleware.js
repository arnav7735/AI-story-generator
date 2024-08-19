document.getElementById('button').addEventListener('click', () => {
    const inputText = document.getElementById('input1').value;

    fetch('/result', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_text: inputText }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the three options
        document.getElementById('output').innerHTML = `
            <p>Option 1: ${data.results1}</p>
            <p>Option 2: ${data.results2}</p>
            <p>Option 3: ${data.results3}</p>
            <label for="choice">Choose an option (0, 1, or 2): </label>
            <input type="number" id="choice" min="0" max="2"><br>
            <button id="continueButton">Continue Story</button>
        `;

        document.getElementById('continueButton').addEventListener('click', () => {
            const choice = parseInt(document.getElementById('choice').value, 10);
            if (choice >= 0 && choice <= 2) {
                fetch('/continue', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ choice: choice }),
                })
                .then(response => response.json())
                .then(data => {
                    // Display the continued story
                    document.getElementById('output').innerHTML = `
                        <p>Continued Story:</p>
                        <p>${data.final_story}</p>
                    `;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('output').innerText = `Error: ${error}`;
                });
            } else {
                alert("Please choose a valid option (0, 1, or 2).");
            }
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output').innerText = `Error: ${error}`;
    });
});
