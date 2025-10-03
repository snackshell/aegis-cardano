"""
Bot module for Aegis Cardano Security Guardian.

This module provides the main bot implementations for Telegram and Discord,
allowing users to interact with the security services through chat interfaces.
"""

from . import telegram
from . import discord

__all__ = ["telegram", "discord"]
