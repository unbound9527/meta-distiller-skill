#!/usr/bin/env python3
"""版本管理工具 - 备份与回滚蒸馏.skill"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "distilled_skills"))


def get_versions_dir(slug: str) -> str:
    """获取指定 skill 的版本目录"""
    return os.path.join(BASE_DIR, slug, ".versions")


def ensure_versions_dir(slug: str) -> str:
    """确保版本目录存在"""
    vd = get_versions_dir(slug)
    os.makedirs(vd, exist_ok=True)
    return vd


def backup_skill(slug: str) -> str:
    """备份 skill 到 .versions 目录"""
    skill_dir = os.path.join(BASE_DIR, slug)
    if not os.path.isdir(skill_dir):
        raise FileNotFoundError(f"Skill not found: {slug}")

    vd = ensure_versions_dir(slug)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_name = f"v_{timestamp}"
    backup_path = os.path.join(vd, version_name)

    # 排除 .versions 目录本身
    items = [i for i in os.listdir(skill_dir) if i != ".versions"]
    for item in items:
        src = os.path.join(skill_dir, item)
        dst = os.path.join(backup_path, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # 保存版本元数据
    meta = {
        "version": version_name,
        "timestamp": timestamp,
        "slug": slug,
        "items": items,
    }
    with open(os.path.join(backup_path, ".version_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[version_manager] Backed up {slug} -> {version_name}")
    return backup_path


def list_versions(slug: str) -> list[dict]:
    """列出 skill 的所有版本"""
    vd = get_versions_dir(slug)
    if not os.path.isdir(vd):
        return []

    versions = []
    for name in sorted(os.listdir(vd)):
        meta_path = os.path.join(vd, name, ".version_meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                meta = json.load(f)
            versions.append(meta)
        else:
            versions.append({"version": name, "timestamp": "unknown"})

    return versions


def rollback_skill(slug: str, version: str) -> bool:
    """将 skill 回滚到指定版本"""
    vd = get_versions_dir(slug)
    version_path = os.path.join(vd, version)

    if not os.path.isdir(version_path):
        print(f"[version_manager] Version not found: {version}", file=sys.stderr)
        return False

    skill_dir = os.path.join(BASE_DIR, slug)

    # 先备份当前版本
    try:
        backup_skill(slug)
    except Exception as e:
        print(f"[version_manager] Warning: pre-rollback backup failed: {e}", file=sys.stderr)

    # 清除当前内容（保留 .versions）
    for item in os.listdir(skill_dir):
        if item == ".versions":
            continue
        path = os.path.join(skill_dir, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    # 恢复版本内容
    for item in os.listdir(version_path):
        if item == ".version_meta.json":
            continue
        src = os.path.join(version_path, item)
        dst = os.path.join(skill_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    print(f"[version_manager] Rolled back {slug} to {version}")
    return True


def main():
    parser = argparse.ArgumentParser(description="版本备份与回滚")
    parser.add_argument("--action", required=True,
                        choices=["backup", "rollback", "list"],
                        help="操作类型")
    parser.add_argument("--slug", help="Skill slug")
    parser.add_argument("--base-dir", default=BASE_DIR, help="基础目录")
    parser.add_argument("--version", help="回滚目标版本号")
    args = parser.parse_args()

    if args.action != "list" and not args.slug:
        print("[version_manager] --slug required for backup/rollback", file=sys.stderr)
        sys.exit(1)

    if args.action == "list" and not args.slug:
        # 列出所有 skill
        if not os.path.isdir(args.base_dir):
            print("[version_manager] Base directory not found:", args.base_dir)
            sys.exit(0)
        slugs = sorted(os.listdir(args.base_dir))
        if not slugs:
            print("[version_manager] No skills found")
        else:
            print("[version_manager] Skills in base_dir:")
            for s in slugs:
                print(f"  - {s}")
        sys.exit(0)

    slug = args.slug

    if args.action == "backup":
        try:
            path = backup_skill(slug)
            print(f"[version_manager] Backup created: {path}")
        except Exception as e:
            print(f"[version_manager] Backup failed: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.action == "rollback":
        if not args.version:
            print("[version_manager] --version required for rollback", file=sys.stderr)
            sys.exit(1)
        success = rollback_skill(slug, args.version)
        if not success:
            sys.exit(1)

    elif args.action == "list":
        versions = list_versions(slug)
        if not versions:
            print(f"[version_manager] No versions for {slug}")
        else:
            print(f"[version_manager] Versions for {slug}:")
            for v in versions:
                print(f"  - {v['version']} ({v.get('timestamp', 'unknown')})")


if __name__ == "__main__":
    main()
