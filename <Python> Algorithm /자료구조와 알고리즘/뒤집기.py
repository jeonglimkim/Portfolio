
if __name__ == "__main__":
    n = input()
    a = list(map(int, n))
    cnt_zero = 0
    cnt_one = 0
    
    if a[0] == 1:
        cnt_one = 1
    else:
        cnt_zero = 1
        
    for i in range(1, len(a)):
        index = a[i-1]
        if index != a[i]:
            if index == 0:
                cnt_zero += 1
            else:
                cnt_one += 1
        if cnt_one > cnt_zero:
            print(cnt_zero)
        else:
            print(cnt_one)
            
            