from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog, messagebox
from PIL import Image

def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b')) # 8bits
    return newd

def modPix(pix, data): # get lsb from pix and fill with data
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]] # get 3 pixels

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encodeEnc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(img_path, message, output_path):
    image = Image.open(img_path, 'r')
    if (len(message) == 0):
        raise ValueError('Data is empty')
    newimg = image.copy()
    encodeEnc(newimg, message)
    newimg.save(output_path, str(output_path.split(".")[1].upper()))

def decode(img_path):
    image = Image.open(img_path, 'r')
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def browseImage():
    filename = filedialog.askopenfilename()
    return filename

def saveImage():
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    return filename

def encodeGui(output_text):
    img_path = browseImage()
    if not img_path:
        return
    message = simpledialog.askstring("Input", "Enter the message to encode:")
    if not message:
        return
    output_path = saveImage()
    if not output_path:
        return
    try:
        encode(img_path, message, output_path)
        output_text.insert(END, "Message encoded and saved successfully!\n")
    except Exception as e:
        output_text.insert(END, f"Error: {str(e)}\n")

def decodeGui(output_text):
    img_path = browseImage()
    if not img_path:
        return
    try:
        message = decode(img_path)
        output_text.insert(END, f"Decoded message: {message}\n")
    except Exception as e:
        output_text.insert(END, f"Error: {str(e)}\n")

def main():
    root = Tk()
    root.title("Outguess Steganography")

    button_frame = Frame(root)
    button_frame.pack(pady=10)

    output_text = Text(root, height=10, width=50)
    output_text.pack(pady=10)

    encode_button = Button(button_frame, text="Encode", command=lambda: encodeGui(output_text))
    encode_button.pack(side=LEFT, padx=5)

    decode_button = Button(button_frame, text="Decode", command=lambda: decodeGui(output_text))
    decode_button.pack(side=LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()