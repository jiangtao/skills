#!/usr/bin/env python3
"""
下载管理执行脚本
基于 yt-dlp 的视频下载管理器
"""

import argparse
import json
import subprocess
import sys
import threading
import time
import os
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
import uuid
import re

# Import YtDlpDownloader
from yt_dlp_downloader import YtDlpDownloader

# 配置
STORAGE_PATH = Path.home() / ".video-downloader" / "links.json"
DEFAULT_OUTPUT_DIR = Path.home() / "Videos" / "baby-videos"
DEFAULT_CONCURRENT = 3  # 默认并发数 (yt-dlp 更高效，降低并发避免服务器限流)


class DownloadManager:
    """下载管理器"""

    def __init__(self, base_dir: Path = DEFAULT_OUTPUT_DIR,
                 max_concurrent: int = DEFAULT_CONCURRENT):
        self.base_dir = Path(base_dir)
        self.max_concurrent = max_concurrent
        self.downloader = YtDlpDownloader()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def load_links(self) -> dict:
        """加载链接"""
        if STORAGE_PATH.exists():
            with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"version": "1.0", "links": []}

    def save_links(self, data: dict):
        """保存链接状态"""
        with open(STORAGE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_source_from_url(self, url: str) -> str:
        """从 URL 推断来源"""
        url_lower = url.lower()
        if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'youtube'
        elif 'bilibili.com' in url_lower or 'b23.tv' in url_lower:
            return 'bilibili'
        return 'direct'

    def download_url(self, url: str) -> bool:
        """下载单个 URL"""
        source = self.get_source_from_url(url)
        date_dir = datetime.now().strftime("%Y/%m")
        output_dir = self.base_dir / source / date_dir

        result = self.downloader.download(url, output_dir)

        if result["success"]:
            print(f"✓ 下载成功: {url}")
            return True
        else:
            print(f"✗ 下载失败: {url}")
            print(f"  错误: {result['error']}")
            return False

    def download_pending(self):
        """下载所有待处理链接"""
        data = self.load_links()
        pending = [link for link in data["links"] if link["status"] == "pending"]

        if not pending:
            print("没有待下载的链接")
            return

        print(f"开始下载 {len(pending)} 个链接...")
        print(f"并发数: {self.max_concurrent}")
        print("")

        # 使用线程池并发下载
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            futures = {
                executor.submit(self.download_url, link["url"]): link
                for link in pending
            }

            for future in as_completed(futures):
                link = futures[future]
                try:
                    success = future.result()
                    # 更新状态
                    for l in data["links"]:
                        if l["id"] == link["id"]:
                            l["status"] = "completed" if success else "failed"
                            l["download_info"]["completed_time"] = datetime.now().isoformat()
                            if not success:
                                l["error"] = "下载失败"
                            break
                except Exception as e:
                    print(f"处理链接时出错: {link['url']}, 错误: {e}")
                    for l in data["links"]:
                        if l["id"] == link["id"]:
                            l["status"] = "failed"
                            l["error"] = str(e)
                            break

        self.save_links(data)
        print(f"\n下载完成！")


def main():
    parser = argparse.ArgumentParser(
        description="视频下载管理工具 (基于 yt-dlp)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
提速建议:
  1. 增加并发数: -c 5 (默认: 3)
  2. 网络较差时: -c 1-2 (减少超时)
  3. yt-dlp 自动合并视频和音频轨道
        """
    )
    parser.add_argument("--url", action="append", help="直接下载 URL（可多次使用）")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT_DIR, help="输出目录")
    parser.add_argument("--concurrent", "-c", type=int, default=DEFAULT_CONCURRENT,
                       help=f"并发下载数 (默认: {DEFAULT_CONCURRENT})")
    parser.add_argument("--pending", action="store_true", help="下载所有待处理链接")
    parser.add_argument("--quality", "-q", default="best",
                       help="视频质量 (best/worst/high/low)")

    args = parser.parse_args()

    # 显示配置信息
    print("=" * 50)
    print("视频下载管理工具")
    print("=" * 50)
    print(f"并发数: {args.concurrent}")
    print(f"视频质量: {args.quality}")
    print("=" * 50)
    print()

    manager = DownloadManager(
        base_dir=args.output,
        max_concurrent=args.concurrent
    )

    if args.url:
        # 直接下载指定 URL
        for url in args.url:
            manager.download_url(url)
    elif args.pending:
        # 下载待处理链接
        manager.download_pending()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
