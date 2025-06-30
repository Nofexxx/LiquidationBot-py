# schemas.py
from typing import Tuple

from pydantic import BaseModel, Field


class Borrow(BaseModel):
    id: int
    userAddress: str
    reserve: str
    amount: int
    block: int
    timestamp: int


class UserAccountData(BaseModel):
    totalCollateralETH: int
    totalDebtETH: int
    availableBorrowsETH: int
    currentLiquidationThreshold: int
    ltv: int
    healthFactor: int

    @classmethod
    def from_tuple(cls, data: Tuple[int, int, int, int, int, int]) -> "UserAccountData":
        return cls(
            totalCollateralETH=data[0],
            totalDebtETH=data[1],
            availableBorrowsETH=data[2],
            currentLiquidationThreshold=data[3],
            ltv=data[4],
            healthFactor=data[5],
        )


class UserDebtData(BaseModel):
    userAddress: str
    debtAssetAddress: str
    collateralAssetAddress: str
    debtToCover: int = Field(gt=0)

    @classmethod
    def from_tuple(cls, data: Tuple[str, str, str, int]) -> "UserDebtData":
        return cls(
            userAddress=data[0],
            debtAssetAddress=data[1],
            collateralAssetAddress=data[2],
            debtToCover=data[3],
        )

    def to_tuple(self) -> Tuple[str, str, str, int]:
        return (
            self.userAddress,
            self.debtAssetAddress,
            self.collateralAssetAddress,
            self.debtToCover,
        )


# class TxData(BaseModel):
#     txHash: str
#     status: int
#     gasUsed: int
