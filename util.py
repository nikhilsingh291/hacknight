from pdf2image import convert_from_path
import pytesseract

def pdf_search(pdf_name,search):
    pages = convert_from_path(pdf_name, 300)
    read_pages=[]
    for page in pages:
        read_pages.append(pytesseract.image_to_string(page))
        read_pages=' '.join(read_pages)
        for i in search:
            if(read_pages.find(i)==-1):
                return False
        return True
    
    
def aws_process(image_path):
    try:
        
        aws = AWS()
        ocr = OCR()

        file_name = os.path.basename(image_path)
        output_file_name = file_name[:-4]+'_ocr.jpg'
        output_file_path = ''

        full_output_file_path = os.path.join(
            output_file_path, output_file_name)
        media_file_path = os.path.join('', output_file_name)

        extracted_text, json = aws.upload_and_process(image_path, file_name)
        ocr.create_annotated_image(json, image_path, full_output_file_path)
        ocr.create_text_file(json, output_file_path, file_name)
        ocr.create_json_file(json, output_file_path, file_name)
        return extracted_text,json
    except:
        return False
    
    
def img_search(img_path,search):
    text,json=aws_process(img_path)
    for i in search:
        if(text.find(i)==-1):
            return False
    return True
    
    