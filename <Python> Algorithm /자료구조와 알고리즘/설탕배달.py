
if __name__ == "__main__":
    n = int(input())
    bags = [5, 3]
    cnt = 0
    temp = n
    
    while temp >= 0:
        if temp % 5 == 0:
            cnt += (temp // 5)
            print(cnt)
            break
        else:
            temp -= 3
            cnt += 1
    else: 
        print(-1)