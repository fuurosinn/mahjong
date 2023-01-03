import cv2
import pyautogui as pag
import numpy as np
from PIL import Image

reg = [(823, 536, 47, 35), (1048, 536, 47, 35), (1040, 391, 46, 33), (832, 391, 47, 31)]
#rivr = [((800, 577, 305, 50), (800, 630, 312, 51), (792, 682, 322, 56)), ((), (), ()), ((), (), ()), ((), (), ())] # 河の読み取る位置、自分から右回りに0, 1, 2, 3で上から0, 1, 2
l = [9, 9, 9, 7]
k = {0:"m", 1:"p", 2:"s", 3:"z"}
# k_ = {"m":0, "p":1, "s":2, "z":3}
wind = {0:"east", 1:"south", 2:"west", 3:"north"}
acc = 0.99
bx = 349
by = 903
wx = 77
wy = 111
wx_ = 78.5
bxe = 1367
bye = 1014
bxet = 26 # 自摸牌の左端と手牌の右端の隙間
uin = ["ツモ", "ロン", "荒牌流局"] # ui name

def startup():
    global img, hands, ret, wind, imgn, ui
    img = []
    hands = []
    ret = []
    imgn = [] # image num
    ui = [] # ボタンとか全般。ツモ、ロン。

startup()

def read():
    global img, imgn
    img.clear()
    for i in range(len(l)): # 牌の読み込み
        img.append([])
        for ia in range(l[i]):
            x = cv2.imread("./pi/{}.png".format(str(ia + 1) + k[i]))
            x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
            img[-1].append(x)
    for i in range(3):
        x = cv2.imread("./pi/5r{}.png".format(k[i]))
        x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        img[i].append(x)

    imgn.clear()
    for i in range(10): # 数字の読み込み
        x = cv2.imread("./num/{}.png".format(i))
        x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        imgn.append(x)

    ui.clear() # ui関連の読み込み
    x = cv2.imread("./mark/tsumo.png") # tsumo
    x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    ui.append(x)
    x = cv2.imread("./mark/ron.png") # ron
    x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    ui.append(x)
    x = cv2.imread("./mark/confirmation.png") # 聴牌流局とかの時に右下に出る確認マークの奴
    x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
    ui.append(x)

read()

"""
def temp(): # テンプレートマッチング。d ==> 牌の画像
    tm = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
#    tm = cv2.cvtColor(tm, cv2.COLOR_BGR2RGB)
    p = None
    resm = 0 # result max
    for i in range(len(img)): # st()からコピーしてきた↓
        for ia in range(len(img[i])):
            if ia != 9:
                pn = str(ia + 1) + k[i]
            else:
                pn = "5r" + k[i]
            res = cv2.matchTemplate(tm, img[i][ia], cv2.TM_CCOEFF_NORMED) # tm ==> temp
            x, y = np.unravel_index(np.argmax(res), res.shape)
            z = res[x][y]
            print("pn = {0}, res = {1}".format(pn, res))
            if z > 0.8 and z > resm:
                resm = z
                p = pn
    return p, resm # ↑
"""

def st(t = 13): # 自摸牌の画像認識。 t ==> 手牌の枚数。
    s = pag.screenshot(region=(bx + wx_ * t + bxet, by, wx, wy)) # bx + wx_ * t + bxet ==> 自摸牌の一番左端のx座標算出する式
    s.save("./pi/hands.png")
    sg = cv2.imread("./pi/hands.png")
    sg = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)
    p = None
    resm = 0 # result max
    for ia in range(len(img)):
        for ib in range(len(img[ia])):
            if ib != 9:
                pn = str(ib + 1) + k[ia]
            else:
                pn = "5r" + k[ia]
            res = cv2.matchTemplate(sg, img[ia][ib], cv2.TM_CCOEFF_NORMED)
            x, y = np.unravel_index(np.argmax(res), res.shape)
            z = res[x][y]
#            print("{1}:z = {0}".format(z, pn))
            if z > 0.8 and z > resm:
                resm = z
                p = pn
    return p, resm

def ss(t): # 手牌の画像認識
    ret.clear()
    for i in t:
        sx = int(bx + wx_ * i)
        s = pag.screenshot(region=(sx, by, wx, wy))
        s.save("./pi/hands.png")
        sg = cv2.imread("./pi/hands.png")
        sg = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)
        p = ""
        a = 0
        for ia in range(len(img)):
            for ib in range(len(img[ia])):
                b = 0
                res = cv2.matchTemplate(sg, img[ia][ib], cv2.TM_CCOEFF_NORMED)
                x, y = np.where(res >= acc)
                for ic in range(len(x)): # 改善可能↓
                    c = res[x[ic], y[ic]]
                    if c > b:
                        b = c
#                        print("acc ==> " + str(c))
                if len(x) != 0:
                    if ib != 9:
                        pn = str(ib + 1) + k[ia]
                    else:
                        pn = "5r" + k[ia]
                    if b > a:
                        a = b
                        p = pn # 改善可能↑
        if p == "":
            ret.append(i)
        else:
            hands.append(p)

def main(t = 13):
    global acc
    counter = 0
    acc = 0.99
    hands.clear()
    while len(hands) == 0: # while 急に追加したから動くかどうかわからない。
        ss(range(t))
    while len(ret) != 0 and counter < 5:
        counter += 1
        acc -= 0.01 * 2 ** counter
        ss(tuple(ret))
    if (len(hands) - 1) % 3 != 0:
        print("ERROR:INSUFFICIENT NUMBER OF PAI!!")
    if counter >= 5:
        print("SCANNING:" + str(len(hands)) + " times") #        print("ERROR:FAILED TO SCAN HANDS!!")
        return tuple(hands)
    else:
#        print(hands)
        return tuple(hands)

# main(13)
# main(range(13))

mk = [] # mark

def mark():
    global mk
    mk = [[] for i in range(len(reg))]
    for i in range(len(reg)):
        s = pag.screenshot(region=(reg[i]))
        s.save("./game/ui/wind.png")
        sg = cv2.imread("./game/ui/wind.png")
        sg = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)
        mark = ""
        resm = 0 # result max
        for ia in range(4):
            temp = cv2.imread("./mark/mark_{0}{1}.png".format(wind[ia], i))
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(sg, temp, cv2.TM_CCOEFF_NORMED)
            x, y = np.unravel_index(np.argmax(res), res.shape) # test
            z = res[x][y]
            if z > resm:
                resm = z
                mark = ia #                mark = wind[ia] エラー出たら元に戻しとけ。
        mk[i] = [mark, resm]
    for i in range(len(reg)):
        if mk[i][0] == "east":
            mark = mk[(4 - i) % 4][0]
            resm = mk[(4 - i) % 4][1]
            break
    print("wind ==> {0} ({1:.2f}%)".format(mark, resm * 100))
    return mark

def re(): # 残りの山の枚数
    r = ((953, 484, 21, 20), (972, 484, 21, 20)) # ssする範囲
    n_ = ""
    for i in range(2):
        resm = 0 # result max
        n = ""
        for ia in range(len(imgn)):
            s = pag.screenshot(region=(r[i]))
            s.save("./num/num.png")
            sg = cv2.imread("./num/num.png")
            sg = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(sg, imgn[ia], cv2.TM_CCOEFF_NORMED)
            x, y = np.unravel_index(np.argmax(res), res.shape) # copy from mark()
            z = res[x][y]
            if z > resm:
                resm = z
                n = ia
        n_ += str(n)
    return n_

def chend(): # check end ==> chend, 和了が発生したかどうか判断。
    s = pag.screenshot(region=(1612, 129, 287, 158))
    s.save("./mark/chend.png")
    sg = cv2.imread("./mark/chend.png")
    sg = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)
    for i in range(2):
        res = cv2.matchTemplate(sg, ui[i], cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(np.argmax(res), res.shape)
        z = res[x][y]
#        print("DEF:chend() acc = " + str(z))
        if z > 0.98:
            print("END " + str(uin[i]))
            return True, i # 0 ==> ツモ, 1 ==> ロン, 2 ==> 流局
    s = pag.screenshot(region=(1578, 926, 130, 66)) # ↓流局時の処理
    s.save("./mark/chend.png")
    sg = cv2.imread("./mark/chend.png")
    sg = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(sg, ui[2], cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(np.argmax(res), res.shape)
    z = res[x][y]
    if z > 0.98:
        print("END " + str(uin[2]))
        return True, 2 # ↑
    return False, "NASHI"

if __name__ == "__main__":
    msg = chend()
    if msg != None:
        print(msg)
    else:
        print(main(13))
        mark()
        print(re())
#    riv(0, 0)