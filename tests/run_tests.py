#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行所有测试脚本
"""

import os
import sys
import subprocess
import argparse

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_test(test_file, verbose=False):
    """运行指定的测试文件"""
    print(f"\n{'='*50}")
    print(f"运行测试: {os.path.basename(test_file)}")
    print(f"{'='*50}")
    
    cmd = [sys.executable, test_file]
    
    try:
        if verbose:
            # 直接在当前控制台运行，显示所有输出
            result = subprocess.run(cmd, check=True)
        else:
            # 捕获输出
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
        
        print(f"\n✅ 测试 {os.path.basename(test_file)} 成功完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 测试 {os.path.basename(test_file)} 失败")
        if e.stdout:
            print("输出:")
            print(e.stdout)
        if e.stderr:
            print("错误:")
            print(e.stderr)
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行测试脚本')
    parser.add_argument('--llm', action='store_true', help='只运行LLM测试')
    parser.add_argument('--speech', action='store_true', help='只运行语音API测试')
    parser.add_argument('--api', action='store_true', help='只运行API接口测试')
    parser.add_argument('--ws', action='store_true', help='只运行WebSocket测试')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')
    args = parser.parse_args()
    
    # 获取测试文件目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 确定要运行的测试
    tests_to_run = []
    
    if args.llm:
        tests_to_run.append(os.path.join(test_dir, 'test_llm.py'))
    
    if args.speech:
        tests_to_run.append(os.path.join(test_dir, 'test_speech.py'))
    
    if args.api:
        tests_to_run.append(os.path.join(test_dir, 'test_debate_api.py'))
        
    if args.ws:
        tests_to_run.append(os.path.join(test_dir, 'test_websocket.py'))
    
    # 如果没有指定任何测试，运行所有测试
    if not tests_to_run:
        tests_to_run = [
            os.path.join(test_dir, 'test_llm.py'),
            os.path.join(test_dir, 'test_speech.py'),
            os.path.join(test_dir, 'test_debate_api.py'),
            os.path.join(test_dir, 'test_websocket.py')
        ]
    
    # 运行测试
    success_count = 0
    for test_file in tests_to_run:
        if run_test(test_file, args.verbose):
            success_count += 1
    
    # 打印测试结果摘要
    print(f"\n{'='*50}")
    print(f"测试完成: {success_count}/{len(tests_to_run)} 个测试通过")
    
    if success_count == len(tests_to_run):
        print("✅ 所有测试都通过了！")
    else:
        print(f"❌ {len(tests_to_run) - success_count} 个测试失败")
    
    return 0 if success_count == len(tests_to_run) else 1


if __name__ == "__main__":
    sys.exit(main())
