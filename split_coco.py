import os,json

path = os.getcwd()
inputPar = os.path.join(path,"Output")
outPar = os.path.join(path,'split coco')

if not os.path.exists(outPar):
    os.makedirs(outPar)
    
clsList = []
timg = tempt = tantn = 0
img_count = {}

for folder in os.listdir(inputPar):
    fimg = fempt = fantn = 0
    inputChild = os.path.join(inputPar,folder)
    outChild = os.path.join(outPar,folder)
    if not os.path.exists(outChild):
        os.makedirs(outChild)

    files = os.listdir(inputChild)
    for file in files:
        finput = os.path.join(inputChild,file)
        with open(finput) as f:
            data = json.load(f)

        # IMAGE KEY - IMAGE DICT
        img_dict = {}
        images = data["images"]
        for img in images:
            img_dict[img['id']] = img

        # CATEGORIES LIST
        categories = data['categories']
        clsid_name = {}
        for ct in categories:
            clsid_name[ ct['id'] ] = ct['name']

        # IMAGES LIST
        for img in img_dict:
                filename = os.path.splitext(img_dict[img]["file_name"])[0]
                fimgName = img_dict[img]["file_name"]

                timg+=1
                fimg+=1
                imgAnn = 0
                new_imgs = []
                new_imgNameId = {}

                print(f"{filename} > {timg}")

                final_result = {
                        "licenses" : [
                            {
                                "name": "",
                                "id": 0,
                                "url": ""
                            }
                            ],
                        "info":{
                                "contributor": "",
                                "date_created": "",
                                "description": "",
                                "url": "",
                                "version": "",
                                "year": ""
                            },
                        "categories": categories,
                        "images" : [],
                        "annotations" : [] 
                    }
                

                img_copy = img_dict[img].copy()
                img_copy['id'] = 1
                new_imgs.append(img_copy)

                new_imgNameId[img_copy['file_name']] = img_copy['id']

                final_result['images'] = new_imgs

                # ANNOTATION LIST
                anid = 1
                new_annos = []
                for ann in data['annotations']:
                    imgid = ann['image_id']
                    clsName = clsid_name[ ann['category_id'] ]
                    if clsName not in clsList:
                        clsList.append(clsName)

                    if imgid == img:
                        imgAnn+=1
                        imgName = img_dict[ann['image_id']]['file_name']
                        new_imgId = new_imgNameId[imgName]
                        ann_copy = ann.copy()
                        ann_copy['id'] = anid
                        ann_copy['image_id'] = new_imgId
                        anid+=1

                        new_annos.append(ann_copy)

                if not new_annos:
                    tempt+=1
                    fempt+=1

                tantn+=len(new_annos)
                fantn+=len(new_annos)

                final_result['annotations'] = new_annos
                img_count[img_dict[img]["file_name"]] = imgAnn

                fout = os.path.join(outChild,filename+".json")
                with open(fout,'w') as f:
                    json.dump(final_result,f,indent=4)


        print(f"{folder} >> images: {fimg} empty: {fempt} annotations: {fantn}")

print(f"\nTotal images: {timg} empty: {tempt} annotations: {tantn}")
print(clsList)


# with open("img_count.json",'w') as f:
#     json.dump(img_count,f,indent=4)

                    

            
            

        