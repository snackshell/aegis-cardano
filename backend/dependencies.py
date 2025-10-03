"""
Dependencies for FastAPI endpoints.

This module provides dependency injection functions and utilities
for the FastAPI application.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..core.exceptions import AuthenticationException, AuthorizationException
from ..core.logging import get_logger
from ..services.cardano.blockfrost import BlockfrostService
from ..services.cardano.koios import KoiosService
from ..services.llm.openai import OpenAIService
from ..services.llm.claude import ClaudeService

logger = get_logger("dependencies")

# Security
security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """Get the current user from the authorization token."""
    try:
        # In a real implementation, you would validate the JWT token
        # For now, we'll just return the token as the user ID
        token = credentials.credentials
        
        # Basic token validation
        if not token or len(token) < 10:
            raise AuthenticationException("Invalid token")
        
        logger.info("User authenticated", token_length=len(token))
        return token
        
    except Exception as e:
        logger.error("Authentication failed", error=str(e))
        raise AuthenticationException("Authentication failed")


async def get_api_key(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """Get and validate the API key."""
    try:
        api_key = credentials.credentials
        
        # In a real implementation, you would validate the API key against a database
        # For now, we'll check if it matches the expected format
        if not api_key or not api_key.startswith("aegis_"):
            raise AuthenticationException("Invalid API key format")
        
        logger.info("API key validated", api_key_prefix=api_key[:10])
        return api_key
        
    except Exception as e:
        logger.error("API key validation failed", error=str(e))
        raise AuthenticationException("Invalid API key")


async def get_blockfrost_service() -> BlockfrostService:
    """Get Blockfrost service instance."""
    try:
        service = BlockfrostService()
        
        # Check if service is healthy
        if not await service.health_check():
            logger.warning("Blockfrost service health check failed")
        
        return service
        
    except Exception as e:
        logger.error("Failed to create Blockfrost service", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockfrost service unavailable"
        )


async def get_koios_service() -> KoiosService:
    """Get Koios service instance."""
    try:
        service = KoiosService()
        
        # Check if service is healthy
        if not await service.health_check():
            logger.warning("Koios service health check failed")
        
        return service
        
    except Exception as e:
        logger.error("Failed to create Koios service", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Koios service unavailable"
        )


async def get_openai_service() -> OpenAIService:
    """Get OpenAI service instance."""
    try:
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI service not configured"
            )
        
        service = OpenAIService(api_key=settings.openai_api_key)
        return service
        
    except Exception as e:
        logger.error("Failed to create OpenAI service", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service unavailable"
        )


async def get_claude_service() -> ClaudeService:
    """Get Claude service instance."""
    try:
        if not settings.anthropic_api_key:
            logger.warning("Anthropic API key not configured")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Claude service not configured"
            )
        
        service = ClaudeService(api_key=settings.anthropic_api_key)
        return service
        
    except Exception as e:
        logger.error("Failed to create Claude service", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Claude service unavailable"
        )


# Type aliases for cleaner dependency injection
BlockfrostServiceDep = Annotated[BlockfrostService, Depends(get_blockfrost_service)]
KoiosServiceDep = Annotated[KoiosService, Depends(get_koios_service)]
OpenAIServiceDep = Annotated[OpenAIService, Depends(get_openai_service)]
ClaudeServiceDep = Annotated[ClaudeService, Depends(get_claude_service)]
UserDep = Annotated[str, Depends(get_current_user)]
APIKeyDep = Annotated[str, Depends(get_api_key)]


async def get_primary_cardano_service() -> BlockfrostService | KoiosService:
    """Get the primary Cardano service based on configuration."""
    # For now, we'll prefer Blockfrost if available
    try:
        return await get_blockfrost_service()
    except HTTPException:
        try:
            return await get_koios_service()
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No Cardano service available"
            )


PrimaryCardanoServiceDep = Annotated[BlockfrostService | KoiosService, Depends(get_primary_cardano_service)]
