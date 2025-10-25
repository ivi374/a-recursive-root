# Workspace Directory

This directory contains active development projects and work-in-progress code.

## Purpose

The `/workspace` directory is the primary location for:
- Current development projects
- Active features being built
- Experimental implementations
- Integration work

## Structure

```
workspace/
├── projects/              # Main project directories
│   ├── core-systems-board/    # Core systems board project
│   └── research-roadmap/      # Research roadmap project
└── experiments/           # Experimental code (if any)
```

## Working in Workspace

### Starting a New Project

1. Create a new directory under `/workspace/projects/`
2. Initialize with proper structure (see `/templates`)
3. Add a project-specific README
4. Configure environment (see `/environment`)

### Best Practices

- **Keep it organized:** Each project should have its own directory
- **Document as you go:** Add README files and inline documentation
- **Use templates:** Start from `/templates` for consistency
- **Test frequently:** Ensure your code works before committing
- **Follow standards:** Adhere to guidelines in [CONTRIBUTING.md](../CONTRIBUTING.md)

## Current Projects

### Core Systems Board

Located in `/workspace/projects/core-systems-board/`

A project focused on core system components and infrastructure.

**Documentation:** See project-specific README in the directory

### Research Roadmap

Located in `/workspace/projects/research-roadmap/`

A project for tracking and managing research initiatives.

**Documentation:** See project-specific README in the directory

## Environment Setup

For environment configuration:
1. Check `/environment` for config templates
2. Use `/containers` for Docker setup
3. Run scripts from `/scripts` for automation
4. Refer to `/docs/technical` for guides

## Related Directories

- **[/ai](../ai/)** - AI agent specifications and prompts
- **[/swarm](../swarm/)** - Orchestration system
- **[/templates](../templates/)** - Project templates
- **[/docs](../docs/)** - Documentation
- **[/tools](../tools/)** - Development utilities

## Questions?

- Check [NAVIGATION.md](../NAVIGATION.md) for finding things
- Read [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines
- See [ARCHITECTURE.md](../ARCHITECTURE.md) for structure

---

**For more information:** See [Repository Navigation Guide](../NAVIGATION.md)
