import io
import sys
import os

def readDataOffset(dat):
    dat.seek(0x14, 0)  # Go to 0x14 in the file
    i = int.from_bytes(dat.read(4), byteorder="little") # Get starting position of data.
    i = i + 0x6DC0 #Offset further by length of garbage data
    return i

def exportToTextFile(filename):
    with open(filename, 'rb') as datastream:
        dat = io.BytesIO(datastream.read())
    offset = readDataOffset(dat)
    size = dat.getbuffer().nbytes
    print("Found data offset at " + str(offset))
    dat.seek(offset, 0)
    bytes_to_read = 2
    blank_char = b'\x00\x00'
    output = ""
    printed_space = False
    while dat.tell() != size:
        char = dat.read(bytes_to_read)
        if char != blank_char:
            output += char.decode('utf-16').rstrip('\r')
            printed_space = False
        elif char == blank_char:
            if not printed_space:
                output += " \n"
                printed_space = True
    f = open(filename + ".txt", "w", encoding="utf-16")
    f.write(output.rstrip())
    f.close()

def main():
	rootdir = os.path.dirname(__file__) + '\\TempData\\resource\\subtitles'
	list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
	for i in range(0,len(list)):
		path = os.path.join(rootdir,list[i])
		if os.path.isfile(path):
			exportToTextFile(path)

main()
print("Operation Complete")