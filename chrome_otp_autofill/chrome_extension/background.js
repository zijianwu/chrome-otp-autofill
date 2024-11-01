chrome.runtime.onMessageExternal.addListener((request, sender, sendResponse) => {
    if (request.code) {
        const timestamp = Date.now();
        chrome.storage.local.set({ code: request.code, timestamp: timestamp }, () => {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                chrome.tabs.sendMessage(tabs[0].id, { code: request.code });
            });
        });
    }
});
