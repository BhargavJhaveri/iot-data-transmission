import os
import zipfile

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()


zip('/Users/bhargav/Study/Study/Sem-II/IoT/Homework/HW2/TextFile/dummy.txt', '/Users/bhargav/Study/Study/Sem-II/IoT/Homework/HW2/TextFile/dummy.txt')

data_file = open('/Users/bhargav/Study/Study/Sem-II/IoT/Homework/HW2/TextFile/dummy.txt.zip','rb')


packet_size = 1024

# Convert data into bits.
data_to_send = 'start'

def read_in_chunks(input_file, chunk_size=1024*64):
    chunk = input_file.read(chunk_size)
    return chunk
        
def send_data(data):
    print data

def string_to_bits(string_data):
    return ''.join(bin(ord(ch))[2:].zfill(8) for ch in string_data)

while(data_to_send):
    data_to_send = read_in_chunks(data_file,packet_size)
    send_data(string_to_bits(data_to_send))



