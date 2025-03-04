const modelCount = document.getElementById('modelCount');
const modelSelectors = document.getElementById('modelSelectors');
const chatForm = document.getElementById('chatForm');
const responseContainer = document.getElementById('response-container');

function createModelSelector(index) {
    return `
        <div class="model-selector">
            <div class="model-selector-header">
                <span class="model-number">#${index + 1}</span>
            </div>
            <div class="model-selector-body">
                <select class="form-select model-select">
                    <option value="gemini">Gemini</option>
                    <option value="openai">OpenAI</option>
                    <option value="llama">Llama</option>
                    <option value="claude">Claude</option>
                </select>
            </div>
        </div>
    `;
}

function displayUserMessage(prompt) {
    const userMessage = `
        <div class="d-flex justify-content-end mb-4">
            <div class="pe-2">
                <div class="user-message p-3">
                    ${prompt}
                </div>
                <div class="text-end small text-secondary mt-1">
                    <i class="fas fa-user me-1"></i> You
                </div>
            </div>
        </div>
    `;
    
    responseContainer.innerHTML += userMessage;
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

function displayModelResponse(model, response) {
    const modelIconClass = `icon-${model.toLowerCase()}`;
    const modelInitial = model.charAt(0).toUpperCase();
    
    // Remove loading spinner
    document.querySelectorAll('.loading-spinner').forEach(spinner => {
        if (spinner.querySelector('.model-name').textContent === model) {
            spinner.remove();
        }
    });
    
    const modelResponse = `
        <div class="d-flex mb-4">
            <div class="pe-2">
                <div class="d-flex align-items-center mb-1">
                    <div class="model-icon ${modelIconClass}">${modelInitial}</div>
                    <div class="model-name text-secondary">${model}</div>
                </div>
                <div class="model-message p-3">
                    ${response}
                </div>
            </div>
        </div>
    `;

    responseContainer.innerHTML += modelResponse;
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

function displayLoadingSpinners(selectedModels) {
    const loadingSpinners = selectedModels.map(model => {
        const modelIconClass = `icon-${model.toLowerCase()}`;
        const modelInitial = model.charAt(0).toUpperCase();
        
        return `
            <div class="d-flex mb-4 loading-spinner">
                <div class="pe-2">
                    <div class="d-flex align-items-center mb-1">
                        <div class="model-icon ${modelIconClass}">${modelInitial}</div>
                        <div class="model-name text-secondary">${model}</div>
                    </div>
                    <div class="model-message p-3">
                        <div class="spinner-grow spinner-grow-sm text-info" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    responseContainer.innerHTML += loadingSpinners;
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

// Add refresh functionality
document.getElementById('refreshButton').addEventListener('click', async () => {
    try {
        // Call the reset endpoint to clear all conversation histories
        const response = await fetch('/reset_conversations', {
            method: 'POST'
        });
        
        if (response.ok) {
            // Clear the response container
            responseContainer.innerHTML = '';
            console.log('All conversation histories cleared successfully');
        } else {
            console.error('Failed to clear conversation histories');
        }
    } catch (error) {
        console.error('Error clearing conversation histories:', error);
    }
});

// Initialize with 1 model
modelCount.dispatchEvent(new Event('change'));
