import os,json,shutil

path = os.getcwd()
inputPar = os.path.join(path,'split coco') 
outputPar = os.path.join(path,'model_coco')

with open("split_info.json") as fl:
    split_info=json.load(fl)

if not os.path.exists(outputPar):
    os.makedirs(outputPar)

folders = os.listdir(inputPar)

for folder in folders:
    inputChild = os.path.join(inputPar,folder)
    files = os.listdir(inputChild)

    for file in files:
        finput = os.path.join(inputChild,file)
        fname,ext = os.path.splitext(file)

        for splitName,img_list in split_info.items():
            img_fname_list=[os.path.splitext(img)[0] for img in img_list]
            outChild=os.path.join(outputPar,splitName)
            os.makedirs(outChild,exist_ok=True)
            fout=os.path.join(outChild,file)

            if fname in img_fname_list:
                shutil.copy(finput,fout)





