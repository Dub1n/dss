---
tags: [Cursor, Implementation, Step-by-Step, Plugin Development, Token Tracker]
provides: [Implementation Guide, Code Examples, Development Steps]
requires: [Plugin Framework Skeleton, Token Count Discovery]
---

# Cursor Token Tracker: Step-by-Step Implementation Guide

## 🎯 Project Overview

**Goal**: Extract Cursor's existing token counts and make them always visible with smart automation
**Time Estimate**: 3-8 hours total
**Difficulty**: Beginner-Intermediate (mostly VS Code extension boilerplate)

## 📋 Phase 1: Project Setup (30-60 minutes)

### Step 1: Create Extension Structure

```bash
# Create project directory
mkdir cursor-token-tracker
cd cursor-token-tracker

# Initialize npm project
npm init -y

# Install VS Code extension dependencies
npm install --save-dev @types/vscode typescript @vscode/test-electron
npm install vscode

# Create basic structure
mkdir src
mkdir src/webview
touch src/extension.ts
touch src/tokenExtractor.ts
touch src/statusBar.ts
touch package.json
```

### Step 2: Configure package.json

```json
{
  "name": "cursor-token-tracker",
  "displayName": "Cursor Token Tracker",
  "description": "Makes Cursor's token counts always visible with smart automation",
  "version": "0.1.0",
  "engines": {
    "vscode": "^1.80.0"
  },
  "categories": ["Other"],
  "activationEvents": [
    "*"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "cursor-token-tracker.showTokens",
        "title": "Show Current Token Count"
      },
      {
        "command": "cursor-token-tracker.exportChat",
        "title": "Export Chat (Auto)"
      }
    ],
    "configuration": {
      "title": "Cursor Token Tracker",
      "properties": {
        "cursorTokenTracker.warningThreshold": {
          "type": "number",
          "default": 24000,
          "description": "Show warning when tokens exceed this number"
        },
        "cursorTokenTracker.autoExportThreshold": {
          "type": "number", 
          "default": 26000,
          "description": "Auto-export chat when tokens exceed this number"
        }
      }
    }
  },
  "scripts": {
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  }
}
```

### Step 3: TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2020",
    "outDir": "out",
    "lib": ["ES2020"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
```

## 📋 Phase 2: Core Token Extraction (2-3 hours)

### Step 4: Basic Extension Entry Point

```typescript
// src/extension.ts
import * as vscode from 'vscode';
import { TokenExtractor } from './tokenExtractor';
import { TokenStatusBar } from './statusBar';

export function activate(context: vscode.ExtensionContext) {
    console.log('Cursor Token Tracker activated');
    
    const tokenExtractor = new TokenExtractor();
    const statusBar = new TokenStatusBar();
    
    // Register commands
    const showTokensCommand = vscode.commands.registerCommand(
        'cursor-token-tracker.showTokens',
        () => {
            const count = tokenExtractor.getCurrentTokenCount();
            vscode.window.showInformationMessage(`Current tokens: ${count}`);
        }
    );
    
    // Start monitoring
    tokenExtractor.startMonitoring((tokenCount) => {
        statusBar.updateDisplay(tokenCount);
    });
    
    context.subscriptions.push(showTokensCommand, statusBar);
}

export function deactivate() {}
```

### Step 5: Token Extraction Logic

```typescript
// src/tokenExtractor.ts
import * as vscode from 'vscode';

export class TokenExtractor {
    private currentTokenCount: number = 0;
    private monitoringInterval?: NodeJS.Timeout;
    private callbacks: Array<(count: number) => void> = [];

    getCurrentTokenCount(): number {
        return this.currentTokenCount;
    }

    startMonitoring(callback: (count: number) => void) {
        this.callbacks.push(callback);
        
        // Poll every 2 seconds for token count changes
        this.monitoringInterval = setInterval(() => {
            this.extractTokenCount();
        }, 2000);
        
        // Initial extraction
        this.extractTokenCount();
    }

    private async extractTokenCount() {
        try {
            // Create webview to access Cursor's DOM
            const panel = vscode.window.createWebviewPanel(
                'tokenExtractor',
                'Token Extractor',
                { viewColumn: vscode.ViewColumn.Active, preserveFocus: true },
                {
                    enableScripts: true,
                    retainContextWhenHidden: true
                }
            );

            // Inject extraction script
            panel.webview.html = this.getWebviewContent();
            
            // Listen for token count from webview
            panel.webview.onDidReceiveMessage(
                message => {
                    if (message.type === 'tokenCount') {
                        this.updateTokenCount(message.count);
                        panel.dispose(); // Close hidden webview
                    }
                }
            );

        } catch (error) {
            console.error('Token extraction failed:', error);
        }
    }

    private getWebviewContent(): string {
        return `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Token Extractor</title>
            </head>
            <body>
                <script>
                    (function() {
                        // Try multiple selectors to find token count
                        const selectors = [
                            // Three dots menu selectors
                            '.chat-controls .three-dots',
                            '.chat-menu [data-testid="menu-trigger"]',
                            '.chat-header .menu-button',
                            '[data-testid="chat-menu"]',
                            '.cursor-chat-menu',
                            
                            // Direct token display selectors
                            '[data-token-count]',
                            '.token-counter',
                            '.context-size'
                        ];
                        
                        let tokenCount = 0;
                        
                        // Try each selector
                        for (const selector of selectors) {
                            const element = document.querySelector(selector);
                            if (element) {
                                const text = element.textContent || element.innerHTML || '';
                                console.log('Found element:', selector, 'Text:', text);
                                
                                // Look for token patterns
                                const patterns = [
                                    /(\d+(?:,\d+)*(?:\.\d+)?)\s*k?\s*tokens?/i,
                                    /context:\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*k?/i,
                                    /(\d+(?:,\d+)*(?:\.\d+)?)\s*k?\s*context/i
                                ];
                                
                                for (const pattern of patterns) {
                                    const match = text.match(pattern);
                                    if (match) {
                                        tokenCount = this.parseTokenNumber(match[1]);
                                        console.log('Found tokens:', tokenCount);
                                        break;
                                    }
                                }
                                
                                if (tokenCount > 0) break;
                            }
                        }
                        
                        // Send result back to extension
                        if (typeof acquireVsCodeApi !== 'undefined') {
                            const vscode = acquireVsCodeApi();
                            vscode.postMessage({
                                type: 'tokenCount',
                                count: tokenCount
                            });
                        }
                        
                        function parseTokenNumber(str) {
                            // Handle formats like "1,234", "5.2k", "1234"
                            str = str.replace(/,/g, '');
                            if (str.toLowerCase().includes('k')) {
                                return Math.round(parseFloat(str) * 1000);
                            }
                            return parseInt(str) || 0;
                        }
                    })();
                </script>
            </body>
            </html>
        `;
    }

    private updateTokenCount(count: number) {
        if (count !== this.currentTokenCount) {
            this.currentTokenCount = count;
            this.callbacks.forEach(callback => callback(count));
        }
    }

    dispose() {
        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
        }
    }
}
```

### Step 6: Status Bar Display

```typescript
// src/statusBar.ts
import * as vscode from 'vscode';

export class TokenStatusBar implements vscode.Disposable {
    private statusBarItem: vscode.StatusBarItem;
    private config = vscode.workspace.getConfiguration('cursorTokenTracker');

    constructor() {
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        this.statusBarItem.command = 'cursor-token-tracker.showTokens';
        this.statusBarItem.show();
    }

    updateDisplay(tokenCount: number) {
        if (tokenCount === 0) {
            this.statusBarItem.hide();
            return;
        }

        // Format display
        const formattedCount = this.formatTokens(tokenCount);
        this.statusBarItem.text = `$(pulse) ${formattedCount}`;
        this.statusBarItem.tooltip = `Current chat: ${tokenCount} tokens`;

        // Color coding based on thresholds
        const warningThreshold = this.config.get('warningThreshold', 24000);
        const autoExportThreshold = this.config.get('autoExportThreshold', 26000);

        if (tokenCount > autoExportThreshold) {
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
            this.statusBarItem.color = '#ffffff';
        } else if (tokenCount > warningThreshold) {
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
            this.statusBarItem.color = '#000000';
        } else {
            this.statusBarItem.backgroundColor = undefined;
            this.statusBarItem.color = undefined;
        }

        this.statusBarItem.show();

        // Trigger smart actions
        this.checkSmartActions(tokenCount);
    }

    private formatTokens(count: number): string {
        if (count > 1000) {
            return `${(count / 1000).toFixed(1)}k tokens`;
        }
        return `${count} tokens`;
    }

    private checkSmartActions(tokenCount: number) {
        const autoExportThreshold = this.config.get('autoExportThreshold', 26000);
        
        if (tokenCount > autoExportThreshold) {
            // Suggest export
            vscode.window.showWarningMessage(
                `Token count is high (${tokenCount}). Consider exporting this chat.`,
                'Export Now',
                'Dismiss'
            ).then(selection => {
                if (selection === 'Export Now') {
                    vscode.commands.executeCommand('cursor-token-tracker.exportChat');
                }
            });
        }
    }

    dispose() {
        this.statusBarItem.dispose();
    }
}
```

## 📋 Phase 3: Testing & Refinement (1-2 hours)

### Step 7: Build and Test

```bash
# Compile TypeScript
npm run compile

# Test in VS Code development host
# Press F5 in VS Code to launch extension development host
```

### Step 8: Debug Token Extraction

Add logging to see what we're finding:

```typescript
// Add to tokenExtractor.ts webview script
console.log('Available elements:', document.querySelectorAll('*[class*="chat"], *[class*="token"], *[class*="menu"]'));
console.log('All text content:', document.body.textContent);
```

## 📋 Phase 4: Enhancement & Polish (1-2 hours)

### Step 9: Add Export Integration

```typescript
// Add to extension.ts
const exportCommand = vscode.commands.registerCommand(
    'cursor-token-tracker.exportChat',
    async () => {
        // Try to trigger Cursor's native export
        await vscode.commands.executeCommand('workbench.action.showCommands');
        // Or implement UI automation to click export button
    }
);
```

### Step 10: Add Configuration UI

```typescript
// Add settings command
const settingsCommand = vscode.commands.registerCommand(
    'cursor-token-tracker.openSettings',
    () => {
        vscode.commands.executeCommand('workbench.action.openSettings', 'cursorTokenTracker');
    }
);
```

## 🚀 Quick Start Guide

**Want to start immediately?**

1. **Create new folder**: `cursor-token-tracker`
2. **Copy the code above** into the respective files
3. **Run**: `npm install` and `npm run compile`
4. **Press F5** in VS Code to test
5. **Iterate on token extraction** until it finds Cursor's three-dot menu

The key is **finding the right DOM selector** for Cursor's token display. Once that works, everything else is standard VS Code extension development.

**Start with Step 1-3 to get the basic structure, then focus on Step 5 (token extraction) as that's the core challenge.**
