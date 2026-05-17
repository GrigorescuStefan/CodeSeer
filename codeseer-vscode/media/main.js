const vscode = acquireVsCodeApi();

function selectInput() {
    vscode.postMessage({ type: 'selectInput' });
}

function selectOutput() {
    vscode.postMessage({ type: 'selectOutput' });
}

function runScan() {
    vscode.postMessage({ type: 'runScan' });
}

window.addEventListener('message', event => {

    const msg = event.data;

    if (msg.type === 'status') {
        document.getElementById('status').innerText = msg.value;
    }

    if (msg.type === 'inputPath') {
        document.getElementById('inputPath').innerText = msg.value;
    }

    if (msg.type === 'outputPath') {
        document.getElementById('outputPath').innerText = msg.value;
    }

    if (msg.type === 'log') {
        const log = document.getElementById('log');
        log.innerText += `\n${msg.value}`;
    }
});