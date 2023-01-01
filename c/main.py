import div
import div_sevenpairs
import div_kokushi
import yaku
import scan

rule = [4, 25000] # 人数, 原点

def setup():
    global s, place, riv
    s = [0, False, False] # 立直状態か否か(-1 ==> 副露, 0 ==> 面前, 1 ==> 面前(暗槓あり), 2 ==> 立直, 3 ==> ダブリー), 一発圏内か否か, 純粋な第一打牌前か否か
    place = [scan.wind, scan.mywind, scan.phase, scan.r, scan.tumibou, scan.honba] # 場風, 自風, 局,残り山, 積み棒, 本場
    riv = [[] for i in range(rule[0])] # 河

def main():
    pass