---
tags: [task_breakdown, project_management, word_addin, bugfix]
provides: [word_addin_fix_plan]
requires: [continue_chat.md, Taskpane.js]
status: draft
priority: high
---

# Word Add-in Fix Plan (Version 5.9.0-draft)

This document breaks down the outstanding work needed to restore full functionality of the Word QR code add-in, based on the hand-off summary in `continue_chat.md` (v5.8.0).

## 1. Top-Level Goal

Restore all core features (QR generation, pair creation, error handling, and tests) so that:

- All existing automated tests pass in Node.js mock environment
- The add-in works reliably inside Word
- Version bumps to **6.0.0** with updated documentation

## 2. Phase Overview

| Phase | Objective | Key Outputs | Status |
|-------|-----------|-------------|--------|
| 1 | Fix QR code generation | Working `generateQrBase64`, updated canvas/QRCODE integration, unit tests | [NOT STARTED] |
| 2 | Restore control creation | Working `createNewPair`, correct tagging & IDs, passing tests | [NOT STARTED] |
| 3 | Harden error handling | Robust empty-selection & invalid-state handling, user-friendly messages | [NOT STARTED] |
| 4 | Expand & pass test suite | Mocked canvas, new edge-case tests, CI script updates | [NOT STARTED] |
| 5 | Documentation & release chores | Version bump, CHANGELOG, manifest update, README tweaks | [NOT STARTED] |

## 3. Detailed Task Breakdown

### 3.1 Phase 1 – Fix QR Code Generation `[BLOCKER]`

| # | Task | Input | Output | Owner | Status |
|---|------|-------|--------|-------|--------|
| 1.1 | Investigate `TypeError: canvas.toDataURL` | Taskpane.js L648-672 | Root-cause notes |  | [NOT STARTED] |
| 1.2 | Ensure proper Canvas element creation in Office context | Word API docs | Working canvas instance |  | [NOT STARTED] |
| 1.3 | Replace / patch QR library if incompatible | davidshimjs-qrcodejs | Compatible QR generation code |  | [NOT STARTED] |
| 1.4 | Add try/catch with user-friendly error message | Error handling guideline | Updated function |  | [NOT STARTED] |
| 1.5 | Write unit test for `generateQrBase64` success & failure paths | test_actual_functions.js | Passing tests |  | [NOT STARTED] |

### 3.2 Phase 2 – Restore Control Creation

| # | Task | Input | Output | Status |
|---|------|-------|--------|--------|
| 2.1 | Debug `createNewPair` flow (L333-404) | Failed test logs | Controls created in mock | [NOT STARTED] |
| 2.2 | Validate tag schema & sequential `nextPairId` update | Pair ID logic | Correct tags & IDs | [NOT STARTED] |
| 2.3 | Add Word runtime validation test | Word add-in manual test | Verified controls in document | [NOT STARTED] |

### 3.3 Phase 3 – Harden Error Handling

| # | Task | Description | Status |
|---|------|-------------|--------|
| 3.1 | Implement empty-selection guard | Show toast & abort | [NOT STARTED] |
| 3.2 | Centralise error display util | Reuse across functions | [NOT STARTED] |
| 3.3 | Add tests for error scenarios | test_real_code.js | [NOT STARTED] |

### 3.4 Phase 4 – Expand & Pass Test Suite

| # | Task | Description | Status |
|---|------|-------------|--------|
| 4.1 | Mock Canvas API for Node tests | Jest / custom mock | [NOT STARTED] |
| 4.2 | Add coverage for duplication & deletion | Extend tests | [NOT STARTED] |
| 4.3 | Integrate tests into CI script | Update `tests/run_tests.js` | [NOT STARTED] |

### 3.5 Phase 5 – Documentation & Release

| # | Task | Description | Status |
|---|------|-------------|--------|
| 5.1 | Update version numbers to 6.0.0 | Manifest & docs | [NOT STARTED] |
| 5.2 | Update CHANGELOG with fixes | New section | [NOT STARTED] |
| 5.3 | Refresh README & troubleshooting docs | Add new instructions | [NOT STARTED] |

## 4. Dependencies & Risks

- **Canvas / QR library compatibility** with OfficeJS runtime is unknown – may require polyfill or alternative library.
- **Word API async pitfalls** – ensure `.sync()` calls & context handling are correct.
- **Mock environment gaps** – Node tests may miss Office-only issues; manual testing required.

## 5. Next Actions

1. Spin up development session and begin **Phase 1.1** investigation.
2. After each sub-task, update this document’s tables and commit.
3. Keep automated tests green before moving to next phase.

---

## Referenced By

- [continue_chat.md](mdc:continue_chat.md) – Handoff context
- Will be linked from future changelog & roadmap entries
