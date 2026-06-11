"""SpecKit integration module."""
from spekificity.speckit.install import install_speckit
from spekificity.speckit.init import run_specify_init
from spekificity.speckit.config import write_spek_config

__all__ = ["install_speckit", "run_specify_init", "write_spek_config"]
