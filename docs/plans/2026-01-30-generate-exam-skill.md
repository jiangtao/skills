# 试卷生成技能实现计划

> **For Claude:** 必需子技能：使用 superpowers:executing-plans 逐步执行此计划。

**目标：** 创建一个手动 Agent Skill，用于生成中国小学数学练习试卷（PDF），包含口算题、计算题和应用题。

**架构：** Type 3 手动技能 - 遵循 AGENTS.md 规范的手写技能，包含 `skill.md` 索引和 `references/` 子目录。这是一个对话式伪命令，由 Claude Code 助手识别，不是可执行二进制文件。

**技术栈：** Markdown (Agent Skills 格式)，AGENTS.md Type 3 规范

---

## 任务 1：创建技能目录结构

**文件：**
- 创建：`skills/exam/`
- 创建：`skills/exam/references/`

**步骤 1：创建目录**

```bash
mkdir -p skills/exam/references
```

**步骤 2：验证目录创建**

运行：`ls -la skills/exam/`
预期：显示 `references/` 目录

**步骤 3：提交**

```bash
git add skills
git commit -m 'feat: add exam skills'
```

---

## 任务 2：创建主 skill.md 索引

**文件：**
- 创建：`skills/exam/skill.md`

**步骤 1：编写 skill.md（包含元数据和核心引用）**

```markdown
---
name: exam
description: 生成中国小学数学练习试卷（PDF）
metadata:
  author: Jiangtao
  version: "0.1.0"
---

> 为中国小学生生成可打印的数学练习卷（口算题、计算题、应用题），支持自定义主题和难度。

## 概述

exam 技能创建专业的人教版数学寒假/暑假作业练习卷（PDF），支持：

- **口算题：** 两位数及以上，必须有进位或退位
- **计算题：** 三个数字的混合运算，遵循运算顺序
- **应用题：** 基于主题的场景化问题

### 命令模式

**使用方法：**
```bash
/edu:exam [--oral=N] [--calculation=N] [--word=N] [--theme="名称"] [--grade=年级] [--output=文件名]
```

**触发短语：**
- `/edu:exam`
- `generate exam` / `generate worksheet`
- `生成试卷` / `生成数学作业`
- `create math worksheet`

## 核心参考

| 主题 | 描述 | 参考 |
|-------|-------------|-----------|
| 题型说明 | 每种题型的详细要求 | [题型说明](references/question-types.md) |
| 参数说明 | 命令参数和配置选项 | [参数说明](references/parameters.md) |
| 使用示例 | 使用示例和输出样例 | [使用示例](references/examples.md) |
| 错误处理 | 错误场景和恢复策略 | [错误处理](references/error-handling.md) |

## 出题规则

### 口算题
- **范围：** 2-4 位数（100-10000）
- **加法：** 必须有进位（个位之和 ≥ 10）
- **减法：** 必须有退位（被减数个位 < 减数个位）
- **乘法：** 三位数 × 一位数（≤9），必须有进位
- **除法：** 三位数 ÷ 一位数（≤9），必须整除，必须有退位

### 计算题
- 每题恰好 3 个数字
- 混合运算（+、-、×、÷）
- 遵循运算顺序
- 最终答案：正整数

### 应用题
- 基于主题的场景（购物、学校、交通、家庭、节日、卡通）
- 2-3 步问题
- 所有答案：正整数

## 输出格式

**PDF 文件名：** `{主题}-{YYYY-MM-DD}.pdf`

**版面布局：**
- 页眉：标题、日期、主题
- 第一部分：口算题（分栏布局）
- 第二部分：计算题（行布局）
- 第三部分：应用题（留答题空间）
- 页脚：参考答案（可选）
```

**步骤 2：验证 frontmatter 格式**

运行：`head -10 skills/exam/skill.md`
预期：显示 YAML frontmatter（name、description、metadata）

**步骤 3：提交**

```bash
git add skills/exam/skill.md
git commit -m "feat: 添加 exam skill.md 核心规范"
```

---

## 任务 3：创建题型说明参考

**文件：**
- 创建：`skills/exam/references/question-types.md`

**步骤 1：编写 question-types.md**

```markdown
---
name: question-types
description: 每种题型的详细要求
---

# 题型说明

## 口算题

### 要求
- **数字范围：** 100 - 10,000（2-4 位数）
- **格式：** 纯计算题（如 "125 + 37 = ?"）
- **布局：** 每页 2-4 栏

### 加法
**规则：** 必须有进位
```
个位之和 ≥ 10
示例：137 + 45 = ?（7 + 5 = 12，进位）
```

**生成方法：**
- 生成数字：A (100-9999)，B (10-99)
- 确保：(A % 10) + (B % 10) ≥ 10

### 减法
**规则：** 必须有退位

```
被减数个位 < 减数个位
示例：152 - 37 = ?（2 < 7，退位）
```

**生成方法：**
- 生成：A (100-9999)，B (10-99)
- 确保：A > B 且 (A % 10) < (B % 10)

### 乘法
**规则：** 三位数 × 一位数（表内乘法），必须有进位

```
第二个数 ≤ 9
示例：115 × 8 = ?（5 × 8 = 40，进位）
```

**生成方法：**
- 生成：A (100-999)，B (2-9)
- 确保：(A % 10) × B ≥ 10 或中间有进位

### 除法
**规则：** 三位数 ÷ 一位数（表内除法），必须整除，必须有退位

```
第二个数 ≤ 9，必须能整除
示例：872 ÷ 8 = ?（百位/十位有退位）
```

**生成方法：**
- 生成：A (100-999)，B (2-9)
- 确保：A % B == 0 且商是三位数

## 计算题

### 要求
- **格式：** 3 个数字 + 2 个运算符（如 "125 × 4 - 60 = ?"）
- **运算：** +、-、×、÷
- **规则：** 遵循运算顺序（先乘除后加减）
- **答案：** 正整数

### 类型分类

#### 加减混合
```
示例：145 + 23 - 67 = ?
模式：A ± B ± C
```

#### 乘加混合
```
示例：25 × 4 + 30 = ?（先乘后加）
模式：A × B ± C 或 A ± B × C
```

#### 乘除混合
```
示例：120 ÷ 4 × 3 = ?（从左到右）
模式：A × B ÷ C 或 A ÷ B × C
```

#### 三种及以上运算
```
示例：15 × 6 - 45 ÷ 9 = ?
模式：混合 3+ 种运算
```

### 生成规则
1. 生成 3 个适合年级的数字
2. 选择 2 个运算符，确保中间结果有效
3. 按运算顺序计算最终答案
4. 验证答案是正整数

## 应用题

### 要求
- **格式：** 2-3 句话场景描述 + 问题
- **步骤：** 2-3 步计算
- **答案：** 正整数
- **主题：** 使用指定主题或默认生活场景

### 默认主题
| 主题 | 描述 |
|-------|-------------|
| 购物 | 买东西、价格、找零 |
| 学校 | 教室、书本、学生 |
| 交通 | 距离、速度、时间 |
| 家庭 | 分享、做饭、家务 |
| 节日 | 礼物、装饰、食物 |
| 卡通 | 海底小纵队、喜羊羊等 |

### 题目结构
```
1. 场景设置（1-2 句话）
2. 问题（要解决什么）
3. 要求：（列式计算）
```

### 示例（购物主题）
```
小明去超市买乐高玩具，买了 3 盒，每盒 45 元。
付给收银员 150 元，应该找回多少钱？
（列式计算）
```

**答案：** 150 - 45 × 3 = 15 元

### 生成规则
1. 选择主题
2. 创建包含 2-3 个数值的场景
3. 设计需要 2-3 步计算的问题
4. 验证答案是正整数
5. 包含"（列式计算）"要求
```

**步骤 2：验证 markdown 格式**

运行：`head -50 skills/exam/references/question-types.md`
预期：显示带有 frontmatter 的正确 markdown 格式

**步骤 3：提交**

```bash
git add skills/exam/references/question-types.md
git commit -m "feat: 添加题型说明参考文档"
```

---

## 任务 4：创建参数说明参考

**文件：**
- 创建：`skills/exam/references/parameters.md`

**步骤 1：编写 parameters.md**

```markdown
---
name: parameters
description: 命令参数和配置选项
---

# 参数说明

## 命令语法

```bash
/edu:exam [选项]
```

## 参数

### `--oral` <数字>
**说明：** 口算题数量
**默认值：** 20
**范围：** 1-100
**示例：** `--oral=30`

### `--calculation` <数字>
**说明：** 计算题数量
**默认值：** 10
**范围：** 1-50
**示例：** `--calculation=15`

### `--word` <数字>
**说明：** 应用题数量
**默认值：** 5
**范围：** 1-20
**示例：** `--word=10`

### `--theme` <字符串>
**说明：** 应用题主题和 PDF 文件名
**默认值：** "default"
**可选主题：** 乐高、迪士尼、购物、学校、交通、家庭、节日、卡通
**示例：** `--theme="乐高"`

### `--grade` <年级>
**说明：** 年级（用于难度调整）
**默认值：** "grade_3"
**可选年级：** grade_1、grade_2、grade_3、grade_4、grade_5、grade_6
**示例：** `--grade=grade_4`

### `--output` <文件名>
**说明：** 自定义输出 PDF 文件名（可选）
**默认值：** 自动生成为 `{主题}-{YYYY-MM-DD}.pdf`
**示例：** `--output="我的试卷.pdf"`

## 输出文件名格式

未指定 `--output` 时，文件名自动生成：

```
{主题}-{YYYY-MM-DD}.pdf
```

**示例：**
- `乐高-2026-01-30.pdf`
- `default-2026-01-30.pdf`
- `迪士尼-2026-01-30.pdf`

## 默认配置

不提供任何参数时：

```bash
/edu:exam
```

**生成：**
- 20 道口算题
- 10 道计算题
- 5 道应用题
- 主题："default"
- 年级："grade_3"
- 输出：`default-2026-01-30.pdf`

## 参数验证

### 验证规则
1. `--oral`、`--calculation`、`--word` 必须是正整数
2. `--theme` 必须是非空字符串
3. `--grade` 必须是有效年级
4. 总题目数应能放在可打印页面（建议 ≤ 100 道）

### 错误处理
验证失败时：
- 显示友好的错误消息
- 展示参数用法
- 建议修正方法
- 允许用正确参数重试
```

**步骤 2：验证参数文档**

运行：`cat skills/exam/references/parameters.md`
预期：显示所有参数及其默认值和示例

**步骤 3：提交**

```bash
git add skills/exam/references/parameters.md
git commit -m "feat: 添加参数说明参考文档"
```

---

## 任务 5：创建使用示例参考

**文件：**
- 创建：`skills/exam/references/examples.md`

**步骤 1：编写 examples.md**

```markdown
---
name: examples
description: 使用示例和输出样例
---

# 使用示例

## 示例 1：默认试卷

**命令：**
```bash
/edu:exam
```

**输出：**
- 文件：`default-2026-01-30.pdf`
- 内容：20 道口算 + 10 道计算 + 5 道应用

**输出样例：**
```
口算题（每题 2 分，共 40 分）

1. 137 + 45 = ______      11. 215 × 4 = ______
2. 152 - 37 = ______      12. 964 ÷ 8 = ______
...

计算题（每题 4 分，共 40 分）

1. 125 × 4 - 60 = ______
2. 345 + 25 - 180 = ______
...

应用题（每题 12 分，共 60 分）

1. 小明去超市买苹果，买了 3 袋，每袋 12 个。
   一共买了多少个苹果？（列式计算）

   答：3 × 12 = 36 个
...
```

## 示例 2：自定义主题

**命令：**
```bash
/edu:exam --theme="乐高"
```

**输出：**
- 文件：`乐高-2026-01-30.pdf`
- 内容：默认数量 + 乐高主题应用题

**应用题示例（乐高主题）：**
```
乐高商店有 5 盒积木，每盒 120 块。
卖出了 285 块，还剩多少块？
（列式计算）

答：120 × 5 - 285 = 315 块
```

## 示例 3：完全自定义

**命令：**
```bash
/edu:exam --oral=30 --calculation=15 --word=10 --theme="迪士尼" --grade=grade_4
```

**输出：**
- 文件：`迪士尼-2026-01-30.pdf`
- 内容：30 道口算 + 15 道计算 + 10 道应用

**应用题示例（迪士尼主题）：**
```
迪士尼乐园有 8 个游乐区，每个区可容纳 156 人。
上午接待了 1250 人，下午还能容纳多少人？
（列式计算）
```

## 示例 4：自定义输出文件名

**命令：**
```bash
/edu:exam --output="寒假作业-第1周.pdf"
```

**输出：**
- 文件：`寒假作业-第1周.pdf`
- 内容：默认题目数量

## 示例 5：精简试卷

**命令：**
```bash
/edu:exam --oral=10 --calculation=5 --word=2
```

**输出：**
- 文件：`default-2026-01-30.pdf`
- 内容：10 道口算 + 5 道计算 + 2 道应用

**用途：** 快速练习或测试

## 交互式示例

**用户说：**
```
生成一个乐高主题的数学卷子，30 道口算，15 道计算，10 道应用题
```

**助手识别为：**
```bash
/edu:exam --theme="乐高" --oral=30 --calculation=15 --word=10
```

**助手响应：**
```
我将为您生成乐高主题的数学试卷：
- 30 道口算题
- 15 道计算题
- 10 道应用题

正在生成题目...
创建 PDF：乐高-2026-01-30.pdf
✅ 完成！
```

## PDF 版面预览

```
┌─────────────────────────────────────────┐
│    数学寒假作业 - 乐高主题                 │
│    2026-01-30                            │
├─────────────────────────────────────────┤
│ 一、口算题（每题 2 分，共 60 分）        │
│                                         │
│  1. 137 + 45 = ______        16. ...   │
│  2. 152 - 37 = ______        17. ...   │
│  ...                                    │
├─────────────────────────────────────────┤
│ 二、计算题（每题 4 分，共 60 分）        │
│                                         │
│  1. 125 × 4 - 60 = ______              │
│  2. 345 + 25 - 180 = ______             │
│  ...                                    │
├─────────────────────────────────────────┤
│ 三、应用题（每题 10 分，共 100 分）      │
│                                         │
│  1. 乐高商店有 5 盒积木，每盒 120 块。  │
│     卖出了 285 块，还剩多少块？          │
│     （列式计算）                         │
│                                         │
│     答：________________________________│
│                                         │
│  ...                                    │
└─────────────────────────────────────────┘
```
```

**步骤 2：验证示例格式**

运行：`grep "示例" skills/exam/references/examples.md | head -5`
预期：显示示例标题

**步骤 3：提交**

```bash
git add skills/exam/references/examples.md
git commit -m "feat: 添加使用示例参考文档"
```

---

## 任务 6：创建错误处理参考

**文件：**
- 创建：`skills/exam/references/error-handling.md`

**步骤 1：编写 error-handling.md**

```markdown
---
name: error-handling
description: 错误场景和恢复策略
---

# 错误处理

## AI 响应错误

### 无效的 JSON 响应

**场景：** 请求生成题目时，AI 返回格式错误或非 JSON 响应。

**恢复策略：**
1. 记录错误日志（时间戳和原始响应）
2. 重试并提示："请仅返回有效的 JSON 格式"
3. 3 次失败后，返回原始文本供人工检查
4. 生成 PDF 并标注警告

**响应示例：**
```
⚠️ 警告：部分题目可能需要人工检查
原始 AI 响应已保存至：exam-error-20260130.log
```

## 答案验证错误

### 答案错误

**场景：** 生成题目的答案与计算不匹配。

**恢复策略：**
1. 记录问题（预期答案 vs 实际答案）
2. 在 PDF 输出中包含警告
3. 用 ⚠️ 标记问题
4. 仍然生成 PDF（不中断整批）

**示例：**
```
⚠️ 5. 137 + 45 = 182（预期：182，AI 说：183）
```

### 非整数答案

**场景：** 计算结果是小数或负数。

**恢复策略：**
1. 用不同数字重新生成
2. 验证答案是正整数
3. 最多 3 次重试
4. 3 次失败后跳过并记录

**示例：**
```
警告：第 7 题重试 3 次后仍失败，已跳过
已生成替换题目。
```

### 除法不能整除

**场景：** 除法题目不能整除。

**恢复策略：**
1. 验证：A % B == 0 后才接受
2. 用新除数重新生成
3. 3 次失败后跳过

## PDF 生成错误

### PDF 库失败

**场景：** PDF 生成抛出错误。

**恢复策略：**
1. 用新参数重试一次
2. 第二次失败后，输出文本格式
3. 保存原始内容到 `.txt` 文件
4. 向用户显示消息

**示例：**
```
⚠️ PDF 生成失败（已尝试 2 次）
降级方案：已生成 default-2026-01-30.txt
您可以手动转换为 PDF。
```

### 中文字符编码

**场景：** 中文字符显示为乱码。

**预防措施：**
- 所有文本使用 UTF-8 编码
- 指定支持中文的字体（如 SimSun、SimHei）
- 生成前用中文样本测试

**恢复方法：**
1. 切换到备选中文字体
2. 重试 PDF 生成
3. 仍然失败则使用文本降级

## 参数错误

### 无效的数字参数

**场景：** 用户提供非整数的数量参数。

**示例：**
```bash
/edu:exam --oral=abc
```

**响应：**
```
❌ 参数无效：--oral 必须是正整数
收到："abc"

正确用法：
/edu:exam --oral=20
```

### 超出范围的参数

**场景：** 用户提供超出有效范围的数字。

**示例：**
```bash
/edu:exam --oral=500
```

**响应：**
```
❌ 参数无效：--oral 必须在 1 到 100 之间
收到：500

建议：使用 --oral=100 获取最多口算题
```

### 无效的年级

**场景：** 用户提供无法识别的年级。

**示例：**
```bash
/edu:exam --grade=grade_7
```

**响应：**
```
❌ 参数无效：--grade 必须是以下之一：grade_1、grade_2、grade_3、grade_4、grade_5、grade_6
收到："grade_7"
```

## 日志记录

### 错误日志格式

**日志文件：** `exam-errors-{date}.log`

**格式：**
```
[2026-01-30 14:30:15] ERROR: JSON 响应无效
  提示词："生成 20 道口算题..."
  响应："当然，这是一些题目..."
  重试：1/3

[2026-01-30 14:30:18] WARNING: 答案验证失败
  题目："137 + 45 = ?"
  预期：182
  收到：183
  操作：已标记警告
```

## 用户沟通

### 错误消息风格

**原则：**
- 清晰可操作
- 说明出了什么问题
- 建议如何修复
- 使用表情符号增强视觉识别
- 中文场景保留中文

**好示例：**
```
❌ PDF 生成失败
原因：中文编码错误
建议：使用支持中文的字体
重试：/edu:exam --theme="乐高"
```

**坏示例：**
```
Error: PDF generation failed
```

## 优雅降级

**优先级顺序：**
1. 完整 PDF（包含所有题目）
2. 带警告的 PDF
3. 文本文件降级
4. 终端显示题目

**绝不：** 无用户反馈地崩溃
```

**步骤 2：验证错误处理章节**

运行：`grep "^##" skills/exam/references/error-handling.md`
预期：显示所有主要错误类别

**步骤 3：提交**

```bash
git add skills/exam/references/error-handling.md
git commit -m "feat: 添加错误处理参考文档"
```

---

## 任务 7：在 meta.ts 中注册技能

**文件：**
- 修改：`meta.ts:36-39`

**步骤 1：读取 meta.ts 的 manual 数组**

当前内容：
```typescript
export const manual = [
  'handoff',
  'jerret',
]
```

**步骤 2：添加 'exam' 到 manual 数组**

```typescript
export const manual = [
  'exam',
  'handoff',
  'jerret',
]
```

**步骤 3：验证 TypeScript 语法**

运行：`pnpm lint`
预期：meta.ts 没有 linting 错误

**步骤 4：提交**

```bash
git add meta.ts
git commit -m "feat: 在 manual 技能中注册 exam"
```

---

## 任务 8：创建 GENERATION.md 跟踪文件

**文件：**
- 创建：`skills/exam/GENERATION.md`

**步骤 1：编写 GENERATION.md**

```markdown
# 生成信息

- **类型：** Type 3 - 手动技能（手写）
- **来源：** 为本集合创建的原创技能
- **创建时间：** 2026-01-30
- **版本：** 1.0.0

## 技能结构

这是一个遵循 AGENTS.md 规范的手动 Type 3 技能：
```
skills/exam/
├── skill.md              # 主技能索引，包含命令模式
├── GENERATION.md         # 本文件
└── references/
    ├── question-types.md # 题型详细规范
    ├── parameters.md     # 命令参数和验证
    ├── examples.md       # 使用示例和输出样例
    └── error-handling.md # 错误场景和恢复
```

## 实现说明

- **命令类型：** 伪命令（对话模式，非可执行）
- **触发模式：** `/edu:exam` 带可选参数
- **输出：** PDF 文件生成（由 Claude Code 助手处理）
- **依赖：** 无（纯 markdown 技能）
- **语言：** 中文题目内容，中文文档

## 测试清单

- [ ] 目录结构符合 AGENTS.md Type 3 规范
- [ ] skill.md 有有效的 frontmatter（name、description、metadata）
- [ ] 所有参考文件都有 frontmatter
- [ ] skill.md 中存在核心参考表
- [ ] 已在 meta.ts 的 manual 数组中注册
- [ ] 无 TypeScript linting 错误
- [ ] 所有提交消息遵循格式："feat: ..."
```

**步骤 2：验证 GENERATION.md 格式**

运行：`cat skills/exam/GENERATION.md | head -20`
预期：显示生成信息标题

**步骤 3：提交**

```bash
git add skills/exam/GENERATION.md
git commit -m "feat: 添加 GENERATION.md 跟踪元数据"
```

---

## 任务 9：验证 AGENTS.md Type 3 合规性

**文件：**
- 测试：`skills/exam/`

**步骤 1：运行目录结构验证**

运行：`find skills/exam -type f -name "*.md" | sort`

预期输出：
```
skills/exam/GENERATION.md
skills/exam/references/error-handling.md
skills/exam/references/examples.md
skills/exam/references/parameters.md
skills/exam/references/question-types.md
skills/exam/skill.md
```

**步骤 2：验证 skill.md frontmatter**

运行：`head -10 skills/exam/skill.md`

预期输出：
```markdown
---
name: exam
description: 生成中国小学数学练习试卷（PDF）
metadata:
  author: Jiangtao
  version: "1.0.0"
---
```

**步骤 3：验证所有参考文件都有 frontmatter**

运行：`for f in skills/exam/references/*.md; do echo "=== $f ==="; head -5 "$f"; done`

预期：每个文件显示包含 name 和 description 的 frontmatter

**步骤 4：验证 meta.ts 注册**

运行：`grep "exam" meta.ts`

预期：在 manual 数组中显示 `'exam'`

**步骤 5：运行 linting**

运行：`pnpm lint`

预期：无错误

**步骤 6：提交验证结果**

```bash
echo "✅ Type 3 合规性验证通过" > skills/exam/.verified
git add skills/exam/.verified
git commit -m "test: 验证 AGENTS.md Type 3 合规性"
```

---

## 任务 10：最终集成测试

**文件：**
- 测试：完整技能安装

**步骤 1：模拟技能安装**

运行：`pnpm start cleanup -y`

预期：Skills manager 运行，新技能无需清理

**步骤 2：验证技能可被发现**

运行：`ls -la skills/ | grep exam`

预期：显示 exam 目录

**步骤 3：统计参考文件**

运行：`ls skills/exam/references/ | wc -l`

预期：4 个参考文件

**步骤 4：验证总 markdown 文件数**

运行：`find skills/exam -name "*.md" | wc -l`

预期：6 个 markdown 文件（skill.md + GENERATION.md + 4 个参考）

**步骤 5：检查 git 状态**

运行：`git status --short skills/exam/`

预期：所有文件已提交（干净状态）

**步骤 6：最终提交**

```bash
git add -A
git commit -m "feat: 完成 exam 技能实现

- 创建 Type 3 手动技能结构
- 添加 skill.md（命令模式和元数据）
- 创建 4 个参考文件（题型、参数、示例、错误处理）
- 在 meta.ts manual 数组中注册
- 验证 AGENTS.md Type 3 合规性
- 所有文件已提交，可安装

使用方法：/edu:exam [--oral=N] [--calculation=N] [--word=N] [--theme=名称]"
```

---

## 实现后的测试

### 手动验证测试

1. **默认配置测试：**
   - 命令：`/edu:exam`
   - 验证：助手识别命令并提示 PDF 生成

2. **自定义参数测试：**
   - 命令：`/edu:exam --oral=30 --theme="乐高"`
   - 验证：助手正确解析参数

3. **帮助/信息请求测试：**
   - 命令："exam 是做什么的？"
   - 验证：助手描述技能和用法

4. **安装测试：**
   - 运行：`pnpm start check`
   - 验证：exam 出现在 manual 技能列表中

### AGENTS.md Type 3 清单

- [x] skill.md 存在且包含有效 frontmatter
- [x] references/ 子目录存在
- [x] 每个参考都有 frontmatter（name、description）
- [x] skill.md 中存在核心参考表
- [x] 已在 meta.ts manual 数组中注册
- [x] GENERATION.md 跟踪元数据
- [x] 无尾随空格或格式问题
- [x] 一致的 markdown 格式

### 创建的文件摘要

| 文件 | 用途 |
|------|---------|
| `skills/exam/skill.md` | 主技能索引，包含命令模式 |
| `skills/exam/GENERATION.md` | 生成跟踪元数据 |
| `skills/exam/references/question-types.md` | 题型详细规范 |
| `skills/exam/references/parameters.md` | 命令参数和验证 |
| `skills/exam/references/examples.md` | 使用示例和输出样例 |
| `skills/exam/references/error-handling.md` | 错误场景和恢复 |
| `meta.ts`（已修改） | 在 manual 数组中注册 exam |

---

**总步骤数：** 10 个任务，30+ 个具体步骤
**预计时间：** 完整实现约 45-60 分钟
**依赖：** 无（纯 markdown 技能）
**复杂度：** 低 - 结构良好，遵循既定模式

---

## 实现后的操作

完成此计划后：

1. **测试安装：** `pnpx skills add jiangtao/skills`（如已发布）
2. **更新 README.md** 将 exam 包含在技能列表中
3. **创建示例输出** 显示生成的题目样例
4. **考虑增强：** 参考答案生成、难度自定义
