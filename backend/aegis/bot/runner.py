"""
Bot runner script for Aegis Cardano Security Guardian.

This script starts both Telegram and Discord bots simultaneously,
allowing users to interact with the security services through multiple platforms.
"""

import asyncio
import signal
import sys
from typing import List
import structlog

from aegis.core.config import settings
from aegis.core.logging import get_logger
from aegis.bot.telegram import start_bot as start_telegram_bot, stop_bot as stop_telegram_bot
from aegis.bot.discord import start_bot as start_discord_bot, stop_bot as stop_discord_bot

logger = get_logger("bot_runner")


class BotRunner:
    """Manages and runs multiple bot instances."""
    
    def __init__(self):
        self.telegram_task = None
        self.discord_task = None
        self.running = False
        
    async def start(self) -> None:
        """Start all enabled bots."""
        logger.info("Starting bot runner...")
        
        self.running = True
        
        # Create tasks for each enabled bot
        tasks: List[asyncio.Task] = []
        
        if settings.enable_telegram_bot and settings.telegram_bot_token:
            logger.info("Starting Telegram bot...")
            self.telegram_task = asyncio.create_task(self._run_telegram_bot())
            tasks.append(self.telegram_task)
        else:
            logger.info("Telegram bot is disabled")
            
        if settings.enable_discord_bot and settings.discord_bot_token:
            logger.info("Starting Discord bot...")
            self.discord_task = asyncio.create_task(self._run_discord_bot())
            tasks.append(self.discord_task)
        else:
            logger.info("Discord bot is disabled")
            
        if not tasks:
            logger.error("No bots are enabled. Please check your configuration.")
            return
            
        # Set up signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_event_loop().add_signal_handler(
                sig, lambda: asyncio.create_task(self.stop())
            )
            
        logger.info("All bots started successfully")
        
        # Wait for all tasks to complete (they should run indefinitely)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            logger.info("Bot tasks cancelled")
            
    async def stop(self) -> None:
        """Stop all running bots."""
        logger.info("Stopping bot runner...")
        
        self.running = False
        
        # Cancel all tasks
        if self.telegram_task:
            self.telegram_task.cancel()
            
        if self.discord_task:
            self.discord_task.cancel()
            
        # Stop bots gracefully
        try:
            await stop_telegram_bot()
        except Exception as e:
            logger.error("Error stopping Telegram bot", error=str(e))
            
        try:
            await stop_discord_bot()
        except Exception as e:
            logger.error("Error stopping Discord bot", error=str(e))
            
        logger.info("Bot runner stopped")
        
    async def _run_telegram_bot(self) -> None:
        """Run the Telegram bot."""
        try:
            await start_telegram_bot()
        except asyncio.CancelledError:
            logger.info("Telegram bot task cancelled")
            raise
        except Exception as e:
            logger.error("Telegram bot crashed", error=str(e))
            if self.running:
                # Restart the bot after a delay
                logger.info("Restarting Telegram bot in 30 seconds...")
                await asyncio.sleep(30)
                if self.running:
                    self.telegram_task = asyncio.create_task(self._run_telegram_bot())
                    
    async def _run_discord_bot(self) -> None:
        """Run the Discord bot."""
        try:
            await start_discord_bot()
        except asyncio.CancelledError:
            logger.info("Discord bot task cancelled")
            raise
        except Exception as e:
            logger.error("Discord bot crashed", error=str(e))
            if self.running:
                # Restart the bot after a delay
                logger.info("Restarting Discord bot in 30 seconds...")
                await asyncio.sleep(30)
                if self.running:
                    self.discord_task = asyncio.create_task(self._run_discord_bot())


async def main() -> None:
    """Main entry point for the bot runner."""
    runner = BotRunner()
    
    try:
        await runner.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error("Bot runner failed", error=str(e))
    finally:
        await runner.stop()


if __name__ == "__main__":
    asyncio.run(main())
