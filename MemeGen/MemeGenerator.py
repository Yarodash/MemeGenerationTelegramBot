from PIL import Image, ImageDraw, ImageFont
import textwrap
import math
from MemeGen import MemeText

class Meme:
    def __init__(self, image, meme_type):
        self.image = image
        self.meme_type = meme_type
        self.h = self.image.size[1]
        if (meme_type == 'under_image'):
            self.createBorders()
        self.draw = ImageDraw.Draw(self.image)

    def createBorders(self):
        image_width, image_height = self.image.size
        new_image = Image.new(size=(int(image_width*1.2), int(image_height*1.1)+max(image_width//4, 100)), mode='RGB', color=(0,0,0))
        draw = ImageDraw.Draw(new_image)
        draw.rectangle(( (image_width//10-3, image_height//10-3) , (image_width//10 + image_width+3, image_height//10 + image_height+3) ), (255, 255, 255))
        new_image.paste(self.image, (image_width//10, image_height//10))
        self.image = new_image

    def add_text(self, text, location, fontcolor=(0, 0, 0),
                 border=0, border_color=(0, 0, 0), points=15):
        if border:
            (x, y) = location
            for step in range(0, math.floor(border * points), 1):
                angle = step * 2 * math.pi / math.floor(border * points)
                self.draw.text((x - border * math.cos(angle), y - border * math.sin(angle)), text, border_color,
                               font=self.font)
        self.draw.text(location, text, fontcolor, font=self.font)

    def draw_multiple_line_text(self, text, text_start_height):
        image_width, image_height = self.image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = self.font.getsize(line)
            self.add_text(line, ((image_width - line_width) / 2, y_text), fontcolor=(255, 255, 255), border=3)
            y_text += line_height

    def addText(self, text, font_name):
        width, height = self.image.size

        self.font = ImageFont.truetype(font_name, width // 19)
        lines = text.split('\\')
        for line, counter in zip(lines, range(100)):
            if (self.meme_type == 'under_image'):
                self.draw_multiple_line_text(line, int(self.h*1.1) + 30 + counter*width // 19)
            if (self.meme_type == 'on_image'):
                self.draw_multiple_line_text(line, int(self.image.size[1] - len(lines)*width//19 + counter*width//19 - 15))
        return self

    def get(self):
        return self.image

def generate(start_file_name, end_file_name, phrase, meme_type, font_type):
    image = Image.open(start_file_name).convert('RGB')
    image = image.resize((image.width, int(image.height*0.8)), Image.ANTIALIAS)
    text = phrase if phrase else MemeText.getPhrase()

    font = f'MemeGen\\{font_type}.ttf'

    Meme(image, meme_type).addText(text, font).get().save(end_file_name, 'PNG')
