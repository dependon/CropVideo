import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import threading
import os
import webbrowser
from datetime import timedelta
import math
import locale # For potential number formatting

# --- Language Dictionary ---
LANGUAGES = {
    'en': {
        'title': "Video Processor",
        'input_frame': "Input Video",
        'file_label': "File:",
        'browse_button': "Browse...",
        'duration_label': "Duration:",
        'resolution_label': "Resolution:",
        'fps_label': "FPS:",
        'frames_label': "Total Frames:",
        'na': "N/A",
        'error': "Error",
        'warning': "Warning",
        'video_processing_options_frame': "Video Processing Options", # New Frame Label
        'time_crop_frame': "Time Cropping", # No longer a frame label, just concept
        'enable_time_crop': "Enable Time Crop",
        'start_time_label': "Start (HH:MM:SS.ms):",
        'end_time_label': "End (HH:MM:SS.ms):",
        'res_scale_frame': "Resolution Scaling (Resize)", # No longer a frame label
        'enable_res_scale': "Enable Resizing",
        'width_label': "Target Width:",
        'height_label': "Target Height:",
        'fps_change_frame': "FPS Change (Output)", # No longer a frame label
        'enable_fps_change': "Enable FPS Change",
        'output_fps_label': "Output FPS:",
        'output_video_frame': "Output Video File", # Changed key slightly
        'save_as_button': "Save As...",
        'process_video_button': "Process Video", # Specific button text
        'extract_frames_button': "Extract Frames", # New specific button text
        'status_label': "Status:",
        'video_information': "Video Information",
        'idle': "Idle",
        'loading': "Loading video info...",
        'loaded': "Loaded",
        'starting_process': "Starting video processing...", # Changed wording
        'starting_extract': "Starting frame extraction...",
        'processing': "Processing video...",
        'extracting': "Extracting frame",
        'of': "of",
        'frames': "frames",
        'complete_process': "Video processing complete! Output saved to",
        'complete_extract': "Frame extraction complete! Frames saved to",
        'error_loading': "Failed to load video info:",
        'error_processing': "Error during video processing:",
        'error_extracting': "Error during frame extraction:",
        'error_input_file': "Please select a valid input video file.",
        'error_output_file': "Please specify an output video file path for processing.", # Added context
        'error_output_dir': "Please select a valid output directory for frames.",
        'error_no_op_video': "Please enable Time Crop, Resizing, or FPS Change to process video.", # Changed
        'error_no_op_frames': "No frame range specified for extraction.", # Changed message
        # 'error_both_ops': "Cannot enable both Video Processing and Frame Extraction simultaneously. Please choose one.", # No longer needed
        'error_invalid_time': "Invalid time format. Use HH:MM:SS or HH:MM:SS.ms",
        'error_negative_time': "Start and End times cannot be negative.",
        'error_end_before_start': "End time must be after start time.",
        'error_start_too_late': "Start time is beyond the video duration.",
        'warning_end_time_capped': "Warning - End time capped to video duration",
        'error_invalid_res_int': "Target Width and Height must be integers.",
        'error_invalid_res_positive': "Target Width and Height must be positive.",
        'error_invalid_fps_format': "Output FPS must be a valid number.",
        'error_invalid_fps_positive': "Output FPS must be a positive number.",
        'error_invalid_frame_int': "Start and End frame numbers must be integers.",
        'error_invalid_frame_positive': "Frame numbers must be non-negative.",
        'error_invalid_frame_order': "End frame must be greater than or equal to start frame.",
        'error_invalid_frame_range': "Specified frame range is outside the total frames of the video.",
        'error_video_writer': "Could not open video writer for path:",
        'error_saving_frame': "Could not save frame {}: {}",
        'check_codecs': "Check codecs and permissions.",
        'check_permissions': "Check directory permissions.",
        'lang_button': "中文",
        'frame_extract_options_frame': "Frame Extraction Options", # Changed key slightly
        'enable_frame_extract': "Enable Frame Extraction", # Checkbox still useful for defaults/clarity
        'start_frame_label': "Start Frame:",
        'end_frame_label': "End Frame:",
        'output_dir_label': "Output Directory:",
        'browse_dir_button': "Browse...",
        'img_format_label': "Image Format:",
        'github_link': "https://github.com/dependon/CropVideo"
    },
    'zh': {
        'title': "视频处理器",
        'input_frame': "输入视频",
        'file_label': "文件:",
        'browse_button': "浏览...",
        'duration_label': "时长:",
        'resolution_label': "分辨率:",
        'fps_label': "帧率:",
        'frames_label': "总帧数:",
        'na': "不可用",
        'error': "错误",
        'warning': "警告",
        'video_information': "视频信息",
        'status': "状态",
        'video_processing_options_frame': "视频处理选项", # New Frame Label
        'time_crop_frame': "时间裁剪",
        'enable_time_crop': "启用时间裁剪",
        'start_time_label': "开始 (时:分:秒.毫秒):",
        'end_time_label': "结束 (时:分:秒.毫秒):",
        'res_scale_frame': "分辨率缩放 (调整大小)",
        'enable_res_scale': "启用调整大小",
        'width_label': "目标宽度:",
        'height_label': "目标高度:",
        'fps_change_frame': "帧率变更 (输出)",
        'enable_fps_change': "启用帧率变更",
        'output_fps_label': "输出帧率:",
        'output_video_frame': "输出视频文件", # Changed key slightly
        'save_as_button': "另存为...",
        'process_video_button': "处理视频", # Specific button text
        'extract_frames_button': "提取帧", # New specific button text
        'status_label': "状态:",
        'idle': "空闲",
        'loading': "正在加载视频信息...",
        'loaded': "已加载",
        'starting_process': "开始处理视频...", # Changed wording
        'starting_extract': "开始提取帧...",
        'processing': "正在处理视频...",
        'extracting': "正在提取第",
        'of': "帧 (共",
        'frames': "帧)",
        'complete_process': "视频处理完成! 输出已保存至",
        'complete_extract': "帧提取完成! 帧已保存至",
        'error_loading': "加载视频信息失败:",
        'error_processing': "视频处理过程中出错:",
        'error_extracting': "提取帧过程中出错:",
        'error_input_file': "请选择一个有效的输入视频文件。",
        'error_output_file': "请指定用于视频处理的输出文件路径。", # Added context
        'error_output_dir': "请选择一个有效的帧输出目录。",
        'error_no_op_video': "请至少启用时间裁剪、调整大小或帧率变更中的一项来处理视频。", # Changed
        'error_no_op_frames': "未指定用于提取的帧范围。", # Changed message
        # 'error_both_ops': "无法同时启用视频处理和帧提取。请选择其中一项。", # No longer needed
        'error_invalid_time': "无效的时间格式。请使用 HH:MM:SS 或 HH:MM:SS.ms",
        'error_negative_time': "开始和结束时间不能为负。",
        'error_end_before_start': "结束时间必须晚于开始时间。",
        'error_start_too_late': "开始时间超出视频总时长。",
        'warning_end_time_capped': "警告 - 结束时间已限制在视频时长内",
        'error_invalid_res_int': "目标宽度和高度必须是整数。",
        'error_invalid_res_positive': "目标宽度和高度必须为正数。",
        'error_invalid_fps_format': "输出帧率必须是一个有效的数字。",
        'error_invalid_fps_positive': "输出帧率必须为正数。",
        'error_invalid_frame_int': "开始和结束帧号必须是整数。",
        'error_invalid_frame_positive': "帧号必须是非负数。",
        'error_invalid_frame_order': "结束帧号必须大于或等于开始帧号。",
        'error_invalid_frame_range': "指定的帧范围超出了视频的总帧数。",
        'error_video_writer': "无法打开视频写入器，路径:",
        'error_saving_frame': "无法保存第 {} 帧: {}",
        'check_codecs': "请检查编解码器和权限。",
        'check_permissions': "请检查目录写入权限。",
        'lang_button': "English",
        'frame_extract_options_frame': "帧提取选项", # Changed key slightly
        'enable_frame_extract': "启用帧提取", # Checkbox still useful
        'start_frame_label': "开始帧:",
        'end_frame_label': "结束帧:",
        'output_dir_label': "输出目录:",
        'browse_dir_button': "浏览...",
        'img_format_label': "图片格式:",
        'github_link': "https://github.com/dependon/CropVideo"
    }
}


# --- Helper Functions ---

def format_time(seconds):
    """Converts seconds to HH:MM:SS.ms format accurately using integer math."""
    if seconds is None or math.isnan(seconds) or seconds < 0:
        seconds = 0
    try:
        # Create timedelta object
        delta = timedelta(seconds=seconds)

        # Extract total days, remaining seconds, and microseconds
        days = delta.days
        secs = delta.seconds
        microsecs = delta.microseconds

        # Calculate total hours, minutes, seconds
        total_hours = days * 24 + secs // 3600
        total_minutes = (secs % 3600) // 60
        total_seconds = secs % 60
        total_milliseconds = microsecs // 1000

        return f"{int(total_hours):02}:{int(total_minutes):02}:{int(total_seconds):02}.{int(total_milliseconds):03}"
    except OverflowError:
         # Handle potential overflow for extremely large second values if necessary
         print(f"Warning: format_time encountered very large number: {seconds}")
         return "00:00:00.000" # Or some other indicator


def time_str_to_seconds(time_str):
    """Converts HH:MM:SS or HH:MM:SS.ms string to seconds"""
    if not time_str: return None
    try:
        parts = time_str.split(':')
        if len(parts) != 3: return None
        seconds_parts = parts[2].split('.')
        sec = int(seconds_parts[0])
        ms = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        if len(seconds_parts) > 1 and len(seconds_parts[1]) > 3:
             ms = int(seconds_parts[1][:3])
        # Ensure components are non-negative after parsing
        if sec < 0 or ms < 0 or int(parts[0]) < 0 or int(parts[1]) < 0:
             return None # Or raise ValueError
        total_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + sec + ms / 1000.0
        return total_seconds
    except Exception:
        return None

# --- Main Application Class ---

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'en'
        self.texts = LANGUAGES[self.current_lang]

        self.root.title(self.texts['title'])
        self.root.geometry("700x900") # Reduced height for more compact layout

        try:
            self.style = ttk.Style(root)
            available_themes = self.style.theme_names()
            if 'clam' in available_themes: self.style.theme_use('clam')
            elif 'alt' in available_themes: self.style.theme_use('alt')
        except tk.TclError: print("ttk themes not available.")

        # --- Variables ---
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar() # Video output
        self.output_dir_str = tk.StringVar() # Frame output

        self.original_duration_str = tk.StringVar(value=f"{self.texts['duration_label']} {self.texts['na']}")
        self.original_resolution_str = tk.StringVar(value=f"{self.texts['resolution_label']} {self.texts['na']}")
        self.original_fps_str = tk.StringVar(value=f"{self.texts['fps_label']} {self.texts['na']}")
        self.original_frame_count_str = tk.StringVar(value=f"{self.texts['frames_label']} {self.texts['na']}")

        self.enable_time_crop = tk.BooleanVar(value=False)
        self.start_time_str = tk.StringVar(value="00:00:00.000")
        self.end_time_str = tk.StringVar(value="00:00:00.000")

        self.enable_res_scale = tk.BooleanVar(value=False)
        self.scale_width_str = tk.StringVar(value="0")
        self.scale_height_str = tk.StringVar(value="0")

        self.enable_fps_change = tk.BooleanVar(value=False)
        self.output_fps_str = tk.StringVar(value="0")

        self.enable_frame_extract = tk.BooleanVar(value=False) # Keep for enabling controls
        self.start_frame_str = tk.StringVar(value="0")
        self.end_frame_str = tk.StringVar(value="0")
        self.image_format_var = tk.StringVar(value="png")

        self.status_text = tk.StringVar(value=f"{self.texts['status_label']} {self.texts['idle']}")
        self.progress_var = tk.DoubleVar(value=0.0)
        self.processing_active = False

        self.video_capture = None
        self.video_duration_sec = 0
        self.video_fps = 0
        self.video_width = 0
        self.video_height = 0
        self.total_frames = 0

        # Link checkboxes to update widget states
        self.enable_time_crop.trace_add("write", self.update_widget_states)
        self.enable_res_scale.trace_add("write", self.update_widget_states)
        self.enable_fps_change.trace_add("write", self.update_widget_states)
        self.enable_frame_extract.trace_add("write", self.update_widget_states)

        # --- UI Layout ---
        self.main_frame = ttk.Frame(root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0)
        
        # Detect system language
        try:
            lang = locale.getdefaultlocale()[0]
            self.current_lang = 'zh' if lang and 'zh' in lang.lower() else 'en'
        except:
            self.current_lang = 'en'
        self.texts = LANGUAGES[self.current_lang]

        # Language Button
        self.lang_button = ttk.Button(self.main_frame, text=self.texts['lang_button'], command=self.toggle_language,
                                     style='Accent.TButton')
        self.lang_button.grid(row=0, column=2, sticky=tk.E, padx=5, pady=(0,10))

        # Input File Section
        self.input_frame = ttk.LabelFrame(self.main_frame, text=self.texts['input_frame'], padding="5")
        self.input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=1)
        self.input_frame.columnconfigure(1, weight=1)
        self.input_file_label = ttk.Label(self.input_frame, text=self.texts['file_label'], font=('Arial', 10))
        self.input_file_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(self.input_frame, textvariable=self.input_path, width=60, font=('Arial', 10)).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.input_browse_button = ttk.Button(self.input_frame, text=self.texts['browse_button'], command=self.browse_input,
                                           style='Accent.TButton')
        self.input_browse_button.grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)

        # Video Info Section
        self.info_frame = ttk.LabelFrame(self.main_frame, text=self.texts['video_information'], padding="5")
        self.info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=1)
        self.info_duration_label = ttk.Label(self.info_frame, textvariable=self.original_duration_str)
        self.info_duration_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.info_resolution_label = ttk.Label(self.info_frame, textvariable=self.original_resolution_str)
        self.info_resolution_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        self.info_fps_label = ttk.Label(self.info_frame, textvariable=self.original_fps_str)
        self.info_fps_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.info_frames_label = ttk.Label(self.info_frame, textvariable=self.original_frame_count_str)
        self.info_frames_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        # --- Video Processing Options Frame ---
        self.video_processing_frame = ttk.LabelFrame(self.main_frame, text=self.texts['video_processing_options_frame'], padding="5")
        self.video_processing_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(3, 1))
        self.video_processing_frame.columnconfigure(1, weight=1)

        # Time Cropping Controls
        self.time_frame = ttk.Frame(self.video_processing_frame, padding="5")
        self.time_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=2)
        self.time_check = ttk.Checkbutton(self.time_frame, text=self.texts['enable_time_crop'], variable=self.enable_time_crop)
        self.time_check.grid(row=0, column=0, columnspan=4, sticky=tk.W, padx=5, pady=(0, 5))
        self.start_time_label = ttk.Label(self.time_frame, text=self.texts['start_time_label'])
        self.start_time_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.start_time_entry = ttk.Entry(self.time_frame, textvariable=self.start_time_str, width=15, state=tk.DISABLED, font=('Arial', 10))
        self.start_time_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.end_time_label = ttk.Label(self.time_frame, text=self.texts['end_time_label'])
        self.end_time_label.grid(row=1, column=2, sticky=tk.W, padx=5)
        self.end_time_entry = ttk.Entry(self.time_frame, textvariable=self.end_time_str, width=15, state=tk.DISABLED, font=('Arial', 10))
        self.end_time_entry.grid(row=1, column=3, sticky=tk.W, padx=5)

        # Resolution Scaling Controls
        self.res_frame = ttk.Frame(self.video_processing_frame, padding="5")
        self.res_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=2)
        self.res_check = ttk.Checkbutton(self.res_frame, text=self.texts['enable_res_scale'], variable=self.enable_res_scale)
        self.res_check.grid(row=0, column=0, columnspan=4, sticky=tk.W, padx=5, pady=(0, 5))
        self.res_w_label = ttk.Label(self.res_frame, text=self.texts['width_label'])
        self.res_w_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.res_w_entry = ttk.Entry(self.res_frame, textvariable=self.scale_width_str, width=8, state=tk.DISABLED)
        self.res_w_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.res_h_label = ttk.Label(self.res_frame, text=self.texts['height_label'])
        self.res_h_label.grid(row=1, column=2, sticky=tk.W, padx=5)
        self.res_h_entry = ttk.Entry(self.res_frame, textvariable=self.scale_height_str, width=8, state=tk.DISABLED)
        self.res_h_entry.grid(row=1, column=3, sticky=tk.W, padx=5)

        # FPS Change Controls
        self.fps_frame = ttk.Frame(self.video_processing_frame, padding="5")
        self.fps_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=2)
        self.fps_check = ttk.Checkbutton(self.fps_frame, text=self.texts['enable_fps_change'], variable=self.enable_fps_change)
        self.fps_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(0,5))
        self.fps_label_widget = ttk.Label(self.fps_frame, text=self.texts['output_fps_label'])
        self.fps_label_widget.grid(row=1, column=0, sticky=tk.W, padx=5)
        self.fps_entry = ttk.Entry(self.fps_frame, textvariable=self.output_fps_str, width=10, state=tk.DISABLED)
        self.fps_entry.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Output Video File Controls
        self.output_video_frame_widget = ttk.LabelFrame(self.video_processing_frame, text=self.texts['output_video_frame'], padding="10") # Renamed var
        self.output_video_frame_widget.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10,5))
        self.output_video_frame_widget.columnconfigure(1, weight=1)
        self.output_file_label = ttk.Label(self.output_video_frame_widget, text=self.texts['file_label'])
        self.output_file_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_video_entry = ttk.Entry(self.output_video_frame_widget, textvariable=self.output_path, width=60) # Video entry
        self.output_video_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.output_browse_button = ttk.Button(self.output_video_frame_widget, text=self.texts['save_as_button'], command=self.browse_output_video,
                                           style='Accent.TButton')
        self.output_browse_button.grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)

        # --- Frame Extraction Options Frame ---
        self.frame_extract_options_frame = ttk.LabelFrame(self.main_frame, text=self.texts['frame_extract_options_frame'], padding="10")
        self.frame_extract_options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(2, 5))
        self.frame_extract_options_frame.columnconfigure(1, weight=1)

        # Frame Extraction Controls
        # Checkbox kept mainly to toggle the sub-controls easily
        self.frame_extract_check = ttk.Checkbutton(self.frame_extract_options_frame, text=self.texts['enable_frame_extract'], variable=self.enable_frame_extract)
        self.frame_extract_check.grid(row=0, column=0, columnspan=4, sticky=tk.W, padx=5, pady=(5,2))
        self.start_frame_label = ttk.Label(self.frame_extract_options_frame, text=self.texts['start_frame_label'])
        self.start_frame_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.start_frame_entry = ttk.Entry(self.frame_extract_options_frame, textvariable=self.start_frame_str, width=10, state=tk.DISABLED)
        self.start_frame_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        self.end_frame_label = ttk.Label(self.frame_extract_options_frame, text=self.texts['end_frame_label'])
        self.end_frame_label.grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.end_frame_entry = ttk.Entry(self.frame_extract_options_frame, textvariable=self.end_frame_str, width=10, state=tk.DISABLED)
        self.end_frame_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        self.output_dir_label = ttk.Label(self.frame_extract_options_frame, text=self.texts['output_dir_label'])
        self.output_dir_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_dir_entry = ttk.Entry(self.frame_extract_options_frame, textvariable=self.output_dir_str, width=45, state=tk.DISABLED)
        self.output_dir_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.output_dir_button = ttk.Button(self.frame_extract_options_frame, text=self.texts['browse_dir_button'], command=self.browse_output_dir, state=tk.DISABLED,
                                           style='Accent.TButton')
        self.output_dir_button.grid(row=2, column=3, sticky=tk.E, padx=5, pady=5)
        self.img_format_label = ttk.Label(self.frame_extract_options_frame, text=self.texts['img_format_label'])
        self.img_format_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.img_format_combo = ttk.Combobox(self.frame_extract_options_frame, textvariable=self.image_format_var, values=['png', 'jpg', 'bmp', 'tiff'], state='readonly', width=8)
        self.img_format_combo.current(0)
        self.img_format_combo.config(state=tk.DISABLED)
        self.img_format_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)


        # --- Action Buttons Frame ---
        action_button_frame = ttk.Frame(self.main_frame)
        action_button_frame.grid(row=5, column=0, columnspan=3, pady=5)

        self.process_video_button = ttk.Button(action_button_frame, text=self.texts['process_video_button'], command=self.start_video_processing, width=20)
        self.process_video_button.pack(side=tk.LEFT, padx=10)

        self.extract_frames_button = ttk.Button(action_button_frame, text=self.texts['extract_frames_button'], command=self.start_frame_extraction, width=20)
        self.extract_frames_button.pack(side=tk.LEFT, padx=10)

        # --- Progress Bar and Status ---
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        self.status_label_widget = ttk.Label(self.main_frame, textvariable=self.status_text)
        self.status_label_widget.grid(row=7, column=0, columnspan=3, sticky=tk.W, padx=5)

        # --- Hyperlink ---
        self.link_frame = ttk.Frame(self.main_frame)
        self.link_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        self.link_label = ttk.Label(self.link_frame, text=self.texts['github_link'], foreground="blue", cursor="hand2")
        self.link_label.pack()
        self.link_label.bind("<Button-1>", self.open_link)

        # Initial UI state update
        self.update_widget_states("","","") # Trigger initial state based on checkboxes


    # --- Language Methods ---
    def toggle_language(self):
        if self.current_lang == 'en': self.current_lang = 'zh'
        else: self.current_lang = 'en'
        self.texts = LANGUAGES[self.current_lang]
        self.update_language_widgets()

    def update_language_widgets(self):
        """Updates the text of all language-dependent widgets."""
        self.root.title(self.texts['title'])
        self.lang_button.config(text=self.texts['lang_button'], bg='#4CAF50', fg='white', font=('Helvetica', 10, 'bold'), relief='groove', bd=2, padx=10, pady=5, activebackground='#45a049')
        
        # Update mutex warning if needed
        if hasattr(self, 'mutex_warning_str'):
            self.mutex_warning_str.set(self._check_mutex_options())

        # Input/Info
        self.input_frame.config(text=self.texts['input_frame'])
        self.input_file_label.config(text=self.texts['file_label'])
        self.input_browse_button.config(text=self.texts['browse_button'], bg='#2196F3', fg='white', font=('Helvetica', 10), relief='groove', bd=2, padx=10, pady=5, activebackground='#0b7dda')
        self.original_duration_str.set(f"{self.texts['duration_label']} {self.texts['na'] if self.video_duration_sec == 0 else format_time(self.video_duration_sec)}")
        self.original_resolution_str.set(f"{self.texts['resolution_label']} {self.texts['na'] if self.video_width == 0 else f'{self.video_width}x{self.video_height}'}")
        self.original_fps_str.set(f"{self.texts['fps_label']} {self.texts['na'] if self.video_fps == 0 else f'{self.video_fps:.2f}'}")
        self.original_frame_count_str.set(f"{self.texts['frames_label']} {self.texts['na'] if self.total_frames == 0 else self.total_frames}")

        # Video Processing Section
        self.video_processing_frame.config(text=self.texts['video_processing_options_frame'])
        self.time_check.config(text=self.texts['enable_time_crop'])
        self.start_time_label.config(text=self.texts['start_time_label'])
        self.end_time_label.config(text=self.texts['end_time_label'])
        self.res_check.config(text=self.texts['enable_res_scale'])
        self.res_w_label.config(text=self.texts['width_label'])
        self.res_h_label.config(text=self.texts['height_label'])
        self.fps_check.config(text=self.texts['enable_fps_change'])
        self.fps_label_widget.config(text=self.texts['output_fps_label'])
        self.output_video_frame_widget.config(text=self.texts['output_video_frame'])
        self.output_file_label.config(text=self.texts['file_label'])
        self.output_browse_button.config(text=self.texts['save_as_button'], bg='#2196F3', fg='white', font=('Helvetica', 10), relief='groove', bd=2, padx=10, pady=5, activebackground='#0b7dda')

        # Frame Extraction Section
        self.frame_extract_options_frame.config(text=self.texts['frame_extract_options_frame'])
        self.frame_extract_check.config(text=self.texts['enable_frame_extract'])
        self.start_frame_label.config(text=self.texts['start_frame_label'])
        self.end_frame_label.config(text=self.texts['end_frame_label'])
        self.output_dir_label.config(text=self.texts['output_dir_label'])
        self.output_dir_button.config(text=self.texts['browse_dir_button'], bg='#2196F3', fg='white', font=('Helvetica', 10), relief='groove', bd=2, padx=10, pady=5, activebackground='#0b7dda')
        self.img_format_label.config(text=self.texts['img_format_label'])

        # Action Buttons
        self.process_video_button.config(text=self.texts['process_video_button'], bg='#FF5722', fg='white', font=('Helvetica', 10, 'bold'), relief='groove', bd=2, padx=15, pady=7, activebackground='#e64a19')
        self.extract_frames_button.config(text=self.texts['extract_frames_button'], bg='#FF5722', fg='white', font=('Helvetica', 10, 'bold'), relief='groove', bd=2, padx=15, pady=7, activebackground='#e64a19')

        # Status & Link
        current_status = self.status_text.get().split(LANGUAGES['en']['status_label'])[-1].split(LANGUAGES['zh']['status_label'])[-1].strip()
        self.status_text.set(f"{self.texts['status_label']} {current_status}")
        self.link_label.config(text=self.texts['github_link'])


    # --- File/Directory Browsing ---
    def open_link(self, event): webbrowser.open_new(r"https://github.com/dependon/CropVideo")
    def browse_input(self):
        path = filedialog.askopenfilename(title=self.texts['input_frame'], filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")])
        if path:
            self.input_path.set(path)
            self.load_video_info()
            # Suggest defaults based on input path
            base, ext = os.path.splitext(path)
            if not self.output_path.get(): self.output_path.set(f"{base}_processed{ext}")
            if not self.output_dir_str.get(): self.output_dir_str.set(f"{base}_frames")

    def browse_output_video(self):
        initial_dir = os.path.dirname(self.output_path.get()) if self.output_path.get() else os.path.dirname(self.input_path.get())
        initial_file = os.path.basename(self.output_path.get()) if self.output_path.get() else ""
        if not initial_file and self.input_path.get():
             base, ext = os.path.splitext(self.input_path.get())
             initial_file = f"{os.path.basename(base)}_processed{ext}"
        path = filedialog.asksaveasfilename(title=self.texts['save_as_button'], filetypes=[("MP4", "*.mp4"), ("AVI", "*.avi"), ("MOV", "*.mov"), ("MKV", "*.mkv"), ("All", "*.*")], defaultextension=".mp4", initialdir=initial_dir, initialfile=initial_file)
        if path: self.output_path.set(path)

    def browse_output_dir(self):
        initial_dir = self.output_dir_str.get() if self.output_dir_str.get() else os.path.dirname(self.input_path.get())
        if not os.path.isdir(initial_dir) and self.input_path.get():
             base, _ = os.path.splitext(self.input_path.get())
             initial_dir = f"{base}_frames"
        dir_path = filedialog.askdirectory(title=self.texts['output_dir_label'], initialdir=os.path.dirname(initial_dir) if os.path.exists(os.path.dirname(initial_dir)) else None)
        if dir_path: self.output_dir_str.set(dir_path)

    # --- Video Loading ---
    def load_video_info(self):
        path = self.input_path.get()
        if not path: return
        self._reset_video_properties()
        self.status_text.set(f"{self.texts['status_label']} {self.texts['loading']}")
        self.root.update_idletasks()

        try:
            if self.video_capture and self.video_capture.isOpened(): self.video_capture.release()
            self.video_capture = cv2.VideoCapture(path)
            if not self.video_capture.isOpened(): raise IOError(f"Cannot open: {path}")

            self.video_fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if not self.video_fps or self.video_fps <= 0:
                print(f"Warning: Invalid FPS ({self.video_fps}) read for {path}. Using 30.0.")
                self.video_fps = 30.0
            if not self.total_frames or self.total_frames < 0:
                 print(f"Warning: Invalid frame count ({self.total_frames}) read for {path}. Using 0.")
                 self.total_frames = 0

            if self.total_frames > 0 and self.video_fps > 0:
                self.video_duration_sec = self.total_frames / self.video_fps
                # --- DEBUG PRINT ---
                print(f"Calculated Duration (seconds): {self.video_duration_sec}")
                print(f"Total Frames: {self.total_frames}, FPS: {self.video_fps}")
                # --- END DEBUG ---
            else:
                 self.video_duration_sec = 0

            formatted_duration = format_time(self.video_duration_sec)
             # --- DEBUG PRINT ---
            print(f"Formatted Duration: {formatted_duration}")
            # --- END DEBUG ---

            self.original_duration_str.set(f"{self.texts['duration_label']} {formatted_duration}")
            self.original_resolution_str.set(f"{self.texts['resolution_label']} {self.video_width}x{self.video_height}")
            self.original_fps_str.set(f"{self.texts['fps_label']} {self.video_fps:.2f}")
            self.original_frame_count_str.set(f"{self.texts['frames_label']} {self.total_frames}")

            self.start_time_str.set(format_time(0))
            self.end_time_str.set(formatted_duration) # Use the formatted string
            self.scale_width_str.set(str(self.video_width))
            self.scale_height_str.set(str(self.video_height))
            self.output_fps_str.set(f"{self.video_fps:.2f}")
            self.start_frame_str.set("0")
            self.end_frame_str.set(str(max(0, self.total_frames - 1)))

            self.status_text.set(f"{self.texts['status_label']} {self.texts['loaded']} '{os.path.basename(path)}'")

        except Exception as e:
            self.show_error_message('error', 'error_loading', f"\n{e}")
            self._reset_video_properties() # Reset display on error
            self.status_text.set(f"{self.texts['status_label']} {self.texts['error_loading']}")
        finally:
             if self.video_capture: self.video_capture.release(); self.video_capture = None
             self.update_widget_states("","","") # Update states after loading

    def _reset_video_properties(self):
        """Resets internal properties and updates UI labels to N/A or default."""
        self.video_duration_sec = 0
        self.video_fps = 0
        self.video_width = 0
        self.video_height = 0
        self.total_frames = 0
        self.original_duration_str.set(f"{self.texts['duration_label']} {self.texts['na']}")
        self.original_resolution_str.set(f"{self.texts['resolution_label']} {self.texts['na']}")
        self.original_fps_str.set(f"{self.texts['fps_label']} {self.texts['na']}")
        self.original_frame_count_str.set(f"{self.texts['frames_label']} {self.texts['na']}")
        self.mutex_warning_str.set("")
        # Also reset default input values? Optional, maybe keep last entered.
        # self.start_time_str.set(format_time(0)) ... etc.


    # --- UI State Management ---
    def update_widget_states(self, var_name, index, mode):
        """Enables/disables sub-widgets based on their parent checkbox state."""
        # Video processing widgets
        time_state = tk.NORMAL if self.enable_time_crop.get() else tk.DISABLED
        self.start_time_entry.config(state=time_state)
        self.end_time_entry.config(state=time_state)

        res_state = tk.NORMAL if self.enable_res_scale.get() else tk.DISABLED
        self.res_w_entry.config(state=res_state)
        self.res_h_entry.config(state=res_state)

        fps_state = tk.NORMAL if self.enable_fps_change.get() else tk.DISABLED
        self.fps_entry.config(state=fps_state)

        # Frame extraction widgets
        frame_state = tk.NORMAL if self.enable_frame_extract.get() else tk.DISABLED
        self.start_frame_entry.config(state=frame_state)
        self.end_frame_entry.config(state=frame_state)
        self.output_dir_entry.config(state=frame_state)
        self.output_dir_button.config(state=frame_state)
        self.img_format_combo.config(state='readonly' if frame_state == tk.NORMAL else tk.DISABLED)


    def update_progress(self, value, text_key, *args):
        """Safely update progress bar and status text"""
        try: message = self.texts[text_key].format(*args)
        except KeyError: message = text_key
        except IndexError: message = self.texts[text_key]
        final_text = f"{self.texts['status_label']} {message}"
        self.progress_var.set(value)
        self.status_text.set(final_text)

    def show_error_message(self, title_key, message_key, *args):
        try: message = self.texts[message_key].format(*args)
        except KeyError: message = message_key
        except IndexError: message = self.texts[message_key]
        messagebox.showerror(self.texts.get(title_key, 'Error'), message)

    def show_warning_message(self, title_key, message_key, *args):
        try: message = self.texts[message_key].format(*args)
        except KeyError: message = message_key
        except IndexError: message = self.texts[message_key]
        messagebox.showwarning(self.texts.get(title_key, 'Warning'), message)

    def reset_processing_state(self):
         """Resets button states and processing flag."""
         self.processing_active = False
         self.process_video_button.config(state=tk.NORMAL)
         self.extract_frames_button.config(state=tk.NORMAL)
         # return value is optional, useful if chained like: return self.reset_processing_state()


    # --- Processing Logic ---

    def start_video_processing(self):
        """Validates and starts the video processing thread."""
        if self.processing_active: return
        in_path = self.input_path.get()
        if not in_path or not os.path.exists(in_path):
            self.show_error_message('error', 'error_input_file'); return

        # Check if any video processing option is actually enabled
        if not (self.enable_time_crop.get() or self.enable_res_scale.get() or self.enable_fps_change.get()):
             self.show_error_message('error', 'error_no_op_video'); return

        out_path = self.output_path.get()
        if not out_path:
            self.show_error_message('error', 'error_output_file'); return

        # --- Reload video info for validation (get fresh values) ---
        temp_cap = cv2.VideoCapture(in_path)
        if not temp_cap.isOpened(): self.show_error_message('error', 'error_loading', in_path); return
        original_fps = temp_cap.get(cv2.CAP_PROP_FPS)
        original_total_frames = int(temp_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_width = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        temp_cap.release()
        if original_fps is None or original_fps <= 0: original_fps = 30.0
        if original_total_frames <= 0: original_total_frames = 0
        original_duration_sec = original_total_frames / original_fps if original_fps > 0 else 0

        # --- Parameter Validation ---
        start_sec, end_sec = 0, original_duration_sec
        if self.enable_time_crop.get():
            start_sec = time_str_to_seconds(self.start_time_str.get())
            end_sec = time_str_to_seconds(self.end_time_str.get())
            if start_sec is None or end_sec is None: self.show_error_message('error', 'error_invalid_time'); return
            if start_sec < 0 or end_sec < 0: self.show_error_message('error', 'error_negative_time'); return
            if end_sec <= start_sec: self.show_error_message('error', 'error_end_before_start'); return
            if end_sec > original_duration_sec: end_sec = original_duration_sec
            if start_sec >= original_duration_sec and original_duration_sec > 0: self.show_error_message('error', 'error_start_too_late'); return

        target_w, target_h = original_width, original_height
        if self.enable_res_scale.get():
            try:
                target_w = int(self.scale_width_str.get())
                target_h = int(self.scale_height_str.get())
                if target_w <= 0 or target_h <= 0: raise ValueError()
            except ValueError: self.show_error_message('error', 'error_invalid_res_positive'); return

        output_fps = original_fps
        if self.enable_fps_change.get():
            try:
                output_fps = float(self.output_fps_str.get())
                if output_fps <= 0: raise ValueError()
            except ValueError: self.show_error_message('error', 'error_invalid_fps_positive'); return

        # --- Start Thread ---
        self.processing_active = True
        self.process_video_button.config(state=tk.DISABLED)
        self.extract_frames_button.config(state=tk.DISABLED) # Disable both
        self.progress_var.set(0)
        self.root.after(0, self.update_progress, 0.0, 'starting_process')

        process_thread = threading.Thread(
            target=self.perform_video_processing,
            args=(in_path, out_path, start_sec, end_sec, target_w, target_h,
                  output_fps, original_fps, original_total_frames, original_duration_sec),
            daemon=True)
        process_thread.start()

    def start_frame_extraction(self):
        """Validates and starts the frame extraction thread."""
        if self.processing_active: return
        in_path = self.input_path.get()
        if not in_path or not os.path.exists(in_path):
            self.show_error_message('error', 'error_input_file'); return

        out_dir = self.output_dir_str.get()
        img_format = self.image_format_var.get()
        if not out_dir:
            self.show_error_message('error', 'error_output_dir'); return

        # Try to create output directory if it doesn't exist
        try:
            if not os.path.isdir(out_dir):
                 print(f"Output directory '{out_dir}' does not exist. Attempting to create.")
                 os.makedirs(out_dir, exist_ok=True)
                 if not os.path.isdir(out_dir): # Check again after creation attempt
                      raise OSError(f"Failed to create directory: {out_dir}")
        except OSError as e:
            self.show_error_message('error', 'error_output_dir', f"\n{self.texts['check_permissions']} ({e})"); return

        # --- Reload video info for validation ---
        temp_cap = cv2.VideoCapture(in_path)
        if not temp_cap.isOpened(): self.show_error_message('error', 'error_loading', in_path); return
        original_total_frames = int(temp_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        temp_cap.release()
        if original_total_frames <= 0: original_total_frames = 0

        # --- Parameter Validation ---
        try:
            start_frame = int(self.start_frame_str.get())
            end_frame = int(self.end_frame_str.get()) # Inclusive end
            if start_frame < 0 or end_frame < 0: raise ValueError(self.texts['error_invalid_frame_positive'])
            if end_frame < start_frame: raise ValueError(self.texts['error_invalid_frame_order'])
            # Check range against actual frames
            if original_total_frames > 0:
                if start_frame >= original_total_frames : raise ValueError(self.texts['error_invalid_frame_range'])
                if end_frame >= original_total_frames:
                    self.show_warning_message('warning', 'error_invalid_frame_range', f"\nEnd frame capped to {original_total_frames - 1}")
                    end_frame = original_total_frames - 1 # Adjust end frame
            elif start_frame > 0 or end_frame > 0: # If video has 0 frames, only 0-0 range is valid
                 raise ValueError(self.texts['error_invalid_frame_range'])

        except ValueError as ve:
             # Check if the error message is one of our specific ones
             if str(ve) in [self.texts['error_invalid_frame_positive'], self.texts['error_invalid_frame_order'], self.texts['error_invalid_frame_range']]:
                 self.show_error_message('error', str(ve))
             else: # General integer conversion error
                 self.show_error_message('error', 'error_invalid_frame_int')
             return

        # --- Start Thread ---
        self.processing_active = True
        self.process_video_button.config(state=tk.DISABLED) # Disable both
        self.extract_frames_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.root.after(0, self.update_progress, 0.0, 'starting_extract')

        extract_thread = threading.Thread(
            target=self.perform_frame_extraction,
            args=(in_path, out_dir, start_frame, end_frame, img_format, original_total_frames),
            daemon=True)
        extract_thread.start()


    def perform_video_processing(self, in_path, out_path, start_sec, end_sec,
                                 target_w, target_h,
                                 output_fps, original_fps, original_total_frames, original_duration_sec):
        """Worker thread function for video processing."""
        cap = None
        out = None
        try:
            cap = cv2.VideoCapture(in_path)
            if not cap.isOpened(): raise IOError(f"Cannot open input: {in_path}")

            # Get original dimensions from video
            original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Calculate frame range based on ORIGINAL FPS
            start_frame = 0
            end_frame = original_total_frames
            if self.enable_time_crop.get(): # Check flag from main thread var
                # Display capped time warning if applicable (check original UI value vs capped value)
                original_end_time_str = self.end_time_str.get() # Access UI var safely
                if end_sec < original_duration_sec and time_str_to_seconds(original_end_time_str) > original_duration_sec:
                     self.root.after(0, self.show_warning_message, 'warning', 'warning_end_time_capped', format_time(original_duration_sec))
                start_frame = max(0, int(start_sec * original_fps))
                end_frame = min(original_total_frames, math.ceil(end_sec * original_fps))
                if end_frame >= original_total_frames : end_frame = original_total_frames # Ensure not out of bounds


            out_width, out_height = original_width, original_height
            is_resizing_needed = False
            if self.enable_res_scale.get(): # Check flag
                out_width, out_height = target_w, target_h
                # Check if resize is actually necessary
                if out_width != int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or out_height != int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)):
                    is_resizing_needed = True

            # Setup Video Writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            if out_path.lower().endswith('.avi'): fourcc = cv2.VideoWriter_fourcc(*'XVID')
            elif out_path.lower().endswith('.mov'): fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            elif out_path.lower().endswith('.mkv'): fourcc = cv2.VideoWriter_fourcc(*'X264')
            out = cv2.VideoWriter(out_path, fourcc, output_fps, (out_width, out_height))
            if not out.isOpened(): raise IOError(f"Cannot open video writer for: {out_path}")

            # Process Frames
            current_frame_index = 0
            processed_frames_count = 0
            frames_to_process = max(0, end_frame - start_frame)

            if start_frame > 0:
                 cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                 # Verify seek accuracy (optional but good)
                 # actual_start = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                 # if abs(actual_start - start_frame) > 1: print(f"Warning: Seek accuracy issue? Requested {start_frame}, got {actual_start}")
                 current_frame_index = start_frame # Track precisely

            while True:
                if current_frame_index >= end_frame: break
                ret, frame = cap.read()
                if not ret: break

                if current_frame_index >= start_frame:
                    output_frame = frame
                    if is_resizing_needed: # Apply resizing only if needed and enabled
                         output_frame = cv2.resize(frame, (out_width, out_height), interpolation=cv2.INTER_AREA)

                    if output_frame is None or output_frame.size == 0:
                         print(f"Warning: Frame {current_frame_index} empty after processing, skipping.")
                         current_frame_index += 1; continue

                    out.write(output_frame)
                    processed_frames_count += 1

                    if frames_to_process > 0 :
                        progress = (processed_frames_count / frames_to_process) * 100
                        # Update less frequently for performance? e.g., every 10 frames
                        # if processed_frames_count % 10 == 0:
                        self.root.after(0, self.update_progress, progress, 'processing', progress)

                current_frame_index += 1

            self.root.after(0, self.update_progress, 100.0, 'complete_process', os.path.basename(out_path))

        except Exception as e:
            error_details = str(e)
            print(f"Error in perform_video_processing: {e}") # Log detailed error
            self.root.after(0, self.update_progress, 0.0, 'error_processing', error_details)
            try:
                if out and out.isOpened(): out.release()
                if os.path.exists(out_path): os.remove(out_path); print(f"Removed partial file: {out_path}")
            except OSError as os_err: print(f"Could not remove output file {out_path}: {os_err}")
        finally:
            if cap and cap.isOpened(): cap.release()
            if out and out.isOpened(): out.release()
            self.root.after(0, self.reset_processing_state)


    def perform_frame_extraction(self, in_path, out_dir, start_frame, end_frame, img_format, total_video_frames):
        """Worker thread function for frame extraction."""
        cap = None
        try:
            cap = cv2.VideoCapture(in_path)
            if not cap.isOpened(): raise IOError(f"Cannot open input: {in_path}")

            # Process Frames
            current_frame_index = 0
            extracted_count = 0
            frames_to_extract_total = max(0, (end_frame - start_frame) + 1) # Inclusive range
            frame_num_width = len(str(total_video_frames)) if total_video_frames > 0 else 4 # Padding width

            if start_frame > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                current_frame_index = start_frame

            while current_frame_index <= end_frame: # Loop until end_frame is processed
                ret, frame = cap.read()
                if not ret:
                    print(f"Warning: Failed read at frame {current_frame_index}, stopping.")
                    self.root.after(0, self.show_warning_message, 'warning', 'error_extracting', f"Read failed at frame {current_frame_index}")
                    break # Exit loop if video ends early

                # Construct filename
                filename = f"frame_{str(current_frame_index).zfill(frame_num_width)}.{img_format}"
                filepath = os.path.join(out_dir, filename)

                try:
                    save_success = cv2.imwrite(filepath, frame)
                    if not save_success: raise IOError(f"imwrite failed for {filepath}")
                    extracted_count += 1

                    if frames_to_extract_total > 0:
                        progress = (extracted_count / frames_to_extract_total) * 100
                        # Update less frequently?
                        # if extracted_count % 5 == 0 or extracted_count == frames_to_extract_total:
                        self.root.after(0, self.update_progress, progress, 'extracting', current_frame_index, end_frame, progress)

                except Exception as save_err:
                     print(f"Error saving frame {current_frame_index}: {save_err}")
                     self.root.after(0, self.show_warning_message, 'warning', 'error_saving_frame', current_frame_index, str(save_err))
                     # Continue to next frame even if one fails

                current_frame_index += 1


            self.root.after(0, self.update_progress, 100.0, 'complete_extract', out_dir)

        except Exception as e:
            error_details = str(e)
            print(f"Error in perform_frame_extraction: {e}") # Log detailed error
            self.root.after(0, self.update_progress, 0.0, 'error_extracting', error_details)
        finally:
            if cap and cap.isOpened(): cap.release()
            self.root.after(0, self.reset_processing_state)


# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()