from sys import stdin

if __name__ == "__main__":
    a = stdin.readline().split("-")
    sum = 0
    
    print(a)

    for i in a[0].split("+"):
        sum += int(i)
    
    for i in a[1:]:
        for j in i.split("+"):
            sum -= int(j)
        
    print(sum)