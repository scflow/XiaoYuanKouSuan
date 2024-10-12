import uiautomator2 as u2
import time
# 连接设备
d = u2.connect()

# 获取设备屏幕的分辨率
device_info = d.info
screen_width = device_info['displayWidth']
screen_height = device_info['displayHeight']

# 定义相对坐标 (比例值)
left_large = [
    (0.5, 0.64),  # 第一个点
    (0.55, 0.65),  # 第二个点
    (0.5, 0.66)   # 第三个点
]

right_large = [
    (0.55, 0.54),  # 第一个点
    (0.5, 0.55),  # 第二个点
    (0.55, 0.56)   # 第三个点
]

# 将相对坐标转换为绝对坐标
left_larges = [(int(x * screen_width), int(y * screen_height)) for x, y in left_large]
right_larges = [(int(x * screen_width), int(y * screen_height)) for x, y in right_large]

def draw(x, y):
    if x > y:
        d.swipe(left_larges[0][0], left_larges[0][1], left_larges[1][0], left_larges[1][1], 0.01)
        d.swipe(left_larges[1][0], left_larges[1][1], left_larges[2][0], left_larges[2][1], 0.01)
    elif x < y:
        d.swipe(right_larges[0][0], right_larges[0][1], right_larges[1][0], right_larges[1][1], 0.01)
        d.swipe(right_larges[1][0], right_larges[1][1], right_larges[2][0], right_larges[2][1], 0.01)
    # time.sleep(0.2)
