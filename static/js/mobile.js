// Minimal JavaScript to sync controls between mobile and desktop
document.addEventListener('DOMContentLoaded', function() {
    // Handle resizing for mobile browsers that show/hide address bar
    function adjustHeight() {
        // Mobile browsers sometimes change height when address bar shows/hides
        document.body.style.height = window.innerHeight + 'px';
    }
    
    window.addEventListener('resize', adjustHeight);
    window.addEventListener('orientationchange', adjustHeight);
    adjustHeight(); // Initial call
    
    // Get all necessary elements
    const desktopConvo = document.getElementById('conversationMode');
    const mobileConvo = document.getElementById('mobileConversationMode');
    const desktopCount = document.getElementById('modelCount');
    const mobileCount = document.getElementById('mobileModelCount');
    const desktopRefresh = document.getElementById('refreshButton');
    const mobileRefresh = document.getElementById('mobileRefreshButton');

    // Add event listeners only if elements exist
    if (mobileConvo && desktopConvo) {
        mobileConvo.addEventListener('change', function() {
            desktopConvo.checked = this.checked;
        });
    }
    
    if (mobileCount && desktopCount) {
        mobileCount.addEventListener('change', function() {
            desktopCount.value = this.value;
            updateMobileSelectors(this.value);
        });
    }
    
    if (mobileRefresh && desktopRefresh) {
        mobileRefresh.addEventListener('click', function() {
            // Clear the response container directly
            const responseContainer = document.getElementById('response-container');
            if (responseContainer) {
                responseContainer.innerHTML = '';
            }
            
            // Call the server reset endpoint
            fetch('/reset_conversations', {
                method: 'POST'
            }).then(response => {
                if (response.ok) {
                    console.log('All conversation histories cleared successfully');
                } else {
                    console.error('Failed to clear conversation histories');
                }
            }).catch(error => {
                console.error('Error clearing conversation histories:', error);
            });
        });
    }

    // Initialize mobile selectors if they exist
    if (mobileCount) {
        updateMobileSelectors(1);
    }
    
    // PDF button functionality
    const pdfBtn = document.querySelector('.pdf-upload-btn');
    const pdfInput = document.getElementById('pdf-file-input');
    
    pdfBtn.addEventListener('click', function() {
        pdfInput.click();
    });
});

// ... existing code ...

function createMobileModelSelector(index) {
    return `
        <div class="mobile-model-selector mb-2">
            <div class="input-group">
                <span class="input-group-text" style="background-color: #0f3460; color: #c0c0c0;">#${index + 1}</span>
                <select class="form-select model-select">
                    <option value="gemini-2_5-pro">Gemini 2.5 Pro</option>
                    <option value="openai-o3-mini">OpenAI gpt o3 mini</option>
                    <option value="openai-o1">OpenAI gpt o1</option>
                    <option value="openai-4o">OpenAI gpt 4o</option>
                    <option value="openai-4_5_preview">OpenAI gpt 4.5 preview</option>
                    <option value="claude_3_7_sonnet">Claude 3.7 sonnet</option>
                    <option value="claude_3_opus">Claude 3 opus</option>
                    <option value="deepseek_reasoner">Deepseek Reasoner</option>
                    <option value="llama3_3">Llama 3.3</option>
                </select>
            </div>
        </div>
    `;
}

function updateMobileSelectors(count) {
    const mobileSelectors = document.getElementById('mobileModelSelectors');
    if (mobileSelectors) {
        mobileSelectors.innerHTML = '';
        for (let i = 0; i < parseInt(count); i++) {
            mobileSelectors.innerHTML += createMobileModelSelector(i);
        }
    }
}

// Update the model count change listener to handle both desktop and mobile selectors
modelCount.addEventListener('change', () => {
    const count = parseInt(modelCount.value);
    const isMobile = window.innerWidth < 768;
    
    // Update desktop selectors
    modelSelectors.innerHTML = '';
    for (let i = 0; i < count; i++) {
        modelSelectors.innerHTML += createModelSelector(i);
    }
    
    // Update mobile selectors
    const mobileSelectors = document.getElementById('mobileModelSelectors');
    if (mobileSelectors) {
        mobileSelectors.innerHTML = '';
        for (let i = 0; i < count; i++) {
            mobileSelectors.innerHTML += createMobileModelSelector(i);
        }
    }
});

// Also handle mobile model count changes
const mobileModelCount = document.getElementById('mobileModelCount');
if (mobileModelCount) {
    mobileModelCount.addEventListener('change', () => {
        const count = parseInt(mobileModelCount.value);
        
        // Update mobile selectors
        const mobileSelectors = document.getElementById('mobileModelSelectors');
        mobileSelectors.innerHTML = '';
        for (let i = 0; i < count; i++) {
            mobileSelectors.innerHTML += createMobileModelSelector(i);
        }
        
        // Keep desktop in sync
        modelCount.value = count;
        modelSelectors.innerHTML = '';
        for (let i = 0; i < count; i++) {
            modelSelectors.innerHTML += createModelSelector(i);
        }
    });
}

// Update resize handler
window.addEventListener('resize', () => {
    modelCount.dispatchEvent(new Event('change'));
});