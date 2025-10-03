"""
Telegram bot module for Aegis Cardano Security Guardian.

This module provides the main bot implementation and utilities for
interacting with Telegram users.
"""

from .bot import AegisTelegramBot, get_bot, start_bot, stop_bot

__all__ = ["AegisTelegramBot", "get_bot", "start_bot", "stop_bot"]
