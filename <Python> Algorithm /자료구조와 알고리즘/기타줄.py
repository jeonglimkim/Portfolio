from sys import stdin

if __name__ == "__main__":
    n, m = map(int, stdin.readline().split())
    a = []
    answer = 0
    
    for _ in range(m):
        bundle, single = map(int, stdin.readline().split())
        a.append((bundle, single))
    
    price_bundle = sorted(a, key = lambda x:x[0])
    prince_single = sorted(a, key = lambda x:x[1])
    
    
    
    
    
        
    