Kanji0 = {0:"零", 1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"七", 8:"八", 9:"九"}
Kanji1 = ["", "十", "百", "千"]
Kanji2 = ["", "万", "億", "兆", "京", "垓", "𥝱", "穣", "溝", "澗", "正", "載","極", "恒河沙", "阿僧祇", "那由他", "不可思議", "無量大数"]

def TransToKanjiSub(n):
    a = len(str(n)) - 1
    x = ""
    for i in range(len(str(n))):
        y = int(str(n)[i])
        if y != 0:
            x = x + Kanji0[int(str(n)[i])] + Kanji1[a-i]
    return x

def TransToKanji(n):
    m = n
    x = len(str(m))
    if x < 4:
        return TransToKanjiSub(m)
    div = []
    if x % 4 != 0:
        div.append(int(str(m)[0:x%4]))
        m = int(str(m)[x%4:])
    for i in range(int(x/4)):
        div.append(int(str(m)[4*i:4*(i+1)]))
    x = ""
    for i in range(len(div)):
        y = TransToKanjiSub(div[-1-i])
        if y != "":
            x = y + Kanji2[i] + x
    return x

if __name__ == "__main__":
    print(TransToKanji(123456789))