---
tags: [project_management]
provides: [project_todo_list]
requires: []
---

# Project TODO List

This file serves as a running list of tasks, improvements, and ideas identified during development or interaction that should be addressed in the future.

## Tasks

- [ ] Decide if dss-guide.mdc and dss-overview.mdc are both needed and if they can be combined/one removed.
- [ ] Add to the task_decomposition.md to add appropriate (and appropriately placed) subtasks for integrating any developments into the assistant workflow
- [ ] Review all existing TODOs in `meta/TODO.md` and add `(@roadmap: [Section Name])` links where appropriate- [ ] Teach the AI to cross-reference .mdc files with commit messages to refine intent tracking.
- [ ] Set up a daily summary ping (here's what changed today, here's what I learned, here's what we should clarify next).
- [ ] Go over all of this repo's files and make sure they are actually usefully laid out and have the appropriate information: start by filling out the INDEX.md as completely as possible, and work from there
    - [ ] This includes file description stubs and frontmatter, backlinks, etc.
- [ ] Think if there are any other template files that could be useful and make those in the template folder (Created Suggested User Rules template 2024-07-29)
- [ ] Make sure all the scripts work (especially sync_dss_mdc.py)
- [ ] Work out when each of the scripts should be run, manually or scheduled/triggered, and how that can be implemeneted. Should assistant.mdc include running the scripts as part of the LLM's routines/routine checks?
- [ ] Explain when and how to use the python scripts (@roadmap: Meta Scripts & Core Logic)
- [ ] Find an appropriate doc to add instructions for what to do when encountering certain keywords such as TODO or FILL (should they be !TODO and !FILL?) (@roadmap: Documentation (`/docs/`))
- [ ] Create a super-repo for managing and developing DSS that contains this repo in its src as a template (perhaps template ver1?) and git it (@roadmap: Project Infrastructure)
- [ ] Find a way of syncing this up with dss-guide.mdc (ideally an LLM-targeted version)
- [ ] Add a link back from `meta/roadmap.md` to `ROADMAP.md`
- [ ] Explore breaking down other detailed instructions from `assistant.mdc` into separate, linked files (maybe)
- [ ] Test all meta scripts
- [ ] Run convert_to_dss.py to make example DSS repo
- [ ] Review default patterns in meta/dss_config.yml for completeness and accuracy
- [ ] Run DSS on a real repo to see if it works smoothly
- [ ] Add sync_dss_mdc.py to sync Cursor MDC files with their source versions
- [ ] Integrate task decomposition workflow into assistant's core process and update assistant.md to incorporate the Hierarchical Atomic Decomposition (HAD) method (@roadmap: DSS Repo Development Timeline)
- [ ] Update LLM prompt injection to explain task decomposition to LLMs
- [ ] Implement tasks from Phase 1 of DSS Repo Development Timeline following the breakdown in meta/tasks/dss_repo_phase1.md (refer to status tracking and tags for current progress and categorization)
- [ ] Adopt tag conventions from meta/guidelines/tag_conventions.md throughout the project
- [ ] Implement the `update_links.py` script that can automatically generate and update backlinks based on references in files (@roadmap: Documentation Tools)
- [ ] Extend `convert_to_dss.py` to support backlink generation during the conversion process
- [ ] Create a pre-commit hook to verify backlink consistency
- [ ] Develop Obsidian MDC Links plugin as specified in meta/integrations/obsidian_mdc_links_plugin.md (@roadmap: Tool Integration)

## Completed Tasks

- [x] Rework detailed roadmap file (`meta/roadmap.md`) to be organized by topic.
- [x] Create and populate top-level roadmap overview file (`ROADMAP.md`).
- [x] Rework project index file (`INDEX.md`) with detailed file tree and descriptions.
- [x] Update `meta/scripts/convert_to_dss.py` to use the `ignored` patterns loaded from `meta/dss_config.yml`. (@meta/scripts/convert_to_dss.py)
- [x] Review binary file handling in `meta/scripts/convert_to_dss.py` to ensure no attempts are made to read or inject metadata into files matching config `binary` patterns. (@meta/scripts/convert_to_dss.py)
- [x] Improve file classification and handling in `meta/scripts/convert_to_dss.py` for files that don't match standard categories (currently go to `meta/misc`). (@meta/scripts/convert_to_dss.py)
- [x] Investigate and fix the issue where newline characters (`\n`) in `code_edit` parameter are not being correctly interpreted by the apply model, resulting in literal `\n` in output files. (Resolved based on testing 2024-07-26)
- [x] Format `docs/automated_formatting` according to its internal guide. (Completed 2024-07-26)
- [x] Create a detailed roadmap in `meta/roadmap.md` based on the suggested steps. (Completed 2024-07-26)
- [x] Update the `INDEX.md` file with a more detailed project structure overview. (Completed 2024-07-26)
- [x] Create a guide document for updating `INDEX.md` at `docs/how_to_update_index.md`. (Completed 2024-07-26)
- [x] Add a reference to the `INDEX.md` update guide in `.cursor/rules/assistant.mdc`. (Completed 2024-07-26)
- [x] Create the `meta/TODO.md` file. (Completed 2024-07-26)
- [x] Update `.cursor/rules/assistant.mdc` with instructions for managing tasks in `meta/TODO.md`. (Completed 2024-07-26)
- [x] Update `.cursor/rules/assistant.mdc` with instructions to reference `meta/TODO.md` from code comments when relevant. (Completed 2024-07-26)
- [x] Update `.cursor/rules/assistant.mdc` with instructions to verify formatting after file edits. (Completed 2024-07-26)
- [x] Update `.cursor/rules/assistant.mdc` with instructions to update itself when new workflows are established. (Completed 2024-07-26)
- [x] Added frontmatter to files based on `dss_config.yml` (Completed 2024-07-26)
- [x] Add a link back from `meta/roadmap.md` to `ROADMAP.md` (Completed 2024-07-29) 
- [x] Create an INDEX.md template file (Completed 2024-07-29)
- [x] Bootstrap DSS template
- [x] Created backlink conventions documentation and updated relevant files to support bidirectional references
- [x] Renamed `dss_overview.mdc` to `dss-overview.mdc` to comply with Cursor's rule naming requirements
- [x] Implement assistant workflow improvements as defined in [Assistant Workflow Improvement](mdc:meta/tasks/assistant_workflow_improvement.md)
- [x] Decide if folder README.md files should include listings for files in subdirectories or not (Completed: Created policy document at meta/guidelines/folder_readme_policy.md and updated folder README template)
- [x] Update the folder README.md template to specify the inclusion of links to files (Completed: Enhanced policy with linking guidelines, added tags column, and created readme_link_checker.py script)
- [x] Add a way to update the README.md files systematically in case they are not synced up (Completed: Created readme_link_checker.py script that scans READMEs, identifies missing links, and generates assistant prompts)

