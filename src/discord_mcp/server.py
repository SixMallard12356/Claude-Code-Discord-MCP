"""
Discord MCP Server - メイン実装

Discordのフォーラムチャンネルからアイデアやメモを取得するMCPサーバー。
"""

import os
import asyncio
from typing import Optional, List, Dict, Any
import discord
from discord.ext import commands
from fastmcp import FastMCP
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# Discord Bot設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 環境変数
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID", "0"))
DISCORD_IDEAS_CHANNEL_ID = int(os.getenv("DISCORD_IDEAS_CHANNEL_ID", "0"))

# グローバル変数でBotの準備完了を管理
bot_ready = asyncio.Event()


@bot.event
async def on_ready():
    """Botが準備完了したときのイベントハンドラ"""
    print(f"Discord Bot logged in as {bot.user}")
    bot_ready.set()


# FastMCP初期化
mcp = FastMCP("Discord Ideas MCP")


async def ensure_bot_ready():
    """Botが準備完了するまで待機"""
    if not bot_ready.is_set():
        # Botをバックグラウンドで起動
        asyncio.create_task(bot.start(DISCORD_BOT_TOKEN))
        await bot_ready.wait()


def get_guild() -> discord.Guild:
    """
    サーバーを取得

    Returns:
        discord.Guild: Discordサーバーオブジェクト

    Raises:
        ValueError: サーバーが見つからない場合
    """
    guild = bot.get_guild(DISCORD_SERVER_ID)
    if not guild:
        raise ValueError(f"Server ID {DISCORD_SERVER_ID} not found")
    return guild


def get_ideas_channel() -> discord.ForumChannel:
    """
    アイデアフォーラムチャンネルを取得

    Returns:
        discord.ForumChannel: フォーラムチャンネルオブジェクト

    Raises:
        ValueError: チャンネルが見つからない、またはフォーラムチャンネルではない場合
    """
    guild = get_guild()
    channel = guild.get_channel(DISCORD_IDEAS_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.ForumChannel):
        raise ValueError(f"Forum channel ID {DISCORD_IDEAS_CHANNEL_ID} not found or not a forum channel")
    return channel


@mcp.tool()
async def list_idea_threads(
    limit: int = 20,
    archived: bool = False
) -> List[Dict[str, Any]]:
    """
    フォーラムチャンネルのスレッド一覧を取得

    Args:
        limit: 取得するスレッド数（デフォルト: 20）
        archived: アーカイブされたスレッドも含めるか（デフォルト: False）

    Returns:
        スレッド情報のリスト。各スレッドには以下の情報が含まれます:
        - id: スレッドID
        - name: スレッド名
        - created_at: 作成日時
        - message_count: メッセージ数
        - archived: アーカイブ状態
        - tags: 適用されているタグのリスト

    Raises:
        ValueError: サーバーまたはチャンネルが見つからない場合
    """
    await ensure_bot_ready()

    guild = get_guild()
    channel = get_ideas_channel()
    threads = []

    # Guildのアクティブスレッドから該当チャンネルのものを取得
    active_threads = await guild.active_threads()

    for thread in active_threads.threads:
        if thread.parent_id == channel.id:
            if len(threads) >= limit:
                break
            threads.append({
                "id": str(thread.id),
                "name": thread.name,
                "created_at": thread.created_at.isoformat() if thread.created_at else None,
                "message_count": thread.message_count or 0,
                "archived": thread.archived,
                "tags": [tag.name for tag in thread.applied_tags] if thread.applied_tags else []
            })

    # アーカイブされたスレッドも取得（必要な場合）
    if archived and len(threads) < limit:
        try:
            async for thread in channel.archived_threads(limit=limit - len(threads)):
                threads.append({
                    "id": str(thread.id),
                    "name": thread.name,
                    "created_at": thread.created_at.isoformat() if thread.created_at else None,
                    "message_count": thread.message_count or 0,
                    "archived": thread.archived,
                    "tags": [tag.name for tag in thread.applied_tags] if thread.applied_tags else []
                })

                if len(threads) >= limit:
                    break
        except Exception as e:
            # アーカイブスレッド取得失敗時はエラーを無視（権限不足の可能性）
            print(f"Warning: Could not fetch archived threads: {e}")

    return threads[:limit]


@mcp.tool()
async def get_thread_messages(
    thread_id: str,
    limit: int = 50
) -> Dict[str, Any]:
    """
    特定スレッドのメッセージを取得

    Args:
        thread_id: スレッドID（文字列）
        limit: 取得するメッセージ数（デフォルト: 50）

    Returns:
        スレッド情報とメッセージのリストを含む辞書:
        - thread_name: スレッド名
        - messages: メッセージのリスト（各メッセージにはid, author, content, created_at, attachmentsが含まれる）

    Raises:
        ValueError: スレッドが見つからない場合
    """
    await ensure_bot_ready()

    guild = get_guild()
    thread = guild.get_thread(int(thread_id))

    if not thread:
        raise ValueError(f"Thread ID {thread_id} not found")

    messages = []
    async for message in thread.history(limit=limit, oldest_first=True):
        messages.append({
            "id": str(message.id),
            "author": str(message.author),
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "attachments": [att.url for att in message.attachments] if message.attachments else []
        })

    return {
        "thread_name": thread.name,
        "messages": messages
    }


@mcp.tool()
async def search_ideas(
    query: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    キーワードでアイデアを検索

    スレッド名とメッセージ内容を検索します。

    Args:
        query: 検索キーワード
        limit: 取得する結果数（デフォルト: 10）

    Returns:
        マッチしたスレッドとメッセージのリスト。各結果には以下が含まれます:
        - thread_id: スレッドID
        - thread_name: スレッド名
        - matched_in: マッチした場所（"thread_name" または "message"）
        - matched_message: マッチしたメッセージ情報（メッセージにマッチした場合のみ）

    Raises:
        ValueError: サーバーまたはチャンネルが見つからない場合
    """
    await ensure_bot_ready()

    channel = get_ideas_channel()
    results = []
    query_lower = query.lower()

    # アクティブスレッドを検索
    for thread in channel.threads:
        if len(results) >= limit:
            break

        # スレッド名をチェック
        if query_lower in thread.name.lower():
            results.append({
                "thread_id": str(thread.id),
                "thread_name": thread.name,
                "matched_in": "thread_name",
                "matched_content": thread.name
            })
            continue

        # メッセージ内容をチェック
        try:
            async for message in thread.history(limit=20):
                if query_lower in message.content.lower():
                    results.append({
                        "thread_id": str(thread.id),
                        "thread_name": thread.name,
                        "matched_in": "message",
                        "matched_message": {
                            "content": message.content[:200],  # 最初の200文字
                            "author": str(message.author),
                            "created_at": message.created_at.isoformat()
                        }
                    })
                    break
        except Exception as e:
            # メッセージ取得に失敗した場合はスキップ
            print(f"Error fetching messages from thread {thread.id}: {e}")
            continue

    return results[:limit]


@mcp.tool()
async def get_recent_ideas(limit: int = 5) -> List[Dict[str, Any]]:
    """
    最新のアイデアスレッドを取得

    Args:
        limit: 取得するスレッド数（デフォルト: 5）

    Returns:
        最新スレッド情報のリスト（list_idea_threadsと同じ形式）
    """
    await ensure_bot_ready()

    channel = get_ideas_channel()
    threads = []

    # アクティブスレッドを取得
    for thread in channel.threads:
        if len(threads) >= limit:
            break

        threads.append({
            "id": str(thread.id),
            "name": thread.name,
            "created_at": thread.created_at.isoformat() if thread.created_at else None,
            "message_count": thread.message_count or 0,
            "archived": thread.archived,
            "tags": [tag.name for tag in thread.applied_tags] if thread.applied_tags else []
        })

    return threads[:limit]


if __name__ == "__main__":
    # 環境変数のバリデーション
    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN environment variable is not set")
    if DISCORD_SERVER_ID == 0:
        raise ValueError("DISCORD_SERVER_ID environment variable is not set")
    if DISCORD_IDEAS_CHANNEL_ID == 0:
        raise ValueError("DISCORD_IDEAS_CHANNEL_ID environment variable is not set")

    # MCPサーバーを起動
    print("Starting Discord MCP Server...")
    mcp.run()
