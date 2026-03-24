# WinRegEditVersion

## CI Status

![Release Workflow](https://github.com/AniketDeshmane/WinRegEditVersion/actions/workflows/release.yml/badge.svg)

## Overview

This project includes a Windows registry spoofing GUI to allow running installers by temporarily changing OS version values.

## Workflow

- Push to `master` triggers GitHub Actions release workflow (`.github/workflows/release.yml`).
- Build idx + release artifact automatically from every commit.

## How to run

1. Build or download executable
2. Run as Administrator
3. Select installer and profile
4. Backup + Spoof + Install -> Restore from Backup
