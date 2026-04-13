#!/usr/bin/env python3
"""Skill 文件写入工具 - 写入/更新/列出/删除蒸馏.skill"""

import argparse
import json
import os
import sys


DEFAULT_BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "distilled_skills")
)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def write_skill(slug: str, file_path: str, content: str, base_dir: str) -> bool:
    """写入或更新 skill 文件"""
    if not file_path:
        file_path = os.path.join(base_dir, slug, "SKILL.md")
    else:
        # 如果是相对路径，拼到 skill 目录下
        if not os.path.isabs(file_path):
            file_path = os.path.join(base_dir, slug, file_path)

    ensure_dir(os.path.dirname(file_path))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[skill_writer] Written: {file_path}")
    return True


def update_skill_json(slug: str, updates: dict, base_dir: str) -> bool:
    """更新 skill 的 meta.json"""
    meta_path = os.path.join(base_dir, slug, "meta.json")

    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
    else:
        meta = {}

    meta.update(updates)

    ensure_dir(os.path.join(base_dir, slug))
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[skill_writer] Updated meta.json for {slug}")
    return True


def list_skills(base_dir: str) -> list[str]:
    """列出所有 skill"""
    if not os.path.isdir(base_dir):
        return []

    skills = []
    for item in sorted(os.listdir(base_dir)):
        skill_path = os.path.join(base_dir, item)
        skill_md = os.path.join(skill_path, "SKILL.md")
        if os.path.isdir(skill_path) and os.path.exists(skill_md):
            skills.append(item)
    return skills


def list_files(slug: str, base_dir: str) -> list[str]:
    """列出 skill 目录下的文件"""
    skill_dir = os.path.join(base_dir, slug)
    if not os.path.isdir(skill_dir):
        print(f"[skill_writer] Skill not found: {slug}", file=sys.stderr)
        return []

    files = []
    for root, dirs, filenames in os.walk(skill_dir):
        # 排除隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in filenames:
            if not f.startswith("."):
                rel = os.path.relpath(os.path.join(root, f), skill_dir)
                files.append(rel)
    return sorted(files)


def delete_skill(slug: str, base_dir: str, force: bool = False) -> bool:
    """删除 skill（需确认）"""
    skill_dir = os.path.join(base_dir, slug)
    if not os.path.isdir(skill_dir):
        print(f"[skill_writer] Skill not found: {slug}", file=sys.stderr)
        return False

    if not force:
        confirm = input(f"[skill_writer] Delete skill '{slug}'? (yes/no): ")
        if confirm.lower() != "yes":
            print("[skill_writer] Cancelled.")
            return False

    import shutil
    shutil.rmtree(skill_dir)
    print(f"[skill_writer] Deleted: {slug}")
    return True


def read_file(slug: str, file_path: str, base_dir: str) -> str:
    """读取 skill 文件内容"""
    if not file_path:
        file_path = "SKILL.md"

    if not os.path.isabs(file_path):
        file_path = os.path.join(base_dir, slug, file_path)

    if not os.path.exists(file_path):
        print(f"[skill_writer] File not found: {file_path}", file=sys.stderr)
        return ""

    with open(file_path, encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="写入/更新 Skill 文件")
    parser.add_argument("--action", required=True,
                        choices=["write", "update", "list", "delete", "read", "files"],
                        help="操作类型")
    parser.add_argument("--slug", help="Skill slug")
    parser.add_argument("--file", help="要写入的文件路径（相对 skill 目录）")
    parser.add_argument("--content", help="文件内容（write 模式）")
    parser.add_argument("--base-dir", default=DEFAULT_BASE, help="基础目录")
    parser.add_argument("--json", help="JSON 内容（update 模式，格式: key=value,key2=value2）")
    parser.add_argument("--force", action="store_true", help="跳过确认")
    parser.add_argument("--output", help="输出文件路径（read 模式）")
    args = parser.parse_args()

    if args.action in ("write", "update") and not args.slug:
        print("[skill_writer] --slug required for write/update", file=sys.stderr)
        sys.exit(1)

    if args.action == "write" and not args.content:
        print("[skill_writer] --content required for write", file=sys.stderr)
        sys.exit(1)

    if args.action == "update" and not args.json:
        print("[skill_writer] --json required for update", file=sys.stderr)
        sys.exit(1)

    if args.action == "list":
        skills = list_skills(args.base_dir)
        if not skills:
            print(f"[skill_writer] No skills found in {args.base_dir}")
        else:
            print(f"[skill_writer] Skills ({len(skills)}):")
            for s in skills:
                print(f"  - {s}")
        return

    if args.action == "files":
        if not args.slug:
            print("[skill_writer] --slug required for files", file=sys.stderr)
            sys.exit(1)
        files = list_files(args.slug, args.base_dir)
        if files:
            print(f"[skill_writer] Files in {args.slug}:")
            for f in files:
                print(f"  - {f}")
        return

    if args.action == "read":
        if not args.slug:
            print("[skill_writer] --slug required for read", file=sys.stderr)
            sys.exit(1)
        content = read_file(args.slug, args.file or "", args.base_dir)
        if args.output:
            ensure_dir(os.path.dirname(args.output))
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[skill_writer] Saved to {args.output}")
        else:
            print(content)
        return

    if args.action == "write":
        success = write_skill(args.slug, args.file, args.content, args.base_dir)
        if not success:
            sys.exit(1)

    elif args.action == "update":
        # 解析 JSON 参数: key=value,key2=value2
        updates = {}
        for pair in args.json.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                updates[k.strip()] = v.strip()

        success = update_skill_json(args.slug, updates, args.base_dir)
        if not success:
            sys.exit(1)

    elif args.action == "delete":
        if not args.slug:
            print("[skill_writer] --slug required for delete", file=sys.stderr)
            sys.exit(1)
        success = delete_skill(args.slug, args.base_dir, args.force)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
