import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';
import { checkDocker } from '../docker/dockerCheck';
import { getWebviewContent } from './webview/template';

const DOCKER_IMAGE = 'ghcr.io/grigorescustefan/codeseer:v16';

type ScanEvent =
    | { type: 'status'; value: string }
    | { type: 'inputPath'; value: string }
    | { type: 'outputPath'; value: string }
    | { type: 'log'; value: string };

export class CodeSeerViewProvider implements vscode.WebviewViewProvider {

    public static readonly viewType = 'codeseerView';

    private view?: vscode.WebviewView;
    private inputPath?: string;
    private outputPath?: string;

    constructor(private readonly extensionUri: vscode.Uri) {}

    resolveWebviewView(webviewView: vscode.WebviewView) {
        this.view = webviewView;

        webviewView.webview.options = {
            enableScripts: true
        };

        webviewView.webview.html = getWebviewContent(
            webviewView.webview,
            this.extensionUri
        );

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

    private async runScan() {

        if (!this.inputPath || !this.outputPath) {
            vscode.window.showErrorMessage('Select input and output folders first.');
            return;
        }

        const dockerStatus = await checkDocker();

        if (!dockerStatus.ok) {
            vscode.window.showErrorMessage(
                dockerStatus.message || 'Docker not available'
            );
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

        const child = spawn('docker', args, { shell: false });

        child.stdout.setEncoding('utf8');
        child.stderr.setEncoding('utf8');

        const handleLine = (line: string) => {
            line = line.trim();
            if (!line) return;

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

            vscode.env.openExternal(
                vscode.Uri.file(path.join(reportsDir, 'report.html'))
            );

            // IMPORTANT: exit code 1 = HIGH findings, NOT failure
            if (code !== null && code !== 0 && code !== 1) {
                this.postEvent({ type: 'status', value: 'Scan failed' });
            }
        });
    }

    private postEvent(event: ScanEvent) {
        this.view?.webview.postMessage(event);
    }
}