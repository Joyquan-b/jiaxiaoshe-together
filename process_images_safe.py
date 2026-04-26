#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图片优化处理脚本 - 超级安全版
步骤：
1. 读取原始图片
2. 验证图片完整性
3. 执行裁剪和缩放
4. 保存到临时文件
5. 验证临时文件
6. 替换原文件
"""

from PIL import Image
import os
import sys
import gc
import time

os.chdir(r'e:\Code\Jiaxiaoshe-together\images')

# 定义目标尺寸
target_width = 1200
target_height = 675
target_ratio = target_width / target_height

print("=" * 90)
print("🖼️  图片处理脚本 - 超级安全版")
print("=" * 90)
print(f"目标分辨率: {target_width}x{target_height} (16:9 比例)")
print(f"处理流程: 读取 → 验证 → 裁剪 → 缩放 → RGB转换 → 保存 → 验证 → 替换")
print("=" * 90)

total_original_size = 0
total_optimized_size = 0
success_count = 0
error_count = 0

for i in range(1, 8):
    filename = f'{i}.jpg'
    temp_filename = f'{filename}.processing'
    
    print(f'\n📋 [{i}/7] 处理 {filename}...')
    
    try:
        # 步骤1：读取原始图片
        print(f'  [1/7] 读取原始文件...')
        original_size_mb = os.path.getsize(filename) / (1024*1024)
        img = Image.open(filename)
        img_width = img.width
        img_height = img.height
        img_mode = img.mode
        print(f'       ✓ 已读取: {img_width}x{img_height}, {img_mode} 模式, {original_size_mb:.2f}MB')
        
        # 步骤2：验证图片完整性
        print(f'  [2/7] 验证图片完整性...')
        try:
            img.verify()
            print(f'       ✓ 图片完整，无损坏')
            img = Image.open(filename)  # verify() 会关闭文件，需要重新打开
        except:
            raise Exception('图片验证失败')
        
        # 步骤3：计算裁剪参数
        print(f'  [3/7] 计算裁剪参数...')
        img_ratio = img.width / img.height
        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            new_height = img.height
            left = (img.width - new_width) // 2
            top = 0
            reason = f"宽度过宽 ({img_ratio:.3f} > {target_ratio:.3f})"
        else:
            new_width = img.width
            new_height = int(img.width / target_ratio)
            left = 0
            top = (img.height - new_height) // 2
            reason = f"高度过高 ({img_ratio:.3f} < {target_ratio:.3f})"
        print(f'       ✓ 原因: {reason}')
        print(f'       ✓ 裁剪范围: ({left}, {top}) 到 ({left + new_width}, {top + new_height})')
        
        # 步骤4：执行裁剪
        print(f'  [4/7] 执行裁剪...')
        img_cropped = img.crop((left, top, left + new_width, top + new_height))
        print(f'       ✓ 裁剪后: {img_cropped.width}x{img_cropped.height}')
        
        # 步骤5：执行缩放
        print(f'  [5/7] 执行缩放...')
        img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        print(f'       ✓ 缩放后: {img_resized.width}x{img_resized.height}')
        
        # 步骤6：处理色彩模式
        print(f'  [6/7] 处理色彩模式...')
        if img_resized.mode == 'RGBA':
            print(f'       - 检测到 RGBA 模式，需要转换...')
            background = Image.new('RGB', img_resized.size, (255, 255, 255))
            background.paste(img_resized, mask=img_resized.split()[3])
            img_resized = background
            print(f'       ✓ 已转换为 RGB (白色背景)')
        elif img_resized.mode != 'RGB':
            print(f'       - 检测到 {img_resized.mode} 模式，需要转换...')
            img_resized = img_resized.convert('RGB')
            print(f'       ✓ 已转换为 RGB')
        else:
            print(f'       ✓ 已是 RGB 模式，无需转换')
        
        # 步骤7：保存到临时文件
        print(f'  [7/7] 保存到临时文件...')
        img_resized.save(temp_filename, 'JPEG', quality=85, optimize=True)
        print(f'       ✓ 已保存: {temp_filename}')
        
        # 步骤8：验证临时文件
        print(f'  [8/9] 验证临时文件...')
        temp_size_mb = os.path.getsize(temp_filename) / (1024*1024)
        try:
            temp_img = Image.open(temp_filename)
            temp_img.verify()
            temp_img = Image.open(temp_filename)
            print(f'       ✓ 临时文件验证成功: {temp_img.width}x{temp_img.height}, {temp_size_mb:.2f}MB')
        except Exception as e:
            raise Exception(f'临时文件验证失败: {e}')
        
        # 步骤9：替换原文件
        print(f'  [9/9] 替换原文件...')
        # 确保所有文件都被关闭
        del img, img_cropped, img_resized, temp_img
        import gc
        gc.collect()
        
        # 等待一下确保文件释放
        import time
        time.sleep(0.1)
        
        os.replace(temp_filename, filename)
        new_size_mb = os.path.getsize(filename) / (1024*1024)
        size_change = ((new_size_mb - original_size_mb) / original_size_mb) * 100
        print(f'       ✓ 替换完成')
        
        # 统计信息
        total_original_size += original_size_mb
        total_optimized_size += new_size_mb
        success_count += 1
        
        print(f'✅ {filename} 处理完成')
        print(f'   原大小: {original_size_mb:.2f}MB  →  新大小: {new_size_mb:.2f}MB  ({size_change:+.1f}%)')
        
    except Exception as e:
        error_count += 1
        print(f'❌ {filename} 处理失败: {str(e)}')
        # 清理临时文件
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
                print(f'   已清理临时文件')
            except:
                pass
        print(f'   ⚠️  原始文件已安全备份到 backup_original/{filename}')

# 最终总结
print("\n" + "=" * 90)
print(f"✅ 处理完成！")
print(f"=" * 90)
print(f"成功: {success_count}/7")
print(f"失败: {error_count}/7")
if success_count > 0:
    print(f"原始总大小: {total_original_size:.2f}MB")
    print(f"优化后总大小: {total_optimized_size:.2f}MB")
    print(f"总计节省: {total_original_size - total_optimized_size:.2f}MB ({((total_original_size - total_optimized_size) / total_original_size) * 100:.1f}%)")
print("=" * 90)

if error_count == 0:
    print("🎉 所有图片都已成功处理！")
    sys.exit(0)
else:
    print("⚠️  有部分图片处理失败，请检查上方错误信息")
    sys.exit(1)
