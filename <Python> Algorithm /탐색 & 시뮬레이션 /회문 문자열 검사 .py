

if __name__ == "__main__":
    n = int(input())
    
    for i in range(n):
        str = input()
        str = str.upper()
        if str == str[::-1]:
            print('#%d YES' %(i+1))
        else:
            print('#%d NO' %(i+1))