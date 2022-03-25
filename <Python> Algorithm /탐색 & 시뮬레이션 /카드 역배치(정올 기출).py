
if __name__ == "__main__":
    card = list(range(21))
    
    for _ in range(10):
        ai, bi = map(int, input().split())
        for _ in range ((bi - ai + 1) // 2):
            card[ai], card[bi] = card[bi], card[ai]
            ai += 1
            bi -= 1
        
    for i in range(1, 21):
        print(card[i], end = " ")
            
        
        
        
        
