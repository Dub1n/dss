---
tags: [assistant_guidelines, installation_report, github_submission, feedback]
provides: [installation_report_submission_guidance]
requires: [meta/scripts/dss_bootstrap.py, meta/guidelines/github_issue_labels.md]
---

# Assistant Guidelines: Installation Report Submission

This document provides guidance for the AI assistant on handling the submission of DSS installation reports to GitHub, with a focus on the label validation process.

## Overview

When a user transforms their repository using DSS, an installation report is automatically generated. This report contains valuable feedback that can help improve DSS. The user can submit this report to the DSS GitHub repository with the assistant's help.

## GitHub Issue Submission Process

### Label Validation

The `dss_bootstrap.py` script now includes label validation functionality to prevent errors when submitting issues with non-existent labels. This ensures that only valid labels are included in the GitHub issue creation command.

The validation process:
1. Tries to fetch actual available labels from the DSS repository using GitHub CLI
2. Filters out any proposed labels that don't exist in the repository
3. Only uses valid labels in the GitHub issue creation command
4. Falls back to a safe subset of common labels if GitHub CLI isn't available

This validation prevents errors during issue submission that previously occurred when attempting to use labels that don't exist in the target repository.

For a comprehensive list of all GitHub issue labels used in the DSS project, refer to the [GitHub Issue Label Conventions](mdc:meta/guidelines/github_issue_labels.md) document.

### Automatic Script Generation

The bootstrap process automatically generates two script files:
- `meta/github_issue_command.sh` (Bash script for Unix systems)
- `meta/github_issue_command.ps1` (PowerShell script for Windows)

These scripts handle the GitHub issue creation process with proper error checking.

## Assistant Response Guidelines

When a user asks about submitting installation feedback:

1. **Acknowledge the importance of feedback**: 
   "Thank you for considering submitting feedback! Installation reports help improve DSS for everyone."

2. **Check for report existence**:
   Look for `meta/dss_installation_report.md` and confirm it exists.

3. **Guide the user based on platform**:
   - For Windows: Suggest running the PowerShell script: `meta/github_issue_command.ps1`
   - For macOS/Linux: Suggest running the bash script: `./meta/github_issue_command.sh`

4. **Include prerequisites**:
   Remind the user they need:
   - GitHub CLI installed (`gh`)
   - GitHub CLI authenticated (`gh auth login`)

5. **Offer to summarize the report content**:
   "Would you like me to summarize the key points in your installation report before you submit it?"

6. **Mention label conventions**:
   If the user is interested in the labeling system, direct them to the [GitHub Issue Label Conventions](mdc:meta/guidelines/github_issue_labels.md) document.

## Example Response

```
I'd be happy to help you submit your DSS installation feedback!

I can see your installation report is ready at meta/dss_installation_report.md. This report contains valuable information that will help improve DSS.

To submit this as a GitHub issue:

1. Make sure you have GitHub CLI installed (https://cli.github.com/)
2. Authenticate with: gh auth login
3. Run the submission script:
   - Windows: meta/github_issue_command.ps1
   - macOS/Linux: ./meta/github_issue_command.sh

The script will validate labels and submit your feedback as an issue to the DSS repository. The issue will be tagged with appropriate labels like 'installation-report' and platform/project-specific tags.

Would you like me to summarize the key points in your report before you submit it?
```

## Troubleshooting

If the user encounters label validation errors:
- Explain that the script is working as designed by filtering out invalid labels
- Assure them that the issue will still be created, just without the invalid labels
- Suggest they can manually add labels after submission if necessary
- If they're a repository maintainer, direct them to the [GitHub Issue Label Conventions](mdc:meta/guidelines/github_issue_labels.md) document for commands to create missing labels

If GitHub CLI isn't installed:
- Guide them to download from https://cli.github.com/
- Explain the authentication process with `gh auth login`
- Offer to provide manual submission instructions if they prefer not to install GitHub CLI 

## Related Documentation

- [GitHub Issue Label Conventions](mdc:meta/guidelines/github_issue_labels.md) - Comprehensive guide to DSS GitHub issue labels
- [DSS Bootstrap Script](mdc:meta/scripts/dss_bootstrap.py) - Script that generates installation reports and handles GitHub submission 