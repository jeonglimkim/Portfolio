
if __name__ == "__main__":
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    sum = set()
    
    for i in range(n-2):
        for j in range(i+1, n-1):
            for m in range(j+1, n):
                sum.add(a[i] + a[j]+ a[m])
    
    sum = list(sum)
    sum.sort(reverse = True)
    print(sum[k-1])
                