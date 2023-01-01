import copy

l = [9, 9, 9, 7] # mpszの牌の種類数
pk = {"m":0,"p":1,"s":2,"z":3} # mpsz変換
nm = {2:"t", 3:"k"} # 4枚以降も追加すれば処理可能

def sep(x): # 入力データ変換関数
    p = [[0 for ia in range(l[i])] for i in range(len(l))]
    for i in range(len(x)):
        p[pk[x[i][1]]][int(x[i][0]) - 1] += 1
    return tuple(p)

def s(p, br): # 順子, 両面, 嵌張, 辺張, 孤立牌の仕分け
    x = 0
    p_ = list(p)
    br_ = list(br)
    for i in range(2):
        p_.append(0)
    while x < 8:
        while x < 8 and p_[x] == 0:
            x += 1
        y = 0
        for i in range(3):
            if p_[x + i] > 0:
                y += 2 ** i
                p_[x + i] -= 1
        if y == 7:
            br_.append("s" + str(x))
        elif y == 5:
            br_.append("b" + str(x))
        elif y == 3:
            br_.append("a" + str(x))
        elif y == 1:
            br_.append("c" + str(x))
    return tuple(br_)

def d(p, cl, n=2, br=[]): # p ==> 入力された手牌, 対子, 刻子系処理
    pa = list(p)
    bl = []
    for i in range(len(p)):
        if pa[i] >= n:
            bl.append(i)
    for i in range(2 ** len(bl)):
        key = bin(i)[2:]
        key = "0" * (len(bl) - len(key)) + key
        pb = copy.copy(pa)
        br_ = copy.copy(br)
        for ia in range(len(key)):
            if key[ia] == "1":
                pb[bl[ia]] -= n
                br_.append(nm[n] + str(bl[ia])) # 取り除いた番号
        if n == list(nm.keys())[-1]: # 指定された奴(n=2で開始e=3の場合は対子から刻子まで)まで分割を試行したら順子へ。
            if cl == len(l) - 1: # 字牌の場合
                for ia in range(l[-1]): # 孤立牌のみ追加する
                    if pb[ia] == 1:
                        br_.append("c" + str(ia))
                h[cl].append(br_)
            else: # 字牌でない場合
                h[cl].append(s(pb, br_))
        else:
            d(pb, cl, n + 1, br_)

def choice(n=0, m=0, t=0, a=0, c=0):
    global sha, dr, dr_
    if n == len(l):
        s = 2 * (4 - fr - m)
        t_ = t
        if t_ > 0:
            t_ -= 1
            s -= 1
        s -= a
        if m + t_ + a > 4:
            s += 4 - m + t_ + a
        if s <= sha:
            if s < sha:
                sha = s
                dr = []
            dr.append(tuple(dr_))
        return
    elif n == 0:
        dr = []
        dr_ = []
    dr_.append(0)
    if len(h[n]) == 0:
        choice(n + 1, m_, t_, a_, c_)
    else:
        for i in range(len(h[n])):
            dr_[-1] = i
            m_, t_, a_, c_ = m, t, a, c
            x = h[n][i] # 調べる対象
            for ia in range(len(x)):
                if x[ia][0] == "k" or x[ia][0] == "s":
                    m_ += 1
                elif x[ia][0] == "t":
                    t_ += 1
                elif x[ia][0] == "a" or x[ia][0] == "b":
                    a_ += 1
                elif x[ia][0] == "c":
                    c_ += 1
            choice(n + 1, m_, t_, a_, c_)
    del dr_[-1]

def z(p):
    global div, h, px, fr, dr, dr_, sha
    div = []
    h = [[] for i in range(len(l))] # 分け方
    px = list(sep(p))
    fr = int((14 - len(p)) / 3)
    dr = []
    dr_ = []
    sha = 8

    for i in range(len(l)): # 各牌に対して処理
        d(px[i], i)
    choice() # 選別
    for i in range(len(dr)): # 番号指定
        div.append([])
        for ia in range(len(l)): # 色
            div[-1].append(h[ia][dr[i][ia]])
        print(div[-1])
    print("向聴数:" + str(sha))
    return div

if __name__ == "__main__":
    print(z(["1m", "1m", "1m", "2m", "2m", "2m", "3m", "3m", "3m", "4m", "4m", "4m", "5m", "5m"]))