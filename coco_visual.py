import os,json,random
from PIL import Image,ImageDraw,ImageFont
from shapely.geometry import Polygon

def find_polygon_center(polygon):

    if not isinstance(polygon, Polygon):
        polygon = Polygon(polygon)

    center = polygon.centroid
    return center.x, center.y

path = os.getcwd()
inputPar = os.path.join(path,'Output')
imgDir = os.path.join(path,r'input_imgs\converted_images') 
outputPar = os.path.join(path,'Visualization')

if not os.path.exists(outputPar):
    os.makedirs(outputPar)

cls_clr ={'car':'red','wheel':'blue',"background":"green","lights":"yellow","window":"#800000"}

folders = os.listdir(inputPar)

for folder in folders:
    inputChild = os.path.join(inputPar,folder)
    files = os.listdir(inputChild)

    for file in files:

        if os.path.splitext(file)[-1] == '.json':
            finput = os.path.join(inputChild,file)
            fname,ext = os.path.splitext(file)

            with open(finput) as cj:
                data = json.load(cj)

            imgid_name = {}
            imgids = []
            imagelist = data['images']

            for im  in imagelist:
                imgid_name[ im['id'] ] = im['file_name']
                imgids.append(im['id'])

            clsid_name = {}
            categorylist = data['categories']

            for ct in categorylist:
                clsid_name[ ct['id'] ] = ct['name']
                
            annotations = data['annotations']

            for id in imgids:
                imgName = imgid_name[id]
                imgpath = os.path.join(imgDir,imgName)

                if os.path.exists(imgpath):
                    print("Plotting_____",imgName)
                    img = Image.open(imgpath).convert("RGB")
                    imgcopy = img.copy()
                    draw = ImageDraw.Draw(img)

                    for ann in annotations:

                        if ann['image_id'] == id:
                            clsName = clsid_name[ ann['category_id'] ]
                            
                            # if clsName not in cls_clr:
                            #     color = "#%06X" % random.randint(0, 0xFFFFFF)
                            #     cls_clr[clsName]=color

                            clr = cls_clr[clsName]

                            contours = ann['segmentation']

                            if clsName=="car":

                                for seg in contours:
                                    n = 2
                                    # using list comprehension
                                    final = [seg[i * n:(i + 1) * n] for i in range((len(seg) + n - 1) // n )]
                                    contourlist = [(point[0],point[1]) for point in final]
                                    draw.polygon(contourlist,fill=clr,outline='yellow', width=3)

                    for ann in annotations:

                        if ann['image_id'] == id:
                            clsName = clsid_name[ ann['category_id'] ]
                            
                            # if clsName not in cls_clr:
                            #     color = "#%06X" % random.randint(0, 0xFFFFFF)
                            #     cls_clr[clsName]=color

                            clr = cls_clr[clsName]

                            contours = ann['segmentation']

                            if clsName!="car": 
                                for seg in contours:
                                    n = 2
                                    # using list comprehension
                                    final = [seg[i * n:(i + 1) * n] for i in range((len(seg) + n - 1) // n )]
                                    contourlist = [(point[0],point[1]) for point in final]
                                    draw.polygon(contourlist,fill=clr,outline='yellow', width=3)   
                                
                    # decrease opacity
                    outimg =Image.blend(img,imgcopy,alpha=.6)
                    draw1 = ImageDraw.Draw(outimg)

                    for ann in annotations:

                        if ann['image_id'] == id:
                            clsName = clsid_name[ ann['category_id'] ]
                            clr = cls_clr[clsName]
                            contours=ann["segmentation"][0]
                            contourlist = [(contours[i], contours[i + 1]) for i in range(0, len(contours), 2)]
                            centroid_x, centroid_y = find_polygon_center(contourlist)
                            x, y = centroid_x, centroid_y
                            font = ImageFont.truetype("arial.ttf", 30)
                            text_w,text_h = font.getbbox(clsName)[2:]
                            draw1.rectangle([(x,y),(x+text_w,y+text_h)],fill = clr)
                            draw1.text(([x,y-3]),clsName,fill='white',font=font)

                    fout = os.path.join(outputPar,imgName)
                    outimg.save(fout)

                else:
                    print('not found:',imgpath)


print(cls_clr)