// Global functions are loaded from Taskpane.js

describe("Word host integration", function() {
  it("should expose createNewPair", function() {
    expect(window.createNewPair).to.be.a("function");
  });

  it("can generate a QR base64 string", function() {
    const dataUri = window.generateQrBase64("Hello World");
    expect(dataUri).to.be.a("string").and.satisfy(s => s.startsWith("data:image/png;base64,"));
  });

  it("generateQrBase64 should create unique data for different strings", function() {
    const hello = window.generateQrBase64("Hello");
    const world = window.generateQrBase64("World");
    expect(hello).to.be.a("string").and.satisfy(s => s.startsWith("data:image/png;base64,"));
    expect(world).to.be.a("string").and.satisfy(s => s.startsWith("data:image/png;base64,"));
    expect(hello).to.not.equal(world);
  });

  it("should expose duplicateSelectedPair and deleteSelectedPair", function() {
    expect(window.duplicateSelectedPair).to.be.a("function");
    expect(window.deleteSelectedPair).to.be.a("function");
  });
}); 