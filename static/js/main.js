const modelCount = document.getElementById('modelCount');
const modelSelectors = document.getElementById('modelSelectors');
const chatForm = document.getElementById('chatForm');
const responseContainer = document.getElementById('response-container');

function createModelSelector(index) {
    return `
        <div class="mb-3">
            <label class="form-label">Model ${index + 1}:</label>
            <select class="form-select model-select">
                <option value="gemini">Gemini</option>
                <option value="openai">OpenAI</option>
                <option value="llama">Llama</option>
                <option value="claude">Claude</option>
            </select>
        </div>
    `;
}

function displayUserMessage(prompt) {
    const userMessage = `
        <div class="d-flex align-items-baseline justify-content-end mb-4">
            <div class="pe-2">
                <div class="card d-inline-block p-2 px-3 m-1 bg-primary text-white">
                    ${prompt}
                </div>
            </div>
            <div>
                <i class="fa fa-user-circle-o"></i>
            </div>
        </div>
    `;
    
    responseContainer.innerHTML += userMessage;
    
    // Scroll to bottom
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

function displayModelResponse(model, response) {
    // Remove the loading spinner for this specific model
    document.querySelectorAll('.loading-spinner').forEach(spinner => {
        if (spinner.querySelector('.text-muted').textContent === model) {
            spinner.remove();
        }
    });
    
    const modelResponse = `
        <div class="d-flex align-items-baseline mb-4">
            <div>
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="pe-2">
                <div class="small text-muted mb-1">${model}</div>
                <div class="card d-inline-block p-2 px-3 m-1">
                    ${response}
                </div>
            </div>
        </div>
    `;

    responseContainer.innerHTML += modelResponse;
    
    // Scroll to bottom
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

function displayLoadingSpinners(selectedModels) {
    const loadingSpinners = selectedModels.map(model => `
        <div class="d-flex align-items-baseline mb-4 loading-spinner">
            <div>
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="pe-2">
                <div class="small text-muted mb-1">${model}</div>
                <div class="card d-inline-block p-2 px-3 m-1">
                    <div class="spinner-grow spinner-grow-sm text-info" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
            </div>
        </div>
    `).join('');

    responseContainer.innerHTML += loadingSpinners;
    
    // Scroll to bottom
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

modelCount.addEventListener('change', () => {
    const count = parseInt(modelCount.value);
    modelSelectors.innerHTML = '';
    for (let i = 0; i < count; i++) {
        modelSelectors.innerHTML += createModelSelector(i);
    }
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt-input').value;
    const selectedModels = Array.from(document.querySelectorAll('.model-select')).map(select => select.value);

    // Display user message immediately
    displayUserMessage(prompt);
    
    // Clear input field after displaying the message
    document.getElementById('prompt-input').value = '';
    
    // Display loading spinners for each model
    displayLoadingSpinners(selectedModels);

    // Process each model's request independently
    selectedModels.forEach(async (model) => {
        try {
            const response = await fetch(`/chat/${model}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });
            const data = await response.json();
            displayModelResponse(model, data.response);
        } catch (error) {
            displayModelResponse(model, `Error: ${error.message}`);
        }
    });
});

// Initialize with 1 model
modelCount.dispatchEvent(new Event('change'));
