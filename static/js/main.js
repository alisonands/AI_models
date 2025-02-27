
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

function displayResponses(prompt, responses, selectedModels) {
    const userPrompt = `
        <div class="bg-light p-4 rounded mb-4">
            <p class="fw-medium">You:</p>
            <p class="mb-0">${prompt}</p>
        </div>
    `;

    const modelResponses = selectedModels.map((model, index) => `
        <div class="col-md-${12/selectedModels.length}">
            <div class="card h-100">
                <div class="card-header">
                    <h5 class="card-title mb-0 text-capitalize">${model}</h5>
                </div>
                <div class="card-body">
                    <p class="card-text whitespace-pre-wrap">${responses[model]}</p>
                </div>
            </div>
        </div>
    `).join('');

    responseContainer.innerHTML += `
        <div class="row g-4 mb-4">
            ${userPrompt}
            ${modelResponses}
        </div>
    ` 
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
    
    const responses = {};
    for (const model of selectedModels) {
        try {
            const response = await fetch(`/chat/${model}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });
            const data = await response.json();
            responses[model] = data.response;
        } catch (error) {
            responses[model] = `Error: ${error.message}`;
        }
    }

    displayResponses(prompt, responses, selectedModels);
});

// Initialize with 1 model
modelCount.dispatchEvent(new Event('change'));
