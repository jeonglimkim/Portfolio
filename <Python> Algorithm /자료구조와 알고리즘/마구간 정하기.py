
from sys import stdin

def Distance(mid):
    start = x[0]
    dist = 0
    cnt = 1
    for i in range(1, n):
        dist = x[i] - start
        if dist >= mid: 
            start = x[i]
            cnt += 1
        if cnt == c:
            return(True)
    return(False)
        

if __name__ == "__main__":
    n, c = map(int, stdin.readline().split())
    x = list(map(int, stdin.readlines()))
    x.sort()
    left = 1
    right = max(x)
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2 #mid = 최대 거리 
        if Distance(mid) == True:
            answer = mid
            left = mid + 1
        else: 
            right = mid - 1
    print(answer)
            
        
        