import os
# threshold_size = 500
for folder, subfolders, files in os.walk('./Php'):
    for file in files:
        print (os.path.join(folder, file))
#       filePath = os.path.join(folder, file)
#       if os.path.getsize(filePath) >= threshold_size:
#           print (filePath, str(os.path.getsize(filePath)/1000)+"kB")