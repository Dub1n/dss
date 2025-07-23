// Global functions are loaded from Taskpane.js

describe("Word host integration", function() {
  it("should expose createNewPair", function() {
    expect(window.createNewPair).to.be.a("function");
  });

  it("can generate a QR base64 string", function() {
    const dataUri = window.generateQrBase64("Hello World");
    expect(dataUri).to.be.a("string").and.satisfy(s => s.startsWith("data:image/png;base64,"));
  });
}); 