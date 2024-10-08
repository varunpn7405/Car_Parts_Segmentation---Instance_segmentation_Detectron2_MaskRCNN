import os,shutil
from PIL import Image

def convert_rgba_to_rgb(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        ext=os.path.splitext(filename)[-1]

        if ext.lower() in [".png",".jpg",".jpeg"]:
            img_path = os.path.join(folder_path, filename)
            fout=os.path.join(ouFolder, f"{filename}")
            Flag=False

            try:
                # Open the image
                img = Image.open(img_path)
                
                if img.mode == 'P':
                    img = img.convert('RGBA')
                # Check if the image is in RGBA mode
                if img.mode == 'RGBA':
                    Flag=True
                    print(f"Found RGBA image: {filename}, converting to RGB")
                    # Convert RGBA to RGB
                    # Extract the alpha channel
                    rgb_img = img.convert('RGB')
                    # Save the converted image (you can overwrite or save as a new file)
                    rgb_img.save(fout)
                # else:
                #     print(f"{filename} is not an RGBA image")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
            
            if not Flag:
                shutil.copy(img_path,fout)

# Path to the folder containing images
folder_path = "images"
ouFolder="input_imgs\converted_images"
os.makedirs(ouFolder,exist_ok=True)
convert_rgba_to_rgb(folder_path)
