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

document.addEventListener('click', (event) => {
    const target = event.target;
    if (target.tagName === 'INPUT' && (target.type === 'text' || target.type === 'number')) {
        chrome.storage.local.get(['code', 'timestamp'], (result) => {
            const currentTime = Date.now();
            const codeAge = currentTime - result.timestamp;
            if (result.code && codeAge <= 300000) { // 5 minutes in milliseconds
                const dropdown = document.createElement('div');
                dropdown.textContent = result.code;
                dropdown.style.position = 'absolute';
                dropdown.style.backgroundColor = 'white';
                dropdown.style.border = '1px solid black';
                dropdown.style.padding = '5px';
                dropdown.style.cursor = 'pointer';
                dropdown.style.zIndex = '1000';
                dropdown.style.top = `${target.offsetTop + target.offsetHeight}px`;
                dropdown.style.left = `${target.offsetLeft}px`;
                document.body.appendChild(dropdown);

                dropdown.addEventListener('click', () => {
                    target.value = result.code;
                    chrome.storage.local.remove(['code', 'timestamp']);
                    document.body.removeChild(dropdown);
                });

                document.addEventListener('click', (event) => {
                    if (event.target !== dropdown && event.target !== target) {
                        document.body.removeChild(dropdown);
                    }
                }, { once: true });
            }
        });
    }
});
