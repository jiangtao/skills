#!/usr/bin/env python3
"""
Tests for DownloadManager using YtDlpDownloader
"""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock, Mock
import sys

# Add parent bin directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))

from download_manager import DownloadManager


def test_download_manager_uses_yt_dlp():
    """Test that DownloadManager uses YtDlpDownloader by default"""
    with patch('download_manager.YtDlpDownloader') as mock_ytdlp:
        mock_downloader = MagicMock()
        mock_downloader.download.return_value = {"success": True}
        mock_ytdlp.return_value = mock_downloader

        manager = DownloadManager(base_dir=tempfile.mkdtemp())
        # Verify the downloader was instantiated
        mock_ytdlp.assert_called_once()
        # Verify it's the YtDlpDownloader class
        assert manager.downloader.__class__.__name__ == "YtDlpDownloader"


def test_download_url_creates_correct_subdirectories():
    """Test that download_url creates source and date subdirectories"""
    with patch('download_manager.YtDlpDownloader') as mock_ytdlp:
        mock_downloader = MagicMock()
        mock_downloader.download.return_value = {"success": True}
        mock_ytdlp.return_value = mock_downloader

        with tempfile.TemporaryDirectory() as tmpdir:
            manager = DownloadManager(base_dir=Path(tmpdir))
            manager.download_url("https://www.bilibili.com/video/BV123")

            # Verify download was called
            assert mock_downloader.download.called
            # Verify the output_dir contains source (bilibili)
            call_args = mock_downloader.download.call_args
            output_dir = call_args[0][1]  # Second argument is output_dir
            assert "bilibili" in str(output_dir)


def test_get_source_from_url():
    """Test URL source detection"""
    manager = DownloadManager(base_dir=tempfile.mkdtemp())

    assert manager.get_source_from_url("https://youtube.com/watch?v=xxx") == "youtube"
    assert manager.get_source_from_url("https://bilibili.com/video/BV123") == "bilibili"
    assert manager.get_source_from_url("https://b23.tv/xxx") == "bilibili"
    assert manager.get_source_from_url("https://example.com/video.mp4") == "direct"


def test_download_url_returns_true_on_success():
    """Test that download_url returns True on successful download"""
    with patch('download_manager.YtDlpDownloader') as mock_ytdlp:
        mock_downloader = MagicMock()
        mock_downloader.download.return_value = {"success": True}
        mock_ytdlp.return_value = mock_downloader

        manager = DownloadManager(base_dir=tempfile.mkdtemp())
        result = manager.download_url("https://youtube.com/watch?v=xxx")
        assert result is True


def test_download_url_returns_false_on_failure():
    """Test that download_url returns False on failed download"""
    with patch('download_manager.YtDlpDownloader') as mock_ytdlp:
        mock_downloader = MagicMock()
        mock_downloader.download.return_value = {
            "success": False,
            "error": "Download failed"
        }
        mock_ytdlp.return_value = mock_downloader

        manager = DownloadManager(base_dir=tempfile.mkdtemp())
        result = manager.download_url("https://youtube.com/watch?v=xxx")
        assert result is False


def test_default_concurrent_is_three():
    """Test that DEFAULT_CONCURRENT is set to 3 for yt-dlp compatibility"""
    from download_manager import DEFAULT_CONCURRENT
    assert DEFAULT_CONCURRENT == 3
