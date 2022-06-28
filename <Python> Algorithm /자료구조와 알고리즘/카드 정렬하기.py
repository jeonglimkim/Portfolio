from sys import stdin
import heapq

if __name__ == "__main__":
    n = int(stdin.readline())
    a = []
    answer = 0
    
    for _ in range(n):
        heapq.heappush(a, int(stdin.readline()))
    
    if len(a) == 1:
        print(0)
    
    else:
        while len(a) > 1:
            temp1 = heapq.heappop(a)
            temp2 = heapq.heappop(a)
            answer += temp1 + temp2
            heapq.heappush(a, temp1 + temp2)
            
        print(answer)