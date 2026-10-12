# 新約聖書を読む

シリーズの入口は `ch00.html`、背景の案内は `ch01.html`。
各書は独立した `new-testament-<book>/` の読書シリーズとして置く。
現在の本文は `../new-testament-john/`（ヨハネ全21章）。

新しい書を収録する場合は、その書の目次と章を作成し、
この入口の収録一覧と `_shared/nav.py` の READERS / BOOKS を更新する。
未収録の書にリンクや空の章を作らない。

- 本文の正本：各 reader の `src/chNN.body.html`。
- ビルド：Site 内で `python3 new-testament/src/build.py`。
- 分類：Religion & Texts。
- 本文の要件：現代の日本語のです・ます調、背景を組み込んだ読み物、
  原文の出来事・主張と解釈を区別、重要な教えを保持、創作した会話や動機を加えない。
- 宗教的主張は各書の主張として紹介し、読者への信仰の勧めを加えない。
