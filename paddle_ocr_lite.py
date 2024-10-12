import cv2
import mss
import numpy as np
import paddle
from paddleocr import PaddleOCR
from PIL import Image
import time
import swipe
import logging
import sys

logging.getLogger('ppocr').setLevel(logging.ERROR)

# 初始化 PaddleOCR 模型
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=paddle.is_compiled_with_cuda())
# 指定要截取的屏幕区域 (x, y, width, height)
monitor_left = {"top": 405, "left": 2120, "width": 80, "height": 70}
monitor_right = {"top": 405, "left": 2300, "width": 80, "height": 70}
# 使用 mss 进行屏幕截图
def capture_screen(monitor):
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        return np.array(img)  # 返回 numpy 格式的图像

# 进行 OCR 识别
def ocr_recognition(img):
    result = ocr.ocr(img, cls=True)  # 使用 PaddleOCR 进行文字识别
    if result is None or len(result) == 0:
        return []
    return result

# 构建显示框架
def build_frame(img, ocr_result, fps):
    # 创建一个 450x300 的空白画布，用于显示图像和文字
    frame = np.ones((300, 450, 3), dtype=np.uint8) * 255  # 白色背景

    # 将图像放在左侧（300x300 区域）
    img_resized = cv2.resize(img, (300, 300))
    frame[0:300, 0:300] = img_resized

    # 在右侧显示 OCR 结果
    if ocr_result:
        try:
            text_output = "\n".join([box[1][0] for line in ocr_result if line for box in line])  # 检查每一层是否为空
        except TypeError:
            text_output = "No valid text detected"
    else:
        text_output = "No text detected"

    # 将文字显示在右侧
    y0, dy = 30, 30
    for i, line in enumerate(text_output.split('\n')):
        y = y0 + i * dy
        cv2.putText(frame, line, (310, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # 显示 FPS
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame

# 主函数
def main():
    last_left = 0
    last_right = 0
    number_left = 0
    number_right = 0
    count = 0
    true_count = 0
    print("Program Start!")
    while True:
        start_time = time.time()
        last_left = number_left
        last_right = number_right
        # 截取屏幕指定区域的图像
        img_left = capture_screen(monitor_left)
        img_right = capture_screen(monitor_right)
        # 识别该区域中的文本
        ocr_result_left = ocr_recognition(img_left)
        ocr_result_right = ocr_recognition(img_right)
        try:
            text_left = "\n".join([box[1][0] for line in ocr_result_left if line for box in line])
            number_left = int(text_left.strip())  # 使用 strip() 去除可能存在的空白字符
        except ValueError:
            number_left = last_left
        try:
            text_right = "\n".join([box[1][0] for line in ocr_result_right if line for box in line])
            number_right = int(text_right.strip())  # 使用 strip() 去除可能存在的空白字符
        except ValueError:
            number_right = last_right
        if number_left == last_left and number_right == last_right:
            count = count + 1
            count = count % 3
            if not count:
                swipe.draw(number_left, number_right)
                time.sleep(0.5)
        else:
            swipe.draw(number_left, number_right)
            time.sleep(0.5)
        # 计算 FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        # sys.stdout.write(f'\rfps:{int(fps)}\tcount:{count}\tnumber_left:{number_left}\tnumber_right:{number_right}\tlast_left:{last_left}\tlast_right:{last_right}')
        # sys.stdout.flush()
        print(f'\rfps:{int(fps):3d}\tcount:{count:3d}\tnumber_left:{number_left:3d}\tnumber_right:{number_right:3d}\tlast_left:{last_left:3d}\tlast_right:{last_right:3d}', end="")
        # print('\r'f'fps:{int(fps)}\tcount:{count} \tnumber_left:{number_left}\tnumber_right:{number_right}\tlast_left:{last_left}\tlast_right:{last_right}', end="")
        # sys.stdout.flush()
        # 构建包含画面和文字的框架
        # frame_left = build_frame(img_left, ocr_result_left, fps)
        # cv2.putText(frame_left, str(number_left), (270, 301), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # frame_right = build_frame(img_right, ocr_result_right, fps)
        # cv2.putText(frame_right, str(number_right), (270, 301), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        # 显示框架
        # cv2.imshow("OCR Recognition_Left", frame_left)
        # cv2.imshow("OCR Recognition_Right", frame_right)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放窗口
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
