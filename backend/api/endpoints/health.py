"""
Health check API endpoints.

This module contains endpoints for health checks, service status,
and monitoring functionality.
"""

from typing import Dict, Any
from datetime import datetime
import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ...core.config import settings
from ...core.logging import get_logger, log_api_call
from ...models.schemas import (
    HealthCheckResponse,
    ServiceStatusResponse,
    StatsResponse,
    APIInfoResponse,
    NetworkType,
)
from ...services.cardano.blockfrost import BlockfrostService
from ...services.cardano.koios import KoiosService
from ..dependencies import BlockfrostServiceDep, KoiosServiceDep, APIKeyDep

logger = get_logger("health_endpoints")
router = APIRouter()

# Global startup time
startup_time = time.time()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(api_key: APIKeyDep):
    """Comprehensive health check endpoint."""
    start_time = datetime.utcnow()
    
    try:
        logger.info("Health check requested")
        
        uptime = time.time() - startup_time
        
        # Check service statuses
        services = {}
        
        # Check Blockfrost
        try:
            blockfrost_service = BlockfrostService()
            blockfrost_status = await blockfrost_service.get_service_status()
            services["blockfrost"] = {
                "healthy": blockfrost_status.is_healthy,
                "response_time_ms": blockfrost_status.response_time_ms,
                "error": blockfrost_status.error_message,
                "network": blockfrost_status.additional_info.get("network", "unknown"),
            }
            await blockfrost_service.close()
        except Exception as e:
            services["blockfrost"] = {
                "healthy": False,
                "response_time_ms": 0,
                "error": str(e),
                "network": "unknown",
            }
        
        # Check Koios
        try:
            koios_service = KoiosService()
            koios_status = await koios_service.get_service_status()
            services["koios"] = {
                "healthy": koios_status.is_healthy,
                "response_time_ms": koios_status.response_time_ms,
                "error": koios_status.error_message,
                "network": koios_status.additional_info.get("network", "unknown"),
            }
            await koios_service.close()
        except Exception as e:
            services["koios"] = {
                "healthy": False,
                "response_time_ms": 0,
                "error": str(e),
                "network": "unknown",
            }
        
        # Check database (if configured)
        services["database"] = {
            "healthy": True,  # Placeholder for database health check
            "response_time_ms": 0,
            "error": None,
            "type": "sqlite",
        }
        
        # Check Redis (if configured)
        services["redis"] = {
            "healthy": True,  # Placeholder for Redis health check
            "response_time_ms": 0,
            "error": None,
            "type": "redis",
        }
        
        # Determine overall status
        all_healthy = all(service["healthy"] for service in services.values())
        overall_status = "healthy" if all_healthy else "degraded"
        
        response = HealthCheckResponse(
            status=overall_status,
            timestamp=datetime.utcnow(),
            version=settings.app_version,
            services=services,
            uptime_seconds=uptime,
            environment=settings.environment,
        )
        
        log_api_call(
            logger,
            endpoint="/health",
            method="GET",
            status_code=200,
            duration=(datetime.utcnow() - start_time).total_seconds(),
            user_id=api_key[:10],
        )
        
        return response
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        log_api_call(
            logger,
            endpoint="/health",
            method="GET",
            status_code=500,
            duration=(datetime.utcnow() - start_time).total_seconds(),
            user_id=api_key[:10],
        )
        
        # Return degraded status if health check fails
        return HealthCheckResponse(
            status="degraded",
            timestamp=datetime.utcnow(),
            version=settings.app_version,
            services={"error": str(e)},
            uptime_seconds=time.time() - startup_time,
            environment=settings.environment,
        )


@router.get("/health/services", response_model=Dict[str, ServiceStatusResponse])
async def get_service_statuses(api_key: APIKeyDep):
    """Get detailed status of all services."""
    start_time = datetime.utcnow()
    
    try:
        logger.info("Service statuses requested")
        
        services = {}
        
        # Check Blockfrost
        try:
            blockfrost_service = BlockfrostService()
            blockfrost_status = await blockfrost_service.get_service_status()
            services["blockfrost"] = ServiceStatusResponse(
                service_name=blockfrost_status.service_name,
                is_healthy=blockfrost_status.is_healthy,
                response_time_ms=blockfrost_status.response_time_ms,
                last_checked=blockfrost_status.last_checked,
                error_message=blockfrost_status.error_message,
                additional_info=blockfrost_status.additional_info,
            )
            await blockfrost_service.close()
        except Exception as e:
            services["blockfrost"] = ServiceStatusResponse(
                service_name="blockfrost",
                is_healthy=False,
                response_time_ms=0,
                last_checked=datetime.utcnow(),
                error_message=str(e),
                additional_info={},
            )
        
        # Check Koios
        try:
            koios_service = KoiosService()
            koios_status = await koios_service.get_service_status()
            services["koios"] = ServiceStatusResponse(
                service_name=koios_status.service_name,
                is_healthy=koios_status.is_healthy,
                response_time_ms=koios_status.response_time_ms,
                last_checked=koios_status.last_checked,
                error_message=koios_status.error_message,
                additional_info=koios_status.additional_info,
            )
            await koios_service.close()
        except Exception as e:
            services["koios"] = ServiceStatusResponse(
                service_name="koios",
                is_healthy=False,
                response_time_ms=0,
                last_checked=datetime.utcnow(),
                error_message=str(e),
                additional_info={},
            )
        
        log_api_call(
            logger,
            endpoint="/health/services",
            method="GET",
            status_code=200,
            duration=(datetime.utcnow() - start_time).total_seconds(),
            user_id=api_key[:10],
        )
        
        return services
        
    except Exception as e:
        logger.error("Service statuses check failed", error=str(e))
        log_api_call(
            logger,
            endpoint="/health/services",
            method="GET",
            status_code=500,
            duration=(datetime.utcnow() - start_time).total_seconds(),
            user_id=api_key[:10],
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get service statuses"
        )


@router.get("/health/simple")
async def simple_health_check():
    """Simple health check endpoint for load balancers."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@router.get("/health/ready")
async def readiness_check(api_key: APIKeyDep):
    """Readiness check endpoint."""
    try:
        # Check if essential services are ready
        blockfrost_service = BlockfrostService()
        blockfrost_ready = await blockfrost_service.health_check()
        await blockfrost_service.close()
        
        if blockfrost_ready:
            return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}
        else:
            return {"status": "not_ready", "timestamp": datetime.utcnow().isoformat()}
            
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        return {"status": "not_ready", "timestamp": datetime.utcnow().isoformat()}


@router.get("/health/live")
async def liveness_check():
    """Liveness check endpoint."""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}


@router.get("/stats", response_model=StatsResponse)
async def get_stats(api_key: APIKeyDep):
    """Get API statistics and usage information."""
    start_time = datetime.utcnow()
    
    try:
        logger.info("Stats requested")
        
        # Placeholder stats - in a real implementation, this would come from a database
        stats = StatsResponse(
            total_requests=0,  # Would be tracked in database
            successful_requests=0,
            failed_requests=0,
            average_response_time_ms=0.0,
            uptime_seconds=time.time() - startup_time,
            endpoints_usage={
                "/check_address": 0,
                "/check_address_reputation": 0,
                "/verify_asset": 0,
                "/policy": 0,
                "/explain_tx": 0,
                "/decode_tx": 0,
                "/health": 0,
            },
            timestamp=datetime.utcnow(),
        )
        
        log_api_call(
            logger,
            endpoint="/stats",
            method="GET",
            status_code=200,
            duration=(datetime.utcnow() - start_time).total_seconds(),
            user_id=api_key[:10],
        )
        
        return stats
        
    except Exception as e:
        logger.error("Stats retrieval failed", error=str(e))
        log_api_call(
            logger,
            endpoint="/stats",
            method="GET",
            status_code=500,
            duration=(datetime.utcnow() - start_time).total_seconds(),
            user_id=api_key[:10],
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get stats"
        )
