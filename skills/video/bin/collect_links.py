#!/usr/bin/env python3
"""
链接收集执行脚本
支持手动输入、书签导入、剪贴板监控
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import uuid

# 配置
STORAGE_PATH = Path.home() / ".video-downloader" / "links.json"
VIDEO_DOMAINS = {
    'youtube.com', 'youtu.be',
    'bilibili.com', 'b23.tv',
    'vimeo.com',
    'douyin.com', 'tiktok.com'
}

def is_video_url(url: str) -> bool:
    """检查是否是视频 URL"""
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
        return any(domain in parsed.netloc.lower() for domain in VIDEO_DOMAINS)
    except Exception:
        return False

def normalize_url(url: str) -> str:
    """规范化 URL，移除追踪参数"""
    from urllib.parse import parse_qs, urlencode, urlunparse

    TRACKING_PARAMS = {'utm_source', 'utm_medium', 'utm_campaign', 'fbclid'}

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    for param in TRACKING_PARAMS:
        query_params.pop(param, None)

    return urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path,
        parsed.params,
        urlencode(query_params, doseq=True),
        ''
    ))

def load_links() -> dict:
    """加载现有链接"""
    if STORAGE_PATH.exists():
        with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "1.0", "last_updated": "", "links": []}

def save_links(data: dict):
    """保存链接"""
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(STORAGE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_url(url: str, source: str = "manual") -> bool:
    """添加单个 URL"""
    if not is_video_url(url):
        print(f"跳过无效视频 URL: {url}", file=sys.stderr)
        return False

    normalized = normalize_url(url)
    data = load_links()

    # 检查重复
    for link in data["links"]:
        if normalize_url(link["url"]) == normalized:
            print(f"链接已存在: {url}")
            return False

    # 添加新链接
    new_link = {
        "id": f"link-{uuid.uuid4().hex[:12]}",
        "url": url,
        "source": source,
        "added_time": datetime.now().isoformat(),
        "title": None,
        "status": "pending",
        "metadata": {"duration": None, "thumbnail": None},
        "download_info": {"file_path": None, "file_size": None, "completed_time": None},
        "error": None
    }

    data["links"].append(new_link)
    save_links(data)
    print(f"已添加: {url}")
    return True

def main():
    parser = argparse.ArgumentParser(description="视频链接收集工具")
    parser.add_argument("--url", action="append", help="添加视频 URL（可多次使用）")
    parser.add_argument("--file", type=Path, help="从文件读取 URL 列表")
    parser.add_argument("--list", action="store_true", help="列出所有待下载链接")
    parser.add_argument("--source", default="manual", help="链接来源标识")

    args = parser.parse_args()

    if args.url:
        for url in args.url:
            add_url(url.strip(), args.source)

    if args.file:
        if args.file.exists():
            with open(args.file, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):
                        add_url(url, args.source)

    if args.list:
        data = load_links()
        pending = [link for link in data["links"] if link["status"] == "pending"]
        print(f"\n待下载链接: {len(pending)}")
        for link in pending:
            print(f"  - {link['url']} [{link['source']}]")

if __name__ == "__main__":
    main()
