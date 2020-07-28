import re
import time
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller

LIST_RECORDER = []
AAA = []


mouse = Controller()

def abc():
    x, y = mouse.position
    LIST_RECORDER.append((x, y))
    print("你按下了r键")
    time.sleep(0.2)
    _delay_s = input(f"输入时长: ")
    time.sleep(0.1)
    _delay_s_list = [i for i in _delay_s if i in "1234567890*"]
    _delay_s = ''.join(_delay_s_list) or '0'
    try:
        _delay_s = eval(_delay_s)
        _delay_m = _delay_s/60
        AAA.append(_delay_s)
        print(f'已经记录坐标位置:  {x}, {y} | 延迟 {_delay_s}秒≈{_delay_m}分')
    except:
        print(f"输入有误{_delay_s}")

def go():
    for n, (x, y) in enumerate(LIST_RECORDER):
        mouse.position = (0, 0)
        mouse.move(x, y)
        print(f"鼠标移动到了({x}, {y})")
        # 按住和放开鼠标
        mouse.press(Button.left)
        mouse.release(Button.left)
        print(f"点击, 等待中...{AAA[n]}秒≈{AAA[n]/60}分")
        time.sleep(AAA[n])
    print("All done")
    mouse.move(774, 502)
    return False

def on_press(key):
    # 监听按键
    if "_name_" in key.__dict__ and "enter" == key._name_:
        print(f"已经记录点位{len(LIST_RECORDER)}个, 播放时长为{AAA}单位秒. 按下g开始")
    elif "char" in key.__dict__ and "r" == key.char:
        abc()
    elif "char" in key.__dict__ and "g" == key.char:
        pass
    else:
        pass

def on_release(key):
    # 监听释放
    if key == Key.esc:
        # Stop listener
        return False
    elif "char" in key.__dict__ and "g" == key.char:
        return go()

# 连接事件以及释放
with Listener(on_press=on_press, on_release=on_release) as listener:
    print(f"移动鼠标到相应位置, 按下 r 键记录当前坐标, 随后输入视频播放时间.\n 同理标记下一个视频\n 标记完成后, 按 g 键开始执行.")
    listener.join()