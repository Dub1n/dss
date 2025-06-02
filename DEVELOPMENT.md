# DSS Development Branch

This is the **development branch** for the DSS Template Repository. This branch contains all the development files, personal configurations, and work-in-progress materials that are excluded from the main branch to keep it clean for end users.

## Branch Purpose

- **main branch**: Clean, production-ready template for end users
- **development branch**: Full development environment with all personal files

## Development Files Included

### Personal Configuration
- `.envrc` - Environment configuration
- `.vscode/` - VSCode workspace settings
- `meta/requirements_autoformatter.txt` - Development dependencies

### Development Tasks & Planning
- `meta/development_queue/` - Task planning and roadmaps
- `meta/tasks/` - Individual development tasks
- `meta/benchmark/` - Performance testing and benchmarks

### Scripts & Tools
- All development scripts in `meta/scripts/`
- Debugging and testing utilities
- Repository management tools

### Backups & Archives
- `meta/rules_backup/` - Previous versions of rules
- Development notes and scratch files

## Usage

### Switching Between Branches

```bash
# Work on main (clean) branch
git checkout main

# Work on development (full) branch  
git checkout development
```

### Developing

1. Make changes in `development` branch
2. When ready for users, cherry-pick or merge specific commits to `main`
3. Keep main branch minimal and clean

### Syncing

- Push both branches to GitHub
- Users clone `main` by default
- Developers can access `development` when needed

## Guidelines

- Keep `main` branch focused on end-user experience
- Use `development` for personal workflow and experimentation
- Document any changes that should eventually go to `main`
- Regular sync between branches for shared improvements 