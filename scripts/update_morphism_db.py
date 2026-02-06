#!/usr/bin/env python3
"""
自动更新morphism_tags.json数据库
当新增领域时，自动提取Core Morphisms并添加标签占位符
"""

import json
import re
from pathlib import Path

def extract_morphisms_from_domain(domain_path):
    """从领域文件中提取Core Morphisms"""
    with open(domain_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找Core Morphisms部分
    pattern = r'## Core Morphisms \(14个\)(.*?)(?=##|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return []
    
    morphisms_section = match.group(1)
    
    # 提取每个Morphism
    morph_pattern = r'- \*\*(.+?)\*\*:\s*(.+?)\n\s+- \*涉及\*:\s*(.+?)\n\s+- \*动态\*:\s*(.+?)(?=\n\s+- \*\*|$)'
    matches = re.findall(morph_pattern, morphisms_section, re.DOTALL)
    
    morphisms = []
    for i, (name, definition, involves, dynamics) in enumerate(matches, 1):
        morphisms.append({
            'id': i,
            'name': name.strip(),
            'dynamics': dynamics.strip(),
            'tags': [],  # 空标签，需要手动标注
            'annotation_method': 'pending'
        })
    
    return morphisms

def update_morphism_tags_db(domain_name, domain_path, db_path):
    """更新morphism_tags.json数据库"""
    
    # 读取数据库
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 如果领域已存在，跳过
    if domain_name in db['domains']:
        print(f"领域 '{domain_name}' 已存在于数据库中")
        return False
    
    # 提取Morphism
    morphisms = extract_morphisms_from_domain(domain_path)
    
    if len(morphisms) != 14:
        print(f"警告: 只提取到 {len(morphisms)} 个Morphism，预期14个")
    
    # 添加到数据库
    db['domains'][domain_name] = {
        'morphisms': morphisms
    }
    
    # 更新metadata
    db['metadata']['total_domains'] = len(db['domains'])
    db['metadata']['total_morphisms'] = sum(len(d['morphisms']) for d in db['domains'].values())
    
    # 保存
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已添加领域 '{domain_name}' 到数据库")
    print(f"   - 提取Morphism: {len(morphisms)} 个")
    print(f"   - 需要手动标注标签")
    print(f"   - 数据库路径: {db_path}")
    
    return True

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python update_morphism_db.py <domain_name>")
        print("示例: python update_morphism_db.py new_domain")
        sys.exit(1)
    
    domain_name = sys.argv[1]
    
    # 路径设置
    script_dir = Path(__file__).parent
    domain_path = script_dir.parent / "references" / "custom" / f"{domain_name}_v2.md"
    db_path = script_dir.parent / "data" / "morphism_tags.json"
    
    if not domain_path.exists():
        print(f"错误: 领域文件不存在: {domain_path}")
        print("请确保领域文件已创建在 references/custom/ 目录下")
        sys.exit(1)
    
    if not db_path.exists():
        print(f"错误: 数据库文件不存在: {db_path}")
        sys.exit(1)
    
    # 更新数据库
    success = update_morphism_tags_db(domain_name, domain_path, db_path)
    
    if success:
        print("\n下一步:")
        print("1. 打开 data/morphism_tags.json")
        print(f"2. 找到 '{domain_name}' 领域")
        print("3. 为每个Morphism的 'tags' 字段添加1-3个标签")
        print("4. 将 'annotation_method' 改为 'manual'")
        print("5. 保存文件，domain_selector.py会自动使用新领域")

if __name__ == "__main__":
    main()
