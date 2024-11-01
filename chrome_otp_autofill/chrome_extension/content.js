// chrome.runtime.onMessage.addListener((message) => {
//     if (message.code) {
//         chrome.storage.local.set({ code: message.code, timestamp: Date.now() });
//     }
// });

// document.addEventListener('click', (event) => {
//     const target = event.target;
//     if (target.tagName === 'INPUT' && (target.type === 'text' || target.type === 'number')) {
//         chrome.storage.local.get(['code', 'timestamp'], (result) => {
//             const currentTime = Date.now();
//             const codeAge = currentTime - result.timestamp;
//             if (result.code && codeAge <= 300000) { // 5 minutes in milliseconds
//                 const dropdown = document.createElement('div');
//                 dropdown.textContent = result.code;
//                 dropdown.style.position = 'absolute';
//                 dropdown.style.backgroundColor = 'white';
//                 dropdown.style.border = '1px solid black';
//                 dropdown.style.padding = '5px';
//                 dropdown.style.cursor = 'pointer';
//                 dropdown.style.zIndex = '1000';
//                 dropdown.style.top = `${target.offsetTop + target.offsetHeight}px`;
//                 dropdown.style.left = `${target.offsetLeft}px`;
//                 document.body.appendChild(dropdown);

//                 dropdown.addEventListener('click', () => {
//                     target.value = result.code;
//                     chrome.storage.local.remove(['code', 'timestamp']);
//                     document.body.removeChild(dropdown);
//                 });

//                 document.addEventListener('click', (event) => {
//                     if (event.target !== dropdown && event.target !== target) {
//                         document.body.removeChild(dropdown);
//                     }
//                 }, { once: true });
//             }
//         });
//     }
// });


// Check if the target is an OTP field based on common attributes and patterns
function isOtpField(target) {
    const isTextInput = target.tagName === 'INPUT' && (target.type === 'text' || target.type === 'number');
    const isTextArea = target.tagName === 'TEXTAREA';

    // Check for common OTP attributes
    const hasOtpAttributes = target.autocomplete === 'one-time-code' ||
                             target.inputMode === 'numeric' || target.inputMode === 'tel' ||
                             (target.maxLength === 4 || target.maxLength === 6 || target.maxLength === 8);

    // Check for OTP-related keywords in attributes
    const attributePatterns = /(otp|code|verification|authcode|pin)/i;
    const hasOtpKeywords = attributePatterns.test(target.name) ||
                           attributePatterns.test(target.id) ||
                           attributePatterns.test(target.className) ||
                           attributePatterns.test(target.getAttribute('aria-label')) ||
                           attributePatterns.test(target.placeholder);

    return (isTextInput || isTextArea) || (hasOtpAttributes || hasOtpKeywords);
}



// Create a full-screen overlay that covers the viewport
const overlay = document.createElement('div');
overlay.style.position = 'fixed';
overlay.style.top = '0';
overlay.style.left = '0';
overlay.style.width = '100vw';
overlay.style.height = '100vh';
overlay.style.pointerEvents = 'none'; // Prevents blocking interactions on other parts of the page
overlay.style.zIndex = '2147483647'; // Very high z-index to stay on top
document.body.appendChild(overlay);

document.addEventListener('click', (event) => {
    const target = event.target;

    // Check if the clicked element is a text input field
    if (isOtpField(target)) {
        // Remove any existing dropdowns before creating a new one
        const existingDropdown = document.querySelector('.code-dropdown');
        if (existingDropdown) {
            existingDropdown.remove();
        }

        // Create the dropdown element with code "123456"
        const dropdown = document.createElement('div');
        dropdown.textContent = "123456";
        dropdown.classList.add('code-dropdown');

        // Styling for the dropdown
        dropdown.style.position = 'absolute';
        dropdown.style.backgroundColor = 'white';
        dropdown.style.border = '1px solid black';
        dropdown.style.padding = '5px';
        dropdown.style.cursor = 'pointer';
        dropdown.style.zIndex = '2147483647'; // Ensures it's on top within overlay
        dropdown.style.boxShadow = '0px 4px 8px rgba(0, 0, 0, 0.2)';
        dropdown.style.pointerEvents = 'auto'; // Allow clicks on the dropdown

        // Function to position the dropdown within the overlay
        function positionDropdown() {
            const rect = target.getBoundingClientRect();
            dropdown.style.top = `${rect.bottom + 5}px`; // Position below the input with 5px gap
            dropdown.style.left = `${rect.left}px`;
        }

        // Initial positioning of the dropdown
        positionDropdown();

        // Append the dropdown to the overlay
        overlay.appendChild(dropdown);

        // Re-position the dropdown on scroll and resize
        window.addEventListener('scroll', positionDropdown, { passive: true });
        window.addEventListener('resize', positionDropdown, { passive: true });

        // Fill the input with "123456" when the dropdown is clicked
        dropdown.addEventListener('click', () => {
            target.value = "123456";
            dropdown.remove();  // Remove dropdown after use
            window.removeEventListener('scroll', positionDropdown); // Clean up event listener
            window.removeEventListener('resize', positionDropdown); // Clean up event listener
            dropdown.remove();
        });

        // Remove the dropdown if clicking outside of it
        document.addEventListener('click', (outsideClickEvent) => {
            if (outsideClickEvent.target !== dropdown && outsideClickEvent.target !== target) {
                dropdown.remove();
                window.removeEventListener('scroll', positionDropdown); // Clean up event listener
                window.removeEventListener('resize', positionDropdown); // Clean up event listener
            }
        }, { once: true });
    }
});