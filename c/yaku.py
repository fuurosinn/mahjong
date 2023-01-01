l = [9, 9, 9, 7]
w = {0:"東", 1:"南", 2:"西", 3:"北", 4:"白", 5:"發", 6:"中"}
pk_ = {"m":0, "p":1, "s":2, "z":3}

def fu():
    x = 20
    if not s[2] and s[4] != -1:
        x += 10
    elif s[2]:
        x += 2
    for i in range(len(p)):
        for ia in range(len(f[i])):
            y = f[i][ia]
            if y[0] == "t":
                continue
            if y[0] == "p":
                x += 4 if y[1] in ("0", "8") or ia == 3 else 2 # 么九牌, 中張牌
            elif y[0] in ("d", "k"): # 大明槓,加槓
                x += 16 if y[1] in ("0", "8") or ia == 3 else 8
            elif y[0] == "a":
                x += 32 if y[1] in ("0", "8") or ia == 3 else 16
        for ia in range(len(p[i])):
            y = p[i][ia]
            if y[0] == "t" and i == 3:
                if int(y[1]) in (s[0], s[1]): # 連風牌
                    x += 4
                elif int(y[1]) in (s[0], s[1], 4, 5, 6):
                    x += 2
            elif y[0] == "k":
                z = 4 if y[1] in ("0", "8") or ia == 3 else 2
                if pk_[s[3][1]] == i and s[3][0] == y[1]:
                    if all("s" + str(ib) not in p[i] for ib in (int(s[3][0]), int(s[3][0]) - 2)):
                        x += z
                    else:
                        x += 2 * z
                else:
                    x += 2 * z

pass

def yakuhai():
    x = []
    for i in range(l[3]):
        if "k" + str(i) in p[3] or any(ia + str(i) in f[3] for ia in ("p", "a", "d", "k")): # ポン, 暗槓, 大明槓, 加槓
            x.append(True)
        else:
            x.append(False)
    if x[s[0]]:
        yaku.append("場風:" + w[s[0]])
    if x[s[1]]:
        yaku.append("自風:" + w[s[1]])
    for i in range(4, 7):
        if x[i]:
            yaku.append("三元牌:" + w[i])
    y = x[:4].count(True) # 四喜和系統
    if y == 4:
        yaku.append("大四喜")
        return
    elif y == 3 and "t" + str(x[:4].index(False)) in p[3]:
        yaku.append("小四喜")
        return
    y = x[4:7].count(True) # 三元系統
    if y == 3:
        yaku.append("大三元")
        return
    elif y == 2 and "t" + str(x[4:7].index(False)) in p[3]:
        yaku.append("小三元")

def allgreen():
    if any(len(p[i]) + len(f[i]) != 0 for i in (0, 1)): # 萬子筒子がある場合 っていうか清一色混一色成立時に呼び出せばいいのでは…?
        return
    if len(p[3]) + len(f[3]) != 0 and any(str(i) in str(p[3]) + str(f[3]) for i in (0, 1, 2, 3, 4, 6)): # 手牌と副露の字牌に、發以外が混じっている場合
        return
    if any(p[2][i] not in ("s1", "t1", "t2", "t3", "t5", "t7", "k1", "k2", "k3", "k5", "k7") for i in range(len(p[2]))):
        return
    if any(str(i) in str(f[2]) for i in (0, 4, 6, 8)): # 1, 5, 7, 9sが副露に含まれる場合
        return
    yaku.append("緑一色")

def ninegates():
    z = [3, 1, 1, 1, 1, 1, 1, 1, 3]
    x = [0 for i in range(9)]
    n = pk_[s[3][1]]
    for i in range(len(p[n])):
        y = int(p[n][i][1])
        if p[n][i][0] == "t":
            x[y] += 2
        elif p[n][i][0] == "k":
            x[y] += 3
        elif p[n][i][0] == "s":
            for ia in range(3):
                x[y + ia] += 1
    n = 0
    while x[n] == z[n]:
        n += 1
    if x[n] < z[n]:
        return False
    if int(s[3][0]) == n:
        yaku.append("純正九蓮宝燈")
    else:
        yaku.append("九蓮宝燈")
    return True

def flush():
    x = []
    for i in range(len(l)):
        if len(p[i]) + len(f[i]) != 0:
            x.append(True)
        else:
            x.append(False)
    y = x[:3].count(True)
    if y >= 2:
        return
    if y == 0:
        yaku.append("字一色")
        return
    if x[3]:
        yaku.append("混一色")
    else:
        yaku.append("清一色")
        if ninegates():
            return
    allgreen()

def tanyao():
    if len(p[3]) + len(f[3]) != 0:
        return
    if all(all("s" + str(ia) not in p[i] and "t" + str(ia) not in f[i] for ia in (0, 6)) and all(all(ib + str(ia) not in p[i] for ib in ("k", "t")) and all(ib + str(ia) not in f[i] for ib in ("p", "a", "d", "k")) for ia in (0, 8)) for i in range(len(3))):
        yaku.append("断么九")

def toitoi(): # 対々和系統
    if any(any(p[i][ia][0] == "s" for ia in range(len(p[i]))) for i in range(3)) or any(any(f[i][ia][0] == "t" for ia in range(len(f[i]))) for i in range(3)):
        return
    x = [[0, 0], [0, 0]] # [[明刻, 暗刻], [明槓, 暗槓]]
    for i in range(len(l)):
        if type(p[i]) == str: # 手牌側検索↓============
            if p[i][0] == "k": # 刻子
                x[0][1] += 1
        else:
            for ia in range(len(p[i])):
                if p[i][ia][0] == "k": # 刻子
                    x[0][1] += 1 # ↑==================
        if type(f[i]) == str: # 副露側検索↓============
            if f[i][0] == "p": # ポン
                x[0][0] += 1
            elif f[i][0] == "a": # 暗槓
                x[0][1] += 1 # 暗刻追加
                x[1][1] += 1 # 暗槓追加
            else: # "d", "k" (大明槓, 加槓)時
                x[0][0] += 1 # 明刻追加
                x[1][0] += 1 # 明槓追加
        else:
            for ia in range(len(f[i])):
                if f[i][ia][0] == "p": # ポン
                    x[0][0] += 1
                elif f[i][ia][0] == "a": # 暗槓
                    x[0][1] += 1
                    x[1][1] += 1
                else:
                    x[0][0] += 1
                    x[1][0] += 1 # ↑===================
    if sum(x[0]) != 4:
        return
    yaku.append("対々和")
    flag = True if "t" + s[3][0] in p[pk_[s[3][1]]] else False # 単騎か否か
    if flag: # 単騎待ちパターン(s[2](ツモかロンか)が条件に入らない)
        if x[0][1] == 3: # 三暗刻単騎成就パターン
            yaku.append("三暗刻")
        elif x[0][1] == 4: # 四暗刻単騎成就パターン
            yaku.append("四暗刻単騎")
    else: # シャボ待ちパターン
        if x[0][1] == 4: # 手牌に刻子4つ
            if not x[2]: # 上記の条件かつ攏和了 ==> 三暗刻対々和
                yaku.append("三暗刻")
            else: # 自摸パターン
                yaku.append("四暗刻") # ツモスーツモ成立
    if sum(x[1]) == 3: # 槓子3つ成立パターン
        yaku.append("三槓子")
    elif sum(x[1]) == 4: # 槓子4つ成立パターン
        yaku.append("四槓子")

def sevenpairs(): # 七対子
    if any(f[i] != () for i in range(len(l))): # 一回でも副露している ==> 七対子不成立
        return False
    x = 0
    for i in range(len(l)):
        if type(p[i]) == str:
            if p[i][0] == "t":
                x += 1
        else:
            for ia in range(len(p[i])):
                if p[i][ia][0] == "t":
                    x += 1
    if x == 7:
        yaku.append("七対子")
        return True
    elif x != 1:
        print("ERROR?:the number of pair is not 1. p={}".format(p))
    return False

def tsumo(): # 自摸系統
    if mz and s[3]: # 面前かつ自摸和了
        yaku.append("門前清自摸和")

def straight():
    if any(all("s" + str(ia) in p[i] or "t" + str(ia) in f[i] for ia in (0, 3, 6)) for i in range(3)):
        yaku.append("一気通貫")

def double():
    x = 0
    for i in range(3):
        ia = 0
        while ia < 9:
            y = p[i].count("s" + str(ia))
            if y == 4:
                yaku.append("二盃口")
                return
            elif y == 2:
                x += 1
                if x == 2:
                    break
        if x == 2:
            yaku.append("二盃口")
    if x == 1:
        yaku.append("一盃口")

def pinfu():
    if type(p[3]) == tuple or p[3][0] != "t" or any(int(p[3][1]) == i for i in (s[0], s[1], 4, 5, 6)) or any(len(f[i]) != 0 for i in range(len(l))) or any(any(p[i][ia][0] == "k" for ia in range(9)) for i in range(3)): # p[3]が複数個存在or(1個のみ存在かつそれが雀頭かつ役牌でない)or副露または暗槓しているor手牌に刻子がある
        return
    if int(s[3][0]) == 2 and "s" + str(s[3][0]) in p[pk_[s[3][1]]]: # 和了牌が数牌の3且つ345の順子が存在する場合
        yaku.append("平和")
    elif int(s[3][0]) == 6 and "s" + str(s[3][0] - 2) in p[pk_[s[3][1]]]: # 7で567の順子
        yaku.append("平和")
    elif any("s" + str(i) in p[pk_[s[3][1]]] for i in (int(s[3][0] - 2, int(s[3][0])))):
        yaku.append("平和")

def threecolor():
    if any(all("s" + str(i) in p[ia] or "t" + str(i) in f[ia] for ia in range(3)) for i in range(9)):
        yaku.append("三色同順")
    elif any(all("k" + str(i) in p[ia] or any(ib + str(i) in f[ia] for ib in ("p", "a", "d", "k")) for ia in range(3)) for i in range(9)):
        yaku.append("三色同刻")

def tyanta():
    if any(any("s" + ia in p[i] or "t" + ia in f[i] for ia in range(1, 5)) or any(any(ib + ia in p[i] for ib in ("t", "k")) or any(ib + ia in f[i] for ib in ("p", "a", "d", "k")) for ia in range(1, 8)) for i in range(3)):
        return
    if len(p[3]) + len(f[3]) == 0:
        yaku.append("純全帯么九")
    else:
        yaku.append("混全帯么九")

def routou():
    if "s" in str(p) or "t" in str(f) or any(str(i) in str(p) + str(f) for i in range(1, 7)): # 順子を手牌に含むorチーをしているor2~8までの刻子系統がある
        return
    if len(p[3]) + len(f[3]) == 0:
        yaku.append("清老頭")
    else:
        yaku.append("混老頭")

def riich():
    if s[4] == 2:
        yaku.append("立直")
    elif s[4] == 3:
        yaku.append("ダブル立直")

def strk(): # string kootsu 連刻系統
    for i in range(3):
        x = None
        for ia in range(9):
            x += "1" if "k" + str(ia) in p[i] or any(ib + str(ia) in f[i] for ib in ("p", "a", "k", "d")) else "0"
        if "1111" in x:
            yaku.append("四連刻")
        elif "111" in x:
            yaku.append("三連刻")
        else:
            continue
        return

def main(p_, f_=None, s_=()): # p ==> 手牌, f ==> 副露, s ==> 盤面(シチュ) (場風, 自風, TF(ツモ-ロン), 和了牌, 状態(-1:副露, 0:面前, 1:暗槓あり面前, 2:立直, 3:ダブル立直)) 全部0m方式で
    global mz, p, f, s, yaku
    mz = True # 面前か否か
    p = p_
    if f_ != None:
        f = f_
    s = s_
    yaku = []
    for i in range(len(f)):
        if type(f[i]) == str:
            if f[i][0] != "a":
                mz = False
                break
            continue
        if any(f[i][ia][0] != "a" for ia in range(len(f[i]))):
            mz = False
            break
    if mz: # 面前成立
        tsumo()
        double()
        pinfu()
    flush()
    tanyao()
    threecolor()
    tyanta()
    routou()
    if not sevenpairs(): # 七対子不成立 ==> 通常手
        toitoi()
        yakuhai()
        straight()