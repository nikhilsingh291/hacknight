'''
AWS Services
'''

import io

import boto3
from PIL import Image



class AWS():
    '''
    AWS Services
    '''

    def __init__(self):
        self.S3_BUCKET = 'utopianameplate'

    def process_by_rekognition(self, file_name):
        '''
        Read data using Rekognition
        '''
        try:
            client = boto3.client('rekognition')
            results = client.detect_text(
                Image={
                    'S3Object': {
                        'Bucket': self.S3_BUCKET,
                        'Name': file_name}})
            return results['TextDetections']
        except Exception as error:
            print(error)
            return None

    def upload_to_s3(self, key, file_name):
        """
        This function takes in bucket, key and output file name as input
        Uploads that Image to S3 Bucket
        """
        try:
            s_3 = boto3.client('s3')
            s_3.upload_file(key, self.S3_BUCKET, file_name)
        except Exception as error:
            print(error)
            return False

    def process_from_s3(self, file_name):
        """
        Input: S3 Bucket Name, file_name, output file path
        Returns: Extracted text, JSON response of text, file_name
        """
        try:
            # Get data from image
            json = self.process_by_rekognition(file_name)

            # Load image from S3 bucket
            s3_object = boto3.resource('s3').Object(self.S3_BUCKET, file_name)
            s3_response = s3_object.get()
            image = Image.open(io.BytesIO(s3_response['Body'].read()))
            img_width, img_height = image.size

            # Save output image with bounding boxes
            for ids in range(0, len(json)):
                # Rescaling Coordinates of poly
                for i in range(4):
                    json[ids]['Geometry']['Polygon'][i]['X'] = round(
                        json[ids]['Geometry']['Polygon'][i]['X'] * img_width)
                    json[ids]['Geometry']['Polygon'][i]['Y'] = round(
                        json[ids]['Geometry']['Polygon'][i]['Y'] * img_height)

            # Saving the file to the out file path
            text_list = []
            for data in json:
                if data['Type'] == 'LINE':
                    text_list.append(data['DetectedText'] + ' ')
            extracted_text = ''.join(text_list)
            return extracted_text, json
        except Exception as error:
            print(error)
            return None, None

    def upload_and_process(self, full_input_file_path, file_name):
        try:
            self.upload_to_s3(full_input_file_path, file_name)
            extracted_text, json = self.process_from_s3(file_name)
            return extracted_text, json
        except Exception as error:
            print(error)
            return None, None
