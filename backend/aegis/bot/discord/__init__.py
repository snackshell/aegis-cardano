"""
Discord bot module for Aegis Cardano Security Guardian.

This module provides the main bot implementation and utilities for
interacting with Discord users.
"""

from .bot import AegisDiscordBot, get_bot, start_bot, stop_bot

__all__ = ["AegisDiscordBot", "get_bot", "start_bot", "stop_bot"]
