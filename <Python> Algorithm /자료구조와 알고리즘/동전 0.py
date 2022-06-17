from sys import stdin


if __name__ == "__main__":
    n, k = map(int, stdin.readline().split())
    coins = []
    cnt = 0
    
    for _ in range(n):
        coin = int(stdin.readline())
        coins.append(coin)
    
    coins.sort(reverse = True)
    
    for coin in coins:
        if k >= coin:
            cnt += k // coin
            k %= coin
            if k <= 0:
                break
        
    print(cnt)