
from sys import stdin

if __name__ == "__main__":
    s = int(stdin.readline())
    cnt = 0
    total = 0
    
    while s > total:
        cnt += 1
        total += cnt
        if s < total:
            cnt -= 1
            break
    
    print(cnt)
    