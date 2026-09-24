# SeaImagine · GitHub Overview

[English](profile/README.md) · [简体中文](profile/README_cn.md) · [All languages / 全部语言](data/website-locales.json)

This repository contains the organization profile displayed at [github.com/seaimagineai](https://github.com/seaimagineai).

本仓库维护 SeaImagine 的 GitHub 组织首页，覆盖官网语言菜单中的 15 种语言。

## 更新方法

1. 修改 `i18n/*.json` 中的对应语言文案。
2. 如官网新增语言，更新 `data/website-locales.json` 和生成脚本中的仓库语言映射。
3. 运行 `python3 scripts/build_profile.py`，生成全部首页。
4. 运行 `python3 scripts/build_profile.py --check` 和 `git diff --check`。

`profile/README.md` 是 GitHub 默认显示的英文 Overview；其他语言通过首页语言按钮进入。图片、按钮和跳转地址使用绝对地址，兼容组织首页和仓库文件页。

排版参考 [FLAQ 组织首页](https://github.com/flaqai)：居中标志与标题、品牌按钮、语言徽章、品牌介绍、开源项目、平台入口和参与方式。内容及项目封面来自 SeaImagine 官网与本组织已有仓库。来源与核验记录见 [docs/sources.md](docs/sources.md)。
