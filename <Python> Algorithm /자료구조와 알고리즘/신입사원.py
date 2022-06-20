from sys import stdin

if __name__ == "__main__":
    t = int(stdin.readline())


    for _ in range(t):
        n = int(stdin.readline())
        rank = []
        highest = n + 1
        cnt = 0
        
        for _ in range(n):
            a, b = map(int, stdin.readline().split())
            rank.append((a, b))
        
        rank.sort()
        
        for x, y in rank:
            if y < highest:
                cnt += 1
                highest = y
                
        print(cnt)
        