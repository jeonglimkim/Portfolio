from sys import stdin


if __name__ == "__main__":
    n = int(stdin.readline())
    a = []
    cnt = 0
    max_weight = 0
    
    for _ in range(n):
        height, weight = map(int, stdin.readline().split())
        a.append((height, weight))
        
    a.sort(reverse = True)
    
    for x, y in a:
        if y >= max_weight:
            cnt += 1
            max_weight = y
            
    print(cnt)