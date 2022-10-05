import boto3
import io
from PIL import Image, ImageDraw, ImageFont

file_name = 'car-and-bike.jpg'
# Get Rekognition client
rek_client = boto3.client('rekognition')
with open(file_name, 'rb') as im:
    # Read image bytes
    im_bytes = im.read()
    # Upload image to AWS 
    response = rek_client.detect_labels(Image={'Bytes': im_bytes})
    # Get default font to draw texts
    image = Image.open(io.BytesIO(im_bytes))
    font = ImageFont.truetype('arial.ttf', size=80)
    draw = ImageDraw.Draw(image)
    # Get all labels
    w, h = image.size
    for label in response['Labels']:
        name = label['Name']
        # Draw all instancex box, if any
        for instance in label['Instances']:
            bbox = instance['BoundingBox']
            x0 = int(bbox['Left'] * w) 
            y0 = int(bbox['Top'] * h)
            x1 = x0 + int(bbox['Width'] * w)
            y1 = y0 + int(bbox['Height'] * h)
            draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=10)
            draw.text((x0, y1), name, font=font, fill=(255, 0, 0))

    image.save('labels.jpg')