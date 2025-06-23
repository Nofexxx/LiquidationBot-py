# schemas.py
from typing import Any, Dict

from pydantic import BaseModel, Field


class Borrow(BaseModel):
    id: int
    userAddress: str
    reserve: str
    amount: int
    block: int
    timestamp: int


class UserAccountData(BaseModel):
    totalCollateralETH: int = Field(gt=0)
    totalDebtETH: int = Field(gt=0)
    availableBorrowsETH: int = Field(gt=0)
    currentLiquidationThreshold: int = Field(gt=0)
    ltv: int = Field(gt=0)
    healthFactor: int = Field(gt=0)

    @classmethod
    def from_Dict(cls, data: Dict[str, int]) -> "UserAccountData":
        return cls(
            totalCollateralETH=data["totalCollateralETH"],
            totalDebtETH=data["totalDebtETH"],
            availableBorrowsETH=data["availableBorrowsETH"],
            currentLiquidationThreshold=data["currentLiquidationThreshold"],
            ltv=data["ltv"],
            healthFactor=data["healthFactor"],
        )


class UserDebtData(BaseModel):
    userAddress: str
    debtAssetAddress: str
    collateralAssetAddress: str
    debtToCover: int = Field(gt=0)

    @classmethod
    def from_Dict(cls, data: Dict[str, Any]) -> "UserDebtData":
        return cls(
            userAddress=data["userAddress"],
            debtAssetAddress=data["debtAssetAddress"],
            collateralAssetAddress=data["collateralAssetAddress"],
            debtToCover=data["debtToCover"],
        )
