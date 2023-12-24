import easyocr as ocr

reader = ocr.Reader(['en'],model_storage_directory='.')

result = reader.readtext("outliers.jpeg")

for text in result:
    print(text[1])