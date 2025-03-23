// Add this to your existing JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    // Connect the visible button to the hidden file input
    const pdfUploadBtn = document.querySelector('.pdf-upload-btn');
    const pdfFileInput = document.getElementById('pdf-file-input');
    
    if (pdfUploadBtn && pdfFileInput) {
        // Prevent the PDF button from being triggered by Enter key
        pdfUploadBtn.setAttribute('type', 'button');
        
        // Explicitly add a key event listener to prevent Enter from triggering the button
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && document.activeElement !== pdfUploadBtn) {
                // Prevent Enter key from triggering the PDF button
                if (pdfUploadBtn === document.activeElement) {
                    event.preventDefault();
                }
            }
        });
        
        pdfUploadBtn.addEventListener('click', function(event) {
            // Prevent default behavior if it's part of a form
            event.preventDefault();
            pdfFileInput.click(); // Trigger the hidden file input
        });
        
        // Handle when a file is selected
        pdfFileInput.addEventListener('change', function() {
            const file = this.files[0];
            
            if (!file) {
                return;
            }
            
            // Create form data to send the file
            const formData = new FormData();
            formData.append('pdf', file);
            
            // Show a loading indicator
            pdfUploadBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
            
            // Send the file to the backend
            fetch('/upload_pdf', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Reset the button
                pdfUploadBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i>';
                
                if (data.error) {
                    console.error('Error processing PDF:', data.error);
                    return;
                }
                
                // Get the extracted text
                const extractedText = data.text;
                
                // Add the extracted text to the input field
                const promptInput = document.getElementById('prompt-input');
                const currentText = promptInput.value.trim();
                
                // Add a prefix to indicate it's from a PDF
                const pdfPrefix = "Briefly summarize this document: \n\n";
                promptInput.value = currentText 
                    ? currentText + '\n\n' + pdfPrefix + extractedText 
                    : pdfPrefix + extractedText;
                
                // Focus the input field
                promptInput.focus();
                
                // Optional: Auto-expand the textarea if it's not already large enough
                promptInput.style.height = 'auto';
                promptInput.style.height = (promptInput.scrollHeight) + 'px';
            })
            .catch(error => {
                // Reset the button
                pdfUploadBtn.innerHTML = '<i class="fa-solid fa-file-pdf"></i>';
                
                // Handle error
                console.error('Error uploading PDF:', error);
            });
            
            // Clear the file input so the same file can be selected again
            this.value = '';
        });
    }
});