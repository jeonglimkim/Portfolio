import PyPDF2
import spacy
import pandas as pd
import requests


def read_pdf():
    
    year = input("Please enter a year: ")
    #year = "2019"
    availble_years = ["2018", "2019"]
    
    if year in availble_years:
        
        url = f'https://www.eia.gov/outlooks/aeo/pdf/aeo{year}.pdf'
        r = requests.get(url, stream=True)
        with open(f"./aeo{year}.pdf",'wb') as f: 
            f.write(r.content)
            
        with open(f"./aeo{year}.pdf",'rb') as f: 
            pdf = PyPDF2.PdfFileReader(f)
            
            for page in (pdf.pages):
                
                text = page.extractText()
                text = text.replace("\n", "") #for disconnected sentences between paragraphs
                
                find_table = "table of contents"
                find_takeaway = "key takeaways"
                
                if find_table in text or find_table.capitalize() in text:
                    if find_takeaway in text or find_takeaway.capitalize() in text:
                        find_slidenumber = "slide number"
                        try: 
                            slide_index = text.index(find_slidenumber.capitalize())
                        except:
                            slide_index = text.index(find_slidenumber)
                        
                        
                        slide_index += len(find_slidenumber)
                        start_page = int(text[slide_index])
                        end_page = int(text[slide_index + 1:slide_index +3]) -1
                        break 
                        #Approach: Find where 'table of contents' and 'key takeaways' both appear. 
                        #          Find corresponding slide numbers. Look at only the "key takeaways". 
                        #When you read slide numbers straight out of texts, there are no spaces between sections.
                        #I found the pattern to find how slide numbers go from key takeaway section to the next. 

            start_page = start_page // 2 - (1 - start_page%2)
            end_page = end_page // 2 - (1 - end_page%2)
            #When you find the pattern between how the pages are set up and how python reads it as an "index":
            #Slide 9 corresponds to index 4 >> 9//2 = 4. 
            #Slide 28 corresponds to index 13 >> 28//2 = 14, but has to be 13, so subtract it by 1.
            #For each even page number, you will have to subtract it by 1. 

            text_list = []
            for page_num in range(start_page, end_page + 1):
                page = pdf.getPage(page_num)
                text = page.extractText()
                text = text.replace("\n", '')
                text_list.append(text) 

        return text_list, year


    else:
        raise RuntimeError(f'{year} is not available yet.')

                    


def analyze_text(AEOPDF):
    
    analyzed_dict = {"coal":{"energy_type": "coal","price":0,"emissions":0,"production":0,"export":0,"import":0}, 
                    "nuclear":{"energy_type": "nuclear","price":0,"emissions":0,"production":0,"export":0,"import":0}, 
                    "wind":{"energy_type": "wind", "price":0,"emissions":0,"production":0,"export":0,"import":0}, 
                    "solar":{"energy_type": "solar", "price":0,"emissions":0,"production":0,"export":0,"import":0}, 
                    "oil":{"energy_type": "oil", "price":0,"emissions":0,"production":0,"export":0,"import":0}}
    #Took a step of creating nested dictionary before creating a data frame before converting it to a csv file.
    
    rows = ["coal", "nuclear", "wind", "solar", "oil"]
    columns = ["price", "emission", "production", "export", "import"] 
    #Separated export and import for clear distinction
    
    nlp = spacy.load("en_core_web_sm")
    
    rate_up = ['raise', 'increase', 'up','grow','larger','bigger','enlarge','expand','rise']
    rate_down = ['lower', 'decrease', 'down','lessen','reduce','smaller','less','drop','diminish','decline','dwindle','contract','shrink','fall off', 'abate']
    
    for text_per_page in AEOPDF:
        page_doc = nlp(text_per_page)
        sentences_per_page = list(page_doc.sents)
        
        for row in rows:
            for col in columns:
                for sentence in sentences_per_page: 
                    word_with_row = []
                    word_with_col = []
                    for word in sentence.noun_chunks:
                        if row in word.string:
                            word_with_row+= [t for t in word if t.text == row]
                        if col in word.string:
                            word_with_col+= [t for t in word if t.text == col]


                    if word_with_row and word_with_col: #both words in a sentence
                        up_count = 0
                        down_count = 0
                        for col_candidates in word_with_col: 
                            for row_candidates in word_with_row:
                                # if "gas production at lower prices" in sentence.string:
                                #     print(sentence.string)
                                #     print(col_candi,row_candi)
                                #     print(list(col_candi.ancestors))
                                #     print(list(row_candi.ancestors))
                                #     print(list(col_candi.children))
                                #     print(list(row_candi.children))
                                
                                for col_anc in list(col_candidates.ancestors) + list(col_candidates.children): 
                                    for row_anc in list(row_candidates.ancestors) + list(col_candidates.children):
                                        for up_word in rate_up:
                                            if up_word in col_anc.string and up_word in row_anc.string:
                                                up_count += 1

                                        for down_word in rate_down:
                                            if down_word in col_anc.string and down_word in row_anc.string:
                                                down_count += 1

                                
                        final_count = up_count - down_count
                                
                        if final_count > 0:
                            analyzed_dict[row][col] += 1
                        elif final_count < 0: 
                            analyzed_dict[row][col] -= 1
                            
    print(analyzed_dict)
    return(analyzed_dict)
                                            
                    
def make_csv(analyzed_dict, year):

    for key in analyzed_dict.keys():
        for row_key in analyzed_dict[key].keys():
            if isinstance(analyzed_dict[key][row_key], int):
                
                if analyzed_dict[key][row_key] > 0:
                    analyzed_dict[key][row_key] = "increase"
                    #categorized as "increase" if final count is greater than zero
                    
                elif analyzed_dict[key][row_key] < 0:
                    analyzed_dict[key][row_key] = "decrease"
                    #categorized as "decrease" if final count is less than zero


    df = pd.DataFrame.from_dict(analyzed_dict, orient = "index")
    df.to_csv(f"aeo{year}.csv")
    
    
def main():
    text_list, year = read_pdf()
    analyzed_dict = analyze_text(text_list)
    make_csv(analyzed_dict, year)


main()
