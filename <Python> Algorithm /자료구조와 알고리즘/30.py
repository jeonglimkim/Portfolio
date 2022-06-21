

if __name__ == "__main__":
    n = input()
    n = sorted(n, reverse = True)
    a = [int(x) for x in n]
    
    if sum(a) % 3 != 0 or "0" not in n:
        print(-1)
    else:
        print(''.join(n))
        
        