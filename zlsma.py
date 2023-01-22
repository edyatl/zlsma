#!/usr/bin/env python3
"""
    Python porting of ZLSMA - Zero Lag LSMA by veryfid
    https://ru.tradingview.com/script/3LGnSrQN-ZLSMA-Zero-Lag-LSMA/
    Developed by @edyatl <edyatl@yandex.ru> January 2023
    https://github.com/edyatl

"""
# Standard imports
import pandas as pd
import numpy as np
import talib as tl

# Set path to dataset
dataset_path = "../"
short_col_names = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "qav",
    "num_trades",
    "taker_base_vol",
    "taker_quote_vol",
    "ignore",
]

# Load Dataset
data = pd.read_csv(
    dataset_path + "BTCUSDT-15m-2023-01-20.csv",
    names=short_col_names,
)
# Convert Open and Close time fields to DateTime
data["open_time"] = pd.to_datetime(data["open_time"], unit="ms")
data["close_time"] = pd.to_datetime(data["close_time"], unit="ms")

# Set Indicator settings variables
length: int = 32  # Default 32
offset: int = 0
src: pd.Series = data["close"]

# Port of TradingView linreg() function with TA-LIB
def linreg(src: pd.Series, length: int = None, offset: int = None) -> pd.Series:
    """Indicator: Linear Regression with TA-LIB module"""
    # Validate arguments
    src = None if src.size < length or not isinstance(src, pd.Series) else src
    length = int(length) if isinstance(length, int) and length > 0 else 32
    offset = int(offset) if isinstance(offset, int) else 0

    # Offset
    if offset != 0:
        # linreg = intercept + slope * (length - 1 - offset)
        return tl.LINEARREG_INTERCEPT(src, length) + tl.LINEARREG_SLOPE(src, length) * (
            length - 1 - offset
        )

    return tl.LINEARREG(src, length)


def main():
    lsma: pd.Series = linreg(src, length, offset) 
    lsma2: pd.Series = linreg(lsma, length, offset)

    eq = lsma - lsma2
    zlsma = lsma + eq

    data["zlsma"] = zlsma
    data[["open_time", "close_time", "zlsma"]].to_csv('zlsma-BTCUSDT-15m-2023-01-20.csv', index = None, header=True)


if __name__ == "__main__":
    main()
