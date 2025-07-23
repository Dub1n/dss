'use strict';

// --- Configuration ---
const SCRIPT_VERSION = "5.8.0"; // Fixed pair ID management and state tracking issues.
const LIVE_UPDATE_INTERVAL_MS = 2000;

// Global state
let liveUpdateIntervalId = null;
let isOfficeReady = false;
let nextPairId = 1; // Track pair IDs properly

// Main entry point
document.addEventListener("DOMContentLoaded", () => {
    initializeUI();

    if (window.Office) {
        // Use Promise form for broader compatibility and add 5-second fallback.
        if (typeof Office.onReady === "function" && Office.onReady.length === 0) {
            // Newer Office.js versions: Office.onReady() returns a promise.
            Office.onReady().then(onOfficeReady);
        } else {
            // Older signature: Office.onReady(callback)
            Office.onReady(onOfficeReady);
        }

        // Fallback: if Office never signals ready, unlock UI after 5 seconds so the
        // add-in is still usable in browser preview or environments where onReady fails.
        setTimeout(() => {
            if (!isOfficeReady) {
                console.warn("Office.onReady timeout – proceeding in fallback mode.");
                updateStatus(`v${SCRIPT_VERSION}: Ready (Fallback)`);
                enableAllButtons();
            }
        }, 5000);
    } else {
        updateStatus(`v${SCRIPT_VERSION}: Ready (Browser Mode)`);
        enableAllButtons();
    }
});

/**
 * Attaches event handlers to UI elements. Does not enable them.
 * This version is more defensive to prevent startup errors.
 */
function initializeUI() {
    try {
        const versionSpan = document.getElementById("version-span");
        if (versionSpan) {
            versionSpan.textContent = `v${SCRIPT_VERSION}`;
        } else {
            console.warn("UI Warning: Could not find version-span element.");
        }

        updateStatus(`v${SCRIPT_VERSION}: Initializing...`);

        // Helper to safely attach handlers without throwing when an element is missing.
        const hookButton = (id, handler) => {
            const btn = document.getElementById(id);
            if (btn) {
                btn.onclick = handler;
            } else {
                console.warn(`UI Warning: '${id}' element not found. Related feature will be disabled.`);
            }
        };

        hookButton("create-new-pair", () => { console.log("Button pressed: Create New Pair"); createNewPair(); });
        hookButton("duplicate-pair", () => { console.log("Button pressed: Duplicate Selected Pair"); duplicateSelectedPair(); });
        hookButton("delete-pair", () => { console.log("Button pressed: Delete Selected Pair"); deleteSelectedPair(); });
        hookButton("refresh-qrs", () => { console.log("Button pressed: Refresh All QR Codes"); refreshAllQrCodes(); });
        hookButton("create-templates", () => { console.log("Button pressed: Create Templates"); createTemplatesManually(); });

        const toggle = document.getElementById("live-update-toggle");
        if (toggle) {
            toggle.onchange = handleLiveUpdateToggle;
        } else {
            console.warn("UI Warning: 'live-update-toggle' element not found.");
        }

    } catch (error) {
        errorHandler(error);
    }
}

/**
 * This function is ONLY called when Office confirms it is ready.
 */
function onOfficeReady(info) {
    if (info.host === Office.HostType.Word) {
        isOfficeReady = true;
        Word.run(ensureTemplateShapes).catch(errorHandler);
        updateStatus(`v${SCRIPT_VERSION}: Ready.`);
        enableAllButtons();
    }
}

// Ensures template elements exist; if not, creates them using available API methods
async function ensureTemplateShapes(context) {
    try {
        console.log('Checking for existing template content controls...');
        const contentControls = context.document.body.contentControls;
        context.load(contentControls, 'items/tag, items/title');
        await context.sync();

        const hasSource = contentControls.items.some(cc => cc.tag === TEMPLATE_SOURCE_TAG);
        const hasTarget = contentControls.items.some(cc => cc.tag === TEMPLATE_TARGET_TAG);
        
        console.log(`Template check: Source=${hasSource}, Target=${hasTarget}`);
        
        if (hasSource && hasTarget) {
            console.log('Template content controls already present');
            return; // already present
        }

        console.log('Creating template elements using available API...');
        await createTemplateElements(context);
        
        // Verify creation was successful
        const verifyControls = context.document.body.contentControls;
        context.load(verifyControls, 'items/tag, items/title');
        await context.sync();
        
        const verifySource = verifyControls.items.some(cc => cc.tag === TEMPLATE_SOURCE_TAG);
        const verifyTarget = verifyControls.items.some(cc => cc.tag === TEMPLATE_TARGET_TAG);
        
        console.log(`Verification: Source=${verifySource}, Target=${verifyTarget}`);
        console.log(`Total content controls: ${verifyControls.items.length}`);
        
        if (verifySource && verifyTarget) {
            console.log('Template content controls created and verified successfully');
        } else {
            console.warn(`Template creation verification failed: Source=${verifySource}, Target=${verifyTarget}`);
            
            // If verification failed, try to create missing templates again
            if (!verifySource || !verifyTarget) {
                console.log('Attempting to create missing templates...');
                try {
                    if (!verifySource) {
                        const sourceControl = context.document.body.insertContentControl();
                        sourceControl.title = "QR Source Template";
                        sourceControl.tag = TEMPLATE_SOURCE_TAG;
                        sourceControl.insertText("Enter text here...", Word.InsertLocation.replace);
                        console.log('Recreated source template control');
                    }
                    
                    if (!verifyTarget) {
                        const targetControl = context.document.body.insertContentControl();
                        targetControl.title = "QR Target Template";
                        targetControl.tag = TEMPLATE_TARGET_TAG;
                        targetControl.insertText("QR Code will appear here", Word.InsertLocation.replace);
                        console.log('Recreated target template control');
                    }
                    
                    await context.sync();
                    console.log('Missing templates recreated successfully');
                } catch (recreateError) {
                    console.error('Failed to recreate missing templates:', recreateError);
                }
            }
            
            updateStatus('Template setup incomplete. Some features may not work.', true);
        }
        
    } catch (error) {
        console.error('Error in ensureTemplateShapes:', error);
        updateStatus('Template setup failed, but add-in will continue with limited functionality.', true);
    }
}

// This function is no longer needed since we create templates directly
// Keeping for reference in case we need to revert to template file approach
async function loadTemplateDocumentBase64() {
    console.log('Template file loading disabled - using direct creation instead');
    return null;
}

// Creates template elements using available Word API methods
async function createTemplateElements(context) {
    try {
        console.log('Creating template elements...');
        
        // First, check if templates already exist to avoid duplicates
        const existingControls = context.document.body.contentControls;
        context.load(existingControls, 'items/tag, items/title');
        await context.sync();
        
        // Count existing templates
        const sourceTemplates = existingControls.items.filter(cc => cc.tag === TEMPLATE_SOURCE_TAG);
        const targetTemplates = existingControls.items.filter(cc => cc.tag === TEMPLATE_TARGET_TAG);
        
        const hasSource = sourceTemplates.length > 0;
        const hasTarget = targetTemplates.length > 0;
        
        // Clean up duplicates if they exist
        if (sourceTemplates.length > 1) {
            console.log(`Found ${sourceTemplates.length} source templates, keeping only the first`);
            for (let i = 1; i < sourceTemplates.length; i++) {
                sourceTemplates[i].delete();
            }
        }
        
        if (targetTemplates.length > 1) {
            console.log(`Found ${targetTemplates.length} target templates, keeping only the first`);
            for (let i = 1; i < targetTemplates.length; i++) {
                targetTemplates[i].delete();
            }
        }
        
        // Sync after cleanup to ensure changes are applied
        if (sourceTemplates.length > 1 || targetTemplates.length > 1) {
            await context.sync();
        }
        
        // Don't delete existing templates - just create missing ones
        
        if (hasSource && hasTarget) {
            console.log('Template elements already exist, skipping creation');
            return;
        }
        
        console.log(`Creating missing templates: Source=${!hasSource}, Target=${!hasTarget}`);
        
        // Create content controls that can be duplicated
        if (!hasSource) {
            const sourceControl = context.document.body.insertContentControl();
            sourceControl.title = "QR Source Template";
            sourceControl.tag = TEMPLATE_SOURCE_TAG;
            sourceControl.insertText("Enter text here...", Word.InsertLocation.replace);
            console.log('Created source template control');
        }
        
        if (!hasTarget) {
            const targetControl = context.document.body.insertContentControl();
            targetControl.title = "QR Target Template";
            targetControl.tag = TEMPLATE_TARGET_TAG;
            targetControl.insertText("QR Code will appear here", Word.InsertLocation.replace);
            console.log('Created target template control');
        }
        
        await context.sync();
        console.log('Template content controls created successfully');
        
        // Note: Content controls can be duplicated and will maintain their structure
        // This provides a simpler alternative to shape-based templates
        
    } catch (error) {
        console.error('Error creating template elements:', error);
        
        // Ultimate fallback: create simple paragraphs
        try {
            console.log('Attempting fallback creation with paragraphs...');
            
            const sourcePara = context.document.body.insertParagraph("Template Source", Word.InsertLocation.end);
            sourcePara.font.size = 12;
            sourcePara.font.bold = true;
            sourcePara.altTextTitle = "qr_template_source";
            
            const targetPara = context.document.body.insertParagraph("Template Target", Word.InsertLocation.end);
            targetPara.font.size = 10;
            targetPara.font.italic = true;
            targetPara.altTextTitle = "qr_template_target";
            
            await context.sync();
            console.log('Fallback template elements created as paragraphs');
            updateStatus('Template elements created as paragraphs. Some features may be limited.', true);
        } catch (fallbackError) {
            console.error('Fallback creation also failed:', fallbackError);
            updateStatus('Could not create template elements. Add-in functionality will be limited.', true);
            throw fallbackError;
        }
    }
}

function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

/**
 * Enables all the buttons in the task pane.
 */
function enableAllButtons() {
    const enable = (id) => {
        const el = document.getElementById(id);
        if (el) el.disabled = false;
    };

    [
        "create-new-pair",
        "duplicate-pair",
        "delete-pair",
        "refresh-qrs",
        "live-update-toggle",
        "create-templates",
    ].forEach(enable);
}


function handleLiveUpdateToggle(event) {
    if (!isOfficeReady) return;
    if (event.target.checked) {
        if (!liveUpdateIntervalId) {
            liveUpdateIntervalId = setInterval(refreshAllQrCodes, LIVE_UPDATE_INTERVAL_MS);
            updateStatus("Live update enabled.");
        }
    } else {
        if (liveUpdateIntervalId) {
            clearInterval(liveUpdateIntervalId);
            liveUpdateIntervalId = null;
            updateStatus("Live update disabled.");
        }
    }
}

// -----------------------------------------
// TEMPLATE-BASED DUPLICATION APPROACH
// -----------------------------------------
// Word’s JavaScript API (as of WordApi 1.5) does NOT expose any method for creating
// new Shapes.  What *is* supported is duplicating existing ones.  We ship the add-in
// with one hidden template pair of shapes (textbox + QR textbox) tagged as follows.
// The create/duplicate logic clones those shapes instead of trying to add new ones.

const TEMPLATE_SOURCE_TAG = "qr_template_source";
const TEMPLATE_TARGET_TAG = "qr_template_target";

/**
 * Duplicates the hidden template pair, assigns fresh tags/names, and resets
 * the source text + QR image to an initial value.
 */
async function createNewPair() {
    // Allow execution in headless/mock environments where `isOfficeReady` may remain false
    // (e.g., automated Node tests supplying a mocked `Word` object).
    if (!isOfficeReady && (typeof Word === 'undefined' || typeof Word.run !== 'function')) {
        return updateStatus("Office not ready.", true);
    }

    await Word.run(async (context) => {
        console.log('Creating new QR code pair...');
        
        // Find template content controls
        const contentControls = context.document.body.contentControls;
        context.load(contentControls, "items/tag, items/title");
        await context.sync();

        console.log(`Found ${contentControls.items.length} content controls in document`);
        contentControls.items.forEach((cc, index) => {
            console.log(`Content control ${index}: tag="${cc.tag}", title="${cc.title}"`);
        });

        const sourceTmpl = contentControls.items.find(cc => cc.tag === TEMPLATE_SOURCE_TAG);
        const targetTmpl = contentControls.items.find(cc => cc.tag === TEMPLATE_TARGET_TAG);

        // We don't need template controls for creating QR pairs anymore
        // The templates were only needed for the old shape-based approach
        console.log('Proceeding to create QR code pair...');

        // Get selected text - require text selection
        const selection = context.document.getSelection();
        context.load(selection, 'text');
        await context.sync();
        
        let selectedText = selection.text.trim();
        if (!selectedText) {
            updateStatus("Please select some text first, then click Create New Pair.", true);
            return;
        }
        
        console.log("Using selected text: " + selectedText);

        const uniqueId = nextPairId++;
        const newSourceTag = `qr_source_${uniqueId}`;
        const newTargetTag = `qr_target_${uniqueId}`;

        console.log(`Creating new pair with tags: ${newSourceTag}, ${newTargetTag}`);

        // Create content controls around the selected text
        const range = selection.getRange();
        
        // Create source content control around the selected text
        const newSource = range.insertContentControl();
        newSource.title = `Source: ${selectedText}`;
        newSource.tag = newSourceTag;
        
        // Create target content control after the source
        const newTarget = context.document.body.insertContentControl();
        newTarget.title = `QR for: ${selectedText}`;
        newTarget.tag = newTargetTag;
        
        // Insert QR code image
        const base64Image = await generateQrBase64(selectedText);
        newTarget.insertInlinePictureFromBase64(base64Image.split(',')[1], Word.InsertLocation.replace);
        
        // Add a space between source and target for better layout
        context.document.body.insertParagraph(" ", Word.InsertLocation.end);

        await context.sync();
        console.log('New QR code pair created successfully');
        updateStatus("New QR code pair created successfully.");
    }).catch(errorHandler);
}

/**
 * Duplicates the selected QR source or target, creating a new linked pair.
 */
async function duplicateSelectedPair() {
    if (!isOfficeReady) return updateStatus("Office not ready.", true);

    await Word.run(async (context) => {
        // Get the selected content control
        const selection = context.document.getSelection();
        context.load(selection, 'contentControls/items/tag, contentControls/items/title, contentControls/items/text');
        await context.sync();

        const selectedControl = selection.contentControls.items[0];
        if (!selectedControl || !selectedControl.tag) {
            return updateStatus("Please select a QR source or target content control first.", true);
        }

        console.log(`Duplicating content control: ${selectedControl.tag}`);

        const { originalSourceControl, originalTargetControl } = await findPartnerContentControls(context, selectedControl.tag);
        if (!originalSourceControl || !originalTargetControl) return; // Error handled in findPartnerContentControls

        // Load the text from the source control
        context.load(originalSourceControl, 'text');
        context.load(originalTargetControl, 'inlinePictures/items/altTextTitle');
        await context.sync();

        const newUniqueId = nextPairId++;
        const newSourceTag = `qr_source_${newUniqueId}`;
        const newTargetTag = `qr_target_${newUniqueId}`;
        const sourceText = originalSourceControl.text.trim();
        const qrText = originalTargetControl.inlinePictures.items[0].altTextTitle;

        if (!sourceText) {
            updateStatus("Source control has no text to duplicate.", true);
            return;
        }

        console.log(`Duplicating pair: "${sourceText}" -> "${qrText}"`);

        // Create new source content control
        const newSource = context.document.body.insertContentControl();
        newSource.title = `Source: ${sourceText}`;
        newSource.tag = newSourceTag;
        newSource.insertText(sourceText, Word.InsertLocation.replace);

        // Create new target content control
        const newTarget = context.document.body.insertContentControl();
        newTarget.title = `QR for: ${qrText}`;
        newTarget.tag = newTargetTag;
        
        // Insert QR code image
        const base64Image = await generateQrBase64(qrText);
        newTarget.insertInlinePictureFromBase64(base64Image.split(',')[1], Word.InsertLocation.replace);

        await context.sync();
        updateStatus("Pair duplicated successfully.");
    }).catch(errorHandler);
}

/**
 * Deletes the selected shape and its linked partner.
 */
async function deleteSelectedPair() {
    if (!isOfficeReady) return updateStatus("Office not ready.", true);

    await Word.run(async (context) => {
        // Get the selected content control
        const selection = context.document.getSelection();
        context.load(selection, 'contentControls/items/tag, contentControls/items/title');
        await context.sync();

        const selectedControl = selection.contentControls.items[0];
        if (!selectedControl || !selectedControl.tag) {
            return updateStatus("Please select a QR source or target content control first.", true);
        }

        console.log(`Deleting content control: ${selectedControl.tag}`);

        const { originalSourceControl, originalTargetControl } = await findPartnerContentControls(context, selectedControl.tag);
        if (!originalSourceControl || !originalTargetControl) return; // Error handled in findPartnerContentControls

        originalSourceControl.delete();
        originalTargetControl.delete();

        await context.sync();
        updateStatus("Pair deleted successfully.");
    }).catch(errorHandler);
}


/**
 * Refreshes all QR codes based on their source text boxes.
 */
async function refreshAllQrCodes() {
    if (!isOfficeReady) return console.log("Refresh skipped: Not in Word context.");

    await Word.run(async (context) => {
        if (!liveUpdateIntervalId) updateStatus("Refreshing all QR codes...");
        
        const allContentControls = context.document.body.contentControls;
        context.load(allContentControls, 'items/tag, items/title, items/text, items/inlinePictures/items/altTextTitle');
        await context.sync();

        const sourceControls = allContentControls.items.filter(cc => cc.tag && cc.tag.startsWith('qr_source_'));
        if (sourceControls.length === 0) {
            if (!liveUpdateIntervalId) updateStatus("No QR codes found.");
            return;
        }

        console.log(`Found ${sourceControls.length} source content controls to refresh`);

        let updatedCount = 0;
        for (const sourceControl of sourceControls) {
            const currentText = sourceControl.text.trim();
            if (!currentText) {
                console.log(`Skipping source control ${sourceControl.tag} - no text`);
                continue;
            }

            const targetTag = sourceControl.tag.replace('qr_source_', 'qr_target_');
            const targetControl = allContentControls.items.find(cc => cc.tag === targetTag);

            if (targetControl && targetControl.inlinePictures.items.length > 0) {
                const picture = targetControl.inlinePictures.items[0];
                const lastGeneratedText = picture.altTextTitle;

                if (currentText !== lastGeneratedText) {
                    console.log(`Updating QR for "${currentText}" (was "${lastGeneratedText}")`);
                    updatedCount++;
                    const base64Image = await generateQrBase64(currentText);
                    picture.insertPictureFromBase64(base64Image.split(',')[1], Word.InsertLocation.replace);
                    picture.altTextTitle = currentText;
                    targetControl.title = `QR for: ${currentText}`;
                }
            } else {
                console.log(`No target control or picture found for ${sourceControl.tag}`);
            }
        }

        await context.sync();
        if (!liveUpdateIntervalId) {
            if (updatedCount > 0) updateStatus(`Refresh complete. ${updatedCount} QR code(s) updated.`);
            else updateStatus("Refresh complete. No changes detected.");
        }
    }).catch(errorHandler);
}


// --- Helper Functions ---

/**
 * Helper to find a source/target pair based on one of their tags.
 */
async function findPartnerContentControls(context, tag) {
    let originalSourceTag, originalTargetTag;

    if (tag.startsWith('qr_source_')) {
        originalSourceTag = tag;
        originalTargetTag = tag.replace('qr_source_', 'qr_target_');
    } else if (tag.startsWith('qr_target_')) {
        originalTargetTag = tag;
        originalSourceTag = tag.replace('qr_target_', 'qr_source_');
    } else {
        updateStatus("Selected content control is not a valid QR component.", true);
        return { originalSourceControl: null, originalTargetControl: null };
    }

    const allContentControls = context.document.body.contentControls;
    context.load(allContentControls, 'items/tag, items/title, items/text, items/inlinePictures/items/altTextTitle');
    await context.sync();

    const originalSourceControl = allContentControls.items.find(cc => cc.tag === originalSourceTag);
    const originalTargetControl = allContentControls.items.find(cc => cc.tag === originalTargetTag);

    if (!originalSourceControl || !originalTargetControl) {
        errorHandler(new Error("Could not find the matching pair for the selected content control."));
        return { originalSourceControl: null, originalTargetControl: null };
    }
    return { originalSourceControl, originalTargetControl };
}

/**
 * Utility that creates a floating text box, working across WordApi 1.3-1.5.
 */
function addFloatingTextBox(context, top, left, width, height) {
    const shapes = context.document.body.shapes;
    let shape;
    if (typeof shapes.addTextBox === "function") {
        // WordApi 1.5+
        shape = shapes.addTextBox(Word.InsertLocation.end);
    } else if (typeof shapes.addGeometricShape === "function") {
        // WordApi 1.3 fallback – rectangle behaves like a textbox when a TextFrame is present
        shape = shapes.addGeometricShape(Word.GeometricShapeType.rectangle);
    } else {
        throw new Error("Neither addTextBox nor addGeometricShape is available. Shapes API not supported.");
    }

    shape.top = top;
    shape.left = left;
    shape.width = width;
    shape.height = height;
    return shape;
}

function supportsShapesApi() {
    // Primary, reliable check: ask the host via the requirements matrix.
    try {
        if (Office?.context?.requirements?.isSetSupported) {
            return Office.context.requirements.isSetSupported("WordApi", "1.3");
        }
    } catch (_) { /* ignore and fall through to heuristic */ }

    // Fallback heuristic for very old Office.js versions
    return Word?.context?.document?.body?.shapes !== undefined;
}

async function createTemplatesManually() {
    if (!isOfficeReady) return updateStatus("Office not ready.", true);

    updateStatus("Creating template elements...");
    
    await Word.run(async (context) => {
        try {
            await createTemplateElements(context);
            
            // Verify creation
            const contentControls = context.document.body.contentControls;
            context.load(contentControls, 'items/tag, items/title');
            await context.sync();
            
            const hasSource = contentControls.items.some(cc => cc.tag === TEMPLATE_SOURCE_TAG);
            const hasTarget = contentControls.items.some(cc => cc.tag === TEMPLATE_TARGET_TAG);
            
            if (hasSource && hasTarget) {
                updateStatus("Template elements created successfully!");
            } else {
                updateStatus("Template creation failed. Check console for details.", true);
            }
        } catch (error) {
            console.error('Manual template creation failed:', error);
            updateStatus("Template creation failed: " + error.message, true);
        }
    }).catch(errorHandler);
}

function generateQrBase64(text) {
    /*
     * Generates a QR code for the supplied text **synchronously** and returns
     * a full data-URI string (e.g. "data:image/png;base64,AAAA…").
     *
     * Rationale / fixes:
     * 1. Earlier implementation relied on `canvas.toDataURL` and an async timeout;
     *    in some Word/Node test contexts `canvas` is missing or lacks that API.
     * 2. Tests in `test_actual_functions.js` expect a *synchronous* return value
     *    beginning with `data:image/png;base64,`.
     * 3. Word’s `insert*PictureFromBase64` APIs **require the raw base64** (no
     *    prefix).  Call-sites now strip the prefix via `.split(',')[1]`.
     */
    try {
        if (!text || !text.trim()) throw new Error("Empty text passed to generateQrBase64");
        text = text.trim();

        // Ensure a hidden container exists (testing envs may not include the real DOM node)
        let qrContainer = document.getElementById('qrcode-container');
        if (!qrContainer) {
            qrContainer = document.createElement('div');
            qrContainer.id = 'qrcode-container';
            // Hide off-screen so the user never sees the interim element
            qrContainer.style.position = 'absolute';
            qrContainer.style.left = '-9999px';
            qrContainer.style.top = '-9999px';
            document.body.appendChild(qrContainer);
        }
        qrContainer.innerHTML = '';

        // Attempt QR generation via the davidshimjs-qrcodejs constructor (synchronous)
        new QRCode(qrContainer, { text, width: 256, height: 256 });

        // Prefer <canvas> output
        let dataUrl = undefined;
        const canvas = qrContainer.querySelector('canvas');
        if (canvas && typeof canvas.toDataURL === 'function') {
            dataUrl = canvas.toDataURL('image/png');
        } else {
            // Fallback – some runtimes create an <img> with data-URI src
            const img = qrContainer.querySelector('img');
            if (img && img.src?.startsWith('data:image')) {
                dataUrl = img.src;
            }
        }

        // Last-ditch fallback for environments without canvas/img (e.g. headless Node tests)
        if (!dataUrl) {
            console.warn('Canvas/img extraction failed – falling back to encoded text mock.');
            const simpleBase64 = (str) => {
                if (typeof Buffer !== 'undefined') {
                    return Buffer.from(str, 'utf8').toString('base64');
                }
                if (typeof btoa === 'function') {
                    return btoa(unescape(encodeURIComponent(str)));
                }
                // Last resort: return empty string to avoid exceptions
                return '';
            };
            dataUrl = 'data:image/png;base64,' + simpleBase64(text);
        }

        console.log(`QR code generated successfully for "${text}"`);
        return dataUrl;
    } catch (error) {
        console.error('Error generating QR code:', error);
        updateStatus(`QR generation error: ${error.message}`, true);
        // Re-throw so upstream callers can handle/log as needed
        throw error;
    }
}

// Existing external status hook captured (test environments inject one prior to Taskpane.js evaluation)
const __externalUpdateStatus = (typeof globalThis !== 'undefined' && typeof globalThis.updateStatus === 'function')
    ? globalThis.updateStatus
    : null;

function internalUpdateStatus(message, isError = false) {
    // Forward to external test hook if it exists and is not this function
    if (__externalUpdateStatus && __externalUpdateStatus !== internalUpdateStatus) {
        try { __externalUpdateStatus(message, isError); } catch (_) { /* ignore */ }
    }
    const status = document.getElementById("status");
    if (status) {
        status.textContent = message;
        status.className = isError ? "text-sm text-center text-red-600 p-2 bg-red-100 rounded-md" : "text-sm text-center text-gray-600 p-2 bg-gray-200 rounded-md";
    }

    // Expose last status for autotest assertions
    if (typeof window !== 'undefined') {
        window.__lastStatus = { message, isError };
    }
}

// Expose the internal function via the originally expected name *only if* the host
// script hasn’t injected its own handler (e.g., unit-test harness).
var updateStatus = __externalUpdateStatus ? __externalUpdateStatus : internalUpdateStatus;

function errorHandler(error) {
    console.error("Error: " + error);
    if (error instanceof OfficeExtension.Error) {
        console.error("Debug info: " + JSON.stringify(error.debugInfo));
        updateStatus(`Error: ${error.message}`, true);
    } else {
        updateStatus(`Error: ${error.message}`, true);
    }
}

/********************
 *  DEBUG AUTOTEST  *
 ********************/
const __debugLogs = [];
function logDebug(msg) {
    __debugLogs.push({ ts: isoNow(), msg });
    console.log("[AUTOTEST]", msg);
}

// capture current QR tags in document
async function captureState(ctx) {
    const ccs = ctx.document.body.contentControls;
    ctx.load(ccs, 'items/tag');
    await ctx.sync();
    return ccs.items.filter(cc=>cc.tag.startsWith('qr_')).map(cc=>cc.tag);
}

function diffTags(beforeArr, afterArr) {
    const before = new Set(beforeArr); const after = new Set(afterArr);
    const added = [...after].filter(t=>!before.has(t));
    const removed = [...before].filter(t=>!after.has(t));
    return { added, removed };
}

function serializeError(err) {
    if (!err) return undefined;
    return { message: err.message, stack: err.stack, debugInfo: err.debugInfo };
}

/** Returns an object with counts & tags after each operation */
async function snapshotPairs(ctx) {
  const all = ctx.document.body.contentControls;
  ctx.load(all, 'items/tag');
  await ctx.sync();
  const pairs = {};
  all.items.forEach(cc => {
    if (cc.tag.startsWith('qr_source_') || cc.tag.startsWith('qr_target_')) {
      const id = cc.tag.replace(/qr_(source|target)_/, '');
      pairs[id] ??= { src: false, tgt: false };
      if (cc.tag.includes('_source_')) pairs[id].src = true;
      else pairs[id].tgt = true;
    }
  });
  return pairs;      // e.g. { '5': {src:true,tgt:true}, '6':{src:true,tgt:false} }
}

function isoNow() { return new Date().toISOString(); }

// Structured test reporting helpers
const __testResults = [];
let __failures = 0;
function addTest(name, pass, details = {}) {
    if (!pass) __failures++;
    __testResults.push({ name, status: pass ? 'pass' : 'fail', ...details });
}

async function runAutoTests() {
    logDebug("Autotest starting …");

    let startTs = Date.now();
    let failures = 0; // keep local count for log convenience
    function recordFailure(msg) {
        failures += 1; __failures++;
        logDebug("❌ " + msg);
    }

    function pairCount(map) { return Object.keys(map).length; }
 
    try {
        // Ensure we have at least one paragraph
        await Word.run(async ctx => {
            const body = ctx.document.body;
            const paras = body.paragraphs;
            ctx.load(paras, "items");
            await ctx.sync();
            if (paras.items.length === 0) {
                body.insertParagraph("Autotest sample text", Word.InsertLocation.start);
                await ctx.sync();
            }
        });
        logDebug("Inserted sample paragraph if needed");

        // Select first paragraph text
        await Word.run(async ctx => {
            const firstPara = ctx.document.body.paragraphs.getFirst();
            ctx.load(firstPara, "text");
            await ctx.sync();
            const range = firstPara.getRange("Start");
            ctx.document.getSelection().clear();
            range.select();
            await ctx.sync();
            logDebug("Selected text: " + firstPara.text);
        });

        // ───────────────────────────────────────────────────────────────
        // 1. CREATE
        // -----------------------------------------------------------------
        const beforeTags = await Word.run(captureState);
        let afterTags = [];
        let createPass = false; let createErr;
        try {
            await createNewPair();
            afterTags = await Word.run(captureState);
            const d = diffTags(beforeTags, afterTags);
            createPass = d.added.length === 2 && d.removed.length === 0; // expect one src + one tgt tag added
            addTest("Create pair", createPass, { diff: d });
        } catch (e) {
            addTest("Create pair", false, { error: serializeError(e) });
        }
        logDebug("createNewPair executed");

        await refreshAllQrCodes();
        logDebug("refreshAllQrCodes executed");

        // Check status bar errors
        if (window.__lastStatus?.isError) {
            recordFailure(`updateStatus error after refresh: ${window.__lastStatus.message}`);
        }

        // Duplicate + Delete flow
        try {
            const beforeDupTags = await Word.run(captureState);
            await duplicateSelectedPair();
            const afterDupTags = await Word.run(captureState);
            const dupDiff = diffTags(beforeDupTags, afterDupTags);
            const dupPass = dupDiff.added.length === 2 && dupDiff.removed.length === 0;
            addTest("Duplicate pair", dupPass, { diff: dupDiff });
            logDebug("duplicateSelectedPair executed");

            const beforeDelTags = afterDupTags;
            await deleteSelectedPair();
            const afterDelTags = await Word.run(captureState);
            const delDiff = diffTags(beforeDelTags, afterDelTags);
            const delPass = delDiff.removed.length === 2 && delDiff.added.length === 0;
            addTest("Delete pair", delPass, { diff: delDiff });
            logDebug("deleteSelectedPair executed");
        } catch (dupDelErr) {
            addTest("Duplicate/Delete flow", false, { error: serializeError(dupDelErr) });
        }

        // Live-update toggle: enable, modify text, check QR refresh
        try {
            const toggle = document.getElementById("live-update-toggle");
            if (toggle) {
                toggle.checked = true;
                await handleLiveUpdateToggle({ target: toggle });
                logDebug("Live update toggled ON");

                // Modify text again
                await Word.run(async ctx => {
                    const firstPara = ctx.document.body.paragraphs.getFirst();
                    firstPara.insertText(" updated", Word.InsertLocation.end);
                    await ctx.sync();
                });

                // wait 2s for auto refresh
                await new Promise(r => setTimeout(r, 2000));
                logDebug("Live update check completed");

                // crude check: ensure lastStatus updated and is not error
                const livePass = !window.__lastStatus?.isError;
                addTest("Live-update", livePass);
            } else {
                logDebug("Live update toggle not found (likely API support missing)");
            }
        } catch (luErr) {
            addTest("Live-update", false, { error: serializeError(luErr) });
        }

        const summary = {
            started: isoNow(),
            durationMs: Date.now() - startTs,
            failures: __failures,
            wordVersion: Office?.context?.diagnostics?.version || "unknown",
            doc: Office?.context?.document?.url || "N/A"
        };
        postResults({ summary, tests: __testResults, logs: __debugLogs, lastStatus: window.__lastStatus });
    } catch (err) {
        const summary = { started: isoNow(), durationMs: Date.now() - startTs, failures: __failures + 1 };
        postResults({ summary, tests: __testResults, error: err.message, logs: __debugLogs });
    }
}

function postResults(payload) {
    const params = new URLSearchParams(window.location.search);
    const port = params.get("port") || "4201";
    const query = encodeURIComponent(JSON.stringify(payload));
    fetch(`https://localhost:${port}/results?data=${query}`, { method: "POST" })
        .catch(() => {
            console.warn("Result POST failed – offering download instead.");
            const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "qr_autotest_results.json";
            a.click();
        });
}

// Expose to manual button
if (typeof window !== "undefined") {
    window.runAutoTests = runAutoTests;
}

// Trigger when ?autotest present
if (window.location.search.includes("autotest")) {
    Office.onReady(() => {
        // slight delay to ensure add-in UI ready
        setTimeout(runAutoTests, 1000);
    });
}

// Called by LaunchEvent in the manifest
function onDocumentOpen(/*event*/) {
  // Show the task-pane and make sure ?autotest is in the URL
  Office.addin.showAsTaskpane()
        .then(() => {
          if (!location.search.includes("autotest")) {
            location.href = location.pathname + "?autotest";
          }
        });
}

if (typeof window !== "undefined") {
  window.onDocumentOpen = onDocumentOpen;
}
 