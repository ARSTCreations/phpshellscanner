import math, re, os
from collections import Counter
from datetime import date
from pathlib import Path
WORD = re.compile(r"/w+")
DATE = str(date.today())
ROOT = os.path.abspath(os.getcwd())
SCAN_MAX_SIZE = 1000
SHELL_LIBRARY_PATH = "C:/Users/USER/Desktop/PHPSHELLCHECKER/phpWebshellLibrary"

diary = Path(DATE+'REPORT.txt')
diary.touch(exist_ok=True)
reporter = open(diary, "a")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator: return 0.0
    else: return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

fileCount = 0
suspicious = 0
for folder, subfolders, files in os.walk(ROOT):
    for file in files:
        if not os.path.getsize(os.path.join(folder, file)) >= SCAN_MAX_SIZE:
            fileCount+=1
            print ('checking: '+os.path.join(folder, file))
            f1 = open(str(os.path.join(folder, file)), 'rb').read()
            for folder2, subfolders2, files2 in os.walk(SHELL_LIBRARY_PATH):
                iteration = 0
                for file2 in files2:
                    iteration+=1
                    f2 = open(str(os.path.join(folder2, file2)), 'rb').read()
                    vector1 = text_to_vector(str(f1))
                    vector2 = text_to_vector(str(f2))
                    # print('checking '+file+' with: '+file2+': '+str(get_cosine(vector1, vector2)))
                    if get_cosine(vector1, vector2) >= 0.3:
                        print(str(os.path.join(folder, file))+" and "+str(os.path.join(folder2, file2))+" =====> Cosine:"+str(get_cosine(vector1, vector2))+"!!!")
                        suspicious+=1
                        try:
                            reporter.write("\n SUSPECTED as "+ file2 +"\t | , Confidence:"+str(get_cosine(vector1, vector2)*100)+"% -->: "+str(os.path.join(folder, file)))
                            break
                        except:
                            reporter.write("Reporting Error at file" + str(fileCount))
                            break
                print('Scan for '+str(file)+' done through '+str(iteration)+' libraries')
                # print('content: '+str(f1))
reporter.close()
print('Scanned '+str(fileCount)+' Files!')
print(str(suspicious)+' Files Detected!')