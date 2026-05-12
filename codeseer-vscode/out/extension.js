"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const DOCKER_IMAGE = 'ghcr.io/grigorescustefan/codeseer:v15';
function activate(context) {
    console.log('CodeSeer extension is active.');
    const disposable = vscode.commands.registerCommand('codeseer.scan', async () => {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            vscode.window.showErrorMessage('No workspace folder open.');
            return;
        }
        const workspace = workspaceFolder.uri.fsPath;
        const outputDir = path.join(workspace, 'reports');
        vscode.window.showInformationMessage('Running CodeSeer scan...');
        // Docker command
        const dockerCommand = [
            'docker run --rm',
            `-v "${workspace}:/input"`,
            `-v "${outputDir}:/output"`,
            DOCKER_IMAGE
        ].join(' ');
        (0, child_process_1.exec)(dockerCommand, (error, stdout, stderr) => {
            // IMPORTANT: Semgrep returns exit code 1 when it finds issues
            // so we ONLY treat it as a real failure if it's NOT code 1
            if (error && error.code !== 1) {
                console.error('Docker error:', error);
                console.error(stderr);
                vscode.window.showErrorMessage('CodeSeer scan failed. Check Docker output.');
                return;
            }
            console.log(stdout);
            vscode.window.showInformationMessage('CodeSeer scan completed.');
            // Open report
            const reportPath = path.join(outputDir, 'report.html');
            const reportUri = vscode.Uri.file(reportPath);
            console.log('Opening report at:', reportPath);
            vscode.env.openExternal(reportUri);
        });
    });
    context.subscriptions.push(disposable);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map