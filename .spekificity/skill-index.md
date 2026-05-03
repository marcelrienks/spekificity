# Unified Skill Index

**Generated**: [auto-updated by spek init and spek update]  
**Last Updated**: [timestamp]

Comprehensive index of all AI agent skills available in this spekificity-enabled project. Skills are organized by layer (spekificity custom, speckit, caveman) and namespace.

---

## Spekificity Custom Skills

All spekificity custom skills use the `/spek.*` namespace prefix.

| Skill | Namespace | Location | Description | Version | Status |
|-------|-----------|----------|-------------|---------|--------|
| Context Loader | `/spek.context-load` | `.spekificity/skills/spek.context-load.md` | Load vault context at session start | 1.0.0 | active |
| Codebase Mapper | `/spek.map-codebase` | `.spekificity/skills/spek.map-codebase.md` | Run graphify → obsidian mapping | 1.0.0 | active |
| Lessons Learnt | `/spek.lessons-learnt` | `.spekificity/skills/spek.lessons-learnt.md` | Capture feature lessons to vault | 1.0.0 | active |
| Platform Status | `/spek.status` | `.spekificity/setup-scripts/status.sh` | Check initialization and integration | 1.0.0 | active |

---

## Speckit Skills

All speckit skills use the `/speckit.*` namespace (or no prefix for core commands).

| Skill | Namespace | Location | Description | Version | Status |
|-------|-----------|----------|-------------|---------|--------|
| Specify | `/speckit.specify` | `.github/agents/speckit.specify.md` | Create feature specification | [version] | active |
| Plan | `/speckit.plan` | `.github/agents/speckit.plan.md` | Create implementation plan | [version] | active |
| Tasks | `/speckit.tasks` | `.github/agents/speckit.tasks.md` | Generate implementation tasks | [version] | active |
| Implement | `/speckit.implement` | `.github/agents/speckit.implement.md` | Execute implementation tasks | [version] | active |

---

## Caveman Skill

Caveman mode for token-efficient responses.

| Skill | Namespace | Location | Description | Version | Status |
|-------|-----------|----------|-------------|---------|--------|
| Caveman Mode | `caveman` | [system location] | Ultra-terse response compression | [version] | [active/unavailable] |

---

## Discovery and Invocation

### Spekificity Skills

All spekificity skills are discoverable with `/spek` prefix:

```
/spek.context-load
/spek.map-codebase
/spek.lessons-learnt
/spek.status
```

### Speckit Skills

All speckit skills are discoverable with `/speckit` prefix or direct invocation:

```
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.implement
```

### Caveman Mode

Activate caveman mode for token efficiency:

```
/caveman lite      (for spec/plan work)
/caveman           (for implementation, default full compression)
/caveman ultra     (maximum compression)
```

---

## Adding New Skills

To create a new spekificity custom skill:

1. Create `spek.<name>.md` in `.spekificity/skills/`
2. Follow skill template format (see `.spekificity/guides/skill-development.md`)
3. Run `spek init` to regenerate this index
4. Commit skill file to feature branch

See `.spekificity/guides/skill-development.md` for detailed guidelines.

---

## Configuration

- **Spekificity Skills**: Installed to `.spekificity/skills/` during `spek init`
- **Speckit Skills**: Installed to `.github/agents/` via `specify init` (called by `spek init`)
- **Caveman Skill**: System-level availability; check with `/caveman --version` if available

**Last Sync**: [timestamp]  
**Next Update**: `spek init` or `spek update`
