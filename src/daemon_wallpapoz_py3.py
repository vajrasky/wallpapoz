#!/usr/bin/env python3

import argparse
import random
import sys
import time
from pathlib import Path

from lib.wallpaper_system import WallpaperSystem
from lib.xml_parser import parse_wallpapoz_file


def default_config_path():
    return Path.home() / ".wallpapoz" / "wallpapoz.xml"


def existing_files(files):
    return [filename for filename in files if Path(filename).expanduser().is_file()]


def load_config(path):
    wallpapers, conf = parse_wallpapoz_file(str(path))
    style = conf.get("style", "2")
    delay = max(float(conf.get("interval", "5")) * 60, 1)
    random_order = conf.get("random", "0") == "1"
    config_type = conf.get("type", "workspace")
    return wallpapers, config_type, style, delay, random_order


def describe_config(path, system):
    wallpapers, config_type, style, delay, random_order = load_config(path)
    print(f"Config: {path}")
    print(f"Desktop: {system.desktop}")
    print(f"Type: {config_type}")
    print(f"Delay: {int(delay)} seconds")
    print(f"Random: {'yes' if random_order else 'no'}")
    print(f"Style: {style}")

    if config_type == "workspace":
        print(f"Configured workspaces: {len(wallpapers)}")
        print(f"Detected workspaces: {system.total_workspaces()}")
        print(f"Current workspace: {system.current_workspace()}")
        for index, (name, files) in enumerate(wallpapers, start=1):
            valid_files = existing_files(files)
            print(f"  {index}. {name}: {len(valid_files)}/{len(files)} usable files")
            for filename in files:
                marker = "ok" if Path(filename).expanduser().is_file() else "missing"
                print(f"     [{marker}] {filename}")
    else:
        valid_files = existing_files(wallpapers)
        print(f"Files: {len(valid_files)}/{len(wallpapers)} usable")
        for filename in wallpapers:
            marker = "ok" if Path(filename).expanduser().is_file() else "missing"
            print(f"  [{marker}] {filename}")


def choose_next(files, current_index, random_order):
    if not files:
        return current_index, None
    if random_order:
        next_index = random.randrange(len(files))
        return next_index, files[next_index]
    next_index = (current_index + 1) % len(files)
    return next_index, files[next_index]


def run_desktop_mode(system, files, style, delay, random_order):
    files = existing_files(files)
    if not files:
        return 1

    index = -1
    while True:
        index, filename = choose_next(files, index, random_order)
        system.set_wallpaper(filename, style)
        time.sleep(delay)


def run_workspace_mode(system, workspaces, style, delay, random_order):
    workspace_files = [existing_files(files) for _name, files in workspaces]
    if not any(workspace_files):
        return 1

    indexes = [-1] * len(workspace_files)
    previous_workspace = None
    previous_changes = [None] * len(workspace_files)

    while True:
        current_workspace = system.current_workspace()
        if not 0 <= current_workspace < len(workspace_files):
            previous_workspace = None
            time.sleep(1)
            continue

        now = time.monotonic()
        previous_change = previous_changes[current_workspace]
        expired = previous_change is None or now - previous_change >= delay
        if expired:
            indexes[current_workspace], filename = choose_next(
                workspace_files[current_workspace],
                indexes[current_workspace],
                random_order,
            )
        else:
            filename = workspace_files[current_workspace][indexes[current_workspace]]
        if filename and (expired or current_workspace != previous_workspace):
            system.set_wallpaper(filename, style)
            if expired:
                previous_changes[current_workspace] = now
        previous_workspace = current_workspace
        time.sleep(1)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the Wallpapoz wallpaper daemon.")
    parser.add_argument(
        "--config",
        default=str(default_config_path()),
        help="Path to wallpapoz.xml. Defaults to ~/.wallpapoz/wallpapoz.xml.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print parsed configuration and desktop status without changing wallpaper.",
    )
    args = parser.parse_args(argv)

    config = Path(args.config).expanduser()
    if not config.exists():
        print(f"Configuration file not found: {config}", file=sys.stderr)
        return 1

    random.seed()
    system = WallpaperSystem()
    if args.check:
        describe_config(config, system)
        return 0

    wallpapers, config_type, style, delay, random_order = load_config(config)

    try:
        if config_type == "workspace":
            return run_workspace_mode(system, wallpapers, style, delay, random_order)
        return run_desktop_mode(system, wallpapers, style, delay, random_order)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
