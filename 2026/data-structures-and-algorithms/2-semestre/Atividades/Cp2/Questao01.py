n = 28

def reduzir(n):
    print(n)
    if n <= 1:
        return
    reduzir(n // 2)

reduzir(n)