import os

files = os.listdir("../corpus")
fwrite = open('text_content.txt', 'w')

for filename in files:
    f = open("../corpus/" + filename, 'r', encoding="utf8")
    fwrite.write(f.read())
    fwrite.write('\n')
fwrite.close()
