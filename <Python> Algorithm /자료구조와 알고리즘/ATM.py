from sys import stdin

if __name__ == "__main__":
    n = int(stdin.readline())
    P = list(map(int, stdin.readline().split()))
    P.sort()
    total = 0    #누적합의 합
    a = 0

    for i in range(n):
        a += P[i] #누적합
        total += a
    
    print(total)