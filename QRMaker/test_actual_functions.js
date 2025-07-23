#!/usr/bin/env node

/**
 * Test the ACTUAL functions from Taskpane.js
 * Run with: node test_actual_functions.js
 */

const fs = require('fs');
const vm = require('vm');

// Create a comprehensive mock environment
const mockEnvironment = {
    // Mock DOM
    document: {
        getElementById: (id) => ({
            textContent: '',
            onclick: null,
            onchange: null,
            disabled: false,
            style: {},
            querySelector: () => ({ appendChild: () => {} }),
            appendChild: () => {}
        }),
        addEventListener: () => {},
        createElement: () => ({ 
            appendChild: () => {},
            querySelector: () => ({ appendChild: () => {} })
        }),
        querySelector: () => ({ appendChild: () => {} })
    },
    
    // Mock window
    window: {
        Office: null
    },
    
    // Mock console
    console: console,
    
    // Mock global variables
    global: {},
    isOfficeReady: true,
    
    // Mock Word API
    Word: {
        run: async (callback) => {
            const mockContext = createMockWordContext();
            await callback(mockContext);
        },
        InsertLocation: {
            replace: 'replace',
            end: 'end'
        }
    },
    
    // Mock Office API
    Office: {
        HostType: { Word: 'Word' },
        onReady: () => Promise.resolve({ host: 'Word' })
    },
    
    // Mock QR code library
    QRCode: function(text) {
        this.toDataURL = function() {
            return `data:image/png;base64,mocked_qr_${text}_${Date.now()}`;
        };
    },
    
    // Mock setTimeout
    setTimeout: (callback, delay) => {
        // For testing, execute immediately
        callback();
    }
};

// Global state to track what the real functions actually do
let actualControls = [];
let actualErrors = [];
let actualStatusMessages = [];

function createMockWordContext() {
    return {
        document: {
            body: {
                contentControls: {
                    items: actualControls,
                    insertContentControl: () => {
                        const control = createMockContentControl();
                        actualControls.push(control);
                        return control;
                    }
                },
                insertContentControl: () => {
                    const control = createMockContentControl();
                    actualControls.push(control);
                    return control;
                },
                insertParagraph: () => ({})
            },
            getSelection: () => ({
                text: 'test text',
                contentControls: {
                    items: actualControls.filter(c => c.isSelected)
                },
                getRange: () => ({
                    insertContentControl: () => {
                        const control = createMockContentControl();
                        actualControls.push(control);
                        return control;
                    }
                })
            })
        },
        sync: async () => {
            // Simulate sync
        },
        load: (obj, properties) => {
            // Simulate loading properties
        }
    };
}

function createMockContentControl() {
    return {
        tag: '',
        title: '',
        text: '',
        isSelected: false,
        inlinePictures: {
            items: []
        },
        insertText: function(text, location) {
            this.text = text;
        },
        insertInlinePictureFromBase64: function(base64, location) {
            this.inlinePictures.items.push({
                altTextTitle: '',
                insertPictureFromBase64: function(base64, location) {
                    this.altTextTitle = 'mocked_qr_code';
                }
            });
        },
        delete: function() {
            const index = actualControls.indexOf(this);
            if (index > -1) actualControls.splice(index, 1);
        }
    };
}

// Mock the functions that Taskpane.js calls
function updateStatus(message, isError = false) {
    actualStatusMessages.push({ message, isError });
    console.log(`${isError ? '❌' : 'ℹ️'} ${message}`);
}

function errorHandler(error) {
    actualErrors.push(error);
    console.log(`❌ ERROR: ${error.message || error}`);
}

// Load and execute Taskpane.js in the mock environment
function loadTaskpaneJS() {
    try {
        const taskpaneCode = fs.readFileSync('Taskpane.js', 'utf8');
        
        // Create a context with all the mocks
        const context = vm.createContext({
            ...mockEnvironment,
            updateStatus,
            errorHandler,
            // Add any other functions that Taskpane.js might call
        });
        
        // Execute the code
        vm.runInContext(taskpaneCode, context);
        
        return context;
    } catch (error) {
        console.error('Failed to load Taskpane.js:', error);
        return null;
    }
}

// Test the actual functions
async function testActualFunctions() {
    console.log("🧪 Testing ACTUAL Taskpane.js Functions\n");
    
    const context = loadTaskpaneJS();
    if (!context) {
        console.log("❌ Failed to load Taskpane.js");
        return false;
    }
    
    const tests = [
        {
            name: "createNewPair Function Exists",
            test: () => {
                if (typeof context.createNewPair !== 'function') {
                    throw new Error("createNewPair function not found");
                }
                return "PASS";
            }
        },
        {
            name: "duplicateSelectedPair Function Exists",
            test: () => {
                if (typeof context.duplicateSelectedPair !== 'function') {
                    throw new Error("duplicateSelectedPair function not found");
                }
                return "PASS";
            }
        },
        {
            name: "deleteSelectedPair Function Exists",
            test: () => {
                if (typeof context.deleteSelectedPair !== 'function') {
                    throw new Error("deleteSelectedPair function not found");
                }
                return "PASS";
            }
        },
        {
            name: "generateQrBase64 Function Exists",
            test: () => {
                if (typeof context.generateQrBase64 !== 'function') {
                    throw new Error("generateQrBase64 function not found");
                }
                return "PASS";
            }
        },
        {
            name: "QR Code Generation Works",
            test: async () => {
                const qr = context.generateQrBase64("test");
                if (!qr || !qr.startsWith('data:image/png;base64,')) {
                    throw new Error("QR generation failed");
                }
                return "PASS";
            }
        },
        {
            name: "createNewPair Creates Controls",
            test: async () => {
                // Reset state
                actualControls = [];
                actualErrors = [];
                actualStatusMessages = [];
                
                // Call the actual function
                await context.createNewPair();
                
                // Check if controls were created
                if (actualControls.length === 0) {
                    throw new Error("createNewPair did not create any controls");
                }
                
                // Check for source and target controls
                const sourceControls = actualControls.filter(c => c.tag.startsWith('qr_source_'));
                const targetControls = actualControls.filter(c => c.tag.startsWith('qr_target_'));
                
                if (sourceControls.length === 0) {
                    throw new Error("createNewPair did not create source control");
                }
                
                if (targetControls.length === 0) {
                    throw new Error("createNewPair did not create target control");
                }
                
                return "PASS";
            }
        },
        {
            name: "Error Handling for Empty Selection",
            test: async () => {
                // Reset state
                actualControls = [];
                actualErrors = [];
                actualStatusMessages = [];
                
                // Mock empty selection
                mockEnvironment.Word.run = async (callback) => {
                    const mockContext = {
                        document: {
                            getSelection: () => ({ text: '' }),
                            body: { contentControls: { items: [] } }
                        },
                        sync: async () => {},
                        load: () => {}
                    };
                    await callback(mockContext);
                };
                
                // Call the actual function
                await context.createNewPair();
                
                // Should have error message
                const errorMessages = actualStatusMessages.filter(s => s.isError);
                if (errorMessages.length === 0) {
                    throw new Error("No error message for empty selection");
                }
                
                return "PASS";
            }
        }
    ];
    
    let passed = 0;
    let failed = 0;
    
    for (const testCase of tests) {
        try {
            const result = await testCase.test();
            console.log(`✅ ${testCase.name}: ${result}`);
            passed++;
        } catch (error) {
            console.log(`❌ ${testCase.name}: FAILED`);
            console.log(`   Error: ${error.message}`);
            failed++;
        }
    }
    
    console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
    
    if (failed === 0) {
        console.log("🎉 All actual function tests passed!");
    } else {
        console.log("⚠️  Some tests failed. The add-in has real bugs.");
    }
    
    return failed === 0;
}

// Run the tests
testActualFunctions().then(success => {
    console.log("\n" + "=".repeat(50));
    console.log("FINAL RESULTS");
    console.log("=".repeat(50));

    if (success) {
        console.log("🎉 ACTUAL FUNCTIONS WORK!");
        console.log("💡 The real Taskpane.js functions are working correctly.");
    } else {
        console.log("⚠️  ACTUAL FUNCTIONS HAVE BUGS!");
        console.log("🔧 The tests revealed real issues in the add-in code.");
    }

    process.exit(success ? 0 : 1);
}).catch(error => {
    console.error("Test execution failed:", error);
    process.exit(1);
}); 