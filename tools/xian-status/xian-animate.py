#!/usr/bin/env python3
"""
星宿老仙状态动画展示
在终端中显示动态状态
"""
import sys
import time
import os

# 清屏函数
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# 状态动画帧
STATES = {
    'meditating': {
        'name': '冥想中',
        'frames': [
            '''
     🧘
    ╱ ╲
   ╱   ╲
  冥想中...
            ''',
            '''
      🧘
     ╱ ╲
    ╱   ╲
   深呼吸...
            ''',
            '''
       🧘
      ╱ ╲
     ╱   ╲
    平静...
            '''
        ]
    },
    'working': {
        'name': '工作中',
        'frames': [
            '''
    ⚡
   ╱│╲
  ╱ │ ╲
 处理中.
            ''',
            '''
     ⚡
    ╱│╲
   ╱ │ ╲
 处理中..
            ''',
            '''
      ⚡
     ╱│╲
    ╱ │ ╲
 处理中...
            '''
        ]
    },
    'sleeping': {
        'name': '休眠中',
        'frames': [
            '''
    😴
   ╱│╲
  z  │  z
  休眠中
            ''',
            '''
     😴
    ╱│╲
   z │ z
   zzz...
            ''',
            '''
      😴
     ╱│╲
    z│z
   呼呼...
            '''
        ]
    },
    'deep_sleep': {
        'name': '深度睡眠',
        'frames': [
            '''
    💤
   ╱│╲
  ╱ │ ╲
 深度睡眠
            ''',
            '''
     💤
    ╱│╲
   ╱ │ ╲
  请勿打扰
            ''',
            '''
      💤
     ╱│╲
    ╱ │ ╲
   zzzZZZ
            '''
        ]
    }
}

def animate_status(status_key, duration=10):
    """播放状态动画"""
    if status_key not in STATES:
        print(f"未知状态: {status_key}")
        print(f"可用状态: {', '.join(STATES.keys())}")
        return
    
    state = STATES[status_key]
    frames = state['frames']
    
    print(f"\n星宿老仙 - {state['name']}\n")
    print("按 Ctrl+C 退出\n")
    
    start_time = time.time()
    frame_idx = 0
    
    try:
        while time.time() - start_time < duration:
            clear()
            print(f"\n{'='*40}")
            print(f"  星宿老仙 - {state['name']}")
            print(f"{'='*40}")
            print(frames[frame_idx % len(frames)])
            print(f"{'='*40}")
            print(f"  状态: {state['name']}")
            print(f"  时间: {time.strftime('%H:%M:%S')}")
            print(f"{'='*40}\n")
            
            frame_idx += 1
            time.sleep(0.8)
    except KeyboardInterrupt:
        clear()
        print("\n老仙退下了 🙏\n")

if __name__ == '__main__':
    status = sys.argv[1] if len(sys.argv) > 1 else 'meditating'
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    animate_status(status, duration)
