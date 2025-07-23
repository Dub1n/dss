const OfficeAddinTestHelpers = require("office-addin-test-helpers");
const { TestServer, defaultPort } = require("office-addin-test-server");
const path = require("path");
const express = require("express");
const { spawnSync, spawn } = require("child_process");

(async () => {
  try {
    // Use built-in simple server from helpers to serve the test page + add-in assets
    const testServer = new TestServer(defaultPort);
    const root = path.join(__dirname, "../../..");
    // Start HTTPS ping/results server
    await testServer.startTestServer();

    // Serve static assets (repo root)
    const expressApp = testServer.m_app; // internal express instance
    expressApp.use(express.static(root));

    const manifestPath = path.join(__dirname, "../../QRMaker/manifest.xml");

    console.log("▶️  Starting Word and sideloading add-in...");
    console.log("▶️  Sideloading manifest via office-addin-dev-settings ...");
    const sideload = spawnSync("npx", ["office-addin-dev-settings", "sideload", "--manifest", manifestPath, "--app", "word"], { stdio: "inherit" });
    if (sideload.status !== 0) {
      throw new Error("Sideload command failed");
    }

    console.log("▶️  Launching Word ...");
    spawn("cmd", ["/c", "start", "", "winword"], { detached: true, stdio: "ignore" });

    // allow Word to load add-in
    await new Promise(res => setTimeout(res, 20000));

    console.log("▶️  Waiting for test results... open Word and load add-in automatically");
    const results = await testServer.getTestResults();
    const errorCount = results.failures || 0;
    console.log("Tests complete – failures:", errorCount);

    // Signal Word to close
    console.log("▶️  Cleaning up – closing Word and removing sideload");
    spawnSync("taskkill", ["/IM", "WINWORD.EXE", "/F"], { stdio: "ignore" });
    spawnSync("npx", ["office-addin-dev-settings", "remove", "--manifest", manifestPath], { stdio: "inherit" });
    await testServer.stopTestServer();

    process.exit(errorCount === 0 ? 0 : 1);
  } catch (err) {
    console.error("🚨 Word automation test failed:", err);
    try { await OfficeAddinTestHelpers.stopWord(); } catch (_) {}
    process.exit(1);
  }
})(); 