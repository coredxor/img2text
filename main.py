from PIL import Image
from pytesseract import pytesseract
import base64
import io
from fastapi import FastAPI

app = FastAPI()
print("Started")

@app.get("/")
async def getCaptcha():
    return {"Message": "get ok!"}
    
@app.post("/captcha2")
async def getCaptcha(imgstring):
    imgstring = imgstring.replace(" ", "+")
    pic = io.StringIO()
    image_string = io.BytesIO(base64.b64decode(imgstring))
    image = Image.open(image_string)
    result = pytesseract.image_to_string(image)
    return {"Message": result}

@app.post("/captcha")
async def getCaptcha(imgstring):
    imgstring = imgstring.replace(" ", "+")
    pic = io.StringIO()
    image_string = io.BytesIO(base64.b64decode(imgstring))
    image = Image.open(image_string)
    pixels = image.load()

    for i in range(image.size[0]): # for every pixel:
        for j in range(image.size[1]):
            if pixels[i,j][0] < 100 :
                pixels[i,j] = (0, 0 ,0)
            else:
                pixels[i,j] = (255, 255 ,255)

    arr = [0,1,2,3,4,5]
    im2 = image.crop((20,0,74,22))
    result=""
    for i in arr:
        crop = im2.crop((i*9,0,(i+1) * 9,22))
        text1 = pytesseract.image_to_string(crop,config="--psm 10")
        text1 = text1.lower().replace("\n","")
        if text1 == 'i':
            text1 = 'j'
        if text1 == 'u':
            text1 = 'y'
        if text1.find('w') != -1:
            text1 = 'w'
        result += text1
    return {"Message": result}


