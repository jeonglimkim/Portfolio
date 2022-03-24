
if __name__ == "__main__":
    a = int(input())
    b = int(input())
    c = int(input())
    result = a * b * c
    cnt = []*10
    
    for i in range (10):
        if result // 10 == i:
            cnt[i] += 1
    
    print(cnt)