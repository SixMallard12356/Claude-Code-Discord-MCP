#!/usr/bin/env python3
"""
Discord MCP Server セットアップスクリプト

このスクリプトは対話的にDiscord MCPサーバーの設定を行います。
"""

import os
import json
import subprocess
import sys
from pathlib import Path


def print_header(text):
    """ヘッダーを表示"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(step_num, text):
    """ステップを表示"""
    print(f"\n[ステップ {step_num}] {text}")


def get_input(prompt, default=None):
    """ユーザー入力を取得"""
    if default:
        user_input = input(f"{prompt} (デフォルト: {default}): ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("  入力が必要です。もう一度入力してください。")


def check_uv():
    """uvがインストールされているか確認"""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    print_header("Discord MCP Server セットアップ")

    print("このスクリプトは、Discord MCPサーバーの設定を対話的に行います。\n")
    print("必要な情報:")
    print("  1. Discord Bot Token")
    print("  2. Discord Server ID (サーバーID)")
    print("  3. Discord Forum Channel ID (フォーラムチャンネルID)")

    # uvのチェック
    print_step(1, "依存関係のチェック")
    if not check_uv():
        print("[エラー] uvがインストールされていません。")
        print("\nuvをインストールしてください:")
        print("  Windows: https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)
    print("[OK] uvが見つかりました")

    # Discord情報の入力
    print_step(2, "Discord情報の入力")
    print("\nDiscord Bot Tokenの取得方法:")
    print("  1. https://discord.com/developers/applications にアクセス")
    print("  2. アプリケーションを選択")
    print("  3. 'Bot' タブ → 'Reset Token' → トークンをコピー")
    bot_token = get_input("\nDiscord Bot Token")

    print("\nServer IDの取得方法:")
    print("  1. Discord設定 → 詳細設定 → 開発者モードを有効化")
    print("  2. サーバーを右クリック → 'IDをコピー'")
    server_id = get_input("\nDiscord Server ID")

    print("\nChannel IDの取得方法:")
    print("  1. フォーラムチャンネルを右クリック → 'IDをコピー'")
    channel_id = get_input("\nDiscord Forum Channel ID")

    # .envファイルの作成
    print_step(3, ".envファイルの作成")
    env_path = Path(__file__).parent / ".env"
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"DISCORD_BOT_TOKEN={bot_token}\n")
        f.write(f"DISCORD_SERVER_ID={server_id}\n")
        f.write(f"DISCORD_IDEAS_CHANNEL_ID={channel_id}\n")
    print(f"[OK] .envファイルを作成しました: {env_path}")

    # 依存関係のインストール
    print_step(4, "依存関係のインストール")
    print("パッケージをインストール中...")
    try:
        subprocess.run(["uv", "sync"], cwd=Path(__file__).parent, check=True)
        print("[OK] 依存関係をインストールしました")
    except subprocess.CalledProcessError:
        print("[エラー] 依存関係のインストールに失敗しました")
        sys.exit(1)

    # Claude Code MCPへの追加
    print_step(5, "Claude Code MCPへの追加")
    add_to_claude = get_input("\nClaude Code MCPに追加しますか？ (y/n)", "y")

    if add_to_claude.lower() == "y":
        project_dir = Path(__file__).parent.absolute()
        cmd = [
            "claude", "mcp", "add", "-s", "user",
            "--transport", "stdio", "discord-ideas",
            "--env", f"DISCORD_BOT_TOKEN={bot_token}",
            "--env", f"DISCORD_SERVER_ID={server_id}",
            "--env", f"DISCORD_IDEAS_CHANNEL_ID={channel_id}",
            "--", "uv", "run", "--directory", str(project_dir),
            "python", "src/discord_mcp/server.py"
        ]

        try:
            subprocess.run(cmd, check=True)
            print("[OK] Claude Code MCPに追加しました")
        except subprocess.CalledProcessError:
            print("[エラー] Claude Code MCPへの追加に失敗しました")
            print("\n手動で追加する場合:")
            print(f"  claude mcp add -s user --transport stdio discord-ideas \\")
            print(f"    --env DISCORD_BOT_TOKEN={bot_token} \\")
            print(f"    --env DISCORD_SERVER_ID={server_id} \\")
            print(f"    --env DISCORD_IDEAS_CHANNEL_ID={channel_id} \\")
            print(f"    -- uv run --directory {project_dir} python src/discord_mcp/server.py")

    # 完了メッセージ
    print_header("セットアップ完了")
    print("Discord MCP Serverのセットアップが完了しました。\n")
    print("次のステップ:")
    print("  1. Discord Developer Portalで以下を確認:")
    print("     - Privileged Gateway Intents (MESSAGE CONTENT, SERVER MEMBERS) が有効")
    print("     - Botがサーバーに招待されている")
    print("     - Botがフォーラムチャンネルにアクセスできる")
    print("\n  2. Claude Codeで試す:")
    print("     claude code")
    print("     > Discordのアイデアスレッドを取得してください")
    print("\n詳細は README.md を参照してください。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n中断されました。")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)
