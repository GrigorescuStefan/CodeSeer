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
exports.CodeSeerViewProvider = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const child_process_1 = require("child_process");
const dockerCheck_1 = require("../docker/dockerCheck");
const template_1 = require("./webview/template");
const DOCKER_IMAGE = 'ghcr.io/grigorescustefan/codeseer:v16';
class CodeSeerViewProvider {
    extensionUri;
    static viewType = 'codeseerView';
    view;
    inputPath;
    outputPath;
    constructor(extensionUri) {
        this.extensionUri = extensionUri;
    }
    resolveWebviewView(webviewView) {
        this.view = webviewView;
        webviewView.webview.options = {
            enableScripts: true
        };
        webviewView.webview.html = (0, template_1.getWebviewContent)(webviewView.webview, this.extensionUri);
        webviewView.webview.onDidReceiveMessage(async (msg) => {
            switch (msg.type) {
                case 'selectInput': {
                    const res = await vscode.window.showOpenDialog({
                        canSelectFolders: true,
                        canSelectFiles: false
                    });
                    if (res?.[0]) {
                        this.inputPath = res[0].fsPath;
                        this.postEvent({ type: 'inputPath', value: this.inputPath });
                    }
                    break;
                }
                case 'selectOutput': {
                    const res = await vscode.window.showOpenDialog({
                        canSelectFolders: true,
                        canSelectFiles: false
                    });
                    if (res?.[0]) {
                        this.outputPath = res[0].fsPath;
                        this.postEvent({ type: 'outputPath', value: this.outputPath });
                    }
                    break;
                }
                case 'runScan':
                    await this.runScan();
                    break;
            }
        });
    }
    async runScan() {
        if (!this.inputPath || !this.outputPath) {
            vscode.window.showErrorMessage('Select input and output folders first.');
            return;
        }
        const dockerStatus = await (0, dockerCheck_1.checkDocker)();
        if (!dockerStatus.ok) {
            vscode.window.showErrorMessage(dockerStatus.message || 'Docker not available');
            return;
        }
        const reportsDir = path.join(this.outputPath, 'reports');
        if (!fs.existsSync(reportsDir)) {
            fs.mkdirSync(reportsDir, { recursive: true });
        }
        this.postEvent({ type: 'status', value: 'Starting scan...' });
        const args = [
            'run',
            '--rm',
            '-v', `${this.inputPath}:/input`,
            '-v', `${reportsDir}:/output`,
            DOCKER_IMAGE
        ];
        const child = (0, child_process_1.spawn)('docker', args, { shell: false });
        child.stdout.setEncoding('utf8');
        child.stderr.setEncoding('utf8');
        const handleLine = (line) => {
            line = line.trim();
            if (!line)
                return;
            // Structured events from Python
            if (line.startsWith('__CODESEER__')) {
                const parts = line.split('|');
                const type = parts[1];
                const value = parts.slice(2).join('|');
                if (type === 'status') {
                    this.postEvent({ type: 'status', value });
                }
                return;
            }
            // Normal logs
            this.postEvent({ type: 'log', value: line });
        };
        child.stdout.on('data', (data) => {
            data.toString().split('\n').forEach(handleLine);
        });
        child.stderr.on('data', (data) => {
            data.toString().split('\n').forEach(handleLine);
        });
        child.on('close', (code) => {
            this.postEvent({ type: 'status', value: 'Finished' });
            vscode.env.openExternal(vscode.Uri.file(path.join(reportsDir, 'report.html')));
            // IMPORTANT: exit code 1 = HIGH findings, NOT failure
            if (code !== null && code !== 0 && code !== 1) {
                this.postEvent({ type: 'status', value: 'Scan failed' });
            }
        });
    }
    postEvent(event) {
        this.view?.webview.postMessage(event);
    }
}
exports.CodeSeerViewProvider = CodeSeerViewProvider;
//# sourceMappingURL=CodeSeerViewProvider.js.map