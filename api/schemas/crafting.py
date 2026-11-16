"""Crafting Pydantic schemas for API endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class QualityCalculation(BaseModel):
    """Result of a quality calculation."""
    
    base_quality: float = Field(
        ge=0,
        le=1,
        description="Base quality score (quality_selector / 1000, range 0-1)",
    )
    resource_qualities: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-resource quality scores (0-1000 range)",
    )
    resource_weights: Dict[str, float] = Field(
        default_factory=dict,
        description="Per-resource weight/count contributing to final quality",
    )
    final_quality: float = Field(
        ge=0,
        le=1,
        description="Final adjusted quality after resource contributions",
    )


class ResourceRequirement(BaseModel):
    """Input parameters for quality calculation / crafting result."""
    
    type: str = Field(
        ...,
        min_length=1,
        description="Resource type identifier (e.g., 'element', 'mercox', 'isogen')",
    )
    amount: Optional[float] = Field(
        default=0.0,
        ge=0,
        description="cSCU amount for ore/gems; 0 if not applicable",
    )
    count: int = Field(
        default=0,
        ge=0,
        description="Number of items (gems, manufactured objects); 0 if not applicable",
    )
    quality_selector: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Base quality selector (0-1000 scale, 500 = average; >500 enhances; <500 reduces quality)",
    )


class CraftingResult(BaseModel):
    """Output of a crafting operation."""
    
    blueprint_id: int = Field(
        ge=0,
        description="Associated blueprint ID from database",
    )
    output_item: str = Field(
        ...,
        min_length=1,
        description="Name of item produced (e.g., 'missile')",
    )
    base_quality: float = Field(
        ge=0,
        le=1,
        description="Base quality before resource adjustments",
    )
    final_quality: float = Field(
        ge=0,
        le=1,
        description="Final quality after resource contributions",
    )
    tier: str = Field(
        ...,
        description="Quality tier: 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'",
    )