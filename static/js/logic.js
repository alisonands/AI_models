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
        <div class="mb-4">
          <div class="bg-light p-4 rounded">
            <p class="fw-medium">You:</p>
            <p class="mb-0">${data.prompt}</p>
          </div>

          <div class="row mt-4 g-4">
            <div class="col-md-4">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-0 text-capitalize">Gemini</h5>
                </div>
                <div class="card-body">
                  <p class="card-text whitespace-pre-wrap">${data.gemini_response}</p>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="card-title mb-0 text-capitalize">OpenAI</h5>
                </div>
                <div class="card-body">
                  <p class="card-text whitespace-pre-wrap">${data.openai_response}</p>
                </div>
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