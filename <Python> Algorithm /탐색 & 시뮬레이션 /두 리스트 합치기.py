
if __name__ == "__main__":
    
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    
    a.extend(b)
    a.sort()
    
    for i in range(len(a)):
        print(a[i], end = " ")