f = open('basic_info/69636.txt','r')
lines =  list(f.xreadlines())

music_name = lines[0]
artist = lines[1]
album_name = lines[2]
description = lines[3]
print len(lines)