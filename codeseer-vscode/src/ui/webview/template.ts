import * as vscode from 'vscode';

export function getWebviewContent(
    webview: vscode.Webview,
    extensionUri: vscode.Uri
) {
    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(extensionUri, 'media', 'main.js')
    );

    const styleUri = webview.asWebviewUri(
        vscode.Uri.joinPath(extensionUri, 'media', 'styles.css')
    );

    return `
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="${styleUri}">
    </head>

    <body>

    <h2>CodeSeer</h2>

    <div class="container">

        <button class="input" onclick="selectInput()">Select Input</button>
        <div id="inputPath" class="path">No input selected</div>

        <button class="output" onclick="selectOutput()">Select Output</button>
        <div id="outputPath" class="path">No output selected</div>

        <button class="scan" onclick="runScan()">Run Scan</button>

        <div id="status" class="status">Idle</div>

        <div id="log"></div>

    </div>

    <script src="${scriptUri}"></script>
</body>
    </html>
    `;
}