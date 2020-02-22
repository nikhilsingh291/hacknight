'''
OCR PROCESSING MODULE
'''
import os
import json
import logging
import cv2

from scipy import misc
from aws_processing import AWS




class OCR(AWS):
    '''
    Ocr Processing modules
    '''

    def create_annotated_image(self, text, img_path, full_output_path):
        """
        Input: JSON Response, Image_path, and full output path
        Output: Writes the file in the output path
        """
        try:
            list_word = []

            for item in text:
                if item['Type'] == 'WORD':
                    list_word.append(item)

            cropping_lst_min = []
            cropping_lst_max = []

            for item in list_word:
                temp = item['Geometry']['Polygon']
                cropping_lst_min.append((temp[0]['X'], temp[0]['Y']))
                cropping_lst_max.append((temp[2]['X'], temp[2]['Y']))
            img = cv2.imread(img_path)

            for i, j in zip(cropping_lst_min, cropping_lst_max):
                img_plot = cv2.rectangle(img, i, j, (0, 255, 0), 1)

            cv2.imwrite(full_output_path, img_plot)
            return True

        except Exception as error:
            print(error)
            return False

    def create_text_file(self, text, output_file_path, file_name):
        """
        Writes the extarcted text to a txt file in the output path
        """
        try:
            with open(output_file_path + file_name[:-4] + '.txt', 'w') as txt_file:
                for texts in text:
                    if texts['Type'] == 'LINE':
                        txt_file.write(texts['DetectedText'] + '\n')
                txt_file.close()
            return True
        except Exception as error:
            print(error)
            return False

    def create_json_file(self, text, output_file_path, file_name):
        """
        Writes the JSON response in output path
        """
        try:
            with open(output_file_path + file_name[:-4] + '.json', 'w') as file_:
                json.dump(text, file_)
                file_.close()
            return True
        except Exception as error:
            print(error)
            return False

  