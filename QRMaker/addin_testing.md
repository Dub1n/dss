Unit testing in Office Add-ins

    02/22/2023

Unit tests check your add-in's functionality without requiring network or service connections, including connections to the Office application. Unit testing server-side code, and client-side code that does not call the Office JavaScript APIs, is the same in Office Add-ins as it is in any web application, so it requires no special documentation. But client-side code that calls the Office JavaScript APIs is challenging to test. To solve these problems, we have created a library to simplify the creation of mock Office objects in unit tests: Office-Addin-Mock. The library makes testing easier in the following ways:

    The Office JavaScript APIs must initialize in a webview control in the context of an Office application (Excel, Word, etc.), so they cannot be loaded in the process in which unit tests run on your development computer. The Office-Addin-Mock library can be imported into your test files, which enables the mocking of Office JavaScript APIs inside the Node.js process in which the tests run.
    The application-specific APIs have load and sync methods that must be called in a particular order relative to other functions and to each other. Moreover, the load method must be called with certain parameters depending on what what properties of Office objects are going to be read in by code later in the function being tested. But unit testing frameworks are inherently stateless, so they cannot keep a record of whether load or sync was called or what parameters were passed to load. The mock objects that you create with the Office-Addin-Mock library have internal state that keeps track of these things. This enables the mock objects to emulate the error behavior of actual Office objects. For example, if the function that is being tested tries to read a property that was not first passed to load, then the test will return an error similar to what Office would return.

The library doesn't depend on the Office JavaScript APIs and it can be used with any JavaScript unit testing framework, such as:

    Jest
    Mocha
    Jasmine

The examples in this article use the Jest framework. There are examples using the Mocha framework at the Office-Addin-Mock home page.
Prerequisites

This article assumes that you are familiar with the basic concepts of unit testing and mocking, including how to create and run test files, and that you have some experience with a unit testing framework.

Tip

If you are working with Visual Studio, we recommend that you read the article Unit testing JavaScript and TypeScript in Visual Studio for some basic information about JavaScript unit testing in Visual Studio and then return to this article.
Install the tool

To install the library, open a command prompt, navigate to the root of your add-in project, and then enter the following command.
command line

npm install office-addin-mock --save-dev

Basic usage

    Your project will have one or more test files. (See the instructions for your test framework and the example test files in Examples below.) Import the library, with either the require or import keyword, to any test file that has a test of a function that calls the Office JavaScript APIs, as shown in the following example.
    JavaScript 

const OfficeAddinMock = require("office-addin-mock");

Import the module that contains the add-in function that you want to test with either the require or import keyword. The following is an example that assumes your test file is in a subfolder of the folder with your add-in's code files.
JavaScript

const myOfficeAddinFeature = require("../my-office-add-in");

Create a data object that has the properties and subproperties that you need to mock to test the function. The following is an example of an object that mocks the Excel Workbook.range.address property and the Workbook.getSelectedRange method. This isn't the final mock object. Think of it as a seed object that is used by OfficeMockObject to create the final mock object.
JavaScript

const mockData = {
  workbook: {
    range: {
      address: "C2:G3",
    },
    getSelectedRange: function () {
      return this.range;
    },
  },
};

Pass the data object to the OfficeMockObject constructor. Note the following about the returned OfficeMockObject object.

    It is a simplified mock of an OfficeExtension.ClientRequestContext object.
    The mock object has all the members of the data object and also has mock implementations of the load and sync methods.
    The mock object will mimic crucial error behavior of the ClientRequestContext object. For example, if the Office API you are testing tries to read a property without first loading the property and calling sync, then the test will fail with an error similar to what would be thrown in production runtime: "Error, property not loaded".

JavaScript

const contextMock = new OfficeAddinMock.OfficeMockObject(mockData);

Note

Full reference documentation for the OfficeMockObject type is at Office-Addin-Mock.

In the syntax of your test framework, add a test of the function. Use the OfficeMockObject object in place of the object that it mocks, in this case the ClientRequestContext object. The following continues the example in Jest. This example test assumes that the add-in function that is being tested is called getSelectedRangeAddress, that it takes a ClientRequestContext object as a parameter, and that it is intended to return the address of the currently selected range. The full example is later in this article.
JavaScript

test("getSelectedRangeAddress should return the address of the range", async function () {
  expect(await getSelectedRangeAddress(contextMock)).toBe("C2:G3");
});

Run the test in accordance with documentation of the test framework and your development tools. Typically, there is a package.json file with a script that executes the test framework. For example, if Jest is the framework, package.json would contain the following:
JSON

"scripts": {
  "test": "jest",
  -- other scripts omitted --  
}

To run the test, enter the following in a command prompt in the root of the project.
command line

    npm test

Examples

The examples in this section use Jest with its default settings. These settings support CommonJS modules. See the Jest documentation for how to configure Jest and Node.js to support ECMAScript modules and to support TypeScript. To run any of these examples, take the following steps.

    Create an Office Add-in project for the appropriate Office host application (for example, Excel or Word). One way to do this quickly is to use the Yeoman generator for Office Add-ins.
    In the root of the project, install Jest.
    Install the office-addin-mock tool.
    Create a file exactly like the first file in the example and add it to the folder that contains the project's other source files, often called \src.
    Create a subfolder to the source file folder and give it an appropriate name, such as \tests.
    Create a file exactly like the test file in the example and add it to the subfolder.
    Add a test script to the package.json file, and then run the test, as described in Basic usage.

Mocking the Office Common APIs

This example assumes an Office Add-in for any host that supports the Office Common APIs (for example, Excel, PowerPoint, or Word). The add-in has one of its features in a file named my-common-api-add-in-feature.js. The following shows the contents of the file. The addHelloWorldText function sets the text "Hello World!" to whatever is currently selected in the document; for example; a range in Word, or a cell in Excel, or a text box in PowerPoint.
JavaScript

const myCommonAPIAddinFeature = {

    addHelloWorldText: async () => {
        const options = { coercionType: Office.CoercionType.Text };
        await Office.context.document.setSelectedDataAsync("Hello World!", options);
    }
}
  
module.exports = myCommonAPIAddinFeature;

The test file, named my-common-api-add-in-feature.test.js is in a subfolder, relative to the location of the add-in code file. The following shows the contents of the file. Note that the top level property is context, an Office.Context object, so the object that is being mocked is the parent of this property: an Office object. Note the following about this code:

    The OfficeMockObject constructor does not add all of the Office enum classes to the mock Office object, so the CoercionType.Text value that is referenced in the add-in method must be added explicitly in the seed object.
    Because the Office JavaScript library isn't loaded in the node process, the Office object that is referenced in the add-in code must be declared and initialized.

JavaScript

const OfficeAddinMock = require("office-addin-mock");
const myCommonAPIAddinFeature = require("../my-common-api-add-in-feature");

// Create the seed mock object.
const mockData = {
    context: {
      document: {
        setSelectedDataAsync: function (data, options) {
          this.data = data;
          this.options = options;
        },
      },
    },
    // Mock the Office.CoercionType enum.
    CoercionType: {
      Text: {},
    },
};
  
// Create the final mock object from the seed object.
const officeMock = new OfficeAddinMock.OfficeMockObject(mockData);

// Create the Office object that is called in the addHelloWorldText function.
global.Office = officeMock;

/* Code that calls the test framework goes below this line. */

// Jest test
test("Text of selection in document should be set to 'Hello World'", async function () {
    await myCommonAPIAddinFeature.addHelloWorldText();
    expect(officeMock.context.document.data).toBe("Hello World!");
});

Mocking the Outlook APIs

Although strictly speaking, the Outlook APIs are part of the Common API model, they have a special architecture that is built around the Mailbox object, so we have provided a distinct example for Outlook. This example assumes an Outlook that has one of its features in a file named my-outlook-add-in-feature.js. The following shows the contents of the file. The addHelloWorldText function sets the text "Hello World!" to whatever is currently selected in the message compose window.
JavaScript

const myOutlookAddinFeature = {

    addHelloWorldText: async () => {
        Office.context.mailbox.item.setSelectedDataAsync("Hello World!");
      }
}

module.exports = myOutlookAddinFeature;

The test file, named my-outlook-add-in-feature.test.js is in a subfolder, relative to the location of the add-in code file. The following shows the contents of the file. Note that the top level property is context, an Office.Context object, so the object that is being mocked is the parent of this property: an Office object. Note the following about this code:

    The host property on the mock object is used internally by the mock library to identify the Office application. It's mandatory for Outlook. It currently serves no purpose for any other Office application.
    Because the Office JavaScript library isn't loaded in the node process, the Office object that is referenced in the add-in code must be declared and initialized.

JavaScript

const OfficeAddinMock = require("office-addin-mock");
const myOutlookAddinFeature = require("../my-outlook-add-in-feature");

// Create the seed mock object.
const mockData = {
  // Identify the host to the mock library (required for Outlook).
  host: "outlook",
  context: {
    mailbox: {
      item: {
          setSelectedDataAsync: function (data) {
          this.data = data;
        },
      },
    },
  },
};
  
// Create the final mock object from the seed object.
const officeMock = new OfficeAddinMock.OfficeMockObject(mockData);

// Create the Office object that is called in the addHelloWorldText function.
global.Office = officeMock;

/* Code that calls the test framework goes below this line. */

// Jest test
test("Text of selection in message should be set to 'Hello World'", async function () {
    await myOutlookAddinFeature.addHelloWorldText();
    expect(officeMock.context.mailbox.item.data).toBe("Hello World!");
});

Mocking the Office application-specific APIs

When you are testing functions that use the application-specific APIs, be sure that you are mocking the right type of object. There are two options:

    Mock a OfficeExtension.ClientRequestObject. Do this when the function that is being tested meets both of the following conditions:
        It doesn't call a Host.run function, such as Excel.run.
        It doesn't reference any other direct property or method of a Host object.

    Mock a Host object, such as Excel or Word. Do this when the preceding option isn't possible.

Examples of both types of tests are in the subsections below.

Note

The Office-Addin-Mock library doesn't currently support mocking collection type objects, which are all the objects in the application-specific APIs that are named on the pattern *Collection, such as WorksheetCollection. We are working hard to add this support to the library.
Mocking a ClientRequestContext object

This example assumes an Excel add-in that has one of its features in a file named my-excel-add-in-feature.js. The following shows the contents of the file. Note that the getSelectedRangeAddress is a helper method called inside the callback that is passed to Excel.run.
JavaScript

const myExcelAddinFeature = {
    
    getSelectedRangeAddress: async (context) => {
        const range = context.workbook.getSelectedRange();      
        range.load("address");

        await context.sync();
      
        return range.address;
    }
}

module.exports = myExcelAddinFeature;

The test file, named my-excel-add-in-feature.test.js is in a subfolder, relative to the location of the add-in code file. The following shows the contents of the file. Note that the top level property is workbook, so the object that is being mocked is the parent of an Excel.Workbook: a ClientRequestContext object.
JavaScript

const OfficeAddinMock = require("office-addin-mock");
const myExcelAddinFeature = require("../my-excel-add-in-feature");

// Create the seed mock object.
const mockData = {
    workbook: {
      range: {
        address: "C2:G3",
      },
      // Mock the Workbook.getSelectedRange method.
      getSelectedRange: function () {
        return this.range;
      },
    },
};

// Create the final mock object from the seed object.
const contextMock = new OfficeAddinMock.OfficeMockObject(mockData);

/* Code that calls the test framework goes below this line. */

// Jest test
test("getSelectedRangeAddress should return address of selected range", async function () {
  expect(await myOfficeAddinFeature.getSelectedRangeAddress(contextMock)).toBe("C2:G3");
});

Mocking a host object

This example assumes a Word add-in that has one of its features in a file named my-word-add-in-feature.js. The following shows the contents of the file.
JavaScript

const myWordAddinFeature = {

  insertBlueParagraph: async () => {
    return Word.run(async (context) => {
      // Insert a paragraph at the end of the document.
      const paragraph = context.document.body.insertParagraph("Hello World", Word.InsertLocation.end);
  
      // Change the font color to blue.
      paragraph.font.color = "blue";
  
      await context.sync();
    });
  }
}

module.exports = myWordAddinFeature;

The test file, named my-word-add-in-feature.test.js is in a subfolder, relative to the location of the add-in code file. The following shows the contents of the file. Note that the top level property is context, a ClientRequestContext object, so the object that is being mocked is the parent of this property: a Word object. Note the following about this code:

    When the OfficeMockObject constructor creates the final mock object, it will ensure that the child ClientRequestContext object has sync and load methods.
    The OfficeMockObject constructor does not add a run function to the mock Word object, so it must be added explicitly in the seed object.
    The OfficeMockObject constructor does not add all of the Word enum classes to the mock Word object, so the InsertLocation.end value that is referenced in the add-in method must be added explicitly in the seed object.
    Because the Office JavaScript library isn't loaded in the node process, the Word object that is referenced in the add-in code must be declared and initialized.

JavaScript

const OfficeAddinMock = require("office-addin-mock");
const myWordAddinFeature = require("../my-word-add-in-feature");

// Create the seed mock object.
const mockData = {
  context: {
    document: {
      body: {
        paragraph: {
          font: {},
        },
        // Mock the Body.insertParagraph method.
        insertParagraph: function (paragraphText, insertLocation) {
          this.paragraph.text = paragraphText;
          this.paragraph.insertLocation = insertLocation;
          return this.paragraph;
        },
      },
    },
  },
  // Mock the Word.InsertLocation enum.
  InsertLocation: {
    end: "end",
  },
  // Mock the Word.run function.
  run: async function(callback) {
    await callback(this.context);
  },
};

// Create the final mock object from the seed object.
const wordMock = new OfficeAddinMock.OfficeMockObject(mockData);

// Define and initialize the Word object that is called in the insertBlueParagraph function.
global.Word = wordMock;

/* Code that calls the test framework goes below this line. */

// Jest test set
describe("Insert blue paragraph at end tests", () => {

  test("color of paragraph", async function () {
    await myWordAddinFeature.insertBlueParagraph();  
    expect(wordMock.context.document.body.paragraph.font.color).toBe("blue");
  });

  test("text of paragraph", async function () {
    await myWordAddinFeature.insertBlueParagraph();
    expect(wordMock.context.document.body.paragraph.text).toBe("Hello World");
  });
})

Note

Full reference documentation for the OfficeMockObject type is at Office-Addin-Mock.
