# Site

自分で作った読み物を GitHub Pages で公開するためのリポジトリ。iobsidian 直下に `Site/` としてクローンし、iobsidian 側では `.gitignore` で除外している（`Content/Zenn/` と同じ方式）。

- 入口: `index.html`（本棚）
- 各読み物は `<name>/` に HTML と原稿 `src/` を置く。`python3 <name>/src/build.py` で再生成
- 検索エンジンには載せない（各ページの `noindex` と `robots.txt`）。URL を知っていれば誰でも読める

| 読み物 | 目次 |
|---|---|
| AgentCore Reader（英語・B1） | `agentcore-reader/ch00.html` |
| Easy Reads（英語・A2+〜B1、毎朝6本追加。`easy-reads` スキル） | `easy-reads/index.html` |
