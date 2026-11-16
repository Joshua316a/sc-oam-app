"""Crafting quality and result endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from core.database import get_db, Base, engine
from api.schemas.crafting import QualityCalculation, ResourceRequirement, CraftingResult


router = APIRouter(prefix="/crafting", tags=["crafting"])

# Configurable tier thresholds (0-1000 scale)
# Format: list of (threshold, tier_name) sorted ascending
TIER_THRESHOLDS: List[Tuple[int, str]] = [
    (0, "Common"),
    (500, "Uncommon"),
    (600, "Rare"),
    (700, "Epic"),
    (800, "Legendary"),
]


def calculate_tier(final_quality: float) -> str:
    """Determine quality tier based on final quality (0-1 scale).
    
    Uses configurable TIER_THRESHOLDS which can be overridden
    for different tier systems.
    """
    for threshold, tier_name in reversed(TIER_THRESHOLDS):
        if final_quality * 1000 >= threshold:
            return tier_name
    return "Common"


@router.post("/quality", response_model=QualityCalculation)
async def calculate_quality(
    req: ResourceRequirement,
) -> QualityCalculation:
    """Calculate quality score for crafting.
    
    Uses 0-1000 scale directly for quality_selector parameter.
    Base quality = quality_selector / 1000 (ratio 0-1).
    Adjustment = (quality_selector - 500) * 0.001
    Final quality = base + adjustment, clamped 0-1.
    
    The 0.001 adjustment factor means:
    - At quality_selector=500 (average): no adjustment, final = base
    - At quality_selector=0 (Mission quality): final reduced significantly
    - At quality_selector=1000 (peak quality): final increased significantly
    """
    # Base quality: ratio of resource quality to maximum (1000)
    base = req.quality_selector / 1000.0  # 0-1 ratio
    
    # Adjustment from average quality (500)
    # Factor 0.001 makes impact proportional to 0-1000 scale
    adjustment = (req.quality_selector - 500) * 0.001
    
    final = base + adjustment
    
    # Clamp to valid 0-1 range
    final = max(0.0, min(1.0, final))
    
    return QualityCalculation(
        base_quality=round(base, 4),
        resource_qualities={req.type: req.quality_selector / 1000.0},
        resource_weights={req.type: 1.0},
        final_quality=round(final, 4),
        tier=calculate_tier(final),
    )


@router.post("/result", response_model=CraftingResult)
async def crafting_result(
    req: ResourceRequirement,
) -> CraftingResult:
    """Get crafting result with tier determination."""
    # Calculate quality first
    quality = await calculate_quality(req)
    
    # Determine tier (already done in calculate_quality)
    tier = calculate_tier(quality.final_quality)
    
    # Use resource type as output item if not specified
    output_item = req.type or "item"
    
    return CraftingResult(
        blueprint_id=0,  # No blueprint required for basic crafting
        output_item=output_item,
        base_quality=quality.base_quality,
        final_quality=quality.final_quality,
        tier=tier,
    )