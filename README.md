# WinShadow
使用python实现windows操作的重放
##环境准备
- Python3.6+
- pynput 1.4.4
- pyautogui 0.9.47
## 使用方式
  安装好环境后，将源码下载到本地，进入到源码目录，执行python win_shadow.py 会出现一个操作面板，点击相应的选项即可进行操作录制，操作的回放及退出操作。
*目前支持的操作有*：

- 鼠标操作： 点击，右键，滚轮，选中，拖拽
- 键盘操作：字符输入，简单组合键
## 实现方式
### 鼠标键盘监听
使用pynput,官网<https://pypi.org/project/pynput/>进行鼠标键盘的监听。

### 操作回放
使用pyautogui,源码地址<https://github.com/asweigart/pyautogui>进行鼠标键盘的回放。这里需要注意的是监听结果的操作类型名称有些是不一致的，需要转换
## 参考文档
- <https://pypi.org/project/pynput/>
- <https://pyautogui.readthedocs.io/en/latest/>
- <https://github.com/asweigart/pyautogui>