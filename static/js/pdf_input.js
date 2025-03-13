// Function to handle PDF file upload
function handlePdfUpload(file) {
    // Show loading indicator in the response container
    const loadingMessage = `
        <div class="d-flex justify-content-center mb-4">
            <div class="model-message p-3">
                <div class="spinner-grow spinner-grow-sm text-info" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <span class="ms-2">Uploading and processing PDF: ${file.name}</span>
            </div>
        </div>
    `;
    responseContainer.innerHTML += loadingMessage;
    responseContainer.scrollTop = responseContainer.scrollHeight;

    // Create FormData object to send the file
    const formData = new FormData();
    formData.append('pdf', file);

    // Get selected models to process the PDF content
    const selectedModels = Array.from(document.querySelectorAll('.model-select')).map(select => select.value);
    
    // Add selected models to the FormData
    selectedModels.forEach(model => {
        formData.append('models', model);
    });

    // Send the PDF to the backend
    fetch('/upload_pdf', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('PDF upload failed');
        }
        return response.json();
    })
    .then(data => {
        // Remove the loading message
        const loadingElement = responseContainer.querySelector('.d-flex.justify-content-center.mb-4');
        if (loadingElement) {
            loadingElement.remove();
        }

        // Display the PDF content as a user message
        const pdfContent = data.content || 'PDF content extracted successfully';
        displayUserMessage(`📄 PDF Upload: ${file.name}\n\n${pdfContent}`);

        // Display loading spinners for models processing the PDF content
        displayLoadingSpinners(selectedModels);

        // Process each model's response to the PDF content
        if (data.modelResponses) {
            Object.entries(data.modelResponses).forEach(([model, response]) => {
                displayModelResponse(model, response);
            });
        } else {
            // If backend doesn't return model responses directly, you may need to 
            // make separate requests for each model to process the PDF content
            selectedModels.forEach(async (model) => {
                try {
                    const response = await fetch(`/process_pdf/${model}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ pdfId: data.pdfId })
                    });
                    const modelData = await response.json();
                    displayModelResponse(model, modelData.response);
                } catch (error) {
                    displayModelResponse(model, `Error processing PDF with ${model}: ${error.message}`);
                }
            });
        }
    })
    .catch(error => {
        // Display error message
        const errorMessage = `
            <div class="d-flex justify-content-center mb-4">
                <div class="model-message p-3 text-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    Error uploading PDF: ${error.message}
                </div>
            </div>
        `;
        
        // Remove the loading message
        const loadingElement = responseContainer.querySelector('.d-flex.justify-content-center.mb-4');
        if (loadingElement) {
            loadingElement.remove();
        }
        
        responseContainer.innerHTML += errorMessage;
        responseContainer.scrollTop = responseContainer.scrollHeight;
    });
}

// Initialize PDF upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const pdfUploadBtn = document.querySelector('.pdf-upload-btn');
    const pdfFileInput = document.getElementById('pdf-file-input');
    
    // When the PDF button is clicked, trigger the file input
    pdfUploadBtn.addEventListener('click', function() {
        pdfFileInput.click();
    });
    
    // When a file is selected, handle the upload
    pdfFileInput.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            
            // Check if the file is a PDF
            if (file.type !== 'application/pdf') {
                alert('Please select a PDF file');
                return;
            }
            
            // Process the PDF file
            handlePdfUpload(file);
            
            // Reset the file input so the same file can be uploaded again if needed
            this.value = '';
        }
    });
});