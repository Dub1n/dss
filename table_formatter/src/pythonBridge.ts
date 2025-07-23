import * as cp from 'child_process';
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs-extra';
import * as readline from 'readline';

export class PythonBridge {
    private pythonPath: string;
    private formatterPath: string;
    private backgroundPath: string;
    private backgroundProcess?: cp.ChildProcessWithoutNullStreams;

    constructor() {
        this.pythonPath = this.getPythonPath();
        this.formatterPath = this.getFormatterPath();
        this.backgroundPath = this.getBackgroundPath();

        const config = vscode.workspace.getConfiguration('markdownTableFormatter');
        const useBg = config.get<boolean>('enableBackgroundFormatter', false);
        if (useBg) {
            this.startBackgroundProcess();
        }
    }

    /**
     * Format a markdown table using the Python formatter
     * @param tableText The table text to format
     * @param options Formatting options
     * @returns Promise resolving to the formatted table text
     */
    async formatTable(tableText: string, options: any = {}): Promise<string> {
        if (this.backgroundProcess && !this.backgroundProcess.killed) {
            return this.formatWithBackground(tableText, options);
        }

        return new Promise<string>((resolve, reject) => {
            try {
                const args = this.buildCommandLineArgs(options);
                const proc = cp.spawn(this.pythonPath, [this.formatterPath, ...args]);

                let stdout = '';
                let stderr = '';

                proc.stdout.on('data', (data: Buffer) => (stdout += data.toString()));
                proc.stderr.on('data', (data: Buffer) => (stderr += data.toString()));

                proc.on('close', (code) => {
                    code === 0 ? resolve(stdout.trim()) : reject(new Error(`Formatter failed (${code}): ${stderr}`));
                });
                proc.on('error', (err) => reject(new Error(`Failed to execute formatter: ${err.message}`)));

                proc.stdin.write(tableText);
                proc.stdin.end();
            } catch (error: any) {
                reject(new Error(`Failed to format table: ${error.message}`));
            }
        });
    }

    /**
     * Validate a markdown table
     * @param tableText The table text to validate
     * @returns Promise resolving to whether the table is valid
     */
    async validateTable(tableText: string): Promise<boolean> {
        try {
            const formatted = await this.formatTable(tableText, { validate: true });
            return formatted !== '';
        } catch (error) {
            return false;
        }
    }

    /**
     * Get the Python executable path from configuration
     * @returns The Python path
     */
    private getPythonPath(): string {
        const config = vscode.workspace.getConfiguration('markdownTableFormatter');
        return config.get<string>('pythonPath', 'python');
    }

    /**
     * Get the formatter script path
     * @returns The path to the formatter script
     */
    private getFormatterPath(): string {
        const config = vscode.workspace.getConfiguration('markdownTableFormatter');
        let formatterPath = config.get<string>('formatterPath', '');
        
        // If path is not specified, use the bundled formatter
        if (!formatterPath) {
            const extensionPath = vscode.extensions.getExtension('dss-tools.markdown-table-formatter')?.extensionPath || '';
            formatterPath = path.join(extensionPath, 'main.py');
            
            // Ensure the formatter exists
            if (!fs.existsSync(formatterPath)) {
                throw new Error(`Formatter script not found at ${formatterPath}`);
            }
        }
        
        return formatterPath;
    }

    /** Get path to background server script */
    private getBackgroundPath(): string {
        const extensionPath = vscode.extensions.getExtension('dss-tools.markdown-table-formatter')?.extensionPath || '';
        return path.join(extensionPath, 'bg_server.py');
    }

    /** Spawn a long-lived Python background formatter process */
    private startBackgroundProcess(): void {
        try {
            if (this.backgroundProcess && !this.backgroundProcess.killed) {
                return;
            }
            this.backgroundProcess = cp.spawn(this.pythonPath, [this.backgroundPath]);
            this.backgroundProcess.stderr.on('data', (d: Buffer) => {
                console.error('[formatter]', d.toString());
            });
            this.backgroundProcess.on('exit', () => {
                this.backgroundProcess = undefined;
            });
        } catch (err) {
            vscode.window.showErrorMessage('Python not found or path invalid for Markdown Table Formatter. Configure "markdownTableFormatter.pythonPath" in Settings.');
            console.error('Failed to start background formatter:', err);
        }
    }

    /**
     * Build command-line arguments for the formatter
     * @param options Formatting options
     * @returns Array of command-line arguments
     */
    private buildCommandLineArgs(options: any): string[] {
        const args: string[] = ['--stdin', '--stdout'];
        
        // Add template
        if (options.template) {
            args.push('--template', options.template);
        }
        
        // Add max width
        if (options.maxWidth) {
            args.push('--max-width', options.maxWidth.toString());
        }
        
        // Add min padding
        if (options.minPadding !== undefined) {
            args.push('--min-padding', options.minPadding.toString());
        }
        
        // Add preserve code blocks flag
        if (options.preserveCodeBlocks !== undefined) {
            args.push('--preserve-code-blocks', options.preserveCodeBlocks ? 'true' : 'false');
        }
        
        // Add wrap text flag
        if (options.wrapText !== undefined) {
            args.push('--wrap-text', options.wrapText ? 'true' : 'false');
        }

        // Add validate flag if needed
        if (options.validate) {
            args.push('--validate');
        }
        
        return args;
    }

    /** Send a request to the persistent formatter and await a single-line JSON response */
    private formatWithBackground(tableText: string, options: any): Promise<string> {
        return new Promise((resolve, reject) => {
            if (!this.backgroundProcess) return reject(new Error('Background formatter not running'));

            const rl = readline.createInterface({ input: this.backgroundProcess.stdout });
            const timer = setTimeout(() => {
                rl.close();
                reject(new Error('Formatter timeout'));
            }, 10000);

            const onLine = (line: string) => {
                clearTimeout(timer);
                rl.removeListener('line', onLine);
                rl.close();
                try {
                    const res = JSON.parse(line);
                    if (res.ok) {
                        resolve(res.result.trim());
                    } else {
                        reject(new Error(res.error));
                    }
                } catch (err) {
                    reject(err as Error);
                }
            };

            rl.on('line', onLine);
            const payload = JSON.stringify({ table: tableText, options });
            this.backgroundProcess.stdin.write(payload + '\n');
        });
    }

    /**
     * Clean up resources
     */
    dispose(): void {
        if (this.backgroundProcess && !this.backgroundProcess.killed) {
            this.backgroundProcess.kill();
        }
    }
} 