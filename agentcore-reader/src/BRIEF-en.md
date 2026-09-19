# Brief: translate "AgentCore 読本" into B1-level English

Source (Japanese): `../../src/chNN.body.html`. Target: `chNN.body.html` in this folder (`en/src/`).
Build: run `python3 build.py` here; it writes `../chNN.html`. Do not edit base.css or build.py. Do not publish anything.

## Keep exactly
- The whole HTML structure, class names, ids, SVG geometry (rect/line/path coordinates), marker ids, row ids in `span.rid` (e.g. 2-2), and all href URLs.
- First line format: `<!-- title: AgentCore Reader NN <Short Name> | accent: <same accent> -->`. Chapter 00 is `AgentCore Reader Contents`.
- AWS / product names as they are: AgentCore, Runtime, Memory, Gateway, Identity, Policy, Observability, Evaluations, Strands Agents, Bedrock, Guardrails, Cedar, MCP, A2A, OpenTelemetry, AIP-C01, GenU, Skill Builder, etc.
- The facts. Translate meaning; do not add new facts, numbers, or features. Do not remove content either (you may split one long sentence into two or three).

## Translate
- All visible text: headings, paragraphs, tables, figcaptions, aria-labels, SVG `<text>` labels, the series line (`<b>AgentCore Reader</b><span>Chapter N / 11 chapters</span>`), meta ("Reading time: about 12 min", "Roadmap stage S1").
- Aside labels: たとえ → "Analogy: ...", 企業ではここで止まる → "Where companies get stuck", ロードマップで出会う場所 → "Where you meet this on the roadmap", 3行まとめ → "Summary in three lines", この章で分かること → "In this chapter".
- Japanese course/book titles: keep the English original where one exists (Skill Builder / Workshop titles are English already). For the Japanese book, write: the book *Amazon Bedrock AgentCore 実践入門* (Japanese) Part N.
- The footer `p.fresh`: "This reader is based on knowledge up to May 2026 and research notes from 2026-09-17. AgentCore adds features almost every month, so check the details in each course and in the developer guide."
- The analogy "新人社員を雇う" = "hiring a new employee". Keep it consistent across chapters.

## B1 English rules (CEFR B1 reader, not a native speaker)
- Short sentences: mostly under 20 words. One idea per sentence.
- Common everyday words. Prefer "use" over "utilize", "check" over "verify", "stop" over "prevent" when possible.
- Explain each technical word the first time it appears in a chapter, in simple words (e.g. "a trace (a record of every step in one request)").
- Avoid idioms, phrasal-verb stacks, slang, and cultural references. Use active voice.
- Keep the friendly, calm tone of the original. No hype words ("powerful", "seamless", "game-changing").

## SVG labels
- English is wider than Japanese. At 13px, one Latin character is about 7px wide (11.5px small text about 6px). Make every label fit inside its box: shorten the wording (1-3 words), or use a smaller class `ts`, or split into two `<text>` lines. You may widen a box or the viewBox only if needed, and keep alignment.

## Links
- In chapter 00, change each chapter link from the claude.ai URL to the local file: `ch01.html`, `ch02.html`, ...

## Report
List the files written, the build result, and any place where you changed meaning slightly to make it simpler.
