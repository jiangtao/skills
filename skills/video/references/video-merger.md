---
name: video-merger
description: 视频合并工具参考文档
---

# VideoMerger 功能描述

VideoMerger 是一个自动化的视频文件合并工具，专门用于处理因版权保护或编码限制而分离的视频和音频文件。它主要用于解决 Bilibili 等平台的 4K 和 1080P60 高清内容下载后产生的分离文件问题。

## 使用场景

### 1. Bilibili 高清内容

Bilibili 的部分高清内容（4K 和 1080P60）由于版权保护，视频和音频流是分离的。使用 yt-dlp 下载时，会产生两个文件：

```
video_title.mp4  # 仅包含视频流
video_title.m4a  # 仅包含音频流
```

VideoMerger 可以自动识别这些文件对并合并为完整的视频文件。

### 2. 批量处理

当下载大量视频后，可以使用 VideoMerger 批量处理所有分离文件：

```bash
python bin/video_merger.py --directory "./videos" --recursive
```

### 3. 自动化工作流

VideoMerger 可以集成到下载流程中，在下载完成后自动触发合并：

```python
from video_merger import VideoMerger

# 在下载完成后触发
merger = VideoMerger(directory=output_dir)
merger.merge()
```

## CLI 用法

### 基本命令

```bash
# 合并指定目录中的所有分离视频文件
python bin/video_merger.py --directory "./videos"

# 预览模式（显示将要进行的操作，但不实际执行）
python bin/video_merger.py --directory "./videos" --dry-run

# 详细模式（显示合并过程的详细信息）
python bin/video_merger.py --directory "./videos" --verbose

# 递归处理（包括所有子目录）
python bin/video_merger.py --directory "./videos" --recursive
```

### 参数说明

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--directory` | `-d` | 要处理的目录路径（必需） | - |
| `--dry-run` | `-n` | 预览模式，不实际执行合并 | False |
| `--recursive` | `-r` | 递归处理子目录 | False |
| `--verbose` | `-v` | 显示详细信息 | False |

### 使用示例

```bash
# 基本使用
python bin/video_merger.py --directory ~/Downloads/videos

# 预览将要合并的文件
python bin/video_merger.py -d ~/Downloads/videos -n

# 递归处理并显示详细信息
python bin/video_merger.py -d ~/Downloads/videos -r -v
```

## 文件命名模式

VideoMerger 使用智能文件名匹配算法来识别需要合并的文件对：

### 识别规则

1. **基本名称相同：** 文件的基本名称（不含扩展名）必须相同
2. **扩展名匹配：** 一个文件必须是 `.mp4`（视频），另一个必须是 `.m4a`（音频）
3. **位置相同：** 两个文件必须位于同一目录中

### 示例

```
# 可识别的文件对
video.mp4 + video.m4a → video.merged.mp4
我的视频.mp4 + 我的视频.m4a → 我的视频.merged.mp4
episode_01.mp4 + episode_01.m4a → episode_01.merged.mp4

# 不可识别的情况
video.mp4 + video_audio.mp4  # 扩展名不匹配
video.mp4 + audio.m4a        # 基本名称不同
dir1/video.mp4 + dir2/video.m4a  # 不同目录
```

### 输出命名

合并后的文件命名规则：

```
<原文件名>.merged.mp4
```

示例：
- `video.mp4` + `video.m4a` → `video.merged.mp4`
- `my_video.mp4` + `my_video.m4a` → `my_video.merged.mp4`

## 性能信息

### 合并速度

- **1080P 视频：** 约 5-10 秒/文件
- **4K 视频：** 约 10-20 秒/文件
- **速度因素：** 文件大小、CPU 性能、磁盘 I/O

### 资源占用

- **内存：** 通常 < 200MB
- **CPU：** 合并期间单核占用较高
- **磁盘：** 临时文件约为原始视频大小的 1.5-2 倍

### 批量处理性能

```python
# 示例：处理 100 个 1080P 视频文件对
# 预期时间：约 8-16 分钟
# 具体时间取决于硬件配置
```

## 错误处理

### 常见错误及解决方案

1. **ffmpeg 未安装**
   ```
   Error: ffmpeg is not installed or not in PATH
   ```
   解决：`brew install ffmpeg` 或 `apt-get install ffmpeg`

2. **文件名包含特殊字符**
   ```
   Error: Unable to process file with special characters
   ```
   解决：重命名文件，避免使用特殊字符

3. **磁盘空间不足**
   ```
   Error: Insufficient disk space
   ```
   解决：清理磁盘空间或使用其他存储位置

### 错误恢复

VideoMerger 在遇到错误时会：
- 记录错误日志
- 跳过当前文件对
- 继续处理其他文件
- 在结束时显示错误摘要

## 集成示例

### Python API

```python
from pathlib import Path
from video_merger import VideoMerger

# 创建合并器
merger = VideoMerger(directory=Path("./videos"))

# 执行合并
results = merger.merge()

# 查看结果
for result in results:
    print(f"{result['video']} + {result['audio']} → {result['output']}")
    print(f"Status: {result['status']}")
    if result.get('error'):
        print(f"Error: {result['error']}")
```

### 与下载管理器集成

```python
from download_manager import DownloadManager
from video_merger import VideoMerger

# 下载视频
manager = DownloadManager(base_dir=Path("./videos"))
manager.add_urls(["BILIBILI_URL"])
manager.start_download()

# 自动合并下载的视频
merger = VideoMerger(directory=Path("./videos"))
merge_results = merger.merge()

print(f"Downloaded and merged {len(merge_results)} videos")
```

## 最佳实践

1. **先预览再执行：** 使用 `--dry-run` 参数预览将要进行的操作
2. **备份原始文件：** 虽然原始文件不会被删除，但建议先备份
3. **验证合并结果：** 合并完成后验证视频是否正常播放
4. **批量处理：** 使用 `--recursive` 参数处理整个目录树
5. **日志记录：** 使用 `--verbose` 参数记录详细的合并过程

## 故障排除

### 问题：合并后视频没有声音

**可能原因：**
- 音频文件损坏
- 音频编码不支持

**解决方案：**
```bash
# 检查音频文件
ffprobe audio_file.m4a

# 使用不同编码重新合并
ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a aac output.mp4
```

### 问题：合并后视频不同步

**可能原因：**
- 音视频时长不一致
- 时间戳问题

**解决方案：**
```bash
# 使用 -shortest 选项
ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a aac -shortest output.mp4
```

### 问题：找不到匹配的文件对

**可能原因：**
- 文件名不匹配
- 文件扩展名不正确

**解决方案：**
```bash
# 检查文件列表
ls -la ./videos/*.mp4 ./videos/*.m4a

# 手动重命名文件以匹配
mv old_name.mp4 video.mp4
mv old_name.m4a video.m4a
```
