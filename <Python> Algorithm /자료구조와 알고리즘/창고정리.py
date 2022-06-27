from sys import stdin

if __name__ == "__main__":
    l = int(stdin.readline())
    h = list(map(int, stdin.readline().split()))
    m = int(stdin.readline())
    
    h.sort()
    
    for _ in range(m):
        h[-1] -= 1
        h[0] += 1
        h.sort()
    
    print(h[-1] - h[0])
    
    
    