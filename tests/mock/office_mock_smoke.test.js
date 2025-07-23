// new file content
const { expect } = require("chai");
const OfficeAddinMock = require("office-addin-mock");

/**
 * Basic smoke-test to ensure OfficeAddinMock works in our repo and
 * provides a foundation for richer unit tests.
 */

describe("OfficeAddinMock basic smoke", function () {
  // Build a minimal mock of Office.context.document
  const mockData = {
    context: {
      document: {
        data: null,
        setSelectedDataAsync: function (str) {
          this.data = str;
        },
      },
    },
  };

  // Instantiate the mock Office object
  const officeMock = new OfficeAddinMock.OfficeMockObject(mockData);
  global.Office = officeMock;

  it("setSelectedDataAsync writes data", async function () {
    await Office.context.document.setSelectedDataAsync("Hello World");
    expect(Office.context.document.data).to.equal("Hello World");
  });
}); 