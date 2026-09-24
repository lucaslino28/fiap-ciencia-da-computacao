n = 28

def reduzir2(n):
    if n <= 1:
        return
    reduzir2(n // 2)
    reduzir2(n // 2)

reduzir2(n)
