# 新約聖書を読む

トップのURLは https://tomada1114.github.io/iobsidian-site/new-testament/ 。
`index.html` がシリーズの入口、`ch01.html` が背景の案内です。

```text
new-testament/
  index.html                 新約全体の入口（生成物）
  src/books.json             27書の順番、呼び名、分類の正本
  src/ch00.body.html         入口の本文と一覧の挿入位置
  src/build.py               入口・収録一覧・旧URLへの案内を生成
  john/
    ch00.html                ヨハネの目次
    ch01.html ... ch21.html   各章
    src/                     章本文とビルド
  <book-slug>/               今後追加する各書
```

未収録の書は books.json に登録済みです。本文のある書だけにリンクが付くため、
空の章ページや未収録のフォルダは作りません。
各書の収録状況と章数は `src/chNN.body.html` の存在から生成します。

## 書を追加する手順

1. books.json の slug を使い `new-testament/<slug>/src/` に目次と章本文を作成する。
2. john/src/build.py の構成を使う。Site までの相対パスは ../../、
   shared nav の reader slug は new-testament/<slug> とする。
3. `_shared/nav.py` の READERS / BOOKS と Site/README.md に登録する。
4. 各書をビルドし、入口をビルドし、本棚と全登録readerを再生成する。
5. 節の対応、リンク、携帯幅の表示を検証して公開する。

Site 内で `python3 new-testament/john/src/build.py`、
`python3 new-testament/src/build.py` を実行します。
本文の正本は各書の `src/chNN.body.html` です。
旧 new-testament/ch00.html と new-testament-john/chNN.html は、
既存リンクを保つ案内ページとしてビルド時に再生成します。

本文は現代日本語のです・ます調で、背景を組み込んだ読み物にします。
聖書の記述、背景、解釈を区別し、重要な教えを残します。
原文にない会話や動機、読者への信仰の勧めは加えません。
