# Discord MCP Server

DiscordのフォーラムチャンネルをClaude Code経由でアクセスできるMCPサーバー実装。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## こんな人におすすめ

- 普段からDiscordでチーム開発をしている
- アイデアやメモをDiscordのフォーラムに書いている
- Claude Codeから直接Discordの内容を確認・検索したい
- NotionやSlackより、使い慣れたDiscordを使いたい

## 機能

- スレッド一覧取得: フォーラムチャンネルのスレッドを一覧表示
- メッセージ取得: 特定スレッドの全メッセージを取得
- キーワード検索: スレッド名やメッセージ内容から検索
- 最新アイデア取得: 直近のアイデアスレッドを取得

## セットアップの難易度

初回セットアップには以下が必要です（所要時間: 約30分）：
- Discord Botの作成（Developer Portal）
- フォーラムチャンネルの作成・設定
- Python環境のセットアップ

詳しくは [セットアップガイド](docs/SETUP_GUIDE.md) を参照してください。

## 必要要件

- Python 3.10以上
- uv (Pythonパッケージマネージャー) - [インストール方法](https://docs.astral.sh/uv/getting-started/installation/)
- Discord Bot Token

## インストール

### クイックスタート（初心者向け）

初めての方は **[詳細セットアップガイド](docs/SETUP_GUIDE.md)** を参照してください。
画像付きで丁寧に説明しています。

### 対話的セットアップ（推奨）

```bash
# 1. リポジトリをクローン
git clone https://github.com/SixMallard12356/Claude-Code-Discord-MCP.git
cd Claude-Code-Discord-MCP

# 2. セットアップスクリプトを実行
python setup.py
```

セットアップスクリプトが以下を自動で行います：
- 必要な情報の入力（Bot Token、Server ID、Channel ID）
- `.env`ファイルの作成
- 依存関係のインストール
- Claude Code MCPへの登録

**困ったら**: [トラブルシューティング](#トラブルシューティング) または [詳細ガイド](docs/SETUP_GUIDE.md) を参照

### 手動セットアップ

<details>
<summary>手動でセットアップする場合はこちらをクリック</summary>

### 1. 依存関係のインストール

```bash
cd discord-mcp
uv sync
```

### 2. Discord Bot の設定

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリックしてアプリケーションを作成
3. 左メニューから「Bot」を選択し、「Add Bot」をクリック
4. Bot Tokenをコピー（後で使用）
5. 「Privileged Gateway Intents」で以下を有効化:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT
6. 左メニューから「OAuth2」→「URL Generator」を選択
7. SCOPESで「bot」を選択
8. BOT PERMISSIONSで以下を選択:
   - Read Messages/View Channels
   - Read Message History
9. 生成されたURLでBotをサーバーに招待

### 3. サーバーIDとチャンネルIDの取得

1. Discordの設定から「詳細設定」→「開発者モード」を有効化
2. サーバーを右クリック→「IDをコピー」
3. フォーラムチャンネルを右クリック→「IDをコピー」

### 4. 環境変数の設定

`.env`ファイルを作成し、必要な情報を記入:

```bash
cp .env.example .env
```

`.env`ファイルを編集:

```env
DISCORD_BOT_TOKEN=あなたのBotトークン
DISCORD_SERVER_ID=サーバーID
DISCORD_IDEAS_CHANNEL_ID=フォーラムチャンネルID
```

## 使用方法

### ローカルでのテスト実行

```bash
uv run python src/discord_mcp/server.py
```

### Claude Code との統合

Claude Desktop/Claude Codeの設定ファイルに追加:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "discord-ideas": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "src/discord_mcp/server.py"
      ],
      "cwd": "C:\\Programming\\Discoed\\discord-mcp",
      "env": {
        "DISCORD_BOT_TOKEN": "あなたのBotトークン",
        "DISCORD_SERVER_ID": "サーバーID",
        "DISCORD_IDEAS_CHANNEL_ID": "チャンネルID"
      }
    }
  }
}
```

設定後、Claude Desktopを再起動してください。

## 使用例

セットアップ完了後、Claude Codeから以下のように利用できます:

```
ユーザー: "Discordのアイデアスレッドを5件取得してください"
Claude: [Discord MCPサーバーを使ってスレッド一覧を取得]

ユーザー: "「機能追加」スレッドの内容を教えて"
Claude: [該当スレッドのメッセージを取得して要約]

ユーザー: "音声に関するアイデアを検索して"
Claude: [キーワード検索でマッチするスレッドを表示]
```

## API

### `list_idea_threads`
フォーラムチャンネルのスレッド一覧を取得

**パラメータ:**
- `limit` (int, optional): 取得するスレッド数（デフォルト: 20）
- `archived` (bool, optional): アーカイブされたスレッドも含めるか（デフォルト: true）
  - `true`: アクティブ+アーカイブ両方を取得（推奨）
  - `false`: アクティブなスレッドのみ

### `get_thread_messages`
特定スレッドのメッセージを取得

**パラメータ:**
- `thread_id` (str, required): スレッドID
- `limit` (int, optional): 取得するメッセージ数（デフォルト: 50）

### `search_ideas`
キーワードでアイデアを検索

**パラメータ:**
- `query` (str, required): 検索キーワード
- `limit` (int, optional): 取得する結果数（デフォルト: 10）

### `get_recent_ideas`
最新のアイデアスレッドを取得

**パラメータ:**
- `limit` (int, optional): 取得するスレッド数（デフォルト: 5）

## トラブルシューティング

### Botがサーバーに接続できない
- Botトークンが正しいか確認
- Botがサーバーに招待されているか確認
- 必要な権限（Intents）が有効化されているか確認

### チャンネルが見つからない
- チャンネルIDが正しいか確認
- Botがそのチャンネルを閲覧できる権限があるか確認
- フォーラムチャンネルのIDを指定しているか確認（通常のテキストチャンネルでは動作しません）

### MCP接続エラー
- Claude Desktopの設定ファイルのパスが正しいか確認
- 環境変数が正しく設定されているか確認
- Claude Desktopを完全に再起動（タスクトレイからも終了）

## 技術スタック

- **FastMCP**: MCP サーバーフレームワーク
- **discord.py**: Discord API クライアント
- **python-dotenv**: 環境変数管理

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。
