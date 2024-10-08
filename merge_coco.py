import os,json

path = os.getcwd()
inputPar = os.path.join(path,"model_coco")
outPar = os.path.join(path,'final_coco')

if not os.path.exists(outPar):
    os.makedirs(outPar)

timg  = tantn = 0
folders = os.listdir(inputPar)

for folder in folders:
    fimg = fantn = 0
    final_result = {
                    "licenses": [{
                                        "name": "",
                                        "id": 0,
                                        "url": ""
                                    }],
                    "info": {
                        "contributor": "",
                        "date_created": "",
                        "description": "",
                        "url": "",
                        "version": "",
                        "year": ""
                    },
                    "categories" : [
                            {
                                "id": 1,
                                "name": "car",
                                "supercategory": "car"
                            },
                            {
                                "id": 2,
                                "name": "wheel",
                                "supercategory": "car"
                            },
                            {
                                "id": 3,
                                "name": "lights",
                                "supercategory": "car"
                            },
                            {
                                "id": 4,
                                "name": "window",
                                "supercategory": "car"
                            }
                        ],
                    "images" : [],
                    "annotations" : [],
    }

    img_id = 1
    ann_id = 1
    img_nameId = {}
    cat_nameId = {}

    for cat in final_result['categories']:
        cat_nameId[cat['name']] = cat['id']


    inputChild = os.path.join(inputPar,folder)
    outChild = os.path.join(outPar,folder,"annotations")
    if not os.path.exists(outChild):
        os.makedirs(outChild)

    files = os.listdir(inputChild)
    for file in files:
        finput = os.path.join(inputChild,file)
        with open(finput) as f:
            data = json.load(f)


        imgIdName = {}
        images = data['images']
        for img in images:
            timg+=1
            fimg+=1
            imgname = img['file_name']
            imgIdName[img['id']] = img['file_name']
            img_copy = img.copy()
            img_copy['id'] = img_id
            img_nameId[imgname] = img_id
            img_id+=1
            final_result['images'].append(img_copy)

        cat_idName = {}
        flcategories = data['categories']
        for flcat in flcategories:
            cat_idName[flcat['id']] = flcat['name']
        
        annotations = data['annotations']
        
        for ann in annotations:
            fantn+=1
            tantn+=1
            imgname = imgIdName[ann['image_id']]
            new_imgId = img_nameId[imgname]
            cat_name = cat_idName[ann['category_id']]
            new_catId = cat_nameId[cat_name]

            ann_copy = ann.copy()
            ann_copy['id'] = ann_id
            ann_copy['image_id'] = new_imgId
            ann_copy['category_id'] = new_catId
            ann_id+=1
            final_result['annotations'].append(ann_copy)

    fout = os.path.join(outChild,f"instances_default.json")
    
    with open(fout,'w') as f:
        json.dump(final_result,f,indent=4)
    
    print(f"{folder} >> images: {fimg}  annotations: {fantn}")

print(f"\nTotal images: {timg}  annotations: {tantn}")
