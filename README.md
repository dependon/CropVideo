# CropVideo 视频处理器

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

### Introduction
CropVideo is a powerful video processing tool that allows users to crop videos by time, resize resolution, change FPS, and extract frames. It provides a user-friendly interface for video editing tasks.

### Features
- **Time Cropping**: Cut videos to specific time segments
- **Resolution Scaling**: Resize video dimensions
- **FPS Adjustment**: Change the frame rate of output videos
- **Frame Extraction**: Extract individual frames from videos
- **Bilingual Interface**: Supports both English and Chinese

### Installation

#### Method 1: Download Executable Files
Download the latest version of the executable file from the [GitHub Releases](https://github.com/dependon/CropVideo/releases) page:

- Windows: `cropVideo_windows_x64.exe`
- Linux: `cropVideo_linux_x64`
- macOS: `cropVideo_macos_x64`

#### Method 2: Install from Source
1. Ensure you have Python 3.6+ installed
2. Clone this repository or download the source code
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
1. Run the application:
   ```
   python cropVideo.py
   ```
2. Use the interface to:
   - Load a video file
   - Set processing options (time crop, resize, FPS change)
   - Specify output location
   - Process the video or extract frames

### Dependencies
- opencv-python: For video processing
- tkinter: For the GUI interface
- Pillow: For image processing

<a name="chinese"></a>
## 中文

### 简介
CropVideo 是一款功能强大的视频处理工具，允许用户按时间裁剪视频、调整分辨率、更改帧率以及提取视频帧。它提供了用户友好的界面来完成视频编辑任务。

### 功能特点
- **时间裁剪**：将视频剪切为特定的时间段
- **分辨率缩放**：调整视频尺寸
- **帧率调整**：更改输出视频的帧率
- **帧提取**：从视频中提取单独的帧
- **双语界面**：支持英文和中文

### 安装方法

#### 方法1：直接下载可执行文件
从 [GitHub Releases](https://github.com/dependon/CropVideo/releases) 页面下载最新版本的可执行文件：

- Windows: `cropVideo_windows_x64.exe`
- Linux: `cropVideo_linux_x64`
- macOS: `cropVideo_macos_x64`

#### 方法2：从源码安装
1. 确保已安装 Python 3.6 或更高版本
2. 克隆此仓库或下载源代码
3. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```

### 使用方法
1. 运行应用程序：
   ```
   python cropVideo.py
   ```
2. 使用界面来：
   - 加载视频文件
   - 设置处理选项（时间裁剪、调整大小、帧率更改）
   - 指定输出位置
   - 处理视频或提取帧

### 依赖项
- opencv-python：用于视频处理
- tkinter：用于图形用户界面
- Pillow：用于图像处理

## License
MIT License - See [LICENSE](LICENSE) file for details.

## Links
[GitHub Repository](https://github.com/dependon/CropVideo)

## 开发者信息

### 自动构建与发布

本项目使用GitHub Actions自动构建和发布可执行文件。每当推送到主分支或创建新的Release时，GitHub Actions会自动执行以下操作：

1. 在多个平台（Windows、Linux、macOS）上构建应用程序
2. 运行测试确保代码质量
3. 使用PyInstaller打包成独立的可执行文件
4. 将构建好的可执行文件上传到GitHub Releases

### 手动触发构建

开发者可以通过GitHub Actions界面手动触发构建流程：

1. 进入项目的GitHub页面
2. 点击"Actions"选项卡
3. 选择"Build and Release CropVideo"工作流
4. 点击"Run workflow"按钮
