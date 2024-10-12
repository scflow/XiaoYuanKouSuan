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
import json

logging.getLogger('ppocr').setLevel(logging.ERROR)

# 初始化 PaddleOCR 模型
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=paddle.is_compiled_with_cuda())

# 指定要截取的屏幕区域 (x, y, width, height) 包含四个数字
monitor = {"top": 395, "left": 2100, "width": 400, "height": 230}  # 假设图片大小适合4个数字

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
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
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

# 导出数据为 JSON
def export_to_json(data, filename="ocr_results.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# 主函数
def main():
    last_numbers = (0, 0, 0, 0)  # 上一次的四个数字 (上1, 上2, 下1, 下2)
    current_numbers = (0, 0, 0, 0)  # 当前识别的四个数字
    count = 0
    swipe_draw_count = 0  # 记录 swipe.draw 调用次数
    ocr_data = []  # 用于存储 OCR 结果和 swipe.draw 记录
    round_number = 0  # 记录轮次
    print("Program Start!")

    try:
        while True:
            round_number += 1  # 每一轮计数
            start_time = time.time()
            img = capture_screen(monitor)
            ocr_result = ocr_recognition(img)
            recognized_numbers = []
            confidence_threshold = 0.99
            for line in ocr_result:
                if line:
                    for box in line:
                        text = box[1][0]
                        confidence = box[1][1]

                        # 检查文本是否为数字并且置信度高于阈值
                        if text.isdigit() and confidence >= confidence_threshold:
                            recognized_numbers.append(int(text))

            if len(recognized_numbers) == 2:
                current_numbers = recognized_numbers[:2] + list(last_numbers[-2:])
                current_numbers = tuple(current_numbers)

            # 拒绝大于4个数字的结果
            if len(recognized_numbers) == 4:
                current_numbers = tuple(recognized_numbers)  # 当前四个数字

                # 判断是否是下一批次
                if current_numbers[:2] != last_numbers[:2]:  # 上面两个数字不同，则算新批次
                    # 在这里调用 swipe.draw，并使用上面两个数字
                    swipe.draw(current_numbers[0], current_numbers[1])  # 画图
                    last_numbers = current_numbers  # 更新 last_numbers
                    swipe_draw_count += 1  # 增加 swipe.draw 调用计数
                    print(f'Drawing for {current_numbers[0]}, {current_numbers[1]}')
                    time.sleep(0.1)  # 添加延迟

                    # 保存 OCR 结果和调用记录
                    ocr_data.append({
                        "round_number": round_number,  # 记录当前轮次
                        "current_numbers": current_numbers,
                        "swipe_draw_call": f"Drawing for {current_numbers[0]}, {current_numbers[1]}",
                        "timestamp": time.time()
                    })
                else:
                    count += 1
                    if count % 20 == 0:
                        swipe.draw(current_numbers[0], current_numbers[1])
                        swipe_draw_count += 1  # 增加 swipe.draw 调用计数
                        print(f'Drawing for {current_numbers[0]}, {current_numbers[1]}')
                        count = 0
                        time.sleep(0.1)  # 添加延迟
                        ocr_data.append({
                            "round_number": round_number,  # 记录当前轮次
                            "current_numbers": current_numbers,
                            "swipe_draw_call": f"Drawing for {current_numbers[0]}, {current_numbers[1]}",
                            "timestamp": time.time()
                        })

            # 计算 FPS
            end_time = time.time()
            fps = 1 / (end_time - start_time)
            print(f'\rfps:{int(fps):3d}\tcount:{count:2d}\tround:{round_number}\tnumbers:{current_numbers}\t', end="")

            # 构建包含画面和文字的框架
            frame = build_frame(img, ocr_result, fps)
            cv2.imshow("OCR Recognition", frame)

            # 按 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")

    finally:
        # 导出 JSON 数据
        export_to_json({
            "ocr_results": ocr_data,
            "swipe_draw_count": swipe_draw_count
        })
        print(f"\nOCR data and swipe.draw call count exported to 'ocr_results.json'")
        
        # 释放窗口资源
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
