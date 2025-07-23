const https = require("https");
const express = require("express");
const devCerts = require("office-addin-dev-certs");
const fs = require("fs");
const path = require("path");

(async () => {
  const app = express();
  const port = process.env.PORT ? parseInt(process.env.PORT) : 4201;

  // Serve project files so Word can load taskpane.html etc.
  const rootPath = path.join(__dirname, "../../");
  app.use(express.static(rootPath));

  app.use(express.json({ limit: "2mb" }));

  app.post("/results", (req, res) => {
    try {
      const json = req.query.data ? JSON.parse(decodeURIComponent(req.query.data)) : req.body;
      const logPath = path.join(__dirname, "autotest_log.json");
      fs.writeFileSync(logPath, JSON.stringify(json, null, 2));
      console.log("↪︎ Results saved to", logPath);
      res.sendStatus(200);
      // exit with failure count code
      setTimeout(() => process.exit(json.failures || 0), 500);
    } catch (err) {
      console.error("Failed to process results", err);
      res.sendStatus(500);
      process.exit(1);
    }
  });

  const options = await devCerts.getHttpsServerOptions();
  https.createServer(options, app).listen(port, () => {
    console.log(`📡 Autotest server listening on https://localhost:${port}`);
  });
})(); 