# Contributing to Discord MCP Server

Discord MCP Serverへの貢献ありがとうございます！

## 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/your-username/discord-mcp.git
cd discord-mcp

# 依存関係をインストール
uv sync

# .envファイルを作成
cp .env.example .env
# .envファイルを編集して、必要な情報を記入
```

## 開発ワークフロー

1. **フォーク**: このリポジトリをフォークします
2. **ブランチ作成**: 機能やバグ修正用のブランチを作成します
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **コード変更**: 変更を加えます
4. **テスト**: 変更が正しく動作することを確認します
5. **コミット**: わかりやすいコミットメッセージで変更をコミットします
   ```bash
   git commit -m "feat: add new feature"
   ```
6. **プッシュ**: フォークしたリポジトリにプッシュします
   ```bash
   git push origin feature/your-feature-name
   ```
7. **プルリクエスト**: 元のリポジトリにプルリクエストを作成します

## コミットメッセージの規約

コミットメッセージは以下の形式に従ってください：

```
<type>: <description>

[optional body]
```

**Type:**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマットなど）
- `refactor`: バグ修正や機能追加ではないコード変更
- `test`: テストの追加や修正
- `chore`: ビルドプロセスやツールの変更

**例:**
```
feat: add support for private threads
fix: handle empty channel gracefully
docs: update installation instructions
```

## コードスタイル

- Python: PEP 8に従う
- 型ヒントを可能な限り使用する
- docstringを各関数に記述する
- エラーハンドリングを適切に実装する

## 新機能の提案

新機能を提案する場合は、まずIssueを作成して議論してください。以下の情報を含めてください：

- 機能の説明
- ユースケース
- 実装案（あれば）

## バグ報告

バグを発見した場合は、以下の情報を含めてIssueを作成してください：

- バグの説明
- 再現手順
- 期待される動作
- 実際の動作
- 環境情報（OS、Pythonバージョンなど）
- ログやエラーメッセージ

## 質問やサポート

質問がある場合は、Issueを作成してください。タグに `question` を付けてください。

## ライセンス

このプロジェクトに貢献することで、あなたの貢献がMITライセンスの下でライセンスされることに同意したものとみなされます。
