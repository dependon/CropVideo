import os
import sys
import pytest
import tkinter as tk
import cv2
import tempfile
import shutil
from unittest.mock import MagicMock, patch
from cropVideo import VideoProcessorApp, format_time, time_str_to_seconds, LANGUAGES

# 测试辅助函数
def test_format_time():
    # 测试时间格式化函数
    assert format_time(0) == "00:00:00.000"
    assert format_time(3661.5) == "01:01:01.500"  # 1小时1分1秒500毫秒
    assert format_time(None) == "00:00:00.000"  # 处理None值
    assert format_time(-1) == "00:00:00.000"  # 处理负值

def test_time_str_to_seconds():
    # 测试时间字符串转换为秒数
    assert time_str_to_seconds("00:00:00.000") == 0
    assert time_str_to_seconds("01:01:01.500") == 3661.5  # 1小时1分1秒500毫秒
    assert time_str_to_seconds("") is None  # 空字符串
    assert time_str_to_seconds("invalid") is None  # 无效格式
    assert time_str_to_seconds("00:00:-1.000") is None  # 负值

# 测试VideoProcessorApp类
class TestVideoProcessorApp:
    @pytest.fixture
    def app(self):
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        root = tk.Tk()
        app = VideoProcessorApp(root)
        yield app
        # 清理
        root.destroy()
        shutil.rmtree(self.temp_dir)
    
    def test_init(self, app):
        # 测试初始化
        assert app.current_lang == 'en'  # 默认语言为英语
        assert app.texts == LANGUAGES['en']  # 文本应该是英语
        assert app.video_duration_sec == 0  # 初始视频时长为0
        assert app.video_fps == 0  # 初始帧率为0
        assert app.video_width == 0  # 初始宽度为0
        assert app.video_height == 0  # 初始高度为0
        assert app.total_frames == 0  # 初始总帧数为0
        assert app.processing_active is False  # 初始处理状态为False
    
    def test_toggle_language(self, app):
        # 测试语言切换
        initial_lang = app.current_lang
        app.toggle_language()
        assert app.current_lang != initial_lang  # 语言应该切换
        assert app.texts == LANGUAGES[app.current_lang]  # 文本应该更新
        app.toggle_language()
        assert app.current_lang == initial_lang  # 切换回原来的语言
    
    def test_update_widget_states(self, app):
        # 测试控件状态更新
        # 启用时间裁剪
        app.enable_time_crop.set(True)
        app.update_widget_states("", "", "")
        assert app.start_time_entry.cget("state") == tk.NORMAL
        assert app.end_time_entry.cget("state") == tk.NORMAL
        
        # 禁用时间裁剪
        app.enable_time_crop.set(False)
        app.update_widget_states("", "", "")
        assert app.start_time_entry.cget("state") == tk.DISABLED
        assert app.end_time_entry.cget("state") == tk.DISABLED
    
    @patch('cropVideo.cv2.VideoCapture')
    def test_load_video_info(self, mock_video_capture, app):
        # 模拟视频加载
        mock_cap = MagicMock()
        mock_video_capture.return_value = mock_cap
        
        # 设置模拟视频属性
        mock_cap.isOpened.return_value = True
        mock_cap.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FPS: 30.0,
            cv2.CAP_PROP_FRAME_COUNT: 300,
            cv2.CAP_PROP_FRAME_WIDTH: 1920,
            cv2.CAP_PROP_FRAME_HEIGHT: 1080
        }.get(prop, 0)
        
        # 设置输入路径并加载视频信息
        test_video_path = os.path.join(self.temp_dir, "test_video.mp4")
        app.input_path.set(test_video_path)
        app.load_video_info()
        
        # 验证视频信息是否正确加载
        assert app.video_fps == 30.0
        assert app.total_frames == 300
        assert app.video_width == 1920
        assert app.video_height == 1080
        assert app.video_duration_sec == 10.0  # 300帧 / 30fps = 10秒
    
    @patch('cropVideo.cv2.VideoCapture')
    @patch('cropVideo.cv2.VideoWriter')
    @patch('cropVideo.os.path.exists')
    def test_perform_video_processing(self, mock_exists, mock_writer, mock_capture, app):
        # 模拟视频处理
        mock_exists.return_value = True
        
        # 设置模拟视频捕获
        mock_cap = MagicMock()
        mock_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, MagicMock())  # 模拟帧读取
        mock_cap.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FPS: 30.0,
            cv2.CAP_PROP_FRAME_COUNT: 300,
            cv2.CAP_PROP_FRAME_WIDTH: 1920,
            cv2.CAP_PROP_FRAME_HEIGHT: 1080
        }.get(prop, 0)
        
        # 设置模拟视频写入器
        mock_out = MagicMock()
        mock_writer.return_value = mock_out
        mock_out.isOpened.return_value = True
        
        # 设置测试参数
        in_path = os.path.join(self.temp_dir, "input.mp4")
        out_path = os.path.join(self.temp_dir, "output.mp4")
        start_sec = 1.0
        end_sec = 5.0
        target_w = 1280
        target_h = 720
        output_fps = 24.0
        original_fps = 30.0
        original_total_frames = 300
        original_duration_sec = 10.0
        
        # 启用时间裁剪和分辨率调整
        app.enable_time_crop.set(True)
        app.enable_res_scale.set(True)
        
        # 执行视频处理
        app.perform_video_processing(
            in_path, out_path, start_sec, end_sec, target_w, target_h,
            output_fps, original_fps, original_total_frames, original_duration_sec
        )
        
        # 验证视频处理是否正确执行
        mock_capture.assert_called_once_with(in_path)
        mock_writer.assert_called_once()
        assert mock_out.write.called  # 应该调用写入方法
    
    @patch('cropVideo.cv2.VideoCapture')
    @patch('cropVideo.cv2.imwrite')
    @patch('cropVideo.os.path.exists')
    @patch('cropVideo.os.path.isdir')
    def test_perform_frame_extraction(self, mock_isdir, mock_exists, mock_imwrite, mock_capture, app):
        # 模拟帧提取
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_imwrite.return_value = True
        
        # 设置模拟视频捕获
        mock_cap = MagicMock()
        mock_capture.return_value = mock_cap
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, MagicMock())  # 模拟帧读取
        
        # 设置测试参数
        in_path = os.path.join(self.temp_dir, "input.mp4")
        out_dir = os.path.join(self.temp_dir, "frames")
        start_frame = 10
        end_frame = 20
        img_format = "png"
        total_video_frames = 300
        
        # 执行帧提取
        app.perform_frame_extraction(
            in_path, out_dir, start_frame, end_frame, img_format, total_video_frames
        )
        
        # 验证帧提取是否正确执行
        mock_capture.assert_called_once_with(in_path)
        assert mock_cap.set.called  # 应该设置起始帧
        assert mock_imwrite.call_count == 11  # 应该提取11帧(10-20，包括两端)

# 运行测试
if __name__ == "__main__":
    pytest.main(['-v', 'test_cropVideo.py'])
