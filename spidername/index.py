from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont

BACKGROUND_IMAGE_FILENAME = 'Images/wall.jpg'
FONT_NAME = 'Font/Spider-Man.otf'

app = Flask(__name__, template_folder='./')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def imageman():
    text = request.form['text']
    THE_TEXT = text
    with open(BACKGROUND_IMAGE_FILENAME, 'rb') as file:
        bgr_img = Image.open(file)
        bgr_img = bgr_img.convert('RGBA')  
        bgr_img_width, bgr_img_height = bgr_img.size
        cx, cy = bgr_img_width//2, bgr_img_height//2

    fgr_img = Image.new('RGBA', bgr_img.size, color=(0, 0, 0, 0))

    font_size = bgr_img_width//len(THE_TEXT)
    font = ImageFont.truetype(FONT_NAME, font_size)

    txt_width, txt_height = font.getsize(THE_TEXT)  
    tx, ty = cx - txt_width//2, cy - txt_height//2  

    mask_img = Image.new('L', bgr_img.size, color=255)
    mask_img_draw = ImageDraw.Draw(mask_img)
    mask_img_draw.text((tx, ty), THE_TEXT, fill=0, font=font, align='center')

    res_img = Image.composite(fgr_img, bgr_img, mask_img)
    res_img.save('LOG/resdownload.png')
    path = 'LOG/resdownload.png'

    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
