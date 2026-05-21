# Lessons Learned from previous Implementations
Below is a list of lessons learnt from previous failed implementations, ensure these lessons are properly specced out in either existing specs, or create new, to ensure that future implementations do not make the same mistakes.

## Lesson 1: various

* Remove all references to, or implementations of old cel. skills, they have been deprecated by this project itself, they should not be a part of this implementation
* Ensure that all skills for this project are prefixed with spek.* and any cli commands use spek as the app name. spek is the official abbreviation of this spekification project.
* I want to use uv as installation tool from my github repo. The act of running this installation will install any dependencies that are not already installed (e.g. Obsidian CLI, codeGraph, Caveman skill, and speckit skills through specify).
* Once I run spek init, this is the function that will provision all infra required for this project to function, as well as call specify init.

---

## Lesson 2: Ensure dependencies

This project initially contained statements that it should be tool agnostic, that was the initial stance. Since then due to research the decisions have been taken to ensure these dependencies are required, and implemented.
* CodeGraph
  * source indexing
  * wiki document indexing
* obsidian for permanent memory store
* Caveman for token reduction 

---

## Lesson 3: Hardcoded Directory Paths and Scattered Constants

### What Went Wrong

**Initial State:**
- Project defined directory paths as scattered global constants throughout `config.py`:
  ```python
  MEMORIES_DIR = Path.home() / ".memories"
  USER_MEMORIES_DIR = MEMORIES_DIR / "user"
  SESSION_MEMORIES_DIR = MEMORIES_DIR / "session"
  REPO_MEMORIES_DIR = MEMORIES_DIR / "repo"
  # ... 5+ additional hardcoded paths
  ```
- Each constant was independently defined and referenced across multiple modules
- No centralization or abstraction layer

**Consequence:**
- When the architecture pivoted to use `vault/` as the persistent store, each reference had to be hunted down and manually updated
- Risk of missed references leading to silent failures
- Future migrations would require similar widespread changes
- Difficult to support multiple storage backends (local, cloud, etc.)

### The Fix Applied

**Consolidated approach:**
- Created a single source of truth: `get_vault_dir()` function
- All path derivations now flow from this single root
- Legacy constants removed entirely
- New functions like `get_obsidian_vault_dir()` centralize path logic

**Corrected Example:**
```python
# Before (bad)
MEMORIES_DIR = Path.home() / ".memories"
USER_MEMORIES_DIR = MEMORIES_DIR / "user"
# ... scattered throughout codebase

# After (good)
def get_vault_dir() -> Path:
    """Single source of truth for vault storage."""
    return Path.cwd() / "vault"

def get_user_vault_dir() -> Path:
    return get_vault_dir() / "user"
```

### Spec Guidance for Future Implementation

**When writing storage-related specs:**
- [ ] Define a **single root storage directory constant** at the architecture level
- [ ] Specify that **all paths derive from this root**, not independently defined
- [ ] Document the path hierarchy explicitly (e.g., `vault/lessons/`, `vault/patterns.md`)
- [ ] Include a function/method signature that all components must use to resolve paths
- [ ] Forbid hardcoding absolute paths except at the root definition point
- [ ] Add validation: "Any spec that defines a new path constant will be rejected"

**Example Spec Language:**
```
3.1.1 Path Resolution (MANDATORY)
- All filesystem paths MUST be derived from get_vault_dir()
- No component may define a new global path constant
- Path resolution MUST go through the config module
- Future backends (S3, Git, etc.) should be swappable at get_vault_dir()
```

---

## Lesson 4: Tight Coupling of Feature States to Legacy Paths

### What Went Wrong

**Initial State:**
- Core system function `get_feature_state_path()` was hardcoded to use `.memories/session/`:
  ```python
  def get_feature_state_path(feature_name: str) -> Path:
      return Path.home() / ".memories" / "session" / f"{feature_name}.yaml"
  ```
- This function was called throughout the memory loading system
- Business logic (what the function does) was intertwined with storage mechanism (where it stores)

**Consequence:**
- When storage migrated to `vault/session/`, the function returned invalid paths
- Functions calling `get_feature_state_path()` silently failed (wrong paths, missing files)
- Difficult to debug: the call site looked correct, but the underlying path was wrong
- Similar issues would occur with any future backend changes

### The Fix Applied

**Separated concerns:**
- Rewrote `get_feature_state_path()` to use the new centralized path resolution
- Made the function explicitly aware of the storage backend at call time
- Added abstraction: "Get the path for feature state in current storage backend"

**Corrected Example:**
```python
# Before (bad) - tightly coupled
def get_feature_state_path(feature_name: str) -> Path:
    return Path.home() / ".memories" / "session" / f"{feature_name}.yaml"

# After (good) - abstracted storage backend
def get_feature_state_path(feature_name: str) -> Path:
    """Get feature state path from current storage backend."""
    session_dir = get_session_memories_dir()  # Delegates to config
    return session_dir / f"{feature_name}.yaml"
```

### Spec Guidance for Future Implementation

**When writing state management specs:**
- [ ] **Separate path construction from business logic** in the spec itself
- [ ] Require that any function returning a file path must first resolve the base directory
- [ ] Specify an abstraction layer: "Feature state resolution MUST NOT hardcode paths"
- [ ] Include this rule: "Changing a storage backend should require changes in exactly one module (config.py)"
- [ ] Require path provider injection or centralized lookup where possible

**Example Spec Language:**
```
4.2 State Path Resolution (MANDATORY ABSTRACTION)
- get_feature_state_path(name) MUST return a path from get_session_memories_dir()
- NOT from hardcoded .memories/ or any other constant
- If a function returns a Path, it MUST first resolve the base directory
- Rationale: This allows swapping storage backends without changing business logic
- Validation: Grep for absolute paths or hardcoded directory names; reject the spec if any are found outside config.py
```

---

## Lesson 5: Underestimating Documentation and Specification Debt

### What Went Wrong

**Initial State:**
- Code changes were relatively contained: ~4-5 files modified, ~10 functions updated
- But documentation changes were massive: 145+ references across specs, markdown, and wiki

**Breakdown of Documentation Debt:**
- 59 references in repo memory specs (old `.memories/repo/` paths)
- 85 references in session memory specs (old `.memories/session/` paths)
- 50+ examples in .md files (getting-started guides, troubleshooting, etc.)
- 30+ cross-references in architecture.md and memory-architecture.md

**Consequence:**
- A 4-file code refactor became a 50+ file documentation refactor
- Manual search-and-replace across 145+ locations was time-consuming and error-prone
- Risk of orphaned references in archived or less-visited docs
- Documentation became out of sync with implementation (major maintainability issue)

### The Fix Applied

**Systematic documentation audit:**
- Grep-searched entire project for old path references
- Updated all wiki/ specs to reference new `vault/` paths
- Updated all examples in .md files
- Verified all cross-references were correct
- Removed legacy reference files entirely

**Example of Scale:**
- Single find-and-replace: 145+ locations
- Files touched: 50+ (specs, guides, examples)
- Manual verification required for each change

### Spec Guidance for Future Implementation

**When writing new specs or system designs:**
- [ ] **Document the impact of path changes upfront** — include a section on "Documentation that depends on this"
- [ ] **Create a specification for documentation structure itself** — don't leave it informal
- [ ] **Use relative paths and abstractions in examples**, not absolute hardcoded values
- [ ] **Include a validation step**: "All examples in documentation MUST be verifiable with grep"
- [ ] **Assume docs debt is 3-5x code debt** for any architectural change
- [ ] **Make internal API paths part of the spec**, not implementation details

**Example Spec Language:**
```
Documentation & Specification Contracts (MANDATORY)
- Any new path/constant introduced must be documented in specs/030-memory-architecture.md
- Documentation debt estimation: All code changes require docs audit for references
- Use abstraction language in examples: "path-to-lessons" not "/memories/repo/lessons"
- Create a reference matrix: Component → Used In (code files, specs, guides)
  * Example: get_session_memories_dir() used in: [5 code files, 12 specs, 8 guides]
- Before approving spec, audit docs for total impact (not just code impact)

Validation Checklist:
- [ ] All internal paths documented in specs
- [ ] All examples verified to exist/work
- [ ] Cross-references in docs checked (dead links = spec rejection)
- [ ] Documentation debt estimated before implementation starts
```

---

## Lesson 6: Overcomplicating Storage Segregation

### What Went Wrong

**Initial State:**
- System used Unix-style hidden directories: `.memories/`
- Assumed users wouldn't browse/edit this directory
- Architecture separated concerns (user, session, repo) but made them inaccessible

**Consequence:**
- Hard to debug: Users can't easily see what the system is storing
- Hard to edit manually: Hidden directories require shell commands to view
- Agent debuggability reduced: No visual inspection possible
- Migration difficult: Hidden, scattered structure made it hard to reason about what to move

**Original Design Assumption:** "Hide system data from users"  
**Actual Problem:** "Users and agents need visibility into system data"

### The Fix Applied

**Switched to visible, standardized format:**
- Moved everything to `vault/` (visible at project root)
- Used Obsidian vault format (standard, human-readable markdown)
- Made all data browseable and manually editable
- Enabled Obsidian integration for visualization

**Consequences of Fix:**
- Data is now directly queryable by agents
- Users can manually edit vault files
- Git commits are meaningful and readable
- Visual exploration (Obsidian graph view) now possible

### Spec Guidance for Future Implementation

**When designing storage/persistence specs:**
- [ ] **Favor visibility and interoperability** over hiding internal data
- [ ] **Prefer human-readable formats** (markdown, YAML, JSON) over binary or opaque formats
- [ ] **Design for Obsidian compatibility** — it's becoming a standard for knowledge graphs
- [ ] **Enable manual editing** — don't lock data in a proprietary format
- [ ] **Make Git diffs meaningful** — users should understand what changed by reading the diff
- [ ] **Document the storage format explicitly** in the spec, not just in code

**Example Spec Language:**
```
Storage & Data Format Requirements (MANDATORY)
- All persistent data MUST be stored in human-readable formats:
  * Markdown (.md) for documents
  * YAML or JSON for structured data
  * NO binary formats
  
- Storage location MUST be visible and accessible:
  * NO hidden directories (no .memories/ prefix)
  * Use vault/ (at project root, visible to users and agents)
  * Users should be able to edit files directly with any editor
  
- Design for Obsidian compatibility:
  * Use [[wikilinks]] for cross-references
  * Follow standard markdown conventions
  * Support frontmatter (YAML) for metadata
  
- Git-friendly:
  * Diffs MUST be human-readable
  * Structure MUST be clear from directory layout
  * File names MUST be descriptive (not hashed or opaque)

Rationale: Visibility enables debugging, manual recovery, and agent transparency.
         Standard formats enable ecosystem integration (Obsidian, Git, etc.)
         Interoperability enables future migrations and tool switching.
```

---

