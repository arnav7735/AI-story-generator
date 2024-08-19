// const { exec } = require('child_process');
// const express = require('express');
// const bodyParser = require('body-parser');
// const path = require('path');
// const fs = require('fs');

// const app = express();
// app.use(bodyParser.json());

// // Serve the HTML file
// app.use(express.static(path.join(__dirname, 'public')));

// app.post('/generate', (req, res) => {
//     const inputText = req.body.input_text;
//     const iteration = req.body.iteration;

//     // Construct the command to run the Python script with input
//     const command = `python story_telling.py`;

//     // Create a temporary input file for Python script
//     const inputFilePath = path.join(__dirname, 'temp_input.json');
//     fs.writeFileSync(inputFilePath, JSON.stringify({ input_text: inputText, iteration: iteration }));

//     exec(command, { input: JSON.stringify({ input_text: inputText, iteration: iteration }) }, (error, stdout, stderr) => {
//         // Clean up temporary input file
//         fs.unlinkSync(inputFilePath);

//         if (error) {
//             console.error(`exec error: ${error}`);
//             return res.status(500).json({ error: stderr || 'Internal Server Error' });
//         }
//         try {
//             const output = JSON.parse(stdout);
//             res.json(output);
//         } catch (parseError) {
//             console.error('Failed to parse Python output:', parseError);
//             res.status(500).json({ error: 'Failed to parse Python output.' });
//         }
//     });
// });

// app.listen(3000, () => {
//     console.log('Server running on http://localhost:3000');
// });

///////////////////////////////

const express = require('express');
const { exec } = require('child_process');
const app = express();
const path = require('path');

app.use(express.json()); // Parse JSON data from the request body

// Endpoint to handle the story generation request
app.use(express.static(path.join(__dirname, 'public')));
app.post('/generate', (req, res) => {
    const { input_text, iteration } = req.body;

    // Prepare the input data for the Python script
    const inputData = JSON.stringify({ input_text: input_text, iteration: iteration });

    // Execute the Python script with input data
    const process = exec('python story_telling.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        try {
            // Parse and return the output from the Python script
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (err) {
            console.error(`Failed to parse output: ${stdout}`);
            res.status(500).json({ error: `Failed to parse output: ${stdout}` });
        }
    });

    // Write the input data to the Python script's stdin
    process.stdin.write(inputData);
    process.stdin.end();
});

// Serve the static HTML file from the current directory
app.use(express.static('.'));

// Start the server
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});

