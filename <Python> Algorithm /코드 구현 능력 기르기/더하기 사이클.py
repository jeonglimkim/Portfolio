if __name__ == "__main__":
    n = int(input())
    cnt = 0 
    temp = n
    
    while True:
        a = temp // 10 #Quotient
        b = temp % 10  #Remainder
        c = (a + b) % 10 
        temp = (b*10) + c
        cnt += 1 
        if n == temp:
            break
    
    print(cnt)
        