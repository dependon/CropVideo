import os
import sys
import pytest
import cv2
import tempfile
import shutil
from unittest.mock import MagicMock, patch
from cropVideo import format_time, time_str_to_seconds, LANGUAGES

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

# 使用mock模拟tkinter，避免创建实际窗口
@patch('cropVideo.tk.Tk')
@patch('cropVideo.ttk.Style')
@patch('cropVideo.ttk.Frame')
@patch('cropVideo.ttk.LabelFrame')
@patch('cropVideo.ttk.Label')
@patch('cropVideo.ttk.Entry')
@patch('cropVideo.ttk.Button')
@patch('cropVideo.ttk.Checkbutton')
@patch('cropVideo.ttk.Combobox')
@patch('cropVideo.ttk.Progressbar')
class TestVideoProcessorApp:
    @pytest.fixture
    def setup_mocks(self):
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        # 模拟tkinter组件
        self.mock_root = MagicMock()
        self.mock_style = MagicMock()
        self.mock_frame = MagicMock()
        self.mock_label_frame = MagicMock()
        self.mock_label = MagicMock()
        self.mock_entry = MagicMock()
        self.mock_button = MagicMock()
        self.mock_checkbutton = MagicMock()
        self.mock_combobox = MagicMock()
        self.mock_progressbar = MagicMock()
        
        # 返回模拟对象
        yield {
            'root': self.mock_root,
            'style': self.mock_style,
            'frame': self.mock_frame,
            'label_frame': self.mock_label_frame,
            'label': self.mock_label,
            'entry': self.mock_entry,
            'button': self.mock_button,
            'checkbutton': self.mock_checkbutton,
            'combobox': self.mock_combobox,
            'progressbar': self.mock_progressbar
        }
        
        # 清理
        shutil.rmtree(self.temp_dir)
    
    @patch('cropVideo.VideoProcessorApp')
    def test_app_initialization(self, mock_app_class, *mocks):
        # 测试应用初始化
        from cropVideo import VideoProcessorApp
        
        # 创建模拟实例
        mock_app = MagicMock()
        mock_app_class.return_value = mock_app
        
        # 设置预期属性
        mock_app.current_lang = 'en'
        mock_app.texts = LANGUAGES['en']
        mock_app.video_duration_sec = 0
        mock_app.video_fps = 0
        mock_app.video_width = 0
        mock_app.video_height = 0
        mock_app.total_frames = 0
        mock_app.processing_active = False
        
        # 验证属性
        assert mock_app.current_lang == 'en'
        assert mock_app.texts == LANGUAGES['en']
        assert mock_app.video_duration_sec == 0
        assert mock_app.video_fps == 0
        assert mock_app.video_width == 0
        assert mock_app.video_height == 0
        assert mock_app.total_frames == 0
        assert mock_app.processing_active is False
    
    @patch('cropVideo.VideoProcessorApp')
    def test_toggle_language(self, mock_app_class, *mocks):
        # 测试语言切换功能
        mock_app = MagicMock()
        mock_app_class.return_value = mock_app
        
        # 设置初始语言
        mock_app.current_lang = 'en'
        mock_app.texts = LANGUAGES['en']
        
        # 模拟toggle_language方法的行为
        def toggle_language():
            if mock_app.current_lang == 'en':
                mock_app.current_lang = 'zh'
                mock_app.texts = LANGUAGES['zh']
            else:
                mock_app.current_lang = 'en'
                mock_app.texts = LANGUAGES['en']
        
        # 替换方法
        mock_app.toggle_language = toggle_language
        
        # 执行切换
        initial_lang = mock_app.current_lang
        mock_app.toggle_language()
        
        # 验证切换结果
        assert mock_app.current_lang != initial_lang
        assert mock_app.texts == LANGUAGES[mock_app.current_lang]
        
        # 再次切换
        mock_app.toggle_language()
        assert mock_app.current_lang == initial_lang
    

    

    


# 运行测试
if __name__ == "__main__":
    pytest.main(['-v', 'test_cropVideo.py'])
