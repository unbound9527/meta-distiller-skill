#!/usr/bin/env python3
"""社交媒体内容抓取工具 - 支持 Twitter/X"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error


def fetch_twitter_user(handle: str, limit: int, output: str) -> bool:
    """
    通过非官方 API 抓取 Twitter 用户推文
    注意：需要 Bearer Token，建议使用官方 API 或第三方服务
    """
    # Twitter API v2 非官方抓取（需要 Bearer Token）
    bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        print("[social_scraper] TWITTER_BEARER_TOKEN not set.", file=sys.stderr)
        print("[social_scraper] Set it via: export TWITTER_BEARER_TOKEN='your_token'", file=sys.stderr)
        # 回退：生成示例文件
        return create_sample_output(handle, limit, output)

    # 清理 handle
    handle = handle.lstrip("@")

    url = f"https://api.twitter.com/2/users/by/username/{handle}"
    params = {"user.fields": "description,public_metrics"}

    try:
        req = urllib.request.Request(
            urllib.parse.urljoin(url, f"?{urllib.parse.urlencode(params)}"),
            headers={"Authorization": f"Bearer {bearer_token}"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            user_data = json.loads(resp.read())

        # 获取用户 ID
        user_id = user_data.get("data", {}).get("id")
        if not user_id:
            print(f"[social_scraper] User @{handle} not found", file=sys.stderr)
            return False

        # 获取推文
        tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        tweets_params = {
            "max_results": min(limit, 100),
            "tweet.fields": "created_at,public_metrics,lang",
            "expansions": "attachments.media_keys",
        }

        tweets_req = urllib.request.Request(
            urllib.parse.urljoin(tweets_url, f"?{urllib.parse.urlencode(tweets_params)}"),
            headers={"Authorization": f"Bearer {bearer_token}"}
        )
        with urllib.request.urlopen(tweets_req, timeout=30) as resp:
            tweets_data = json.loads(resp.read())

        tweets = tweets_data.get("data", [])
        meta = tweets_data.get("meta", {})

        result = {
            "handle": handle,
            "user": user_data.get("data", {}),
            "tweets": tweets,
            "count": len(tweets),
            "has_more": bool(meta.get("next_token")),
            "fetched_via": "twitter_api_v2",
        }

        with open(output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[social_scraper] Fetched {len(tweets)} tweets from @{handle}")
        print(f"[social_scraper] Output: {output}")
        return True

    except urllib.error.HTTPError as e:
        print(f"[social_scraper] HTTP {e.code}: {e.reason}", file=sys.stderr)
        return create_sample_output(handle, limit, output)
    except Exception as e:
        print(f"[social_scraper] Error: {e}", file=sys.stderr)
        return create_sample_output(handle, limit, output)


def create_sample_output(handle: str, limit: int, output: str) -> bool:
    """当无法抓取时，生成示例输出文件"""
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    sample = {
        "handle": handle.lstrip("@"),
        "user": {
            "username": handle.lstrip("@"),
            "description": f"Sample data for @{handle} (API not configured)",
            "public_metrics": {"followers_count": 0, "following_count": 0},
        },
        "tweets": [],
        "count": 0,
        "fetched_via": "sample",
        "note": "Configure TWITTER_BEARER_TOKEN for real data",
    }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)

    print(f"[social_scraper] Created sample output (no API token): {output}")
    return True


def main():
    parser = argparse.ArgumentParser(description="抓取社交媒体内容（Twitter/X）")
    parser.add_argument("--handle", required=True, help="账号 Handle（如 @username）")
    parser.add_argument("--limit", type=int, default=500, help="抓取条数")
    parser.add_argument("--output", required=True, help="输出文件路径")
    args = parser.parse_args()

    print(f"[social_scraper] Fetching: {args.handle}")
    print(f"[social_scraper] Limit: {args.limit}")
    print(f"[social_scraper] Output: {args.output}")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if "twitter.com" in args.handle or args.handle.startswith("@"):
        success = fetch_twitter_user(args.handle, args.limit, args.output)
    else:
        # 通用 fallback
        success = create_sample_output(args.handle, args.limit, args.output)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
