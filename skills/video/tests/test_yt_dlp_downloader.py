#!/usr/bin/env python3
"""
YtDlpDownloader 单元测试
"""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))

from yt_dlp_downloader import YtDlpDownloader


def test_yt_dlp_downloader_requires_yt_dlp():
    """Test that YtDlpDownloader raises error when yt-dlp is not available"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = FileNotFoundError()
        with pytest.raises(RuntimeError, match="yt-dlp"):
            YtDlpDownloader()


def test_check_available_with_yt_dlp():
    """Test _check_available returns True when yt-dlp exists"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="2026.02.04")
        downloader = YtDlpDownloader()
        assert downloader.yt_dlp_path == "yt-dlp"


def test_download_creates_output_dir():
    """Test that download creates output directory if it doesn't exist"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "videos" / "test"
            downloader = YtDlpDownloader()
            # Mock Popen to avoid actual subprocess call
            with patch('subprocess.Popen') as mock_popen:
                mock_process = MagicMock()
                mock_process.returncode = 0
                mock_process.stdout = iter([])
                mock_popen.return_value = mock_process
                result = downloader.download("https://example.com/video", output_dir)
                assert output_dir.exists()


def test_download_returns_success_on_zero_exit():
    """Test that download returns success=True when yt-dlp exits with 0"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with tempfile.TemporaryDirectory() as tmpdir:
            downloader = YtDlpDownloader()
            # Mock Popen to avoid actual subprocess call
            with patch('subprocess.Popen') as mock_popen:
                mock_process = MagicMock()
                mock_process.returncode = 0
                mock_process.stdout = iter([])
                mock_popen.return_value = mock_process
                result = downloader.download("https://example.com/video", Path(tmpdir))
                assert result["success"] is True
                assert result["error"] == ""


def test_download_returns_failure_on_non_zero_exit():
    """Test that download returns success=False when yt-dlp fails"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with tempfile.TemporaryDirectory() as tmpdir:
            downloader = YtDlpDownloader()
            # Mock Popen to simulate failure
            with patch('subprocess.Popen') as mock_popen:
                mock_process = MagicMock()
                mock_process.returncode = 1
                mock_process.stdout = iter(["Error occurred\n"])
                mock_popen.return_value = mock_process
                result = downloader.download("https://example.com/video", Path(tmpdir))
                assert result["success"] is False
                assert "Error occurred" in result["error"]


def test_download_uses_correct_output_format():
    """Test that download uses correct output template with filename sanitization"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        with tempfile.TemporaryDirectory() as tmpdir:
            downloader = YtDlpDownloader()
            # Mock Popen to capture command arguments
            with patch('subprocess.Popen') as mock_popen:
                mock_process = MagicMock()
                mock_process.returncode = 0
                mock_process.stdout = iter([])
                mock_popen.return_value = mock_process
                downloader.download("https://bilibili.com/video/BV123", Path(tmpdir))

                # Check the command was called correctly
                call_args = mock_popen.call_args
                cmd = call_args[0][0] if call_args else []
                assert "-o" in cmd
                assert str(Path(tmpdir)) in str(cmd)
