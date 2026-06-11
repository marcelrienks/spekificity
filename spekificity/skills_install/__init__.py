"""Skills installation module."""
from spekificity.skills_install.integrations import get_skills_config, FLAT_INTEGRATIONS, INTEGRATION_SKILLS_DIR, INTEGRATION_MCP_CONFIG
from spekificity.skills_install.copy import copy_skills

__all__ = ["get_skills_config", "copy_skills", "FLAT_INTEGRATIONS", "INTEGRATION_SKILLS_DIR", "INTEGRATION_MCP_CONFIG"]
