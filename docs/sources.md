# 来源与适配说明

核对日期：2026-09-24。

## 排版参考

[FLAQ 组织首页](https://github.com/flaqai)，对应 [.github 源码](https://github.com/flaqai/.github/tree/c0a32bea3f8375828495b6258dfc5ca5a5606d96/profile)。保留居中 88 像素标志、独立品牌标题、一句话介绍、紫色官网按钮、黑色 GitHub 按钮、当前语言绿色徽章、项目用途与适用人群、平台入口和居中页脚。

源库正文没有案例画廊。SeaImagine 的三个可点击项目封面属于本次品牌适配；按项目纵向排列，适合窄屏阅读。源库的 API（应用程序接口）市场、其他品牌项目及联盟佣金没有直接搬入本品牌介绍。

## 官网及语言

- 品牌功能与标志：[SeaImagine 官网](https://seaimagine.com/)、[官方标志](https://seaimagine.com/images/logo.png)。标志保存在 `assets/logo.png`。
- 官网首页 HTML 的语言菜单列出 15 种语言，原始对应关系见 [website-locales.json](../data/website-locales.json)。英文官网使用根路径；简体与繁体分别使用 `/cn/` 与 `/tw/`。
- 功能入口：文字生成视频、图片生成视频、图片生成、图片编辑及创作工作区。各语言地址的 HTTP 核验见 [link-checks.json](../data/link-checks.json)。页面可访问不等于完成了生成测试。

## 项目与图片

| 项目 | 已核对的版本 | 本库封面来源 |
| --- | --- | --- |
| [Gemini Omni](https://github.com/seaimagineai/awesome-gemini-omni-prompts) | `a6b14f09c056e6d3fea8405248ef3d6c9d1c089e` | `assets/seaimagine-omni-hero.png` → `assets/gemini-omni.png` |
| [Grok Imagine](https://github.com/seaimagineai/awesome-grok-imagine-prompts) | `a125427996e881d9b9d5426c72da2d636fb3f7e0` | `assets/seaimagine-grok-hero.webp` → `assets/grok-imagine.webp` |
| [Seedance 2.5](https://github.com/seaimagineai/awesome-seedance-2-5-prompts) | `64fa1ac3a18cdb1f99a67b95e86075a1a5abbc8c` | `assets/seaimagine-seedance-hero-v5.jpg` → `assets/seedance.jpg` |

图片作为提示词资料库的封面使用，不能据此判断模型生成效果。各项目中的官方、社区案例及第三方素材，仍以该项目的来源和授权说明为准。Overview 覆盖 15 种语言，并不代表所有项目中的完整提示词均已翻译成 15 种语言。

## 字形与按钮

普通徽章沿用 Shields.io。包含泰语、阿拉伯语的徽章由 `scripts/build_profile.py` 生成本地 SVG，保留灰色标签区、紫色或黑色操作区，以及绿色当前语言标记。使用原生文字排版，避免外部徽章服务将这些文字逐字符拉开。徽章文件与正文一起检查是否与生成源一致。

模型入口的 45 条语言地址核验见 [model-link-checks.json](../data/model-link-checks.json)。

## 扩写中的案例依据

项目介绍所述案例分别来自 [Gemini Omni 香水案例](https://github.com/seaimagineai/awesome-gemini-omni-prompts#example-02)、[Grok 钟表修复师双人对白](https://github.com/seaimagineai/awesome-grok-imagine-prompts#case-clockwork-dialogue)及 [Seedance 社区案例入口](https://github.com/seaimagineai/awesome-seedance-2-5-prompts#seedance-25-videos-from-x--watch-inspect-remix)。相关描述用于说明资料库里可以学习的创作方法，不作为模型能力比较或效果保证。

## 组织定位与长期维护

按用户要求再次对照 [FLAQ Overview](https://github.com/flaqai/.github/blob/main/profile/README.md) 的组织叙述：先介绍品牌与开放理念，再呈现具体项目。SeaImagine 的组织介绍不限定项目类型；目前的提示词项目保留为一个实际存在的分类。工具、工作流程、教程、资料和代码是欢迎贡献的形式，并非已经上线的项目清单。

实际展示项目以 [projects.json](../data/projects.json) 为准，不能把未发布的项目或空分类写成已有成果。
