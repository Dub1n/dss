---
tags: [TODO, tasks, roadmap, overhaul]
provides: []
requires: []
---
# TODOs

## Unsorted

### Not Started

- [ ] Add a coding task
- [ ] Currently the benchmark is specifically testing how well a cusor ruleset meetsDSS, not how well it completes any given task
- [ ] Establish a 'Marker' ruleset so that all of the marking is as unbiased as possible
- [ ] Add the overall token usage count (in or out) to the scores and report: this might be able to be got from a cursor log
- [ ] Add to the rubric deductions to penalise not using docstring for frontmatter in scripts
- [ ] The assistnat does not run the reset_project.py script
- [ ] the rules_store folder needs to be scripted to be added and removed from the .gitignore file

### In Progress

### Complete

- [x] Hide EVALUATE_BENCHMARK.md during tests using same system as marking schemes
- [x] Add automated comparison table that gets updated by reset_project.py script with benchmark results and links to archived rules
- [x] Automation: have reset_project.py automatically move rules folder to rules_store with proper naming conventions (kebab-case: v{counter}_{dd-mm-yy})
- [x] VB stands for Version: Baseline - it is an empty ruleset (documented in comparison table automation)
- [X] Add a table to a file comparing the scores of the different rules with links to the rules folders and the scores/reports,  
and a brief section for each on what is different in that version of the rules and anything of note from its benchmarking. This should  
be appended to/filled in by the assistant at the end of the evaluation phase, ideally it would be scripted to be done by the  
reset_project.py script (ensuring it is non-destructive so that manual changes are never overwritten etc)
- [x] Enhanced rules organization: reset_project.py now handles different rule folder configurations intelligently - wraps loose files,  
renames generic "rules" folders, preserves unique names, and merges results for same rulesets across multiple task runs

## Overhaul

- [ ] Carry out the rework as per the roadmap.md
