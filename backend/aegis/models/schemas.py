"""
Pydantic models for API requests and responses.

This module defines the data models used by the FastAPI endpoints
for request validation and response formatting.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

from ..services.protocol import (
    AddressInfo,
    AddressReputation,
    AssetInfo,
    AssetVerification,
    TransactionInfo,
    TransactionExplanation,
    LinkAnalysis,
    ServiceStatus,
)


class RiskLevel(str, Enum):
    """Risk level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NetworkType(str, Enum):
    """Cardano network type enumeration."""
    MAINNET = "mainnet"
    PREVIEW = "preview"
    PREPROD = "preprod"


# Request Models

class AddressCheckRequest(BaseModel):
    """Request model for address checking."""
    address: str = Field(..., description="Cardano address to check")
    include_transactions: bool = Field(default=False, description="Include transaction history")
    include_utxos: bool = Field(default=False, description="Include UTXO information")

    @validator('address')
    def validate_address(cls, v):
        """Validate Cardano address format."""
        if not v or not v.startswith('addr'):
            raise ValueError('Invalid Cardano address format')
        if len(v) < 50 or len(v) > 150:
            raise ValueError('Invalid Cardano address length')
        return v


class AssetVerificationRequest(BaseModel):
    """Request model for asset verification."""
    policy_id: str = Field(..., description="Asset policy ID")
    asset_name: Optional[str] = Field(default=None, description="Asset name (optional)")

    @validator('policy_id')
    def validate_policy_id(cls, v):
        """Validate policy ID format."""
        if not v or len(v) != 56:
            raise ValueError('Invalid policy ID length')
        return v


class LinkScanRequest(BaseModel):
    """Request model for link scanning."""
    url: str = Field(..., description="URL to scan for security threats")
    include_content_analysis: bool = Field(default=True, description="Include content analysis")

    @validator('url')
    def validate_url(cls, v):
        """Validate URL format."""
        if not v or not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('URL must start with http:// or https://')
        return v


class TransactionExplanationRequest(BaseModel):
    """Request model for transaction explanation."""
    tx_hash: Optional[str] = Field(default=None, description="Transaction hash")
    tx_cbor: Optional[str] = Field(default=None, description="Transaction CBOR hex")

    @validator('tx_hash')
    def validate_tx_hash(cls, v):
        """Validate transaction hash format."""
        if v and len(v) != 64:
            raise ValueError('Invalid transaction hash length')
        return v

    @validator('tx_cbor')
    def validate_tx_cbor(cls, v):
        """Validate transaction CBOR format."""
        if v and not all(c in '0123456789abcdef' for c in v.lower()):
            raise ValueError('Invalid CBOR hex format')
        return v


class TransactionDecodeRequest(BaseModel):
    """Request model for transaction decoding."""
    tx_cbor: str = Field(..., description="Transaction CBOR hex")

    @validator('tx_cbor')
    def validate_tx_cbor(cls, v):
        """Validate transaction CBOR format."""
        if not v or not all(c in '0123456789abcdef' for c in v.lower()):
            raise ValueError('Invalid CBOR hex format')
        return v


# Response Models

class AddressInfoResponse(BaseModel):
    """Response model for address information."""
    address: str
    balance: Dict[str, int]
    stake_address: Optional[str]
    transaction_count: int
    first_transaction_time: Optional[datetime]
    last_transaction_time: Optional[datetime]
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class AddressReputationResponse(BaseModel):
    """Response model for address reputation."""
    address: str
    reputation_score: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    flags: List[str]
    age_days: Optional[int]
    transaction_count: int
    total_ada_received: int
    total_ada_sent: int
    unique_counterparties: int
    suspicious_patterns: List[str]
    recommendation: str
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class AssetInfoResponse(BaseModel):
    """Response model for asset information."""
    policy_id: str
    asset_name: Optional[str]
    asset_name_hex: Optional[str]
    fingerprint: Optional[str]
    supply: int
    minting_tx_hash: Optional[str]
    metadata: Dict[str, Any]
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class AssetVerificationResponse(BaseModel):
    """Response model for asset verification."""
    policy_id: str
    asset_name: Optional[str]
    is_legitimate: bool
    verification_source: Optional[str]
    confidence_score: float = Field(ge=0.0, le=1.0)
    known_project: Optional[str]
    metadata: Dict[str, Any]
    warnings: List[str]
    recommendation: str
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class TransactionInfoResponse(BaseModel):
    """Response model for transaction information."""
    tx_hash: str
    block_hash: Optional[str]
    block_height: Optional[int]
    slot: Optional[int]
    index: Optional[int]
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    fee: int
    deposit: int
    size: int
    validity_interval_start: Optional[int]
    validity_interval_end: Optional[int]
    included_at: Optional[datetime]
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class TransactionExplanationResponse(BaseModel):
    """Response model for transaction explanation."""
    tx_hash: Optional[str]
    summary: str
    risks: List[str]
    recommendations: List[str]
    fee_analysis: str
    input_output_analysis: str
    contract_interactions: List[str]
    metadata_analysis: str
    overall_assessment: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class LinkAnalysisResponse(BaseModel):
    """Response model for link analysis."""
    url: str
    security_score: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    threats_detected: List[str]
    ssl_info: Dict[str, Any]
    domain_info: Dict[str, Any]
    content_analysis: Dict[str, Any]
    recommendation: str
    analysis_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, Dict[str, Any]]
    uptime_seconds: Optional[float] = None
    environment: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ServiceStatusResponse(BaseModel):
    """Response model for service status."""
    service_name: str
    is_healthy: bool
    response_time_ms: float
    last_checked: datetime
    error_message: Optional[str]
    additional_info: Dict[str, Any]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class APIInfoResponse(BaseModel):
    """Response model for API information."""
    name: str
    version: str
    description: str
    documentation_url: str
    endpoints: List[Dict[str, str]]
    features: List[str]
    supported_networks: List[NetworkType]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class BatchAddressCheckRequest(BaseModel):
    """Request model for batch address checking."""
    addresses: List[str] = Field(..., description="List of addresses to check")
    include_transactions: bool = Field(default=False, description="Include transaction history")

    @validator('addresses')
    def validate_addresses(cls, v):
        """Validate addresses list."""
        if not v or len(v) > 100:
            raise ValueError('Addresses list must contain 1-100 addresses')
        
        for addr in v:
            if not addr or not addr.startswith('addr'):
                raise ValueError('Invalid Cardano address format')
            if len(addr) < 50 or len(addr) > 150:
                raise ValueError('Invalid Cardano address length')
        
        return v


class BatchAddressCheckResponse(BaseModel):
    """Response model for batch address checking."""
    results: List[Dict[str, Any]]
    total_addresses: int
    successful_checks: int
    failed_checks: int
    network: NetworkType
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class StatsResponse(BaseModel):
    """Response model for API statistics."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time_ms: float
    uptime_seconds: float
    endpoints_usage: Dict[str, int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
