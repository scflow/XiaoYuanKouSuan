# XiaoYuanKouSuan

基于PaddleOCR用于小猿口算的口算PK Python代码

<p align="center">
  <h3 align="center">“小猿口算 口算PK 比大小”</h3>
  <p align="center">
    使用视觉OCR方案，采用百度PaddleOCR，Paddle系列
    <br/>
    <a href="https://github.com/scflow/XiaoYuanKouSuan_PaddlePCR"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/scflow/XiaoYuanKouSuan_PaddlePCR/issues">报告Bug</a>
    ·
    <a href="https://github.com/scflow/XiaoYuanKouSuan_PaddlePCR/issues">提出新特性</a>
  </p>


</p>


## 目录

- [开发前的配置要求](#开发前的配置要求)
- [安装步骤](#安装步骤)

- [使用到的框架](#使用到的框架)
- [使用说明](#使用说明)
- [如何参与开源项目](#如何参与开源项目)
- [作者](#作者)
- [鸣谢](#鸣谢)




### 开发前的配置要求

1. 本项目基于Python 3.12进行开发
2. 本项目使用了PaddleOCR文本识别(OCR)引擎

### **安装步骤**

1. 在[Python](https://www.python.org/) 下载对应Python版本
2. Paddle系列包推荐在[Paddle官网](https://www.paddlepaddle.org.cn/)根据个人配置选择对应安装版本
3. 安装所需的Python库（有两种安装命令，第一种是安装速度更快的清华大学镜像源，第二种是官方镜像源）👇无论哪个都行，反正选一个
4. 手机投屏工具[scrcpy](https://scrcpy.org/)
5. [ADB](https://developer.android.com/studio/releases/platform-tools?hl=zh-cn)需保存到环境变量中

清华大学镜像源
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
### 使用说明

1. 手机启用ADB，开启USB模拟点击选项(USB安全调试)
2. paddle_ocr_full.py为截取整个数字区域进行识别
3. paddle_ocr_lite.py为分别截取比大小两个数字区域进行识别
4. 可以先试运行代码测试所需的截图区域及swipe中的画图区域
5. 模型加载时间较长，启动时需等待数秒，paddle.is_compiled_with_cuda()若为真则会启用GPU加速计算，帧率会有提升(不过最终效果似乎有限)

```python
monitor = {"top": 395, "left": 2100, "width": 400, "height": 230}#为截图区域
```

### 问题

1. OCR识别存在一定问题，当数字切换时有概率会导致上一轮仍然在画，但当前已经是下一轮了，然后代码会继续画当前的，导致出现大于号与小于号同时出现，目前组好解决方案是增加time.sleep()增加延时避免该问题，但是也会导致速率下降，目前测过的最快速度为0.7秒每道
2. 代码运行后并不会自己判断是否启停，会一直识别，需要自行决定程序运行与否


### 使用到的框架

- [Python](https://www.python.org/)
- [Paddle](https://www.paddlepaddle.org.cn/)

### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



### 作者

Hyperslip@outlook.com

### 参考


- [ChaosJulien/XiaoYuanKouSuan_Auto](https://github.com/ChaosJulien/XiaoYuanKouSuan_Auto)
