
if __name__ == "__main__":
    n = input()
    word = input()
    cnt = 0
    left = 0
    right = len(word)
    
    while left <= len(n) - len(word):
        if word == n[left:right]:
            cnt += 1
            left += len(word)
            right += len(word)
            
        else:
            left += 1
            right += 1
        
            
    
    print(cnt)
    
    
