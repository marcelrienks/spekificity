"""
Spekificity initialization command.

Handles project setup:
- Create project directories (.cel, .memories, wiki)
- Initialize CodeGraph database
- Run SpecKit initialization
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import click
from loguru import logger

from spekificity.utils.config import CEL_DIR


def ensure_celdir() -> None:
    """Ensure .cel directory exists."""
    CEL_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"✓ Created .cel directory at {CEL_DIR}")


def initialize_speckit(cwd: Optional[Path] = None) -> bool:
    """
    Initialize SpecKit in current directory.
    
    Runs 'specify init .' to set up SpecKit in the project.
    SpecKit is expected to be pre-installed via 'uv tool install spekificity'.
    """
    try:
        logger.info("Running specify init...")
        
        if cwd is None:
            cwd = Path.cwd()
        
        # Run specify init
        result = subprocess.run(
            ["specify", "init", "."],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        
        if result.returncode == 0:
            logger.info("✓ SpecKit initialized successfully")
            return True
        else:
            logger.warning(f"SpecKit initialization had issues: {result.stderr}")
            # Don't fail entirely - SpecKit init might have partial success
            return True
    except FileNotFoundError:
        logger.error("SpecKit (specify) not found in PATH")
        logger.error("Make sure to install spekificity with: uv tool install spekificity --from [url]")
        logger.error("This installs all dependencies including SpecKit")
        return False
    except subprocess.TimeoutExpired:
        logger.warning("SpecKit initialization timed out")
        return False
    except Exception as e:
        logger.warning(f"Error initializing SpecKit: {e}")
        return False


def initialize_codegraph() -> bool:
    """Initialize CodeGraph database."""
    try:
        logger.info("Initializing CodeGraph...")
        
        # Import locally to avoid hard dependency
        from spekificity.graph.codegraph import CodeGraph
        
        # Create CodeGraph instance (initializes database)
        graph = CodeGraph()
        logger.info(f"✓ CodeGraph initialized at {graph.db_path}")
        return True
    except ImportError:
        logger.warning("CodeGraph module not available. Install with: pip install sqlalchemy")
        return False
    except Exception as e:
        logger.warning(f"Error initializing CodeGraph: {e}")
        return False


def create_memory_structure() -> None:
    """Create memory directory structure."""
    memory_dir = Path.cwd() / ".memories"
    memory_dir.mkdir(exist_ok=True)
    
    session_dir = memory_dir / "session"
    session_dir.mkdir(exist_ok=True)
    
    logger.info(f"✓ Created memory structure in {memory_dir}")


def create_vault_structure() -> None:
    """Create Obsidian vault structure for persistent memory."""
    vault_dir = Path.cwd() / "vault"
    vault_dir.mkdir(exist_ok=True)
    
    lessons_dir = vault_dir / "lessons"
    lessons_dir.mkdir(exist_ok=True)
    
    # Initialize vault files with templates
    patterns_file = vault_dir / "patterns.md"
    if not patterns_file.exists():
        patterns_file.write_text("""# Patterns Library

## [Pattern Name]

**First Used:** spec-[number] (date)  
**Last Used:** spec-[number] (date)  
**Frequency:** used in N features

**Summary:** [1-2 sentence description]

**When to Use:**
- Context: [situations where this pattern applies]
- Benefits: [why use this pattern]

**Implementation:**
[Code example or high-level steps]

---
""")
    
    decision_file = vault_dir / "decision.md"
    if not decision_file.exists():
        decision_file.write_text("""# Decision Index

## [Decision Title]

**Date:** YYYY-MM-DD  
**Feature:** spec-[number]  
**Status:** active | deprecated | superseded-by-[link]

**Context:** Why this decision was needed

**Options Considered:**
- Option A: [description, pros, cons]
- Option B: [description, pros, cons]

**Decision:** [Option chosen] because [rationale]

**Impact:** [affected systems, patterns, future constraints]

---
""")
    
    intention_file = vault_dir / "intention.md"
    if not intention_file.exists():
        intention_file.write_text("""# Project Intention & Vision

## Vision

[Project vision statement]

## Tenets

- [Core tenet 1]
- [Core tenet 2]
- [Core tenet 3]

## Constraints

- [Technical constraint]
- [Organizational constraint]

## Success Criteria

- [Criterion 1]
- [Criterion 2]

---
""")
    
    logger.info(f"✓ Created vault structure in {vault_dir}")


def create_wiki_structure() -> None:
    """Create wiki directory structure if it doesn't exist."""
    wiki_dir = Path.cwd() / "wiki"
    wiki_dir.mkdir(exist_ok=True)
    
    specs_dir = wiki_dir / "specs"
    specs_dir.mkdir(exist_ok=True)
    
    lessons_dir = wiki_dir / "lessons"
    lessons_dir.mkdir(exist_ok=True)
    
    logger.info(f"✓ Created wiki structure in {wiki_dir}")


@click.command()
@click.option(
    "--skip-speckit",
    is_flag=True,
    help="Skip SpecKit initialization",
)
@click.option(
    "--skip-codegraph",
    is_flag=True,
    help="Skip CodeGraph initialization",
)
@click.option(
    "--cwd",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=None,
    help="Directory to initialize (default: current directory)",
)
@click.option(
    "--verbose/--no-verbose",
    "-v/-q",
    default=False,
    help="Verbose output",
)
def execute(
    skip_speckit: bool,
    skip_codegraph: bool,
    cwd: Optional[str],
    verbose: bool,
) -> None:
    """
    Initialize Spekificity project structure and infrastructure.
    
    This command sets up all necessary components for Spekificity:
    - Creates vault/ directory (Obsidian persistent memory)
    - Creates .memories/ directories (session memory)
    - Creates .cel/ directory for project metadata
    - Creates wiki/ directory for documentation
    - Initializes CodeGraph database
    - Runs 'specify init .' to initialize SpecKit
    
    All dependencies including SpecKit are pre-installed via:
    'uv tool install spekificity --from [github-url]'
    
    This command is typically run once after installation to set up project infrastructure.
    """
    work_dir = Path(cwd) if cwd else Path.cwd()
    
    if not verbose:
        logger.remove()
        logger.add(sys.stderr, level="INFO")
    
    click.echo("🚀 Initializing Spekificity project...\n")
    
    try:
        # Step 1: Create directory structures
        logger.info("Setting up directory structures...")
        original_cwd = Path.cwd()
        
        try:
            # Create structures in target directory
            import os
            os.chdir(work_dir)
            
            create_memory_structure()
            create_vault_structure()
            create_wiki_structure()
            ensure_celdir()
            
        finally:
            os.chdir(original_cwd)
        
        # Step 2: Initialize CodeGraph
        if not skip_codegraph:
            logger.info("\nInitializing CodeGraph database...")
            initialize_codegraph()
        
        # Step 3: Initialize SpecKit
        if not skip_speckit:
            logger.info("\nInitializing SpecKit...")
            initialize_speckit(work_dir)
        
        click.echo("\n✅ Spekificity initialization complete!")
        click.echo("\nNext steps:")
        click.echo("  1. Run: spek prepare           (Initialize workspace)")
        click.echo("  2. Run: spek context           (Load project context)")
        click.echo("  3. Run: spek plan [feature]    (Create specification & plan)")
        click.echo("\nFor help, run: spek --help")
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        click.echo(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    execute()
