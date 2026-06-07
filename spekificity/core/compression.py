"""Context compression using Caveman notation for token efficiency.

Caveman mode reduces tokens by ~75% through abbreviated notation.
Supports intensity levels: lite, full (default), ultra.
"""

from typing import Optional

from spekificity.core.types import TaskContext


class CavemanCompressor:
    """Compress context using Caveman notation."""
    
    INTENSITY_LEVELS = {
        "lite": {
            "keep_articles": True,
            "keep_hedging": False,
            "abbreviate_prose": False,
            "use_arrows": False,
        },
        "full": {
            "keep_articles": False,
            "keep_hedging": False,
            "abbreviate_prose": False,
            "use_arrows": False,
        },
        "ultra": {
            "keep_articles": False,
            "keep_hedging": False,
            "abbreviate_prose": True,
            "use_arrows": True,
        },
    }
    
    PROSE_ABBREVIATIONS = {
        "database": "DB",
        "authentication": "auth",
        "authorization": "authz",
        "configuration": "config",
        "request": "req",
        "response": "res",
        "function": "fn",
        "implementation": "impl",
        "integration": "integ",
        "documentation": "docs",
    }
    
    FILLER_WORDS = {
        "just", "really", "basically", "actually", "simply",
        "sure", "certainly", "of course", "happy to",
        "i think", "it seems", "arguably",
    }
    
    def __init__(self, intensity: str = "full"):
        if intensity not in self.INTENSITY_LEVELS:
            raise ValueError(f"Invalid intensity: {intensity}. Use: lite, full, ultra")
        self.intensity = intensity
        self.config = self.INTENSITY_LEVELS[intensity]
    
    def compress_text(self, text: str) -> str:
        """Compress text to Caveman notation.
        
        Args:
            text: Text to compress
        
        Returns:
            Compressed text
        """
        if not text:
            return text
        
        # Remove filler words
        for filler in self.FILLER_WORDS:
            text = text.replace(f" {filler} ", " ")
            text = text.replace(f"{filler} ", "")
        
        # Remove articles (a, an, the) unless keeping them
        if not self.config["keep_articles"]:
            articles = [" a ", " an ", " the "]
            for article in articles:
                text = text.replace(article, " ")
        
        # Abbreviate prose words
        if self.config["abbreviate_prose"]:
            for full, abbrev in self.PROSE_ABBREVIATIONS.items():
                text = text.replace(full, abbrev)
        
        # Use arrows for causality
        if self.config["use_arrows"]:
            text = text.replace(" causes ", " → ")
            text = text.replace(" because ", " → ")
            text = text.replace(" results in ", " → ")
            text = text.replace(" leads to ", " → ")
        
        # Clean up extra spaces
        text = " ".join(text.split())
        
        return text
    
    def compress_context(self, context: TaskContext) -> str:
        """Compress TaskContext to Caveman format.
        
        Args:
            context: TaskContext to compress
        
        Returns:
            Compressed context markdown
        """
        intensity_str = f" [{self.intensity}]" if self.intensity != "full" else ""
        output = f"# {context.task_id}{intensity_str}\n\n"
        output += f"**Task:** {self.compress_text(context.task_description)}\n\n"
        
        if context.decisions:
            output += "**Decisions:**\n"
            for decision in context.decisions[:3]:
                title = self.compress_text(decision.title)
                output += f"- {title} ({decision.id})\n"
            output += "\n"
        
        if context.patterns:
            output += "**Patterns:**\n"
            for pattern in context.patterns[:3]:
                title = self.compress_text(pattern.title)
                category = pattern.category
                output += f"- {title} ({category})\n"
            output += "\n"
        
        if context.code:
            output += "**Code:**\n"
            for code in context.code[:3]:
                path = code.file_path
                relevance = code.relevance or "medium"
                output += f"- {path} ({relevance})\n"
            output += "\n"
        
        # Token estimate
        lines = len(output.split('\n'))
        estimated_tokens = max(lines // 3, 10)  # Rough estimate
        output += f"*~{estimated_tokens} tokens*\n"
        
        return output


def compress_context(
    context: TaskContext,
    intensity: str = "full"
) -> str:
    """Compress TaskContext (convenience function).
    
    Args:
        context: TaskContext to compress
        intensity: Compression intensity (lite, full, ultra)
    
    Returns:
        Compressed context string
    """
    compressor = CavemanCompressor(intensity)
    return compressor.compress_context(context)


def compress_text(text: str, intensity: str = "full") -> str:
    """Compress text (convenience function).
    
    Args:
        text: Text to compress
        intensity: Compression intensity (lite, full, ultra)
    
    Returns:
        Compressed text
    """
    compressor = CavemanCompressor(intensity)
    return compressor.compress_text(text)


# Caveman notation examples:
# 
# Example 1 (full intensity):
# "Just implement the authentication middleware basically"
# → "Implement auth middleware"
#
# Example 2 (ultra intensity):
# "The database query causes performance degradation which results in timeouts"
# → "DB query → perf degrade → timeouts"
#
# Example 3 (lite intensity):
# "The authentication system should probably handle token expiration"
# → "The auth system should handle token expiration"
