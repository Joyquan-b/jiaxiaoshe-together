#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证脚本：检查所有图片是否完整有效
"""
from PIL import Image
import os

os.chdir(r'e:\Code\Jiaxiaoshe-together\images')

print("=" * 80)
print("🔍 图片验证 - 检查每张图片是否可正常打开")
print("=" * 80)

all_valid = True
for i in range(1, 8):
    filename = f'{i}.jpg'
    try:
        img = Image.open(filename)
        img.verify()
        img = Image.open(filename)
        size_mb = os.path.getsize(filename) / (1024*1024)
        print(f'✓ {filename} | {img.width}x{img.height} ({img.mode}) | {size_mb:.2f}MB | 状态: OK')
    except Exception as e:
        print(f'✗ {filename} | 错误: {e} | 状态: 损坏')
        all_valid = False

print("=" * 80)
if all_valid:
    print("✅ 所有图片都完整有效，可以继续处理")
else:
    print("❌ 有图片无法打开，请检查")
print("=" * 80)
