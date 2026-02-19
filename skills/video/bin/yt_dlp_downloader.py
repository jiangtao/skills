#!/usr/bin/env python3
"""
yt-dlp 下载器封装
支持自动合并视频和音频轨道
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any
import re


class YtDlpDownloader:
    """yt-dlp 下载器封装 - 自动合并视频和音频"""

    def __init__(self, yt_dlp_path: str = "yt-dlp"):
        self.yt_dlp_path = yt_dlp_path
        self._check_available()

    def _check_available(self) -> bool:
        """检查 yt-dlp 是否可用"""
        try:
            result = subprocess.run(
                [self.yt_dlp_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError(f"yt-dlp 不可用，请安装: brew install yt-dlp 或 pipx install yt-dlp")
            return True
        except FileNotFoundError:
            raise RuntimeError(f"yt-dlp 未找到，请安装: brew install yt-dlp 或 pipx install yt-dlp")
        except Exception as e:
            raise RuntimeError(f"yt-dlp 不可用: {e}")

    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名中的非法字符

        Note: This method is currently unused as yt-dlp handles filename
        sanitization internally. Kept for potential future use or custom
        filename handling needs beyond yt-dlp's default behavior.
        """
        # 移除或替换 Windows/Linux 不允许的字符
        illegal_chars = r'[<>:"/\\|?*]'
        # 替换为下划线
        sanitized = re.sub(illegal_chars, '_', filename)
        # 移除前后空格
        sanitized = sanitized.strip()
        # 限制长度 (大多数文件系统限制为 255 字符)
        if len(sanitized) > 200:
            sanitized = sanitized[:200]
        return sanitized

    def download(self, url: str, output_dir: Path,
                 quality: str = "best") -> Dict[str, Any]:
        """
        执行下载，自动合并视频和音频

        Args:
            url: 视频 URL
            output_dir: 输出目录
            quality: 视频质量 (best/worst/high/low)

        Returns:
            包含下载结果的字典
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 使用 yt-dlp 的格式选择器
        # bestvideo+bestaudio/best 会下载最佳质量并自动合并
        format_map = {
            "best": "bestvideo+bestaudio/best",
            "worst": "worstvideo+worstaudio/worst",
            "high": "bestvideo[height<=1080]+bestaudio/best",
            "low": "worstvideo[height>=480]+worstaudio/worst"
        }
        format_selector = format_map.get(quality, "bestvideo+bestaudio/best")

        cmd = [
            self.yt_dlp_path,
            "-f", format_selector,
            "--merge-output-format", "mp4",  # 确保输出为 MP4
            "-o", str(output_dir / "%(title)s.%(ext)s"),  # 输出模板
            "--no-playlist",  # 默认不下载播放列表
            url
        ]

        result = {
            "success": False,
            "output": "",
            "error": "",
            "file_path": None
        }

        try:
            print(f"开始下载: {url}")
            print(f"输出目录: {output_dir}")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            output_lines = []
            for line in process.stdout:
                output_lines.append(line)
                print(line, end='')

            process.wait(timeout=3600)  # 1 hour timeout for downloads

            result["output"] = "".join(output_lines)
            result["success"] = process.returncode == 0

            if process.returncode != 0:
                result["error"] = result["output"]

        except subprocess.TimeoutExpired:
            result["error"] = "Download timeout exceeded"
        except Exception as e:
            result["error"] = str(e)

        return result
