import base64

def getBase64(filename):
    try:
        fin = open(filename, "rb")
        data = fin.read()
    finally:
        fin.close()
    return base64.encodestring(data)

#print getBase64("groovy.gif")
print getBase64("Graphics/transparent.gif")