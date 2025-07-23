---
tags: [docs, project_management, qr_addin]
provides: [qr_addin_current_state, testing_roadmap]
requires: [debug_word_script, runAutoTests]
status: draft
priority: high
---

# QR-Maker Word Add-in — Current State & Testing Roadmap  

> This document: captures **where the project really stands today**, **which automated checks already exist**, and **exactly what we must do** to achieve repeatable, end-to-end validation from the PowerShell launch script.

---

## 0. TL;DR (Executive Summary)

- The add-in now **loads successfully*- in Word via `tools/debug-word.ps1`.
- A *headless* autotest harness already exists:
  - **`Taskpane.js › runAutoTests()`** — executes a minimal smoke-test inside Word once the task-pane loads.
  - **`tools/local-autotest-server.js`** — collects results at `/results`, logs them, and then **exits with the failure count**.
- **Gap**: the PowerShell launcher does **not** currently wait for that harness to finish nor does it fail the CI step if tests fail.
- **Next step**: Enhance `debug-word.ps1` so that it:
  1. Boots Word *and* injects `?autotest` into the task-pane URL.
  2. Waits for the Node server to terminate and propagates its exit code.
  3. Optionally executes additional Node / Mocha unit tests.

---

## 1. How can the script detect that the add-in has fully loaded?

### Existing hooks

1. **Manifest LaunchEvent** → `onDocumentOpen()` in *Taskpane.js* calls `Office.addin.showAsTaskpane()` and appends `?autotest` (if missing).
2. When the UI is ready `Office.onReady()` fires; `runAutoTests()` executes **after a 1-second delay** and POSTs to `https://localhost:<port>/results`.
3. `local-autotest-server.js` writes `tools/autotest_log.json` and calls `process.exit(failures)`.

### Detection Strategy (no polling required)

- `debug-word.ps1` already holds a reference to the Node process in `$server` and calls `Wait-Process -Id $server.Id`.
- **We simply need to**:
  - Remove the manual *“Press Ctrl-C to stop”* wait loop.
  - After `Wait-Process`, **inspect** `$server.ExitCode` and bubble it up: `exit $server.ExitCode`.

This creates a clean signalling chain:  
Word → JS autotest → Node server **exit code** → PowerShell script → calling shell / CI runner.

---

## 2. Which tests should run?

| Layer | File | Purpose |
|-------|------|---------|
| **Smoke / E2E (Word)** | `Taskpane.js › runAutoTests()` | Validate create & refresh on live document |
| **Browser host (Word Edge WebView2)** | `tests/word/tests.js` (Mocha/Chai) | Assert exported globals & base64 generator |
| **Pure Node** | `tests/run_tests.js` | Sanity-check helper logic that is host-agnostic |

The PowerShell script should invoke **all three tiers** in sequence:

1. **Node unit tests** (`node tests/run_tests.js`)
2. **Browser-in-Word tests** (automatically via `runAutoTests`)
3. **Mocha host tests** — loaded inside task-pane via `<script>` tag when `?autotest` is present (see *Fixes* section).

---

## 3. Do the tests work right now?

| Layer             | Current Behaviour                                                         | Pass/Fail |
|-------------------|---------------------------------------------------------------------------|-----------|
| Node unit tests   | ✅ Pass locally (pure JS, no host deps)                                   | ✅        |
| runAutoTests      | ⚠️ *Untested*; code exists but script doesn’t wait for result             | ❌        |
| Mocha host tests  | ❌ Not executed; `tests/word/tests.js` is never loaded in the task-pane   | ❌        |

---

## 4. Fixes & Script Enhancements

### PowerShell (`tools/debug-word.ps1`)

1. **Introduce `-RunTests` switch** (default `$true`).
2. **After** `$server = Start-Process … -PassThru`, call `Wait-Process -Id $server.Id`.
3. **Propagate exit code**: `exit $server.ExitCode` (CI friendly).

### Task-pane boot sequence

1. **Conditionally load Mocha tests** when `?autotest` is present:

   ```html
   <script src="https://cdnjs.cloudflare.com/ajax/libs/mocha/10.2.0/mocha.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/chai/4.3.7/chai.min.js"></script>
   <script src="tests/word/tests.js"></script>
   ```

2. Make sure `mocha.run()` executes *after* Office is ready.

### Additional smoke checks

Extend `runAutoTests()` to:

- Duplicate & delete a pair.
- Toggle live update and verify automatic QR refresh (can poll for image `src` change).

---

## 5. Is current coverage sufficient?

**No.** Missing critical user flows:

- **Delete & Duplicate** commands
- **Live-update toggle**
- **Shapes API fallback** for platforms without `InsertOnlinePictureFromBase64` (Edge case)
- **Error handling** paths (e.g., no text selected)

---

## 6. How to extend coverage?

1. **Augment `runAutoTests()`** — cheapest path, already runs inside Word with full API surface.
2. **Integrate Mocha in the task-pane** to make assertions explicit rather than log-based.
3. **Snapshot testing** of the document state:
   - Query `ContentControls` and assert count/tags.
   - Compare QR code image `src` before/after edits.
4. **CI Integration**:
   - Use GitHub Actions with `windows-latest`, install Office via O365 test container, run `debug-word.ps1 -RunTests`.
5. **Long-term**: headless testing via the [Office Add-in Automation](https://learn.microsoft.com/office/dev/add-ins/testing/automated-tests) preview; but that’s out-of-scope for MVP.

---

## 7. Next Steps Checklist (for implementation phase)

- [ ] **Update PowerShell script** with exit-code handling and `-RunTests` switch.
- [ ] **Load Mocha + Chai** in `taskpane.html` when `?autotest` flag present.
- [ ] **Refactor `runAutoTests()`** to cover Delete, Duplicate, Live-update.
- [ ] **Add assertion helpers** to convert log-based tests into failures.
- [ ] **Write additional node-level unit tests** for helper functions if needed.
- [ ] **Set up GitHub Action** to run the new script.

> *Once the above is done this document should be moved to `docs/usage/validation_notes.md` and its `status` field set to `active`.*

## 8. Should we adopt `office-addin-mock`?
The newly-discovered Microsoft library provides **node-side mocks of the Office JS APIs** so we can unit-test logic that currently **requires Word**. After review:

**Pros**
1. **Fast feedback loop** – run in seconds on any platform, no Office install.
2. **CI friendly** – avoids O365 licensing headaches for most tests.
3. **Granular assertions** – we can mock `ContentControl` collections and verify tag linkage without manipulating a live document.

**Cons / Limitations**
1. **Partial API coverage** – complex objects like `ContentControlCollection` may not be fully mocked (library docs note missing *Collection types*).
2. **No rendering / timing** – can’t truly verify QR images or floating shape placement.
3. **Learning curve & maintenance** – adds another testing paradigm (mock definitions).

**Recommendation**
* **Yes, adopt it as a **unit-test layer** for functions that don’t rely on Word’s rendering or shape APIs.**
  * Examples: tag-generation helpers, linking logic, error-handling on empty selection, etc.
* **Keep the current in-Word autotest harness for E2E flows** like create-duplicate-delete & live-update which depend on actual Office behavior.

**Implementation sketch**
1. Add `office-addin-mock` as dev dependency.
2. Create `tests/mock/` folder with Jest (or Mocha) suites using mocks.
3. Gradually move logic from `run_tests.js` into proper unit tests, and add new tests for Office interactions.
4. Update CI to run: `npm run test:mock` → `node tests/run_tests.js` → `pwsh tools/debug-word.ps1 -RunTests`.

> In short: **both** layers make sense – mocks for speed and coverage, live Word for true integration confidence.
