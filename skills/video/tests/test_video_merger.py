import unittest
from pathlib import Path
import tempfile
import subprocess
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "bin"))

from video_merger import VideoMerger, find_split_files


class TestVideoMerger(unittest.TestCase):

    def test_find_split_files_identifies_pairs(self):
        """Test that find_split_files correctly identifies video/audio pairs"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create test files matching Bilibili split pattern
            (tmpdir / "video1.f100026.mp4").touch()
            (tmpdir / "video1.f30280.m4a").touch()
            (tmpdir / "video2.f30077.mp4").touch()
            (tmpdir / "video2.f30280.m4a").touch()
            (tmpdir / "standalone.mp4").touch()

            pairs = list(find_split_files(tmpdir))

            self.assertEqual(len(pairs), 2)
            # Compare Path objects, not strings
            pair_names = [(p[0].name, p[1].name) for p in pairs]
            self.assertIn(("video1.f100026.mp4", "video1.f30280.m4a"), pair_names)
            self.assertIn(("video2.f30077.mp4", "video2.f30280.m4a"), pair_names)

    @patch('subprocess.run')
    def test_merge_requires_ffmpeg(self, mock_run):
        """Test that VideoMerger raises error when ffmpeg is not available"""
        mock_run.side_effect = FileNotFoundError()
        with self.assertRaises(RuntimeError) as ctx:
            VideoMerger()
        self.assertIn("ffmpeg", str(ctx.exception))

    @patch('subprocess.run')
    def test_merge_creates_merged_file(self, mock_run):
        """Test that merge creates a new merged file"""
        mock_run.return_value = MagicMock(returncode=0)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            (tmpdir / "test.f100026.mp4").touch()
            (tmpdir / "test.f30280.m4a").touch()

            merger = VideoMerger()
            result = merger.merge(
                tmpdir / "test.f100026.mp4",
                tmpdir / "test.f30280.m4a",
                tmpdir / "test.mp4"
            )

            self.assertTrue(result["success"])
            self.assertTrue((tmpdir / "test.mp4").exists())

    @patch('subprocess.run')
    def test_merge_removes_split_files_after_success(self, mock_run):
        """Test that merge removes original split files after successful merge"""
        mock_run.return_value = MagicMock(returncode=0)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            video_file = tmpdir / "test.f100026.mp4"
            audio_file = tmpdir / "test.f30280.m4a"
            video_file.touch()
            audio_file.touch()

            merger = VideoMerger()
            merger.merge(video_file, audio_file, tmpdir / "test.mp4", cleanup=True)

            self.assertFalse(video_file.exists())
            self.assertFalse(audio_file.exists())

    @patch('subprocess.run')
    def test_merge_all_processes_all_pairs(self, mock_run):
        """Test that merge_all processes all split file pairs"""
        mock_run.return_value = MagicMock(returncode=0)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            (tmpdir / "video1.f100026.mp4").touch()
            (tmpdir / "video1.f30280.m4a").touch()
            (tmpdir / "video2.f30077.mp4").touch()
            (tmpdir / "video2.f30280.m4a").touch()

            merger = VideoMerger()
            results = merger.merge_all(tmpdir, cleanup=False)

            self.assertEqual(len(results), 2)
            self.assertTrue(all(r["success"] for r in results))


if __name__ == '__main__':
    unittest.main()
