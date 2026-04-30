#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图片优化脚本：裁剪和压缩所有背景图片到 16:9 比例
"""

from PIL import Image
import os

os.chdir(r'e:\Code\Jiaxiaoshe-together\images')

# 定义目标尺寸 - 使用 1200x675 (16:9 比例，适合web)
target_width = 1200
target_height = 675
target_ratio = target_width / target_height  # 16:9 ≈ 1.778

print("=" * 70)
print("图片优化工具：统一裁剪为 16:9 比例 (1200x675)")
print("=" * 70)

# 处理 1-7 号图片
for i in range(1, 8):
    filename = f'{i}.jpg'
    if not os.path.exists(filename):
        print(f'⚠ {filename} 不存在，跳过')
        continue
    
    try:
        img = Image.open(filename)
        img_ratio = img.width / img.height
        old_size = os.path.getsize(filename) / (1024*1024)
        
        # 计算裁剪尺寸 - 中心裁剪
        if img_ratio > target_ratio:
            # 图片太宽，需要裁剪宽度
            new_width = int(img.height * target_ratio)
            new_height = img.height
            left = (img.width - new_width) // 2
            top = 0
        else:
            # 图片太高，需要裁剪高度
            new_width = img.width
            new_height = int(img.width / target_ratio)
            left = 0
            top = (img.height - new_height) // 2
        
        # 执行中心裁剪
        img_cropped = img.crop((left, top, left + new_width, top + new_height))
        
        # 调整大小到目标分辨率
        img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # 转换为 RGB 模式（JPEG 不支持透明通道）
        if img_resized.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', img_resized.size, (255, 255, 255))
            background.paste(img_resized, mask=img_resized.split()[3])  # 使用 Alpha 通道作为蒙版
            img_resized = background
        elif img_resized.mode != 'RGB':
            img_resized = img_resized.convert('RGB')
        
        # 保存，质量设置为 85 以平衡质量和文件大小
        img_resized.save(filename, 'JPEG', quality=85, optimize=True)
        
        new_size = os.path.getsize(filename) / (1024*1024)
        size_change = ((new_size - old_size) / old_size) * 100
        
        print(f'✓ {filename} | 原: {img.width:4d}x{img.height:<4d} {old_size:5.2f}MB -> 新: {target_width}x{target_height} {new_size:5.2f}MB ({size_change:+.1f}%)')
        
    except Exception as e:
        print(f'✗ {filename} 处理失败: {e}')

# 删除多余的 8.jpg
if os.path.exists('8.jpg'):
    os.remove('8.jpg')
    print(f'\n✓ 8.jpg 已删除（多余图片）')

print("\n" + "=" * 70)
print("✅ 所有图片处理完成！")
print("=" * 70)
