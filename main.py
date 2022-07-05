import math, re, os
from collections import Counter
from datetime import date
from pathlib import Path
WORD = re.compile(r"/w+")
DATE = str(date.today())
ROOT = os.path.abspath(os.getcwd())
SCAN_MAX_SIZE = 5000#MB
WEBSHELL_LIBRARY_PATH = "C:/Users/USER/Desktop/phpshellcheck/phpWebshellLibrary/"
COMMON_KEYWORDS = [ 'shell','newfile','newfolder',
                    'password','passwd','upload',
                    'hacked','linux','windows',
                    'base_64','hacker','shell_exec',
                    'base64_decode','chmod','php_uname',
                    'passthru','shell_exec','pass']

WebShellArchive = 'CapturedWebShell'+DATE
try: os.mkdir(WebShellArchive,0o666)
except FileExistsError: pass
diary = Path(WebShellArchive+'/!!'+DATE+'REPORT.txt')
diary.touch(exist_ok=True)
reporter = open(diary, "a")

# Get the Cosine Similarity
def theMathemetician(v1, v2):
    intrsct = set(v1.keys()) & set(v2.keys())
    numr = sum([v1[x]*v2[x] for x in intrsct])
    s1 = sum([v1[a]**2 for a in list(v1.keys())])
    s2 = sum([v2[a]**2 for a in list(v2.keys())])
    denom = math.sqrt(s1) * math.sqrt(s2)
    if not denom: return 0.0
    else: return float("{:.2f}".format(float(numr) / denom))

# Convert Text to Vector
def theVectorer(text):
    words = WORD.findall(text)
    return Counter(words)

# Archives the sample
def theArchiver(stringtowrite,fileName,origin,trigger):
    filename = Path('./CapturedWebShell'+DATE+'/CapturedWebShell'+fileName)
    filename.touch(exist_ok=True)
    file = open(filename, "a")
    file.write("ORIGINAL FILE: "+str(str(origin).encode("utf-8"))+"\nTRIGGER: "+str(str(trigger).encode("utf-8"))+"\ndie('Shell Disabled')\n\n")
    file.write(str(str(stringtowrite).encode("utf-8")))
    file.close()

print(""" _____ _____ _____ _____ _____ _____ __    __
|  _  |  |  |  _  |   __|  |  |   __|  |  |  |
|   __|     |   __|__   |     |   __|  |__|  |__
|__|  |__|__|__|  |_____|__|__|_____|_____|_____|
 _____ _____ _____ _____ _____ _____ _____
|   __|     |  _  |   | |   | |   __| __  |
|__   |   --|     | | | | | | |   __|    -|
|_____|_____|__|__|_|___|_|___|_____|__|__|
""")

fileCount = 0
suspicious = 0
for folder, subfolders, files in os.walk(ROOT):
    for fileToCheck in files:
        if not os.path.getsize(os.path.join(folder, fileToCheck)) >= SCAN_MAX_SIZE:
            fileCount+=1
            # print ('checking: '+os.path.join(folder, fileToCheck)[0:35])
            f1 = open(str(os.path.join(folder, fileToCheck)), 'rb').read()
            for folder2, subfolders2, files2 in os.walk(WEBSHELL_LIBRARY_PATH):
                iteration = 0
                for shellComparison in files2:
                    iteration+=1
                    f2 = open(str(os.path.join(folder2, shellComparison)), 'rb').read()
                    vector1 = theVectorer(str(f1))
                    vector2 = theVectorer(str(f2))
                    # print('checking '+fileToCheck+' with: '+shellComparison+': '+str(theMathemetician(vector1, vector2)))
                    if len(f2) <= 11:
                        # print('Not worth of intersection calculation')
                        break
                    elif theMathemetician(vector1, vector2) >= 0.3:
                        # print(str(os.path.join(folder, fileToCheck))+" and "+str(os.path.join(folder2, shellComparison))+" =====> Cosine:"+str(theMathemetician(vector1, vector2))+"!!!")
                        print('cossimm:'+str(os.path.join(folder, fileToCheck))+": "+str(theMathemetician(vector1, vector2)*100)+"%")
                        suspicious+=1
                        try:
                            reporter.write("\n SUSPECTED as "+ shellComparison +"\t | , Confidence:"+str(theMathemetician(vector1, vector2)*100)+"% -->: "+str(os.path.join(folder, fileToCheck)))
                            theArchiver(f1,''+str(suspicious)+'.txt',str(os.path.join(folder, fileToCheck)),shellComparison)
                            # print('Scan for '+str(fileToCheck)+' done through '+str(iteration)+' comparisons')
                            break
                        except:
                            reporter.write("Reporting Error at fileToCheck" + str(fileCount))
                            break
                if suspicious != suspicious+1:
                    # print('Checking for common keywords...')
                    res = [element for element in COMMON_KEYWORDS if(element in str(f1))]
                    if len(res) >= 1:
                        # print('SUSPECTED as COMMON KEYWORD: '+str(res) +'\t | , Confidence:COMM -->: '+str(os.path.join(folder, fileToCheck)))
                        print('word(s):'+str(res) +' at '+str(os.path.join(folder, fileToCheck)))
                        suspicious+=1
                        reporter.write("\n SUSPECTED as COMMON KEYWORD: "+str(res)+"\t | , Confidence:???% -->: "+str(os.path.join(folder, fileToCheck).encode("utf-8")))
                        theArchiver(f1,''+str(suspicious)+'.txt',str(os.path.join(folder, fileToCheck)),str(res))
                # print('content: '+str(f1))
reporter.close()
print('Scanned '+str(fileCount)+' Files and '+str(suspicious)+' Files Suspected!')