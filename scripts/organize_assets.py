#!/usr/bin/env python3
"""organize_assets.py — Redimensionne et organise les assets de la plateforme Callibr.

Usage:
    python scripts/organize_assets.py          # Exécute l'organisation complète
    python scripts/organize_assets.py --dry-run # Affiche ce qui serait fait sans modifier

Conventions:
    img/avatar/agents/{homme,femme}/   — Avatars agents 160x160
    img/avatar/clients/{homme,femme}/  — Avatars clients 160x160
    img/assets/icons/                  — Icônes logo (32, 48, 180px)
    img/temp/                          — Originaux 1024x1024 (backup)
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AVATAR_DIR = PROJECT_ROOT / "img" / "avatar"
TEMP_DIR = PROJECT_ROOT / "img" / "temp"
ASSETS_DIR = PROJECT_ROOT / "img" / "assets"
TARGET_SIZE = (160, 160)


def ensure_dirs() -> None:
    """Create the directory structure if it doesn't exist."""
    for subdir in [
        AVATAR_DIR / "agents" / "homme",
        AVATAR_DIR / "agents" / "femme",
        AVATAR_DIR / "clients" / "homme",
        AVATAR_DIR / "clients" / "femme",
        ASSETS_DIR / "icons",
    ]:
        subdir.mkdir(parents=True, exist_ok=True)


def resize_image(src: Path, dst: Path, size: tuple[int, int] = TARGET_SIZE) -> bool:
    """Resize a PNG image to target size using LANCZOS. Returns True if created."""
    if dst.exists():
        return False
    img = Image.open(src)
    resized = img.resize(size, Image.LANCZOS)
    resized.save(dst, "PNG")
    return True


def migrate_flat_avatars(dry_run: bool = False) -> list[str]:
    """Migrate flat avatar files to gender-based subdirectories."""
    migrations = [
        ("agents/agent_male.png", "agents/homme/agent_male.png"),
        ("agents/agent_femelle.png", "agents/femme/agent_femelle.png"),
        ("clients/cliente_femelle.png", "clients/femme/cliente_femelle.png"),
    ]
    results = []
    for src_rel, dst_rel in migrations:
        src = AVATAR_DIR / src_rel
        dst = AVATAR_DIR / dst_rel
        if src.exists() and not dst.exists():
            if dry_run:
                results.append(f"DRY-RUN: Would migrate {src_rel} -> {dst_rel}")
            else:
                img = Image.open(src)
                if img.size == TARGET_SIZE:
                    shutil.copy2(src, dst)
                else:
                    resized = img.resize(TARGET_SIZE, Image.LANCZOS)
                    resized.save(dst, "PNG")
                src.unlink()
                results.append(f"Migrated: {src_rel} -> {dst_rel}")
        elif dst.exists() and not src.exists():
            results.append(f"SKIP: Already in target (flat source gone): {dst_rel}")
    return results


def resize_temp_images(dry_run: bool = False) -> list[str]:
    """Resize temp images from 1024x1024 to 160x160 and place in correct dirs."""
    mappings = [
        ("Gemini_Generated_Image_kawh93kawh93kawh.png", "clients/homme/client_commercial_inquiet.png"),
        ("Gemini_Generated_Image_70m7hl70m7hl70m7.png", "clients/homme/client_support_stresse.png"),
        ("Gemini_Generated_Image_lai4hplai4hplai4.png", "clients/homme/client_recouvrement_embarrasse.png"),
        ("assets1.png", "agents/homme/agent_sav.png"),
        ("assets2.png", "clients/femme/client_commercial_inquiet_femme.png"),
        ("assets3.png", "agents/femme/agent_commercial.png"),
    ]
    results = []
    for filename, dest_rel in mappings:
        src = TEMP_DIR / filename
        dst = AVATAR_DIR / dest_rel
        if not src.exists():
            results.append(f"SKIP: Source not found: {filename}")
            continue
        if dst.exists():
            results.append(f"SKIP: Already exists: {dest_rel}")
            continue
        if dry_run:
            results.append(f"DRY-RUN: Would resize {filename} -> {dest_rel}")
        else:
            resize_image(src, dst)
            results.append(f"Resized: {filename} -> {dest_rel}")
    return results


def create_favicon_variants(dry_run: bool = False) -> list[str]:
    """Create favicon-sized logo variants from the main logo."""
    logo_src = PROJECT_ROOT / "img" / "callibr_logo.png"
    results = []
    if not logo_src.exists():
        results.append("SKIP: Logo not found: img/callibr_logo.png")
        return results

    sizes = [(32, 32), (48, 48), (180, 180)]
    for size in sizes:
        dst = ASSETS_DIR / "icons" / f"callibr_logo_{size[0]}x{size[1]}.png"
        if dst.exists():
            results.append(f"SKIP: Already exists: icons/callibr_logo_{size[0]}x{size[1]}.png")
            continue
        if dry_run:
            results.append(f"DRY-RUN: Would create icons/callibr_logo_{size[0]}x{size[1]}.png")
        else:
            resize_image(logo_src, dst, size)
            results.append(f"Created: icons/callibr_logo_{size[0]}x{size[1]}.png")
    return results


def verify_structure() -> dict:
    """Verify all avatar files are 160x160 and return summary."""
    summary = {"avatars": [], "icons": [], "errors": []}
    for root, _dirs, files in os.walk(AVATAR_DIR):
        for f in sorted(files):
            path = Path(root) / f
            if f.endswith(".png"):
                img = Image.open(path)
                rel = path.relative_to(AVATAR_DIR)
                entry = {"path": str(rel), "size": f"{img.size[0]}x{img.size[1]}", "ok": img.size == TARGET_SIZE}
                summary["avatars"].append(entry)
                if not entry["ok"]:
                    summary["errors"].append(f"WRONG SIZE: {rel} is {entry['size']}")
            elif f.endswith(".json"):
                summary["manifest"] = str(Path(root).relative_to(AVATAR_DIR) / f)

    for root, _dirs, files in os.walk(ASSETS_DIR):
        for f in sorted(files):
            if f.endswith(".png"):
                path = Path(root) / f
                img = Image.open(path)
                rel = path.relative_to(ASSETS_DIR)
                summary["icons"].append({"path": str(rel), "size": f"{img.size[0]}x{img.size[1]}"})

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize Callibr platform assets to 160x160")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    args = parser.parse_args()

    dry = args.dry_run
    print(f"{'[DRY-RUN] ' if dry else ''}Organizing Callibr assets...\n")

    ensure_dirs()

    print("Phase 1: Migrate flat avatars")
    for msg in migrate_flat_avatars(dry):
        print(f"  {msg}")

    print("\nPhase 2: Resize temp images (1024→160)")
    for msg in resize_temp_images(dry):
        print(f"  {msg}")

    print("\nPhase 3: Create favicon variants")
    for msg in create_favicon_variants(dry):
        print(f"  {msg}")

    print("\nPhase 4: Verification")
    summary = verify_structure()
    for av in summary["avatars"]:
        marker = "✓" if av["ok"] else "✗"
        print(f"  {marker} {av['path']} ({av['size']})")
    for icon in summary["icons"]:
        print(f"  📐 {icon['path']} ({icon['size']})")

    if summary["errors"]:
        print(f"\n❌ {len(summary['errors'])} error(s) found!")
        for err in summary["errors"]:
            print(f"  {err}")
        sys.exit(1)
    else:
        print(f"\n✅ {len(summary['avatars'])} avatars, {len(summary['icons'])} icons — all verified!")


if __name__ == "__main__":
    main()
