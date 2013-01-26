"""mr.bob exceptions module."""


class MrBobError(Exception):
    """Base class for errors"""


class ConfigurationError(MrBobError):
    """Raised during configuration phase"""


class TemplateConfigurationError(ConfigurationError):
    """Raised reading template configuration"""


class ValidationError(MrBobError):
    """Raised during question validation"""


class SkipQuestion(MrBobError):
    """Raised during pre_ask_question if we should skip it"""
