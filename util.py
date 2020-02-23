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
    
    
def search_documents(files,details):
    name=details['name']
    vehicle_no=details['vehicle']
    policy_no=details['policy']
    for i in files.keys():
        if i== 'policy':
            if file[i].split()[-1]=='.pdf':
                p=pdf_search(file[i],[name,vehicle_no,policy_no])
            else:
                p=img_search(file[i],[name,vehicle_no,policy_no])
                
        if i== 'dl':
            if file[i].split()[-1]=='.pdf':
                d=pdf_search(file[i],[name])
            else:
                d=img_search(file[i],[name])
                
        if i== 'rc':
            if file[i].split()[-1]=='.pdf':
                r=pdf_search(file[i],[name,vehicle_no])
            else:
                r=img_search(file[i],[name,vehicle_no])
                
        if i== 'fir':
            if file[i].split()[-1]=='.pdf':
                f=pdf_search(file[i],[name,vehicle_no])
            else:
                f=img_search(file[i],[name,vehicle_no])
        if i== 'img':
            if file[i].split()[-1]=='.pdf':
                m=pdf_search(file[i],[vehicle_no])
            else:
                m=img_search(file[i],[vehicle_no])
        
    if(d and r and p and m and f):
        return True
    