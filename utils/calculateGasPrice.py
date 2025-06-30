# utils.py
MAX_GAS_VALUE_LIQUIDATION: int = 5952994
PERCENT: float = 0.8


def calculateGasPrice() -> int:
    gasPrice: int = int(MAX_GAS_VALUE_LIQUIDATION * PERCENT)
    return gasPrice
