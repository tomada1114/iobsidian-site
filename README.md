# Site

自分で作った読み物を GitHub Pages で公開するためのリポジトリ。iobsidian 直下に `Site/` としてクローンし、iobsidian 側では `.gitignore` で除外している（`Content/Zenn/` と同じ方式）。

- 入口: `index.html`（カテゴリへの入口と直近1冊の続きから読む）。検索・カテゴリフィルタは使わない。
- カテゴリは内容で分ける。英語多読は `english.html`、AWS は `aws.html`、エンジニアリングは `engineering.html`、仕事・キャリアは `work.html`、対話・人間関係は `relationships.html`、お金は `money.html`、学び・言語は `learning.html`、思考・社会は `thinking.html`、暮らし・健康は `life.html`。日本語の本もテーマに沿って分類する。
- 本棚のカテゴリ・操作と、全ページ共通のヘッダー・目次は落ち着いた緑で統一する。色は `_shared/nav.py` の `--nav-*` トークンで管理し、本文の配色・章ごとのアクセントとは独立させる。
- 本棚と各読み物のヘッダーにある月／太陽ボタンでライト・ダークテーマを切り替えられる。初回は端末の配色設定に合わせ、手動で選んだテーマは同じブラウザ内の全ページで保持する（ページ移動・再読み込み・オフライン時も共通）。
- 各読み物は `<name>/` に HTML と原稿 `src/` を置く。`python3 <name>/src/build.py` で再生成
- 検索エンジンには載せない（各ページの `noindex` と `robots.txt`）。URL を知っていれば誰でも読める
- ヘッダー（全ページ）は本棚へのリンクと現在の読み物を一行で表示する。読み物のサイドバー（章一覧。PC は左固定、スマホは Contents ボタンのドロワー）には所属カテゴリと本棚へ戻るリンクを置く。本棚 `index.html` とテーマ別のカテゴリページも `_shared/nav.py` が生成する。読み物を足したら `READERS` と `BOOKS`（カテゴリ・一言説明・所要時間・レベル・本文の言語 `en`/`ja`）に1行ずつ足し、新しいカテゴリなら `CATEGORIES` と `CATEGORY_PAGES` にも足して、`python3 _shared/nav.py` と全読み物の `src/build.py` を実行する。UI は英語、読み物の本文は日本語でもよい（日本語の読み物は `build.py` の `LANG = "ja"`、`BOOKS` も `"ja"`）
- ホーム画面に追加できる Web アプリで、オフラインでも読める。`sw.js`（service worker）・`manifest.webmanifest`・`icons/` はサイト直下。本棚・カテゴリページの「Save all for offline」ボタンで本棚・全カテゴリ・全読み物の全ページを端末に保存し、サイトから消えたページは端末からも消す。オンラインで本棚を開くと未保存の新ページ数と消えたページ数が出るので、そのときに押し直す。一度開いたページも自動で保存される。iPad・iPhone では、ホーム画面に追加したアプリの中でボタンを押す（Safari とホーム画面のアプリは保存領域が別）

| 読み物 | 目次 |
|---|---|
| Engineering Readers: Architecture（英語・B2・解説文） | `1on1-architecture/ch00.html` |
| Engineering Readers: API and TypeScript（英語・B2・解説文） | `1on1-api-types/ch00.html` |
| Engineering Readers: AWS Foundation（英語・B2・解説文） | `1on1-aws/ch00.html` |
| Engineering Readers: AI in Production（英語・B2・解説文） | `1on1-ai/ch00.html` |
| Engineering Readers: Operations and Quality（英語・B2・解説文） | `1on1-ops/ch00.html` |
| AgentCore Reader（英語・B2・08〜13は解説文、01〜07は対話） | `agentcore-reader/ch00.html` |
| 一拍おいて話す（日本語・Quick Book・解説型） | `book-pause-before-speaking/ch00.html` |
| キャリアの移り目（日本語・Quick Book・解説型） | `book-career-transitions/ch00.html` |
| 貯めるより、使いきる設計（日本語・Quick Book・解説型） | `book-spend-by-design/ch00.html` |
| 思い込みを外して、世界をデータで見る（日本語・Quick Book・解説型） | `book-world-by-data/ch00.html` |
| 情報は人をつなぎ、分断する（日本語・Quick Book・解説型） | `book-information-networks/ch00.html` |
| 整えてから変えるか、変えてから整えるか（日本語・Quick Book・学習テキスト型） | `book-tidy-then-change/ch00.html` |
| その不安は、お金で消えるのか（日本語・Quick Book・解説型） | `book-money-anxiety/ch00.html` |
| その文から何が言えるか（日本語・Quick Book・学習テキスト型） | `book-what-follows/ch00.html` |
| 全身全霊で働かないという選択（日本語・Quick Book・解説型） | `book-not-all-in/ch00.html` |
| ゆるく、でも毎日積み上げる（日本語・Quick Book・解説型） | `book-loose-steady/ch00.html` |
| 答えを出す前に、問いを選ぶ（日本語・Quick Book・解説型） | `book-choose-the-question/ch00.html` |
| 技能を更新しつづける（日本語・Quick Book・解説型） | `book-keep-skills-current/ch00.html` |
| 不確実性から考えるチームと組織（日本語・Quick Book・解説型） | `book-uncertainty-teams/ch00.html` |
| 話を聞いてもらうと、なぜ人は変わるのか（日本語・Quick Book・解説型） | `book-being-heard/ch00.html` |
| ジョブ型とメンバーシップ型で読む働き方（日本語・Quick Book・解説型） | `book-job-membership/ch00.html` |
| 英語でチームを回す仕事の型（日本語・Quick Book・学習テキスト型） | `book-team-english/ch00.html` |
| 計画と対話を行き来する（日本語・Quick Book・解説型） | `book-plan-and-dialogue/ch00.html` |
| 富を積み上げる人の考え方（日本語・Quick Book・解説型） | `book-wealth-mindset/ch00.html` |
| 命令の組織から、探検の組織へ（日本語・Quick Book・解説型） | `book-beyond-command/ch00.html` |
| アドラー心理学で人間関係をほどく（日本語・Quick Book・解説型） | `book-adler-relationships/ch00.html` |
| 稼いだ分は、どこへ行ったのか（日本語・Quick Book・解説型） | `book-where-gains-went/ch00.html` |
| 歩くと、頭と体に何が起きるか（日本語・Quick Book・解説型） | `book-walk-and-think/ch00.html` |
| 人生を物語にしない生き方（日本語・Quick Book・解説型） | `book-life-not-a-story/ch00.html` |
| AIの時代に、センスはどう育つか（日本語・Quick Book・解説型） | `book-growing-sense/ch00.html` |
| アメリカを割る信仰（日本語・Quick Book・解説型） | `book-faith-divides-america/ch00.html` |
| 仕事選びのものさしを科学で直す（日本語・Quick Book・解説型） | `book-job-yardstick/ch00.html` |
| 思い出して覚える、勉強の組み立て方（日本語・Quick Book・学習テキスト型） | `book-recall-to-learn/ch00.html` |
| 大人の英語は、ずれに気づいて身につける（日本語・Quick Book・学習テキスト型） | `book-english-gaps/ch00.html` |
| ことばは体から育つ（日本語・Quick Book・解説型） | `book-grounded-words/ch00.html` |
| 論理はひとつではない（日本語・Quick Book・解説型） | `book-many-logics/ch00.html` |
| 流行に左右されない作り手の心得（日本語・Quick Book・解説型） | `book-lasting-craft/ch00.html` |
| 全部はできない前提で、時間を使う（日本語・Quick Book・解説型） | `book-finite-time/ch00.html` |
