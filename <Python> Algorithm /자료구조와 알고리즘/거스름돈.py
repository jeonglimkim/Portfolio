
if __name__ == "__main__":
    n = int(input())
    change = 1000 - n
    coins = [500, 100, 50, 10, 5, 1]
    cnt = 0 
    
    for i in coins:   
        while change >= i:
            change = change - i
            cnt += 1
            
    print(cnt)
            