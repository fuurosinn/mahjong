import math # 符の繰り上げで使用

h = []
f = []
hp = None
w = None
pw = None
z = {"東":0, "南":1, "西":2, "北":3, "白":4, "發":5, "中":6}
z_ = {0:"東", 1:"南", 2:"西", 3:"北", 4:"白", 5:"發", 6:"中"}
pk = {"m":0, "p":1, "s":2, "z":3}
ya = {"門前清自摸和":1, "平和":1, "断么九":1, "一盃口":1, "槍槓":1, "嶺上開花":1, "一発":1, "立直":1, "三元牌:白":1, "三元牌:發":1, "三元牌:中":1, "場風:東":1, "場風:南":1, "場風:西":1,"場風:北":1, "自風:東":1, "自風:南":1, "自風:西":1, "自風:北":1, "一気通貫":2, "小三元":2, "混全帯么九":2, "純全帯么九":3, "対々和":2, "二盃口":3, "三暗刻":2, "三槓子":2, "両立直":2, "海底撈月":1, "河底撈魚":1, "三色同順":2, "三色同刻":2, "混老頭":2, "七対子":2, "混一色":3, "清一色":6}
yd = ["一気通貫", "混全帯么九", "純全帯么九", "三色同順", "混一色", "清一色"] # 食い下がりする役、 yaku down。
yakuman = ["国士無双", "国士無双十三面", "四暗刻", "四暗刻単騎", "大三元", "字一色", "小四喜", "大四喜", "四槓子", "天和", "地和", "緑一色", "清老頭", "九連宝燈", "純正九連宝燈"] # 役満貫
yakuman_ = {"国士無双":1, "国士無双十三面":2, "四暗刻":1, "四暗刻単騎":2, "大三元":1, "字一色":1, "小四喜":1, "大四喜":2, "四槓子":1, "天和":1, "地和":1, "緑一色":1, "清老頭":1, "九連宝燈":1, "純正九連宝燈":2} # 役満の打点

def fu_(): # 符計算
    fu = 20
    if "平和" in yaku and "門前清自摸和" in yaku:
    #    print("符:20(平和自摸)")
        return fu
    if all(all(f[i][ia][0] == "k" for ia in range(len(f[i]))) for i in range(len(f))) and not tm:
        fu += 10
    for i in range(len(h)):
        if len(h[i]) > 0:
            iz = 1 if any(h[i][0] == ib for ib in ("t", "k", "s")) else len(h[i])
            for ia in range(iz):
                x = h[i] if any(h[i][0] == ib for ib in ("t", "k", "s")) else h[i][ia]
                if x[0] == "k": # 刻子
                    if i == 3 or x[1] == 0 or x[1] == 8: # 刻子かつ么九牌
                        if not tm and pk[hp[1]] == i and int(hp[0]) == x[1]: # 自摸和了ではない かつ 和了牌と同じ色 かつ 和了牌と同じ数牌(字牌) ==> ロン和了で明刻扱いの場合
                            fu += 4
                        else:
                            fu += 8
                    else: # 刻子かつ么九牌ではない
                        if not tm and pk[hp[1]] == i and int(hp[0]) == x[1]: # ロン和了時の和了牌の場合
                            fu += 2
                        else: # 暗刻の場合
                            fu += 4
                elif x[0] == "t": # 雀頭
                    if i == 3:
                        if any(int(hp[0]) == iz for iz in range(4, 7, 1)): # 雀頭が三元牌の場合
                            fu += 2
                        if int(hp[0]) == w: # 自風の場合
                            fu += 2
                        if int(hp[0]) == pw: # 場風の場合。連符牌4符の時の処理。
                            fu += 2
        iz = 1 if type(f[i]) == str else len(f[i])
        for ia in range(iz):
            x = f[i][ia] if type(f[i]) == tuple else f[i]
            if x[0] == "t":
                continue
            p = 0
            if x[0] == "k": # 槓子の場合。k410r k ==> 槓子、4 ==> 副露した牌の番号、1 ==> 自分から数えて右回りで1番目の奴から副露した(0なら暗槓)、0 ==> 加槓していない(1は加槓)、r ==> 赤ドラあり(無い場合は存在しない。赤ドラで加槓した場合はR)。
                p = 8
                if x[2] == "0": # 暗槓の場合
                    p *= 2
            elif x[0] == "p": # 明刻子の場合。p42R p ==> ポン、 4 ==> 5番目を副露した、 2 ==> 対面から、 R ==> 赤ドラを鳴いた。
                p = 2
            if i == 3 or x[1] == "0" or x[1] == "8": # 么九牌の場合
                p *= 2
            fu += p
    if "平和" not in yaku:
        if "s" + str(int(hp[0]) - 1) in h[pk[hp[1]]]: # 嵌張
            fu += 2
        elif hp[0] == "2" and "s0" in h[pk[hp[1]]]: # 辺3
            fu += 2
        elif hp[0] == "6" and "s6" in h[pk[hp[1]]]: # 辺7
            fu += 2
        elif "t" + str(hp[0]) in h[pk[hp[1]]]: # 単騎
            fu += 2
        if tm: # 自模符
            fu += 2
#    print("符:" + str(fu), end=" ==> ")
    fu = int(math.ceil(fu / 10) * 10) # 符切り上げ
#    print(fu)
    return fu

def points(han, t): # t ==> 自摸か否か
    a = []
    if han < 5:
        fu = 25 if "七対子" in yaku else fu_() # 七対子の場合/通常手の場合
        x = fu * 2 ** (han + 2) # 基本打点計算
    if han > 4 or x >= 2000:
        if han >= 13:
#            print("数え役満")
            x = 32000
        elif han >= 11:
#            print("三倍満")
            x = 24000
        elif han >= 8:
#            print("倍満")
            x = 16000
        elif han >= 6:
#            print("跳満")
            x = 12000
        else:
#            print("満貫")
            x = 8000
        if w == 0:
            x *= 1.5
            if t:
                for i in range(3):
                    a.append(int(x / 3))
            else:
                a.append(int(x))
        else:
            if t:
                a.append(int(x / 2))
                for i in range(2):
                    a.append(int(x / 4))
            else:
                a.append(int(x))
#        print(a)
        return a
    x /= 100
    if t:
        if w == 0:
            for i in range(3):
                y = math.ceil(x * 2)
                a.append(int(y * 100))
        else:
            y = math.ceil(x * 2)
            a.append(int(y * 100))
            for i in range(2):
                y = math.ceil(x)
                a.append(int(y * 100))
    else:
        if w == 0:
            y = math.ceil(x * 6)
            a.append(int(y * 100))
        else:
            y = math.ceil(x * 4)
            a.append(int(y * 100))
#    print(a)
    return a

def setup():
    global yaku
    yaku = []

def straight(): # A
    for i in range(3):
        if all("s" + str(ia) in h[i] or "t" + str(ia) in f[i] for ia in (0, 3, 6)):
            yaku.append("一気通貫")
            return

def flush():
    x = []
    for i in range(4):
        if len(h[i]) + len(f[i]) > 0:
            x.append(i)
    if len(x) > 2:
        return
    if len(x) == 1:
        if x == [3]:
            yaku.append("字一色")
        else:
            yaku.append("清一色")
    elif 3 in x:
        yaku.append("混一色")

def pinfu():
    if any(len(f[i]) > 0 for i in range(4)):
        return
    if any("t" + str(i) in h[3] for i in (w, pw, 4, 5, 6)):
        return
    if any(any(h[i][ia][0] == "k" for ia in range(len(h[i]))) for i in range(4)):
        return
    x = pk[hp[1]]
    if hp[0] == 3 and "s2" in h[x]: # 3で和了かつ平和がつく ==> (4, 5) + 3
        yaku.append("平和")
        return
    elif hp[0] == 7 and "s4" in h[x]: # 7で~ ==> (5, 6) + 7
        yaku.append("平和")
        return
    if any("s" + str(int(hp[0]) + i) in h[x] for i in (-3, -1)):
        yaku.append("平和")

def tanyao():
    if len(h[3]) + len(f[3]) > 0:
        return
    if any(any(ia in h[i] for ia in ("s0", "s6", "t0", "t8", "k0", "k8")) for i in range(len(h))):
        return
    for i in range(len(f)):
        if len(f[i]) == 0: # 存在しない場合
            continue
        for ia in range(len(f[i])):
            x = f[i] if type(f[i]) == str else f[i][ia]
            if x[0] == "t": # チー
                if x[1] == "0" or x[1] == "6": # 123/789
                    return
            elif x[0] == "p" or x[0] == "k":
                if x[1] == "0" or x[1] == "8": # 111/999 or 1111/9999
                    return
    yaku.append("断么九")

def cups(): # 一盃口、二盃口
#    if any(any(h[i][ia][0] == "t" for ia in range(len(h[i]))) for i in range(len(h))):
#        return
    if not mz:
        return
    iz = 0
    for i in range(len(h) - 1):
        if type(h[i]) == str:
            continue
        x = [0 for i in range(7)]
        for ia in range(len(h[i])):
            if h[i][ia][0] == "s":
                x[int(h[i][ia][1])] = x[int(h[i][ia][1])] + 1
        for ia in range(len(h[i])):
            if x[ia] == 2:
                iz += 1
            elif x[ia] == 4:
                yaku.append("二盃口")
                return
    if iz == 1:
        yaku.append("一盃口")
    elif iz == 2:
        yaku.append("二盃口")

def sevenpair(): # 七対子
    if any(any(h[i][ia][0] == "t" for ia in range(len(h[i]))) for i in range(len(h))):
        return
    for i in range(len(h)):
        if type(h[i]) == str:
            if h[i][0] != "t":
                return
        else:
            for ia in range(len(h[i])):
                if h[i][ia][0] != "t":
                    return
    yaku.append("七対子")

def toitoi():
    x = 0 # 暗刻(暗槓)の数
    y = 0 # 明刻(明槓)の数
    k = 0 # 槓子の数
    hp_ = hp[0] + hp[2] if hp[1] == "r" else hp
    for i in range(len(h)):
        for ia in range(len(h[i])):
            if h[i][ia][0] == "k":
                if not tm and i == pk[hp_[1]] and h[i][ia][1] == hp_[0]:
                    y += 1
                else:
                    x += 1
    for i in range(len(f)):
        for ia in range(len(f[i])):
            if f[i][ia][0] == "p":
                y += 1
            elif f[i][ia][0] == "k":
                k += 1
                if type(f[i]) == str:
                    if f[i][2] == "0":
                        x += 1
                    else:
                        y += 1
                else:
                    if f[i][ia][2] == "0":
                        x += 1
                    else:
                        y += 1
    if k == 4: # 四槓子確定
        yaku.append("四槓子")
    elif k == 3:
        yaku.append("三槓子")
    if x == 4: # 四暗刻以上確定
        if "t" + str(int(hp_[0]) - 1) in h[pk[hp_[1]]]: # 単騎待ち。(四暗刻単騎に派生)
            yaku.append("四暗刻単騎")
        else: # シャボ待ち
            print("hp = " + str(hp_))
            yaku.append("四暗刻")
        return
    elif x == 3:
        yaku.append("三暗刻")
    if x + y == 4:
        yaku.append("対々和")

def threecolor(): # 三色系統
    for i in range(7):
        if all("s" + str(i) in h[ia] or "t" + str(i) in f[ia] for ia in range(3)):
            yaku.append("三色同順")
            return
    for i in range(9):
        x = 0
        for ia in range(3):
            if "k" + str(i) in h[ia]:
                x += 1
                continue
            if len(f[ia]) == 0:
                continue
            iz = 1 if type(f[ia]) == str else len(f[ia])
            if any(f[ia][ib][:2] == "p" + str(i) for ib in range(iz)):
                x += 1
        if x == 3:
            yaku.append("三色同刻")
            return

def chan(): # 混全帯么九、純全帯么九。x = f[i] if type(f[i]) == tuple else pass /n if x != None: /n     x = [] /n     x.append(f[i]) /n     x = tuple(x) でxを利用して高速化~みたいな処理を後で試す。
    for i in range(3):
        if any(any(ib + str(ia) in h[i] for ib in ("t", "k")) for ia in range(1, 8)): # 2~8の刻子対子が含まれているかどうか
            return
        if any("s" + str(ia) in h[i] for ia in range(1, 6)): # (2, 3, 4)~(6, 7, 8)の順子が含まれるかどうか
            return
        if type(f[i]) == str: # 数牌で一回のみしか鳴いていない牌種がある場合に必須。
            if f[i][0] == "t" and any(int(f[i][1]) == ia for ia in range(1, 6)): # 么九牌が含まれないチーが存在するか確認
                return
            if any(any(f[i] == ia + ib for ib in range(1, 8)) for ia in ("p", "k")): # 2~8のポンまたはカンが存在するか確認
                return
        else: # 複数回同じ牌種を鳴いている場合はこの処理で問題ない。
            if any(any("t" + str(ib) == f[i][ia][:2] for ib in range(1, 6)) for ia in range(len(f[i]))): # チー
                return
            if any(any(any(ic + str(ib) == f[i][ia][2:] for ic in ("p", "k")) for ib in range(1, 8)) for ia in range(len(f[i]))):
                return
    if len(h[3]) + len(f[3]) > 0: # 字牌を含むかどうか。順子を含まない場合は混全帯么九系統ではないが、後のtin()で混老頭の場合はdel yaku[-2]で混全帯么九の入力を削除しているので問題ない。
        yaku.append("混全帯么九")
    else:
        yaku.append("純全帯么九")

def tin(): # 清老頭、混老頭。chan()の直後に実行しないとエラー吐く。
    if any(i in yaku for i in ("混全帯么九", "純全帯么九")):
        for i in range(3):
            if any(h[i][ia][0] == "s" for ia in range(len(h[i]))): # 手牌に順子があるか確認
                return
            if type(f[i]) == str: # 一回のみしか鳴いていない牌種がある場合
                if f[i][0] == "t": # チーをしているか確認
                    return
            else: # 複数回鳴いている牌種はこっちの処理
                if any(any(f[i][ia][0] == "t") for ia in range(len(f[i]))): # チーをしているか確認
                    return
        if "混全帯么九" in yaku:
            yaku.append("混老頭")
        elif "純全帯么九" in yaku:
            yaku.append("清老頭")
        del yaku[-2] # 順子が確認されなかったのでリストyakuから"混全帯么九"または"純全帯么九"を削除して"混老頭"または"清老頭"を追加

def yakuhai(): # 役牌関連
    global green
    x = [False for i in range(7)]
    if type(f[3]) == str: # もし複数字牌を鳴いていないならtupleにならずにバグるのでここで処理している
        x[int(f[3])] = True
        flag = False
    else:
        flag = True
    for i in range(7):
        if "k" + str(i) in h[3]:
            x[i] = True
        elif "t" + str(i) in h[3]: # 対子の場合
            x[i] == None
        elif flag and any(any(ia + str(i) == f[3][ib][:2] for ib in range(len(f[3]))) for ia in ("p", "k")): # 字牌の副露
            x[i] = True
    y = 0 # 面子の数
    z = 0 # 対子の数
    for i in range(4): # 四喜和の判定
        if not x[i]: # 面子または対子判定ではない時はFalseなのでnotをつけてcontinueするようにしている
            continue
        if x[i]: # 面子の場合
            y += 1
        else: # 面子でもない場合。対子確定
            z += 1
    if y == 4:
        yaku.append("大四喜")
    elif y == 3 and z == 1:
        yaku.append("小四喜")
    else:
        if x[w]: # 自風
            yaku.append("自風:" + z_[w])
        if x[pw]: # 場風
            yaku.append("場風" + z_[pw])
    y = 0
    z = 0
    for i in range(4, 7): # 三元系統の判定
        if not x[i]:
            continue
        if x[i]:
            y += 1
            yaku.append("三元牌:" + z_[i]) # ついでに三元牌の判定
        else:
            z += 1
    if y == 3:
        yaku.append("大三元")
    elif y == 2 and z == 1:
        yaku.append("小三元")
    green = False if any(x[i] for i in (0, 1, 2, 3, 4, 6)) else 2 if x[5] == False else True # 字牌を鳴いていたとして發しか鳴いていないかどうか。わざわざ三項演算子を重ねたのは發無し緑一色の割合が知りたかったから。

def tsumo():
    if tm:
        flag = True
        for i in range(len(f)):
            for ia in range(len(f[i])):
                if type(f[i][ia]) == str:
                    if f[i][0] != "k" or f[i][2] != "0": # 副露確認
                        flag = False
                    break
                if f[i][ia][0] != "k" or f[i][ia][2] != "0":
                    flag = False
                    break
            if not flag:
                break
        else:
            yaku.append("門前清自摸和")
    if r[0] == 1:
        yaku.append("立直")
    elif r[0] == 2:
        yaku.append("両立直")
    if r[1] == 1:
        yaku.append("一発")
    if r[2] == 1:
        yaku.append("海底")
    elif r[2] == 2:
        yaku.append("河底")
    elif r[2] == 3:
        yaku.append("嶺上開花")
    elif r[2] == 4:
        yaku.append("槍槓")
    elif r[2] == 5:
        print()
        if tm and mz: # 自摸かつ面前聴牌
            if w == 0:
                yaku.append("天和")
            else:
                yaku.append("地和")
        elif not tm and mz:
            print("ローカル役満発生:人和(不採用)")

def allgreen(): # 緑一色
    if green == False or any(len(h[i]) > 0 for i in range(2)): # green == Falseにしないと2が吐かれた時(發無し)に...
        return
    if any(i != h[2] for i in ("s1", "k1", "k2", "k3", "k5", "k7", "t1", "t2", "t3", "t5", "t7")): # 索子が緑一色が成立する牌のみか確認
        return
    yaku.append("緑一色")
    if green:
        print("發有り緑一色")
    else:
        print("發無し緑一色")

def ninth():
    if "清一色" not in yaku: # 清一色が最低条件なので...
        return
    x = None
    for i in range(3):
        if len(h[i]) > 0:
            x = i
            break
    hands = [0 for i in range(9)]
    for i in range(len(h[x])): # 普通にこれrange(5)でいいかも
        y = h[x][i]
        if y[0] == "s": # 順子
            for ia in range(3):
                hands[int(y[1]) + ia] = hands[int(y[1]) + ia] + 1
        elif y[0] == "k": # 刻子
            hands[int(y[1])] = hands[int(y[1])] + 3
        elif y[0] == "t": # 対子
            hands[int(y[1])] = hands[int(y[1])] + 2
    if hands[0] >= 3 and hands[8] >= 3 and all(hands[i] >= 1 for i in range(1, 8)):
        z = int(hp[0]) - 1
        if z == 0 or z == 8:
            if hands[z] == 4:
                yaku.append("純正九連宝燈")
            else:
                yaku.append("九連宝燈")
        else:
            if hands[z] == 2:
                yaku.append("純正九連宝燈")
            else:
                yaku.append("九連宝燈")

def strings(): # 連刻系統 ローカル役
    for i in range(3):
        x = [0 for i in range(9)]
        for ia in range(len(h[i])):
            if h[i][ia][0] == "k":
                x[ia] = 1
        if type(f[i]) == str:
            if f[i][0] == "k" or f[i][0] == "p":
                x[int(f[i][1])] = 1
        else:
            for ia in range(len(f[i])):
                if f[i][ia][0] == "k" or f[i][ia] == "p":
                    x[int(f[i][ia][1])] = 1
        x.append(0) # 10番目を入れて四連刻でも処理できるようにしている
        ia = 0
        while ia < 7:
            while ia < 7 or x[ia] == 0:
                ia += 1
            y = 0
            for ib in range(4):
                if x[ia + ib] == 1:
                    y += 1
            else:
                if y == 3:
                    yaku.append("三連刻")
                    return
                elif y == 4:
                    yaku.append("四連刻")
                    return

def y(): # 役関係
    han = 0
#    mz = True if all(all(f[i][ia][0] == "k" and f[i][ia][2] == "0" for ia in range(len(f[i]))) for i in range(len(f))) else False # 面前か否か判断
    for i in range(len(yaku)):
        if yaku[i] in yakuman:
            break
        x =  ya[yaku[i]]
        if mz == False and yaku[i] in yd: # 食い下がり役の補正
            x -= 1
        han += x
    else:
        for ia in range(len(dora)): # ドラ
            han += dora[ia]
        if dora[0] > 0:
            yaku.append("ドラ" + str(dora[0]))
        if dora[1] > 0:
            yaku.append("赤ドラ" + str(dora[1]))
        if dora[2] > 0 and any(ib in yaku for ib in ("立直", "両立直")):
            yaku.append("裏ドラ" + str(dora[2]))
        return han
    global ym # 役満
    ym = 0
    for i in range(len(yaku)):
        if yaku[i] in yakuman:
            ym += yakuman_[yaku[i]]
    for i in range(len(yaku) - 1, -1, -1):
        if yaku[i] in ya:
            del yaku[i]
    return None

def main(p, f_, hp_, wind, pwind, s): # 0mとかの方式で, hp ==> hit pai, 和了牌, tm ==> 自摸和了か否か, r ==> 立直とか諸々 立直状態か否か(1==>立直, 2==>ダブリー)、一発か、特殊自摸(1==>海底, 2==>河底, 3==>嶺上開花, 4 ==> 槍槓, 5 ==> 第一ツモ以前に和了(天和地和人和)), dora ==> 事前に数えてそれを引数として送る。(ドラ、赤ドラ、裏ドラ)
    if p == ((), ):
        return
    mentsu, toitsu = 0, 0 # ↓和了しているかどうか。z.check()がうまく働いていないっぽいから応急処置。
    for i in range(len(p)):
        for ia in range(len(p[i])):
            if p[i][ia][0] == "k" or p[i][ia][0] == "s":
                mentsu += 1
            elif p[i][ia][0] == "t":
                toitsu += 1
        for ia in range(len(f_[i])):
            if f_[i][ia][0] == "p" or p[i][ia][0] == "t" or p[i][ia][0] == "k":
                mentsu += 1
    if (mentsu != 4 and toitsu != 1) and (mentsu != 0 and toitsu != 7):
#        print(mentsu, toitsu)
        return None, None # ↑
    global h, f, hp, w, pw, tm, r, dora, mz
#    print("check:" + str(p))
    h = p
    f = f_
    hp = hp_
    w = wind
    pw = pwind
    tm = s[0]
    r = list([s[i] for i in range(1, 4)])
    dora = list([s[i] for i in range(4, 7)])
    mz = True # ↓面前聴牌なのか判断
    for i in range(len(f)):
        iz = 1 if type(f[i]) == str else len(f[i])
        for ia in range(iz):
            if type(f[i]) == str:
                if f[i][0] != "k" or f[i][2] != "0":
                    mz = False
            if not mz:
                break
            if type(f[i]) == tuple:
                if f[i][ia][0] != "k" or f[i][ia][2] != "0":
                    mz = False
        if not mz:
            break # ↑
    setup()

    tsumo()
    straight() # ?
    flush() # B
    pinfu() # B
    tanyao() # A
    cups()
    sevenpair()
    threecolor()
    toitoi()
    chan()
#    tin()
    yakuhai()
    allgreen()
    ninth()

    a = y()
    if a == None:
        a = []
        if tm:
            if w == 0: # 親で役満自摸の場合
                for i in range(3):
                    a.append(ym * 16000)
            else: # 子で役満自摸の場合
                a.append(ym * 16000)
                for i in range(2):
                    a.append(ym * 8000)
        else:
            if w == 0:
                a.append(ym * 48000)
            else:
                a.append(ym * 32000) 
#        print(a)
#        print(yaku)
        daten = a               
    else:
        daten = points(a, tm)
    if daten != None:
        print(daten, yaku)
    return daten, yaku
# 国士はこっちでは処理ができない(面子状態で送られてくるので)
if __name__ == "__main__": # tm_, r_, dの統合後 ==> s = (自摸和了か否か, 立直状態か(0==>False, 1==>立直, 2 ==> ダブリー), 一発か(True or False), 特殊自摸(0==>無し, 1==>海底, 2==>河底, 3==>嶺上開花, 4==>槍槓, 5==>第一ツモ以前に和了かつ副露無し(天和地和)), ドラ枚数, 赤ドラ枚数, 裏ドラ枚数))
#    print(main((("s0", "s0", "t8"), ("s0"), ("s0"), ()),((), (), (), ()), ("1m"), (0), (0), True, (0, 0, 0), (0, 0, 0)))
    print(main((("s0", "s0", "t8"), ("s0"), ("s0"), ()),((), (), (), ()), ("1m"), (0), (0), (1, 1, 0, 0, 2, 0, 2)))
#    print(main((("s0", "s3"), ("s0"), ("s2"), ("t2")), ((), (), (), ()), ("4m"), (0), (0), True, (0, 0, 0), (0, 0, 0)))
    print(main((("s0", "s3"), ("s0"), ("s2"), ("t2")), ((), (), (), ()), ("4m"), (0), (0), (0, 2, 0, 0, 0, 0, 0)))