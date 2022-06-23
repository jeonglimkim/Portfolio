from collections import deque
from sys import stdin

if __name__ == "__main__":
    n, m = map(int, stdin.readline().split())
    weight = list(map(int, stdin.readline().split()))
    weight.sort()
    cnt = 0

    
    while weight:
        if len(weight) == 1:   #유효성 검사로서 의미있는
            cnt += 1
            break
            
        if weight[0] + weight[-1] <= m:
            weight.pop(0)
            weight.pop(-1)
            cnt += 1
        
        else: 
            weight.pop(-1)
            cnt += 1
    
    print(cnt)
            
                
            