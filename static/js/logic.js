// logic.js

document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Get the input from the text box
    const promptInput = document.getElementById("prompt-input").value;

    // Send the input to the backend (Python script)
    fetch("http://127.0.0.1:5000/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: promptInput }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display the response in the frontend
            const responseContainer = document.getElementById("response-container");
            responseContainer.innerHTML += `
        <div class="response-container">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0 text-capitalize">Gemini</h5>
            </div>
            <div class="card-body scrollable">
              <p class="card-text whitespace-pre-wrap">${data.gemini_response}</p>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0 text-capitalize">OpenAI</h5>
            </div>
            <div class="card-body scrollable">
              <p class="card-text whitespace-pre-wrap">${data.openai_response}</p>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0 text-capitalize">Llama</h5>
            </div>
            <div class="card-body scrollable">
              <p class="card-text whitespace-pre-wrap">${data.llama_response}</p>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-header">
              <h5 class="card-title mb-0 text-capitalize">Claude</h5>
            </div>
            <div class="card-body scrollable">
              <p class="card-text whitespace-pre-wrap">${data.claude_response}</p>
            </div>
          </div>
        </div>
      `
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while submitting the prompt.");
        });
});