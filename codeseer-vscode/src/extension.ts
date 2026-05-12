import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

const DOCKER_IMAGE = 'ghcr.io/grigorescustefan/codeseer:v15';

export function activate(context: vscode.ExtensionContext) {

    console.log('CodeSeer extension is active.');

    const disposable = vscode.commands.registerCommand(
        'codeseer.scan',
        async () => {

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

            exec(
                dockerCommand,
                (error: Error | null, stdout: string, stderr: string) => {

                    // IMPORTANT: Semgrep returns exit code 1 when it finds issues
                    // so we ONLY treat it as a real failure if it's NOT code 1
                    if (error && (error as any).code !== 1) {
                        console.error('Docker error:', error);
                        console.error(stderr);

                        vscode.window.showErrorMessage(
                            'CodeSeer scan failed. Check Docker output.'
                        );

                        return;
                    }

                    console.log(stdout);

                    vscode.window.showInformationMessage(
                        'CodeSeer scan completed.'
                    );

                    // Open report
                    const reportPath = path.join(outputDir, 'report.html');
                    const reportUri = vscode.Uri.file(reportPath);

                    console.log('Opening report at:', reportPath);

                    vscode.env.openExternal(reportUri);
                }
            );
        }
    );

    context.subscriptions.push(disposable);
}

export function deactivate() {}