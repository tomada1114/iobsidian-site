# Site

自分で作った読み物を GitHub Pages で公開するためのリポジトリ。iobsidian 直下に `Site/` としてクローンし、iobsidian 側では `.gitignore` で除外している（`Content/Zenn/` と同じ方式）。

- 入口: `index.html`（本棚）
- 各読み物は `<name>/` に HTML と原稿 `src/` を置く。`python3 <name>/src/build.py` で再生成
- 検索エンジンには載せない（各ページの `noindex` と `robots.txt`）。URL を知っていれば誰でも読める
- ヘッダー（全ページ）と読み物のサイドバー（全ページ一覧。PC は左固定、スマホは Menu ボタンのドロワー）は `_shared/nav.py` が出す。本棚 `index.html` も `_shared/nav.py` が生成する（カテゴリ別のカード、検索とカテゴリ絞り込み、続きから読む）。読み物を足したら `READERS` と `BOOKS`（カテゴリ・一言説明・所要時間・レベル・本文の言語 `en`/`ja`）に1行ずつ足し、新しいカテゴリなら `CATEGORIES` にも足して、`python3 _shared/nav.py` を実行する。UI は英語、読み物の本文は日本語でもよい（日本語の読み物は `build.py` の `LANG = "ja"`、`BOOKS` も `"ja"`）
- ホーム画面に追加できる Web アプリで、オフラインでも読める。`sw.js`（service worker）・`manifest.webmanifest`・`icons/` はサイト直下。本棚の「Save all readers for offline」ボタンで全読み物の全ページを端末に保存し、サイトから消えたページは端末からも消す。オンラインで本棚を開くと未保存の新ページ数と消えたページ数が出るので、そのときに押し直す。一度開いたページも自動で保存される。iPad・iPhone では、ホーム画面に追加したアプリの中でボタンを押す（Safari とホーム画面のアプリは保存領域が別）

| 読み物 | 目次 |
|---|---|
| One-on-Ones: Architecture（英語・B2・対話） | `1on1-architecture/ch00.html` |
| One-on-Ones: API and TypeScript（英語・B2・対話） | `1on1-api-types/ch00.html` |
| One-on-Ones: AWS Foundation（英語・B2・対話） | `1on1-aws/ch00.html` |
| One-on-Ones: AI in Production（英語・B2・対話） | `1on1-ai/ch00.html` |
| One-on-Ones: Operations and Quality（英語・B2・対話） | `1on1-ops/ch00.html` |
| AgentCore Reader（英語・B2・対話） | `agentcore-reader/ch00.html` |
| Easy Reads（英語・A2+〜B1、毎朝6本追加。`easy-reads` スキル） | `easy-reads/index.html` |
| 一拍おいて話す（日本語・Quick Book・解説型） | `book-pause-before-speaking/ch00.html` |
