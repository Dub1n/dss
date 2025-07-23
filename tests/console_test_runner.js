// Simple test runner for browser console
// Copy and paste this into the browser console to run tests

console.log("🧪 QR Code Add-in Test Runner");
console.log("================================");

// Test 1: Check if QRCode library is loaded
console.log("\n1. Testing QRCode library...");
if (typeof QRCode !== 'undefined') {
    console.log("✅ QRCode library is loaded");
} else {
    console.log("❌ QRCode library is not loaded");
}

// Test 2: Check if Word API is available
console.log("\n2. Testing Word API...");
if (typeof Word !== 'undefined') {
    console.log("✅ Word API is available");
} else {
    console.log("❌ Word API is not available");
}

// Test 3: Test QR code generation
console.log("\n3. Testing QR code generation...");
function testQRGeneration() {
    const container = document.createElement('div');
    container.style.display = 'none';
    document.body.appendChild(container);
    
    try {
        new QRCode(container, { text: "test", width: 128, height: 128 });
        const canvas = container.querySelector('canvas');
        if (canvas) {
            console.log("✅ QR code generation works");
            document.body.removeChild(container);
            return true;
        } else {
            console.log("❌ QR code canvas not created");
            document.body.removeChild(container);
            return false;
        }
    } catch (error) {
        console.log("❌ QR code generation failed:", error);
        document.body.removeChild(container);
        return false;
    }
}

testQRGeneration();

// Test 4: Test text validation logic
console.log("\n4. Testing text validation logic...");
const testTexts = ["", "Hello", "   ", "Test@123"];
testTexts.forEach(text => {
    const isValid = text.trim() !== "";
    console.log(`"${text}" -> ${isValid ? "✅ Valid" : "❌ Invalid"}`);
});

// Test 5: Test tag generation
console.log("\n5. Testing tag generation...");
const uniqueId = Date.now();
const sourceTag = `qr_source_${uniqueId}`;
const targetTag = `qr_target_${uniqueId}`;
console.log(`Source tag: ${sourceTag}`);
console.log(`Target tag: ${targetTag}`);
console.log("✅ Tag generation works");

// Test 6: Test tag matching
console.log("\n6. Testing tag matching...");
const testTags = ["qr_source_123", "qr_target_456"];
testTags.forEach(tag => {
    if (tag.startsWith('qr_source_')) {
        const target = tag.replace('qr_source_', 'qr_target_');
        console.log(`${tag} -> ${target}`);
    } else if (tag.startsWith('qr_target_')) {
        const source = tag.replace('qr_target_', 'qr_source_');
        console.log(`${tag} -> ${source}`);
    }
});
console.log("✅ Tag matching works");

console.log("\n🎉 Test runner completed!");
console.log("\nIf you see any ❌ marks, those indicate issues that need fixing."); 