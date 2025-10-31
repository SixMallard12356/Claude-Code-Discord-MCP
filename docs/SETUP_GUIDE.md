# Discord MCP Server セットアップガイド（初心者向け）

このガイドでは、Discord MCP Serverを一から設定する方法を、画像付きで詳しく説明します。

## 前提知識

このガイドは以下の前提で説明します：
- Discordアカウントを持っている
- 自分のDiscordサーバーを持っている（または管理者権限がある）
- Windowsを使用している（Mac/Linuxの場合は一部コマンドが異なります）

## 所要時間

初めての方：約30分〜1時間
経験者：約15分

---

## ステップ1: 必要なソフトウェアのインストール

### 1-1. Python のインストール

1. [Python公式サイト](https://www.python.org/downloads/)にアクセス
2. 「Download Python 3.xx」をクリック
3. インストーラーを実行
4. **重要**: 「Add Python to PATH」にチェックを入れる
5. 「Install Now」をクリック

確認方法（コマンドプロンプトで）:
```bash
python --version
```

### 1-2. uv のインストール

PowerShellを開いて以下を実行：
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

確認方法：
```bash
uv --version
```

### 1-3. Claude Code のインストール

既にインストール済みであればスキップ。

---

## ステップ2: Discord Botの作成

### 2-1. Discord Developer Portalにアクセス

1. https://discord.com/developers/applications にアクセス
2. Discordにログイン
3. 右上の「New Application」をクリック

### 2-2. アプリケーションを作成

1. アプリケーション名を入力（例: "My Ideas Bot"）
2. 利用規約に同意
3. 「Create」をクリック

### 2-3. Botを追加

1. 左メニューから「Bot」を選択
2. 「Add Bot」をクリック
3. 「Yes, do it!」をクリック

### 2-4. Bot Tokenを取得

1. 「Reset Token」をクリック（初回は「View Token」）
2. 表示されたトークンを**メモ帳などに保存**（後で使います）
   - 例: `MTQzMzYxODMzMjYyNzYzNjM1Nw.G21Uxr.EAN3bVr...`
3. **重要**: このトークンは誰にも見せないでください！

### 2-5. Privileged Gateway Intents を有効化

1. 同じ「Bot」ページで下にスクロール
2. 「Privileged Gateway Intents」セクションを見つける
3. 以下の2つを**ON**にする：
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT
4. 「Save Changes」をクリック

### 2-6. Botをサーバーに招待

1. 左メニューから「OAuth2」→「URL Generator」を選択
2. 「SCOPES」で以下を選択：
   - ✅ bot
3. 「BOT PERMISSIONS」で以下を選択：
   - ✅ View Channels
   - ✅ Read Message History
4. 一番下に生成されたURLをコピー
5. URLをブラウザで開く
6. Botを追加したいサーバーを選択
7. 「認証」をクリック

---

## ステップ3: Discord IDの取得

### 3-1. 開発者モードを有効化

1. Discordを開く
2. 左下の「ユーザー設定」（歯車アイコン）をクリック
3. 「詳細設定」（Advanced）を選択
4. 「開発者モード」（Developer Mode）を**ON**にする

### 3-2. サーバーIDを取得

1. Discordのサーバー一覧で、対象のサーバーを**右クリック**
2. 「IDをコピー」をクリック
3. メモ帳に貼り付けて保存
   - 例: `1355798461076869130`

### 3-3. フォーラムチャンネルを作成（まだない場合）

**既にフォーラムチャンネルがある場合はスキップ**

1. Discordサーバーで、チャンネル一覧の上にある「+」をクリック
2. 「チャンネルを作成」を選択
3. チャンネルタイプで「フォーラム」を選択
4. チャンネル名を入力（例: "アイデア", "ideas"）
5. 「チャンネルを作成」をクリック

**初期設定ウィザードが表示される場合**:
- 「推奨権限の設定」: そのまま次へ（または@everyoneのまま）
- 「投稿ガイドライン」: スキップ可能
- 「タグを作成」: スキップ可能（後で追加できます）
- 「デフォルトのリアクション」: スキップ可能
- 「最初の投稿」: 「後で」を選択してスキップ可能

**簡単セットアップ**: 全部スキップして後で設定してもOKです。まずは動作確認を優先しましょう。

### 3-4. フォーラムチャンネルIDを取得

1. 作成したフォーラムチャンネルを**右クリック**
2. 「IDをコピー」をクリック
3. メモ帳に貼り付けて保存
   - 例: `1356557137429659841`

**注意**: 必ず**フォーラムチャンネル**のIDを取得してください。通常のテキストチャンネルでは動作しません。

---

## ステップ4: Discord MCP Serverのセットアップ

### 4-1. プロジェクトをダウンロード

コマンドプロンプトまたはPowerShellで：
```bash
git clone https://github.com/SixMallard12356/Claude-Code-Discord-MCP.git
cd Claude-Code-Discord-MCP
```

gitがインストールされていない場合：
1. https://github.com/SixMallard12356/Claude-Code-Discord-MCP にアクセス
2. 緑色の「Code」→「Download ZIP」
3. ZIPを解凍
4. コマンドプロンプトで解凍したフォルダに移動

### 4-2. セットアップスクリプトを実行

```bash
python setup.py
```

以下の情報を入力してください（先ほどメモした情報）：
1. **Discord Bot Token**: `MTQzMzYxODMzMjYyNzYzNjM1Nw.G21Uxr...`
2. **Discord Server ID**: `1355798461076869130`
3. **Discord Forum Channel ID**: `1356557137429659841`

「Claude Code MCPに追加しますか？」と聞かれたら `y` を入力。

---

## ステップ5: 動作確認

### 5-1. Claude Codeを起動

```bash
claude code
```

### 5-2. MCP接続を確認

```bash
/mcp
```

`discord-ideas` が表示されていればOK！

### 5-3. 試しに使ってみる

```
Discordのアイデアスレッドを5件取得してください
```

スレッド一覧が表示されれば成功です！

---

## トラブルシューティング

### エラー: "uvがインストールされていません"

1. uvのインストールコマンドを再度実行
2. PowerShellまたはコマンドプロンプトを再起動
3. `uv --version` で確認

### エラー: "403 Forbidden: Missing Access"

**原因**: Botがチャンネルにアクセスできない

**解決方法**:
1. フォーラムチャンネルを右クリック→「チャンネルを編集」
2. 「権限」タブ
3. Botのロールを追加
4. 以下の権限を**許可**（緑）にする：
   - チャンネルを見る
   - メッセージを読む
   - メッセージ履歴を読む

### エラー: "PrivilegedIntentsRequired"

**原因**: Privileged Gateway Intentsが有効化されていない

**解決方法**:
1. Discord Developer Portal → Bot タブ
2. Privileged Gateway Intentsの2つをONにする
3. Save Changes

### スレッドが表示されない

**確認事項**:
1. フォーラムチャンネルに実際にスレッドが存在するか
2. チャンネルIDが正しいか（フォーラムチャンネルのIDか）
3. Botがそのチャンネルを見る権限があるか

---

## よくある質問（FAQ）

### Q: Botトークンを忘れました

A: Discord Developer Portalの「Bot」タブで「Reset Token」をクリックして新しいトークンを生成してください。`.env`ファイルも更新する必要があります。

### Q: 複数のフォーラムチャンネルを監視できますか？

A: 現在は1つのチャンネルのみサポートしています。複数チャンネルのサポートは今後の機能として検討中です。

### Q: プライベートスレッドは取得できますか？

A: 現在はパブリックスレッドとアーカイブスレッドのみサポートしています。

### Q: 他の人も使えるようにするには？

A: 同じサーバーのメンバーであれば、各自がこのセットアップを行うことで使用できます。

---

## サポート

問題が解決しない場合：
1. [GitHub Issues](https://github.com/SixMallard12356/Claude-Code-Discord-MCP/issues) で報告
2. エラーメッセージの全文を含めてください
3. 環境情報（OS、Pythonバージョンなど）も記載してください

---

## 次のステップ

- [使用例](../README.md#使用例) を見て、どんなことができるか確認
- [トラブルシューティング](../README.md#トラブルシューティング) で困ったときの対処法を確認
- [貢献ガイド](../CONTRIBUTING.md) でプロジェクトへの貢献方法を確認
