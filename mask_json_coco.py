import os,json, random

path = os.getcwd()
inputPar = os.path.join(path,'input')
outputPar = os.path.join(path,r'Output')

if not os.path.exists(outputPar):
    os.makedirs(outputPar)

folders = os.listdir(inputPar)

for folder in folders:
    out_coco={}
    new_img_list=[]
    category_list=[]
    cat_nameId={}
    img_nameId={}
    annotations_list=[]
    img_id=1
    cat_id=1
    ann_id=1

    img_id+=1
    inputChild = os.path.join(inputPar,folder)
    outputChild = os.path.join(outputPar,folder)
    
    if not os.path.exists(outputChild):
        os.makedirs(outputChild)

    files = os.listdir(inputChild)
    
    for file in files:
        fname, ext = os.path.splitext(file)

        if ext.lower()==".json":
            finput = os.path.join(inputChild,file)

            with open(finput) as cj:
                data = json.load(cj)
            
            for cat in data["tags"]:
                cat_dict={
                    "id": cat_id,
                    "name": cat["name"],
                    "supercategory": "car"
                }
                cat_nameId[cat["name"]]=cat_id
                
                category_list.append(cat_dict)
                cat_id+=1

            for obj in data["assets"]:
                imgData=data["assets"][obj]
                imgName=imgData["asset"]["name"]
                

                imCpy={
                "id": img_id,
                "license": 1,
                "file_name":os.path.splitext(imgName)[0]+".png",
                "width": imgData["asset"]["size"]["width"],
                "height": imgData["asset"]["size"]["height"],
                "date_captured": "2024-05-13T06:25:49+00:00"
                }
                new_img_list.append(imCpy)

                for ann in imgData["regions"]:
                    seg_list=[]

                    for pt in ann["points"]:
                        seg_list.append(pt["x"])
                        seg_list.append(pt["y"])

                    clsName=ann["tags"][0]
                    xmin=ann["boundingBox"]['left']
                    ymin=ann["boundingBox"]['top']
                    bw=ann["boundingBox"]['width']
                    bh=ann["boundingBox"]['height']

                    annot_={
                        "id": ann_id,
                        "image_id": img_id,
                        "category_id": cat_nameId[clsName],
                        "bbox": [
                            xmin,
                            ymin,
                            bw,
                            bh
                        ],
                        "area": bw*bh,
                        "segmentation": [seg_list],
                        "iscrowd": 0,
                    }
                    annotations_list.append(annot_)
                    ann_id+=1

                img_id+=1

    fout=os.path.join(outputChild,"annotations.json")
    out_coco['categories']=category_list
    out_coco['images']=new_img_list
    out_coco['annotations']=annotations_list

    with open(fout,"w") as f:
        json.dump(out_coco,f,indent=4)



            
            