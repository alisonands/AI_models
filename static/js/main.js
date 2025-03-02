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
    // User message
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

    // AI responses
    const modelResponses = selectedModels.map(model => `
        <div class="d-flex align-items-baseline mb-4">
            <div>
                <i class="fa fa-robot"></i>
            </div>
            <div class="pe-2">
                <div class="small text-muted mb-1">${model}</div>
                <div class="card d-inline-block p-2 px-3 m-1">
                    ${responses[model]}
                </div>
            </div>
        </div>
    `).join('');

    responseContainer.innerHTML += userMessage + modelResponses;
    
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
