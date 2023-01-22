## Python porting of ZLSMA - Zero Lag LSMA by veryfid

<https://ru.tradingview.com/script/3LGnSrQN-ZLSMA-Zero-Lag-LSMA/>

>Developed by [@edyatl](https://github.com/edyatl) January 2023 <edyatl@yandex.ru>

### Using [Python wrapper](https://github.com/TA-Lib/ta-lib-python) for [TA-LIB](http://ta-lib.org/) based on Cython instead of SWIG.

### Original Indicator code

```python
study(title = "ZLSMA - Zero Lag LSMA", shorttitle="ZLSMA", overlay=true, resolution="")
length = input(title="Length", type=input.integer, defval=32)
offset = input(title="Offset", type=input.integer, defval=0)
src = input(close, title="Source")
lsma = linreg(src, length, offset)
lsma2 = linreg(lsma, length, offset)
eq= lsma-lsma2
zlsma = lsma+eq

plot(zlsma, color=color.yellow, linewidth=3)
```

**formula:** `linreg = intercept + slope * (length - 1 - offset)`

`linreg(source, length, offset) → series[float]`

where 

* **length** is the y argument, 
* **offset** is the z argument, 
* **intercept** and **slope** are the values calculated with the least squares method on source series (x argument)