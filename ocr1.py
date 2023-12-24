import easyocr as ocr
from PIL import Image
import numpy as np 
import re

def extract_information(text):
    print("OCR Output:", text)
    PH=[]
    PHID=[]  
    ADD=set()
    AID=[]
    EMAIL=''
    EID=''
    PID=''
    WEB=''
    WID=''

    for i, string in enumerate(result_text):   
  

        if re.search(r'@', string.lower()):
            EMAIL=string.lower()
            EID=i

        match = re.search(r'(?:ph|phone|phno)?\s*(?:[+-]?\d\s*[\(\)]*){7,}', string)
        if match and len(re.findall(r'\d', string)) > 7:
            PH.append(string)
            PHID.append(i)


            
        # TO FIND ADDRESS 
        keywords = ['road', 'floor', ' st ', 'st,', 'street', ' dt ', 'district',
                    'near', 'beside', 'opposite', ' at ', ' in ', 'center', 'main road',
                   'state','country', 'post','zip','city','zone','mandal','town','rural',
                    'circle','next to','across from','area','building','towers','village',
                    ' ST ',' VA ',' VA,',' EAST ',' WEST ',' NORTH ',' SOUTH ']
        # Define the regular expression pattern to match six or seven continuous digits
        digit_pattern = r'\d{6,7}'
        # Check if the string contains any of the keywords or a sequence of six or seven digits
        if any(keyword in string.lower() for keyword in keywords) or re.search(digit_pattern, string):
            ADD.add(string)
            AID.append(i)
            
        # TO FIND STATE (USING SIMILARITY SCORE)
        states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 
          'Haryana','Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
              "United States", "China", "Japan", "Germany", "United Kingdom", "France", "India", 
               "Canada", "Italy", "South Korea", "Russia", "Australia", "Brazil", "Spain", "Mexico", 'USA','UK']

        import Levenshtein
        def string_similarity(s1, s2):
            distance = Levenshtein.distance(s1, s2)
            similarity = 1 - (distance / max(len(s1), len(s2)))
            return similarity * 100
        
        for x in states:
            similarity = string_similarity(x.lower(), string.lower())
            if similarity > 50:
                ADD.add(string)
                AID.append(i)
                
        # WEBSITE URL          
        if re.match(r"(?!.*@)(www|.*com$)", string):
            WEB=string.lower()
            WID=i 

        # DISPLAY ALL THE ELEMENTS OF BUSINESS CARD 
    print("EXTRACTED TEXT")
    print('[WEBSITE URL: ] '+ str(WEB))
    print('[EMAIL: ] '+ str(EMAIL)) 
    ph_str = ', '.join(PH)
    print('[PHONE NUMBER(S): ] '+ph_str)
    add_str = ' '.join([str(elem) for elem in ADD])
    print('[ADDRESS: ] ', add_str)

    IDS= [EID,PID,WID]
    IDS.extend(AID)
    IDS.extend(PHID)
#         st.write(IDS)
    oth=''                               
    fin=[]                        
    for i, string in enumerate(result_text):
        if i not in IDS:
            if len(string) >= 4 and ',' not in string and '.' not in string and 'www.' not in string:
                if not re.match("^[0-9]{0,3}$", string) and not re.match("^[^a-zA-Z0-9]+$", string):
                    numbers = re.findall('\d+', string)
                    if len(numbers) == 0 or all(len(num) < 3 for num in numbers) and not any(num in string for num in ['0','1','2','3','4','5','6','7','8','9']*3):
                        fin.append(string)
    print('[CARD HOLDER & COMPANY DETAILS: ] ')
    for i in fin:
        print(''+i)

# Load the OCR model
reader = ocr.Reader(['en'], model_storage_directory='.')

# Image path in the same directory as the script
image_path = "hello.png"  # Replace with your image file name

# Open the image
input_image = Image.open(image_path)

# Perform OCR on the image
result = reader.readtext(np.array(input_image))
result_text = [text[1] for text in result]

# Extract information from the OCR result
extract_information(result_text)
