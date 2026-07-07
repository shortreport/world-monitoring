# World News Site

AI を活用した世界ニュースまとめサイトです。

## ページ構成

| ページ | 内容 |
|--------|------|
| **ホーム** | 米中・中東・日本経済など主要ニュースのカード形式まとめ |
| **メール要約** | 受信メールを Claude AI が送信者別に要約 |
| **USトランプ** | トランプ大統領・主要閣僚の言動モニタリング（Truth Social / WH RSS / YouTube） |

## 公開サイト

[https://shondo.github.io/world-news-site/](https://shondo.github.io/world-news-site/)

## サイト生成

```bash
# USトランプページのデータ収集・更新
python trump_monitor.py

# 全ページの HTML 生成
python generate_site.py
```

## 技術仕様

- 静的 HTML サイト（サーバー不要）
- GitHub Pages でホスティング（`docs/` ディレクトリ）
- Claude AI (claude-haiku) で要約・構造化
- データソース: Truth Social / White House RSS / YouTube / Google News RSS / World News API
