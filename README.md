# SeaImagine · GitHub Overview

[English](profile/README.md) · [简体中文](profile/README_cn.md) · [All languages / 全部语言](data/website-locales.json)

This repository maintains the organization profile at [github.com/seaimagineai](https://github.com/seaimagineai), covering all 15 languages listed on the SeaImagine website.

本仓库维护 SeaImagine 的品牌与开源项目首页。首页的组织介绍独立于具体项目类型；当前已收录的提示词库归在“提示词库与创作参考”分类下。

## 内容放在哪里

- `data/projects.json`：项目清单、分类顺序、仓库名称、各语言文档地址，以及可选封面和官网入口。
- `i18n/*.json`：组织介绍、分类介绍，以及按项目标识保存的介绍和适用人群。
- `profile/README*.md`：生成的 15 种语言页面。GitHub 默认展示 `profile/README.md`，其他语言从导航进入。
- `assets/`：标志、封面与本地文字徽章。

## 添加或更新项目

1. 先核对实际公开仓库、用途、使用文档和许可证。
2. 在 `data/projects.json` 的 `projects` 中添加记录。`id` 是固定标识，不随排序变化；`repository` 填本组织的仓库名；`title` 是显示名称；`category` 对应分类标识。
3. `readmes` 可按语言配置文档路径。缺少某种语言时，使用明确配置的英文文档；没有文档映射时，链接至仓库首页。不要将英文内容标成已有完整翻译。
4. `image` 和 `website_route` 均可省略。只有配了官网入口才显示第二个按钮；模型项目可用 `website_label_key: "try_model"`，普通官网入口默认使用 `visit`。没有封面的项目直接展示文字介绍。
5. 若新增分类，将其标识加入 `categories` 数组，并在每种语言的 `categories` 下添加 `title` 与 `intro`。只在分类有项目时显示它，不展示尚未发布项目的空分类。
6. 在每种语言的 `projects.<id>` 下添加 `description` 和 `audience`。介绍应回答项目包含什么、能帮助读者做什么、适合谁，不把单个项目的定位套到整个组织上。
7. 更新 `data/project-files.json` 中相关仓库的文档路径核验记录。该文件保存已经核实存在的路径；应以远程仓库实际文件为准。
8. 运行生成和检查，再查看 GitHub 实际渲染效果：

```sh
python3 scripts/build_profile.py
python3 scripts/build_profile.py --check
python3 scripts/check_profile.py
python3 -m unittest discover -s scripts -p 'test_*.py'
git diff --check
```

普通文案调整只需修改对应 `i18n` 文件并重新生成；增加项目不需要修改生成器或固定数量检查。

## 来源与维护记录

排版与组织方式参考 [FLAQ 组织首页](https://github.com/flaqai)：品牌介绍、开源理念、项目展示、平台入口和参与贡献。图文与具体项目内容以 SeaImagine 的真实公开资源为准，来源见 [docs/sources.md](docs/sources.md)，审查记录见 [docs/review.md](docs/review.md)。
