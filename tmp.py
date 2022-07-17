import os, re

r = re.compile("MID\d{5}_FID\d{5}.h5")
for root, dir, files in os.walk(r"C:\Users\z0048drc\Desktop\data_fm\MRCP\PF_o"):
    for file in files:
        m = r.match(file)
        if m:
            print(m.group())
