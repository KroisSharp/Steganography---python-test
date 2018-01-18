from PIL import Image
import binascii
import optparse

def rgb2hex(r,g,b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def hex2rgb(hexcode):
        return tuple(map(ord,hexcode[1:].decode('hex')))

def str2bin(msg):
    binary = bin(int(binascii.hexlify(msg),16))
    return binary[2:]

def bin2str(binary):
    msg = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
    return msg

def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2','3','4','5'):
        hexcode = hexcode[:-1]+digit
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0','1'):
        return hexcode[-1]
    else:
        return None



def hide(filename, msg):
    img = Image.open(filename)
    binary = str2bin(msg) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        NewData = []
        digit = 0;
        temp = ''
        for i in datas:
            if (digit < len(binary)):
                newpix = encode(rgb2hex(i[0], i[1], i[2]), binary[digit])
                if newpix == None:
                    NewData.append(i)
                else:
                        r,g,b = hex2rgb(newpix)
                        NewData.append((r,g,b,255))
                        digit += 1
            else:
                NewData.append(i)
        img.putdata(NewData)
        img.save(filename,"PNG")
        return "Done"
    return "Error"




def retr(filename):
    img = Image.open(filename)
    binary = ''

    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()

        for i in datas:
            digit = decode(rgb2hex(i[0],i[1],i[2]))
            if digit == None:
                pass
            else:
                binary = binary + digit
                if (binary[-16:] == '1111111111111110'):
                    print ("Success")
                    return bin2str(binary[:-16])
        return bin2str(binary)
    return "error"



def Main():
    parser = optparse.OptionParser('usage %prog ' + \
        '-e/-d <target file>')
    parser.add_option('-e', dest='hide', type='string', \
        help='target picture path to hide text')
    parser.add_option('-d', dest='retr', type='string', \
        help='target picture to hide retrive text')
    (options, args) = parser.parse_args()
    if (options.hide != None):
        text = raw_input("enter massage to hide")
        print (hide(options.hide, text))
    elif (options.retr != None):
            print(retr(options.retr))
    else: 
        print (parser.usage)
        exit(0)


if __name__ == '__main__':
    Main()