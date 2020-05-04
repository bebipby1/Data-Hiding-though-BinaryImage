import cv2
import numpy as np

class Program:

    path = ""
    def __init__(self, path):
        self.path = path

    def convertImageToBinaryImage(self):
        img = cv2.imread(self.path, 0)
        #cv2.imshow('image', img)
        #cv2.waitKey(0)
        mat, bw = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
        np_img = np.array(bw)#black and white
        return  np.where(np_img == 255, 1, 0)

    def convertTextToBinary(self, s):
        st = ' '.join(format(ord(x), '08b') for x in s)
        return st
    def matrixMul(self, m1, m2):
        rs = []
        for i in range(len(m1)):
            ar = []
            for j in range(len(m1)):
                if m1[i][j] == 0:
                    ar.append(0)
                else:
                    ar.append(m2[i][j])
            rs.append(ar)
        return rs

    def maxTrixChangeBit(self, m, pos):
        m = np.array(m)
        for i in range(len(pos)):
            x = pos[i][0]
            y = pos[i][1]

            val = 0
            if m[x][y] == 0:
                val = 1
            m[x][y] = val

        return np.matrix(m)

    def encode(self, f, k, w, bit):
        t = np.array(np.bitwise_xor(f, k))

        #convert matrix to array
        f = np.array(f)
        k = np.array(k)
        #sum * w
        s = self.matrixMul(t, w)

        #sum s
        su = np.sum(s)

        #get d
        d = (int(bit, 2) - su) % pow(2, len(bit))

        posBitwise = []
        r = len(bit)

        if d != 0:
            jk = self.calcS(w,t,d, bit)
            if jk is not None:
                posBitwise.append(jk)
            else:
                #tim so tu nhien h in {1,2,3,..2r-1} nho nhat sao cho Shd != null va Sd-hd != null
                for h in range(1,pow(2,r) - 1):
                    jk = self.calcS(w,t,h, bit)
                    if jk is not None:
                        h2 = pow(2,r) + (d-h)
                        uv = self.calcS(w,t,h2, bit)
                        if uv is not None:
                            posBitwise.append(jk)
                            posBitwise.append(uv)
                            break

        return self.maxTrixChangeBit(f,posBitwise)

    def calcS(self, w, t, d, bit):
        for i in range(len(t)):
            if d in w[i]:
                pos = np.where(w[i] == d)
                if t[i][pos] == 0:
                    return [i, pos]
            elif (pow(2, len(bit)) - d) in w[i]:
                pos = np.where(w[i] == (pow(2, len(bit)) - d))
                if t[i][pos] == 1:
                    return [i, pos]
        return None

    def decode(self, f, k, w, r):

        t = np.array(np.bitwise_xor(f, k))
        # convert matrix to array
        f = np.array(f)
        k = np.array(k)
        w = np.array(w)

        # sum
        t = np.array(t)

        # sum * w
        s = self.matrixMul(t, w)

        # sum s
        su = np.sum(s)

        # print(su % (pow(2,)))
        result = (su % (pow(2, r)))
        print(format(result, '08b'))

    def splitMatrix_Row(self,f, r, soluongChu, row):
        rs = []
        for j in range(soluongChu):
            fsp = f[row:row + r, j * r:j * r + r]
            if np.size(fsp, 0) == 0 or np.size(fsp, 1) < r:
                break
            else:
                rs.append(fsp)
        return rs

    def splitMatrix(self,f, r, soluongChu):
        rs = []
        sl = soluongChu
        i = 0
        while (len(rs) < soluongChu):
            kq = self.splitMatrix_Row(f, r, sl, i)
            for mt in kq:
                rs.append(mt)
            sl = soluongChu - len(rs)
            i += r
            if (sl > 0 and i >= np.size(f, 0)):
                print("Hinh anh k  du kich thuoc")
                break

        return rs

    def convert(self, k, w, r):
        np_img_arr = program.convertImageToBinaryImage()
        st = program.convertTextToBinary("anh")
        print("==== truoc khi giau ====")
        print(st)

        i = 0
        j = 0
        row = 0
        rs = []
        while (" " in st):
            pos = st.index(" ")
            bit = st[0:pos]
            st = st[pos + 1:]
            f = np_img_arr[row : row + r, j * r : j * r + r]
            rs.append(self.encode(f, k, w, bit))

            j+=1

        bit = st
        f = np_img_arr[row: row + r, j * r: j * r + r]
        rs.append(self.encode(f, k, w, bit))

        print("======sau khi giau file=====")
        return rs

r = 16
k = np.matrix([[1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
           [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
           [1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0],
           [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0],
           [0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0],
           [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1],
           [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
           [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
           [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
           [1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
           [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]])

w = [[208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223],
     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
     [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47],
     [144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159],
     [240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255],
     [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63],
     [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95],
     [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207],
     [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
     [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143],
     [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
     [160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175],
     [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
     [176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191],
     [224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239],
     [112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127]]

program = Program('./img/icon.png')
#
rs = program.convert(k,w,r)
for xxx in rs:
    program.decode(xxx,k,w,r)