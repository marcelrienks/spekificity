"""lat.md integration module."""
from spekificity.lat_md.install import install_lat
from spekificity.lat_md.index import run_lat_index
from spekificity.lat_md.mcp_config import write_mcp_config
from spekificity.lat_md.git_hook import write_git_hook

__all__ = ["install_lat", "run_lat_index", "write_mcp_config", "write_git_hook"]
