import os, shutil,json

cPath = os.getcwd()
inputPar = os.path.join(cPath, "input_imgs")
outPar = os.path.join(cPath, "Dataset")
split_info={}

def copyFiles(fldr, files, category, inputChild):
    outSub = os.path.join(outPar, category, "images")
    os.makedirs(outSub, exist_ok=True)

    for fl in files:
        finput = os.path.join(inputChild, fl)
        fout = os.path.join(outSub, fl)
        shutil.copy(finput, fout)

for folder in os.listdir(inputPar):
    inputChild = os.path.join(inputPar, folder)
    files = os.listdir(inputChild)
    
    # Select 2 files for the test set
    testSet = files[:2]
    split_info["test"]=testSet
    
    # Remove testSet files from the list of files
    remainingFiles = files[2:]
    
    # Compute new proportions for train and valid
    trainLen = int(len(remainingFiles) * 0.85)
    trainset = remainingFiles[:trainLen]
    valSet = remainingFiles[trainLen:]

    split_info["train"]=trainset
    split_info["valid"]=valSet

    # Copy the files to their respective directories
    copyFiles(folder, trainset, "train", inputChild)
    copyFiles(folder, valSet, "valid", inputChild)
    copyFiles(folder, testSet, "test", inputChild)

with open("split_info.json","w") as f:
    json.dump(split_info,f,indent=4)