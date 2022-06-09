
from sys import stdin

n = int(stdin.readline())
a = []
cnt = 0
last_time = 0

for _ in range(n):
    start, end = map(int, stdin.readline().split()) #tuple 입력받기
    a.append((start, end))

a.sort(key = lambda x : (x[1], x[0])) #tuple 뒤에 부분 sort

for x, y in a:
    if last_time <= x:
        last_time = y
        cnt += 1

print(cnt)

