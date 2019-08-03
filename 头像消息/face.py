from PIL import Image, ImageFont, ImageDraw

def transparent(img):
    """抠图操作，把红色圈圈抠出来"""
    img = img.convert('RGBA') #返回一个转换后的图像副本
    datas = img.getdata()  #像素数据队列
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255:
            newData.append((255,255,255,0))  #把白色变为透明色
        else:
            newData.append(item)
    img.putdata(newData) #赋值给图片新的像素数据
#    img.save("change.png","PNG")
    return img

#图片的名字
p1_name = 'wechat.png'
p2_name = 'logo.png'

#打开图片
p1_image = Image.open(p1_name)
p2_image = Image.open(p2_name)

#把红色圈圈插入到头像图片中
p2_new = transparent(p2_image)
p1_image.paste(p2_new,(40,0),p2_new)

usr_font = ImageFont.truetype('arial.ttf', 50)
draw=ImageDraw.Draw(p1_image) #在p1_image上绘制文字
draw.text((198,3),u'1',font=usr_font)
p1_image.save("final.png","PNG")

