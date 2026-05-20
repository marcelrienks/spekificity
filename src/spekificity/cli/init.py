"""
Spekificity initialization command.

Handles post-install setup:
- Install external dependencies (SpecKit, CodeGraph, Obsidian integration)
- Initialize project structure
- Run SpecKit initialization
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import click
from loguru import logger

from spekificity.utils.config import CEL_DIR


def is_tool_available(tool_name: str) -> bool:
    """Check if a tool is available in PATH."""
    result = subprocess.run(
        ["which", tool_name],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def install_tool_via_uv(tool_name: str, package_url: Optional[str] = None) -> bool:
    """Install a tool via uv tool install."""
    try:
        logger.info(f"Installing {tool_name}...")
        
        if package_url:
            cmd = ["uv", "tool", "install", tool_name, "--from", package_url]
        else:
            cmd = ["uv", "tool", "install", tool_name]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            logger.info(f"✓ {tool_name} installed successfully")
            return True
        else:
            logger.warning(f"Failed to install {tool_name}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout installing {tool_name}")
        return False
    except Exception as e:
        logger.warning(f"Error installing {tool_name}: {e}")
        return False


def ensure_celdir() -> None:
    """Ensure .cel directory exists."""
    CEL_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"✓ Created .cel directory at {CEL_DIR}")


def initialize_speckit(cwd: Optional[Path] = None) -> bool:
    """Initialize SpecKit in current directory."""
    try:
        logger.info("Initializing SpecKit...")
        
        if cwd is None:
            cwd = Path.cwd()
        
        # Check if specify is available
        if not is_tool_available("specify"):
            logger.warning("SpecKit (specify) not found. Attempting installation...")
            if not install_tool_via_uv("specify-cli", "git+https://github.com/github/spec-kit.git"):
                logger.warning("Could not install SpecKit. You can install it manually with:")
                logger.warning("  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git")
                return False
        
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
            # Don't fail - SpecKit init might have partial success
            return True
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
    Initialize Spekificity project structure.
    
    This command sets up all necessary components for Spekificity:
    - Creates .cel directory for project-specific data
    - Creates .memories directory for memory persistence
    - Creates wiki directory for documentation
    - Initializes CodeGraph database
    - Initializes SpecKit (if available)
    
    Typically run once after: uv tool install spekificity --from [github-url]
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
