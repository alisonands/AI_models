const modelCount = document.getElementById('modelCount');
const modelSelectors = document.getElementById('modelSelectors');
const chatForm = document.getElementById('chatForm');
const messages = document.getElementById('messages');
const conversationMode = document.getElementById('conversationMode');
const promptInput = document.getElementById('promptInput');
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');

const modelOptions = [
    { value: 'gemini-2_5-pro', label: 'Gemini 2.5 Pro' },
    { value: 'openai-o3-mini', label: 'GPT o3 Mini' },
    { value: 'openai-o1', label: 'GPT o1' },
    { value: 'openai-4o', label: 'GPT-4o' },
    { value: 'openai-4o-mini', label: 'GPT-4o Mini' },
    { value: 'openai-4_5_preview', label: 'GPT-4.5 Preview' },
    { value: 'claude_3_7_sonnet', label: 'Claude 3.7 Sonnet' },
    { value: 'claude_3_opus', label: 'Claude 3 Opus' },
    { value: 'claude_3_haiku', label: 'Claude 3 Haiku' },
    { value: 'deepseek_chat', label: 'Deepseek Chat' },
    { value: 'deepseek_reasoner', label: 'Deepseek Reasoner' },
    { value: 'llama3_3', label: 'Llama 3.3' }
];

// Mobile menu toggle
menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
});

overlay.addEventListener('click', () => {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
});

function getModelClass(model) {
    if (model.includes('gemini')) return 'gemini';
    if (model.includes('openai')) return 'openai';
    if (model.includes('claude')) return 'claude';
    if (model.includes('deepseek')) return 'deepseek';
    if (model.includes('llama')) return 'llama';
    return '';
}

function createModelSelector(index) {
    const options = modelOptions.map(opt =>
        `<option value="${opt.value}">${opt.label}</option>`
    ).join('');

    return `
                <div class="model-selector">
                    <span class="model-number">Model ${index + 1}</span>
                    <select class="model-select">
                        ${options}
                    </select>
                </div>
            `;
}

function displayUserMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'message user';
    msg.innerHTML = `
                <div class="message-header">
                    <div class="avatar">U</div>
                    <div class="message-name">You</div>
                </div>
                <div class="message-content">${text}</div>
            `;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}

function displayModelResponse(model, response) {
    const existing = document.querySelector(`.loading[data-model="${model}"]`);
    if (existing) existing.remove();

    const modelClass = getModelClass(model);
    const initial = model.charAt(0).toUpperCase();
    const html = marked.parse(response.replace(/\\n/g, '\n'));

    const msg = document.createElement('div');
    msg.className = 'message';
    msg.innerHTML = `
                <div class="message-header">
                    <div class="avatar ${modelClass}">${initial}</div>
                    <div class="message-name">${model}</div>
                </div>
                <div class="message-content">${html}</div>
            `;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}

function displayLoading(model) {
    const modelClass = getModelClass(model);
    const initial = model.charAt(0).toUpperCase();

    const msg = document.createElement('div');
    msg.className = 'message loading';
    msg.setAttribute('data-model', model);
    msg.innerHTML = `
                <div class="message-header">
                    <div class="avatar ${modelClass}">${initial}</div>
                    <div class="message-name">${model}</div>
                </div>
                <div class="message-content">
                    <div class="loading">
                        <div class="loading-dot"></div>
                        <div class="loading-dot"></div>
                        <div class="loading-dot"></div>
                    </div>
                </div>
            `;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
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
    const prompt = promptInput.value.trim();
    const selectedModels = Array.from(document.querySelectorAll('.model-select')).map(s => s.value);

    // Close mobile menu if open
    sidebar.classList.remove('active');
    overlay.classList.remove('active');

    if (selectedModels.length === 0) return;

    if (prompt) displayUserMessage(prompt);
    promptInput.value = '';

    if (conversationMode.checked) {
        displayLoading(selectedModels[0]);

        try {
            const response = await fetch('/conversation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt, models: selectedModels })
            });

            const data = await response.json();

            if (data.responses) {
                for (let i = 0; i < data.responses.length; i++) {
                    const r = data.responses[i];
                    displayModelResponse(r.model, r.response);
                    if (i < data.responses.length - 1) {
                        await new Promise(resolve => setTimeout(resolve, 300));
                        displayLoading(selectedModels[i + 1]);
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        if (!prompt) return;

        selectedModels.forEach(displayLoading);

        selectedModels.forEach(async (model) => {
            try {
                const response = await fetch(`/chat/${model}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });
                const data = await response.json();
                displayModelResponse(model, data.response);
            } catch (error) {
                displayModelResponse(model, `Error: ${error.message}`);
            }
        });
    }
});

document.getElementById('refreshButton').addEventListener('click', async () => {
    try {
        await fetch('/reset_conversations', { method: 'POST' });
        messages.innerHTML = '';
    } catch (error) {
        console.error('Error:', error);
    }
});

// Initialize
modelCount.dispatchEvent(new Event('change'));