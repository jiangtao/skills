---
name: usage
description: 使用示例和命令行接口
---

# 使用示例

## 基本使用

### Python API

```python
from pathlib import Path
from download_manager import DownloadManager

# 创建下载管理器
manager = DownloadManager(
    base_dir=Path("./videos"),
    max_concurrent=3
)

# 添加下载链接
urls = [
    "https://www.youtube.com/watch?v=example1",
    "https://www.bilibili.com/video/BV1xx411c7mD",
]
task_ids = manager.add_urls(urls)

# 开始下载
manager.start_download()

# 查看状态
status = manager.get_status()
print(f"Status: {status}")
```

### 命令行使用

```bash
# 下载单个视频
yt-dlp -o "./videos/%(title)s.%(ext)s" "https://www.bilibili.com/video/BVxxx"

# 下载视频并指定格式
yt-dlp -f "bestvideo+bestaudio/best" -o "./videos/%(title)s.%(ext)s" "URL"

# 仅获取信息
yt-dlp --dump-json "https://www.youtube.com/watch?v=xxx"

# 列出可用格式
yt-dlp --list-formats "URL"
```

### 视频合并使用

```bash
# 自动合并指定目录中的所有分离视频文件
python bin/video_merger.py --directory "./videos"

# 预览将要进行的合并操作（不实际执行）
python bin/video_merger.py --directory "./videos" --dry-run

# 详细模式显示合并过程
python bin/video_merger.py --directory "./videos" --verbose

# 递归处理子目录
python bin/video_merger.py --directory "./videos" --recursive
```

## 依赖安装

```bash
# 安装 yt-dlp
brew install yt-dlp

# 或使用 pip 安装
pip install yt-dlp

# 安装 ffmpeg
brew install ffmpeg

# 验证安装
yt-dlp --version
ffmpeg --version
```

## Bilibili 4K/1080P60 内容说明

### 分离文件问题

Bilibili 的部分高清内容（如 4K 和 1080P60）由于版权保护，视频和音频流是分离的。使用 yt-dlp 下载时，可能会得到两个文件：

```
video_name.mp4  (仅视频，无音频)
video_name.m4a  (仅音频，无视频)
```

### 自动合并解决方案

video skill 包含自动合并功能：

1. **自动触发：** 下载完成后自动检测并合并分离文件
2. **手动合并：** 使用 `/video --merge` 命令手动触发合并
3. **命名模式：** 自动识别相同名称的 `.mp4` 和 `.m4a` 文件对

### 示例

```bash
# 下载 Bilibili 1080P60 视频（会产生分离文件）
yt-dlp -f "137+140" -o "./videos/%(title)s.%(ext)s" "BILIBILI_URL"

# 自动合并
python bin/video_merger.py --directory "./videos"

# 结果：
# - video_name.mp4 (仅视频) + video_name.m4a (仅音频)
# → video_name.merged.mp4 (完整视频，包含音频)
```

## FAQ

### Q: 为什么下载的视频没有声音？

A: 这通常发生在 Bilibili 的高清内容上。视频和音频流是分离的。使用 `video_merger.py` 工具自动合并它们。

### Q: yt-dlp 和 lux 有什么区别？

A: yt-dlp 是一个更活跃维护的 YouTube-DL 分支，支持更多网站和格式更新。相比 lux，yt-dlp 在处理分离的视频/音频流方面更可靠。

### Q: 如何处理批量合并？

A: video_merger.py 会自动扫描目录中的所有文件对。只需指定目录即可批量处理：

```bash
python bin/video_merger.py --directory "./videos" --recursive
```

### Q: 合并后的文件会替换原文件吗？

A: 不会。原文件（.mp4 和 .m4a）会被保留，合并后的文件命名为 `.merged.mp4`。原文件可以在确认合并成功后手动删除。

## 高级用法

### 指定下载格式

```bash
# 下载最佳质量
yt-dlp -f "bestvideo+bestaudio/best" "URL"

# 下载特定分辨率
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL"

# 下载 Bilibili 1080P60
yt-dlp -f "137+140" "BILIBILI_URL"
```

### 批量下载

```bash
# 从文件读取 URL 列表
yt-dlp -a urls.txt -o "./videos/%(title)s.%(ext)s"

# 下载整个播放列表
yt-dlp -o "./videos/%(playlist_title)s/%(title)s.%(ext)s" "PLAYLIST_URL"
```
