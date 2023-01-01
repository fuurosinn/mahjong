# mahjong
Personal mahjong programs.

↓Japanese
最善手計算の部分で「最高期待値」の合算部分(最善手の期待値×発生確率の合計)に「最高期待値"以外"」の期待値まで足しています。完全なる設計ミスです。受験勉強の合間を縫って修正予定です(覚えていれば…)
さらに言うとこのコード達は2022の夏に某ネット麻雀で理不尽ラスばかり喰らってキレて書いたやつです。これを描いているのが2023の正月ですので、大半の関数の処理の意味を忘れています。
yaku.py(成立している役の判定)ならわかります。ちなみにいうと、多分緑一色の部分で1579sのポンカンの判定でバグります。条件書き忘れてます。
scan.pyはマクロ用の画像認識関連です。本当はゲームを起動せずに直で通信だけしたかったのですが、単純にノリで始めたのでそんな高度なこと無理でした。
div.pyはバグの集合体です。3~7割くらいは正常に動作していると思いたいです。現在バグのない奴が1%くらいできています。

...後なんか
for i in range(len(リスト名)):
    関数(リスト名[i])
みたいな意味不明な処理している部分は
for i in range(リスト名):
    関数(i)
に直しても問題ありません。鼻ほじってるときに気付きました。

↓English
This codes has some serious bugs in calculating expected value. I might be going to fix...?(I can fix it, but I have to study for college entrance exam.)
I'm not good at English. (´・ω・)
