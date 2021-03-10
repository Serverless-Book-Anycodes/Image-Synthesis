# -*- coding: utf-8 -*-
import base64, json
from PIL import Image


def do_circle(base_pic):
    icon_pic = Image.open(base_pic).convert("RGBA")
    icon_pic = icon_pic.resize((500, 500), Image.ANTIALIAS)
    icon_pic_x, icon_pic_y = icon_pic.size
    temp_icon_pic = Image.new('RGBA', (icon_pic_x + 600, icon_pic_y + 600), (255, 255, 255))
    temp_icon_pic.paste(icon_pic, (300, 300), icon_pic)
    ima = temp_icon_pic.resize((200, 200), Image.ANTIALIAS)
    size = ima.size

    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)

    # 最后生成圆的半径
    r3 = 60
    imb = Image.new('RGBA', (r3 * 2, r3 * 2), (255, 255, 255, 0))
    pima = ima.load()  # 像素的访问对象
    pimb = imb.load()
    r = float(r2 / 2)  # 圆心横坐标

    for i in range(r2):
        for j in range(r2):
            lx = abs(i - r)  # 到圆心距离的横坐标
            ly = abs(j - r)  # 到圆心距离的纵坐标
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径

            if l < r3:
                pimb[i - (r - r3), j - (r - r3)] = pima[i, j]
    return imb


def add_decorate():
    try:
        base_pic = "./code/decorate.png"
        user_pic = Image.open("/tmp/picture.png").convert("RGBA")
        temp_basee_user_pic = Image.new('RGBA', (440, 440), (255, 255, 255))
        user_pic = user_pic.resize((400, 400), Image.ANTIALIAS)
        temp_basee_user_pic.paste(user_pic, (20, 20))
        temp_basee_user_pic.paste(do_circle(base_pic), (295, 295), do_circle(base_pic))
        temp_basee_user_pic.save("/tmp/output.png")
        return True
    except Exception as e:
        print(e)
        return False


def handler(event, context):
    jsonResponse = {
        'statusCode': 200,
        'isBase64Encoded': False,
        'headers': {
            "Content-type": "application/json"
        },
    }

    # 将接收到的base64图像转为pic
    imgData = base64.b64decode(json.loads(base64.b64decode(event["body"]))["image"])
    with open('/tmp/picture.png', 'wb') as f:
        f.write(imgData)
    addResult = add_decorate()
    if addResult:
        with open("/tmp/output.png", "rb") as f:
            base64Data = str(base64.b64encode(f.read()), encoding='utf-8')
        jsonResponse['body'] = json.dumps({"picture": base64Data})
    else:
        jsonResponse['body'] = json.dumps({"error": True})

    return jsonResponse
