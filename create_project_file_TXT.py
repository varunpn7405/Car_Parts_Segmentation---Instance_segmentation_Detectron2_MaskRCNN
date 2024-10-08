import json
import random

with open("classes.txt") as f:
    prjt_data=f.readlines()

attr_list=[]
unique_lst=[]

for cls in prjt_data:
    cls = cls.replace("\n","")
    cls = cls.strip()
    if cls:
        if cls not in unique_lst:
            unique_lst.append(cls)

            if len(cls) >80:
                print(cls,len(cls))

            id_val=random.randint(1000000000,4000000000)
            hexadecimal = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])

            template=  {
            "name": cls,
            "id": id_val,
            "color": hexadecimal,
            "type": "any",
            "attributes": []
            }

            attr_list.append(template)

        else:
            print("Class repeat!!",cls)    

with open("projectFile_2.json","w") as f:
    json.dump(attr_list,f,indent=4)

    



