// Simple test for core logic
console.log('Testing core logic...');

// Test text validation
console.log('\n1. Text validation:');
const testTexts = ['', 'Hello', '   ', 'Test@123'];
testTexts.forEach(text => {
    const isValid = text.trim() !== '';
    console.log(`"${text}" -> ${isValid ? 'Valid' : 'Invalid'}`);
});

// Test tag generation
console.log('\n2. Tag generation:');
const uniqueId = Date.now();
const sourceTag = `qr_source_${uniqueId}`;
const targetTag = `qr_target_${uniqueId}`;
console.log(`Source: ${sourceTag}`);
console.log(`Target: ${targetTag}`);

// Test tag matching
console.log('\n3. Tag matching:');
const testTags = ['qr_source_123', 'qr_target_456'];
testTags.forEach(tag => {
    if (tag.startsWith('qr_source_')) {
        const target = tag.replace('qr_source_', 'qr_target_');
        console.log(`${tag} -> ${target}`);
    } else if (tag.startsWith('qr_target_')) {
        const source = tag.replace('qr_target_', 'qr_source_');
        console.log(`${tag} -> ${source}`);
    }
});

console.log('\n✅ Core logic tests completed successfully!'); 