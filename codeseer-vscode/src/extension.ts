import * as vscode from 'vscode';
import { CodeSeerViewProvider } from './ui/CodeSeerViewProvider';

export function activate(context: vscode.ExtensionContext) {

    const provider = new CodeSeerViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            CodeSeerViewProvider.viewType,
            provider
        )
    );

    console.log('CodeSeer activated');
}

export function deactivate() {}