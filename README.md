# Site

自分で作った読み物を GitHub Pages で公開するためのリポジトリ。iobsidian 直下に `Site/` としてクローンし、iobsidian 側では `.gitignore` で除外している（`Content/Zenn/` と同じ方式）。

- 入口: `index.html`（本棚）
- 各読み物は `<name>/` に HTML と原稿 `src/` を置く。`python3 <name>/src/build.py` で再生成
- 検索エンジンには載せない（各ページの `noindex` と `robots.txt`）。URL を知っていれば誰でも読める

| 読み物 | 目次 |
|---|---|
| One-on-Ones: Architecture（英語・B2・対話） | `1on1-architecture/ch00.html` |
| One-on-Ones: API and TypeScript（英語・B2・対話） | `1on1-api-types/ch00.html` |
| One-on-Ones: AWS Foundation（英語・B2・対話） | `1on1-aws/ch00.html` |
| One-on-Ones: AI in Production（英語・B2・対話） | `1on1-ai/ch00.html` |
| One-on-Ones: Operations and Quality（英語・B2・対話） | `1on1-ops/ch00.html` |
| AgentCore Reader（英語・B2・対話） | `agentcore-reader/ch00.html` |
| Easy Reads（英語・A2+〜B1、毎朝6本追加。`easy-reads` スキル） | `easy-reads/index.html` |
