chrome.runtime.onMessageExternal.addListener((request, sender, sendResponse) => {
    if (request.code) {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.sendMessage(tabs[0].id, { code: request.code });
        });
    }
});