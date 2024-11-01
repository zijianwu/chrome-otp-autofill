chrome.runtime.onMessage.addListener((message) => {
    if (message.code) {
        const inputs = document.querySelectorAll("input[type='text'], input[type='number']");
        inputs.forEach(input => {
            if (input.placeholder.includes("code") || input.ariaLabel.includes("code")) {
                input.value = message.code;
            }
        });
    }
});