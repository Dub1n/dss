/**
 * ---
 * tags: [code, vscode_extension, options_prompt]
 * provides: [promptForFormattingOptions]
 * requires: [vscode]
 * ---
 *
 * A small utility that prompts the user (via QuickPick / InputBox) for formatting
 * options such as template style, maximum table width, and text-wrapping.
 * The chosen options are cached for the current VS Code session and can be
 * persisted back to the user's `markdownTableFormatter.*` settings if desired.
 */

import * as vscode from 'vscode';

// In-memory cache so the user doesn’t have to answer the same questions again
let lastOptions: FormattingOptions | undefined;

export interface FormattingOptions {
    template: string;
    maxWidth: number;
    minPadding: number;
    wrapText: boolean;
    preserveCodeBlocks: boolean;
}

/**
 * Prompt the user for formatting options. Returns undefined if the user cancels
 * at any stage.
 */
export async function promptForFormattingOptions(): Promise<FormattingOptions | undefined> {
    // Re-use previous answers when available
    if (lastOptions) {
        const reuse = await vscode.window.showQuickPick([
            { label: 'Yes', description: 'Reuse previous formatting options' },
            { label: 'No', description: 'Choose new options' }
        ], { placeHolder: 'Use the same formatting options as last time?' });

        if (!reuse) {
            return undefined; // User cancelled
        }
        if (reuse.label === 'Yes') {
            return lastOptions;
        }
    }

    const cfg = vscode.workspace.getConfiguration('markdownTableFormatter');

    // 1. Template style
    const templateChoices = ['github', 'smart', 'none'];
    const template = await vscode.window.showQuickPick(templateChoices, {
        placeHolder: 'Select the table template style',
        ignoreFocusOut: true
    });
    if (!template) {
        return undefined;
    }

    // 2. Maximum table width
    const maxWidthInput = await vscode.window.showInputBox({
        prompt: 'Maximum table width (number, press ⏎ to accept default)',
        value: cfg.get<number>('maxTableWidth', 80).toString(),
        ignoreFocusOut: true,
        validateInput: v => (v.trim() === '' || /^\d+$/.test(v)) ? undefined : 'Enter a valid integer'
    });
    if (maxWidthInput === undefined) { // Esc pressed
        return undefined;
    }
    const maxWidth = maxWidthInput.trim() === '' ? cfg.get<number>('maxTableWidth', 80) : parseInt(maxWidthInput, 10);

    // 3. Minimum cell padding
    const paddingInput = await vscode.window.showInputBox({
        prompt: 'Minimum cell padding (spaces, default 1)',
        value: cfg.get<number>('minPadding', 1).toString(),
        ignoreFocusOut: true,
        validateInput: v => (v.trim() === '' || /^\d+$/.test(v)) ? undefined : 'Enter a valid integer'
    });
    if (paddingInput === undefined) {
        return undefined;
    }
    const minPadding = paddingInput.trim() === '' ? cfg.get<number>('minPadding', 1) : parseInt(paddingInput, 10);

    // 4. Wrap text
    const wrapChoice = await vscode.window.showQuickPick([
        { label: 'Yes', description: 'Wrap long text within cells' },
        { label: 'No', description: 'Do not wrap text' }
    ], { placeHolder: 'Wrap text in table cells?', ignoreFocusOut: true });
    if (!wrapChoice) {
        return undefined;
    }
    const wrapText = wrapChoice.label === 'Yes';

    // 5. Preserve code blocks
    const codeChoice = await vscode.window.showQuickPick([
        { label: 'Yes', description: 'Leave fenced code blocks untouched' },
        { label: 'No', description: 'Treat code blocks as normal text' }
    ], { placeHolder: 'Preserve fenced code blocks inside tables?', ignoreFocusOut: true });
    if (!codeChoice) {
        return undefined;
    }
    const preserveCodeBlocks = codeChoice.label === 'Yes';

    const options: FormattingOptions = {
        template,
        maxWidth,
        minPadding,
        wrapText,
        preserveCodeBlocks
    };

    // Save in-memory for the session
    lastOptions = options;

    // 6. Ask whether to persist to settings
    const persist = await vscode.window.showQuickPick([
        { label: 'Yes', description: 'Save these as defaults (User Settings)' },
        { label: 'No', description: 'Use for this session only' }
    ], { placeHolder: 'Persist these options to your VS Code settings?', ignoreFocusOut: true });

    if (persist && persist.label === 'Yes') {
        await cfg.update('defaultTemplate', template, vscode.ConfigurationTarget.Global);
        await cfg.update('maxTableWidth', maxWidth, vscode.ConfigurationTarget.Global);
        await cfg.update('minPadding', minPadding, vscode.ConfigurationTarget.Global);
        await cfg.update('wrapText', wrapText, vscode.ConfigurationTarget.Global);
        await cfg.update('preserveCodeBlocks', preserveCodeBlocks, vscode.ConfigurationTarget.Global);
    }

    return options;
} 