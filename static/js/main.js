const modelCount = document.getElementById('modelCount');
const modelSelectors = document.getElementById('modelSelectors');
const chatForm = document.getElementById('chatForm');
const responseContainer = document.getElementById('response-container');
const conversationModeSwitch = document.getElementById('conversationMode');

// function to add more models 
function createModelSelector(index) {
    return `
        <div class="model-selector">
            <div class="model-selector-header">
                <span class="model-number">#${index + 1}</span>
            </div>
            <div class="model-selector-body">
                <select class="form-select model-select">
                    <option value="gemini-2_0-flash">Gemini 2.0 Flash</option>
                    <option value="openai-o3-mini">OpenAI gpt o3 mini</option>
                    <option value="openai-o1">OpenAI gpt o1</option>
                    <option value="openai-4o">OpenAI gpt 4o</option>
                    <option value="openai-4o-mini">OpenAI gpt 4o mini</option>
                    <option value="openai-4_5_preview">OpenAI gpt 4.5 preview</option>
                    <option value="claude_3_7_sonnet">Claude 3.7 sonnet</option>
                    <option value="claude_3_opus">Claude 3 opus</option>
                    <option value="claude_3_haiku">Claude 3 haiku</option>
                    <option value="deepseek_chat">Deepseek Chat</option>
                    <option value="deepseek_reasoner">Deepseek Reasoner</option>
                    <option value="llama3_3">Llama 3.3</option>
                </select>
            </div>
        </div>
    `;
}

// function to enter user message 
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

// function to show model response
function displayModelResponse(model, response) {
    const modelIconClass = `icon-${model.toLowerCase()}`;
    const modelInitial = model.charAt(0).toUpperCase();
    
    // Remove loading spinner
    document.querySelectorAll('.loading-spinner').forEach(spinner => {
        if (spinner.querySelector('.model-name').textContent === model) {
            spinner.remove();
        }
    });

    // First, sanitize the response by replacing any escaped characters
    const sanitizedResponse = response
        .replace(/\\n/g, '\n')  // Replace \n with newlines
        .replace(/\\'/g, "'")   // Replace escaped single quotes
        .replace(/\\"/g, '"');  // Replace escaped double quotes
    
    const htmlResponse = marked.parse(sanitizedResponse);
    
    const modelResponse = `
        <div class="d-flex mb-4">
            <div class="pe-2">
                <div class="d-flex align-items-center mb-1">
                    <div class="model-icon ${modelIconClass}">${modelInitial}</div>
                    <div class="model-name text-secondary">${model}</div>
                </div>
                <div class="model-message p-3">
                    ${htmlResponse}
                </div>
            </div>
        </div>
    `;

    responseContainer.innerHTML += modelResponse;
    responseContainer.scrollTop = responseContainer.scrollHeight;
}

// loading function 
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

// call createModelSelector function when model count changes
modelCount.addEventListener('change', () => {
    const count = parseInt(modelCount.value);
    modelSelectors.innerHTML = '';
    for (let i = 0; i < count; i++) {
        modelSelectors.innerHTML += createModelSelector(i);
    }
});

// function to submit user message; also checks conversation mode
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt-input').value;
    
    // Determine if we're in mobile view
    const isMobile = window.innerWidth < 768;
    
    // Get selected models based on view
    let selectedModels;
    if (isMobile) {
        selectedModels = Array.from(document.querySelectorAll('#mobileModelSelectors .model-select')).map(select => select.value);
    } else {
        selectedModels = Array.from(document.querySelectorAll('#modelSelectors .model-select')).map(select => select.value);
    }
    
    const isConversationMode = conversationModeSwitch && conversationModeSwitch.checked;

    // Check if we have selected models
    if (selectedModels.length === 0) {
        responseContainer.innerHTML += `
            <div class="d-flex mb-4">
                <div class="pe-2">
                    <div class="model-message p-3 text-warning">
                        <p>Please select at least one model to continue.</p>
                    </div>
                </div>
            </div>
        `;
        return;
    }

    // Only display user message if it's not blank
    if (prompt.trim() !== '') {
        displayUserMessage(prompt);
    } else if (isConversationMode) {
        // For blank prompts in conversation mode, add a subtle indicator
        responseContainer.innerHTML += `
            <div class="d-flex justify-content-center mb-2">
                <div class="small text-secondary">
                    <i class="fas fa-sync-alt me-1"></i> Continuing model conversation...
                </div>
            </div>
        `;
    }
    
    // Clear input field after displaying the message
    document.getElementById('prompt-input').value = '';
    
    if (isConversationMode) {
        // Conversation mode - models talk to each other
        try {
            // Display loading spinner for the first model
            if (selectedModels.length > 0) {
                displayLoadingSpinners([selectedModels[0]]);
            }
            
            // Log what we're sending to help debug
            console.log("Sending to /conversation:", { 
                prompt: prompt, 
                models: selectedModels 
            });
            
            // Start the conversation with all selected models
            const response = await fetch('/conversation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    prompt: prompt, // This can be blank
                    models: selectedModels
                })
            });
            
            // Log the raw response for debugging
            const rawResponse = await response.text();
            console.log("Raw response:", rawResponse);
            
            // Parse the JSON response
            let data;
            try {
                data = JSON.parse(rawResponse);
            } catch (parseError) {
                console.error("Error parsing response:", parseError);
                throw new Error("Invalid response from server");
            }
            
            // Check if we have a valid responses array
            if (data && data.responses && Array.isArray(data.responses)) {
                // Display each model's response in sequence
                for (let i = 0; i < data.responses.length; i++) {
                    const modelResponse = data.responses[i];
                    displayModelResponse(modelResponse.model, modelResponse.response);
                    
                    // If not the last model, show loading spinner for the next model
                    if (i < data.responses.length - 1) {
                        await new Promise(resolve => setTimeout(resolve, 500)); // Small delay for better UX
                        displayLoadingSpinners([selectedModels[i + 1]]);
                    }
                }
            } else {
                // Handle case where responses array is missing or invalid
                console.error('Invalid response format:', data);
                responseContainer.innerHTML += `
                    <div class="d-flex mb-4">
                        <div class="pe-2">
                            <div class="model-message p-3 text-danger">
                                <p>Error: Invalid response format from server</p>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            // If there was an error message in the response, display it
            if (data && data.error) {
                console.error('Server reported error:', data.error);
                responseContainer.innerHTML += `
                    <div class="d-flex mb-4">
                        <div class="pe-2">
                            <div class="model-message p-3 text-danger">
                                <p>Error: ${data.error}</p>
                            </div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error in conversation mode:', error);
            responseContainer.innerHTML += `
                <div class="d-flex mb-4">
                    <div class="pe-2">
                        <div class="model-message p-3 text-danger">
                            <p>Error in conversation mode: ${error.message}</p>
                        </div>
                    </div>
                </div>
            `;
        }
    } else {
        // Original mode - process each model independently
        // Only proceed if the prompt is not blank
        if (prompt.trim() === '') {
            responseContainer.innerHTML += `
                <div class="d-flex mb-4">
                    <div class="pe-2">
                        <div class="model-message p-3 text-warning">
                            <p>Please enter a prompt to continue.</p>
                        </div>
                    </div>
                </div>
            `;
            return;
        }
        
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
    }
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

