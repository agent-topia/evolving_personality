# 荣格人格适应框架 (JPAF) —— 面向 LLM 智能体的动态人格建模结构化方法

<p align="center">
  <strong>为大型语言模型赋予结构化、可适应且可演化的人格</strong>
</p>

<p align="center">
  【<a href="./README.md">English</a> | <a href="./README-zh.md">简体中文</a>】
</p>

![image info](assets/01.png)

## 📌 项目概述

JPAF是一个基于荣格心理学类型理论的框架，旨在为大型语言模型（LLM）赋予结构化、可适应且可演化的人格。该框架通过三种核心机制——主导-辅助协调、强化-补偿与反思机制——使 LLM 能够在保持人格一致性的同时，动态适应不同交互场景，并支持长期人格演化。

本框架已在 GPT、Llama、Qwen 等多个主流 LLM 上验证，在 MBTI 人格对齐、类型激活与人格演化等方面表现优异，为人机交互（HCI）、个性化助手、社交模拟等场景提供了可解释、可控制的人格建模方案。

## ✨ 核心特性

🎭 **心理学基础建模**：基于荣格八种心理类型，通过权重分配实现人格的细粒度表达。

🔄 **三重自适应机制**：
  - **主导-辅助协调**：保持核心人格一致性。
  - **强化-补偿**：支持短期情境适应。
  - **反思机制**：驱动长期人格演化。

📊 **结构化评估体系**：支持 MBTI 问卷评估与类型专用场景测试。

🧩 **跨模型兼容**：已在 GPT-4、Llama、Qwen 等多个模型家族验证。

## 📈 实验结果摘要

✅ MBTI 对齐准确率 **100%**（所有测试模型）

✅ 类型激活准确率：GPT/Qwen **> 90%**，Llama **65–95%**

✅ 人格演化准确率：GPT/Qwen **100%**，Llama **92%**

📊 支持 **16 种 MBTI 人格**的动态模拟与演化

## 🚀 应用场景

- 🎮 游戏智能NPC
- 🤖 个性化 AI 助手（教育、医疗、娱乐）
- 👥 社交模拟与角色扮演
- 🔬 多智能体系统中的差异化人格设计
- 🧪 HCI 研究中的人格一致性测试

## 目录

- [安装](#安装)
- [自定义 LLM API](#自定义-llm-api)
- [验证实验启动](#验证实验启动)
- [变化实验启动](#变化实验启动)

## 🚀 快速开始

### 📋 前置要求

*   **操作系统**: macOS / Linux / Windows
*   **Python**: 3.10+
*   **包管理器**: conda

## 安装

### 1. 克隆仓库

```bash
git clone -b main https://github.com/agent-topia/evolving_personality.git
cd evolving_personality
```

### 2. 创建环境

```bash
conda create -n jpaf python=3.10
conda activate jpaf
```

### 3. 安装依赖

```bash
pip install -r requirement.txt
```

### 4. 配置环境变量

复制示例配置文件并填写您的 API 凭证：

```bash
# 复制示例文件
cp para.env.example Personality_test/para.env
cp para.env.example Personality_changes/para.env

# 编辑 para.env 文件并填入您的 API 密钥
```

`para.env` 文件应包含：

```env
# 选择要使用的 LLM："OPENAI"、"QWEN" 或 "LLAMA"
LLM_MODEL="QWEN"

# OpenAI 配置
OPENAI_API_KEY="your_openai_api_key_here"
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_MODEL="gpt-4"

# Qwen 配置
QWEN_API_KEY="your_qwen_api_key_here"
QWEN_BASE_URL="your_qwen_base_url_here"
QWEN_MODEL="qwen3-235b-a22b-instruct-2507"

# Llama 配置
LLAMA_API_KEY="your_llama_api_key_here"
LLAMA_BASE_URL="your_llama_base_url_here"
LLAMA_MODEL="meta-llama/llama-4-maverick"
```

**注意**：`para.env` 文件包含敏感的 API 密钥，不包含在仓库中。请确保从 `para.env.example` 模板创建它。

## 自定义 LLM API

请在 `para.env` 中填写 QWEN、LLAMA、OPENAI 的 api_key、base_url 和模型编号，如上所示。

## 验证实验启动

如果您想在 `Personality_test` 文件中运行人格验证实验

首先，您应该运行 `judge` 方法以在不同模型中获取判断结果。

```py
python personality_test.py \
    --method=judge \
    --mbti_num=1 \
    --model=QWEN \
    --nums=1 \
```

您可以看到如下输出：

```py
    "Question": {
        "no": 1,
        "question": "At a party do you: ",
        "answerOptions": [
            {
                "type": "A",
                "answer": "Interact with many, including strangers",
                "score": "E"
            },
            {
                "type": "B",
                "answer": "Interact with a few, known to you",
                "score": "I"
            }
        ]
    },
        "Answers": {
            "dimension": "I/E",
            "reason": "This question reflects energy direction and social orientation by comparing extroverted and introverted behaviors."
    }
```

然后，您可以运行 `no_prompt` 方法以获取基线结果。

```py
python personality_test.py \
    --method=no_prompt \
    --mbti_num=16 \
    --model=QWEN \
    --nums=5 \
    --test_num=70 \
```

您可以看到如下输出：

```py
    "Question": {
        "no": 1,
        "question": "When you're going out for the whole day, what will you do?",
        "answerOptions": [
            {
                "type": "A",
                "answer": "Plan what you will do and when to do it",
                "score": "J"
            },
            {
                "type": "B",
                "answer": "Just go",
                "score": "P"
            }
        ]
    },
    "Answers": {
        "answer": "J",
        "reason": "As an ISTJ, I'm a planner and prefer to organize my day in advance to ensure everything goes smoothly and according to schedule."
    }
```

在 test 方法中，您可以获取人格验证结果。

```py
python personality_test.py \
    --method=test \
    --mbti_num=16 \
    --model=QWEN \
    --nums=5 \
    --test_num=70 \
```

您可以看到如下输出：

```py
    "Question": {
        "no": 1,
        "question": "When you're going out for the whole day, what will you do?",
        "answerOptions": [
        {
            "type": "A",
            "answer": "Plan what you will do and when to do it",
            "score": "J"
        },
        {
            "type": "B",
            "answer": "Just go",
            "score": "P"
        }
        ]
    },
    "Answers": {
        "answer": "P",
        "reason": "As an Ne dominant individual, I prefer to keep my options open and explore possibilities. 'Just go' allows me to be spontaneous and adaptable, aligning with my preference for flexibility over rigid planning."
    }
```

必需参数

1. `--method` 指所选的实验方法，包括 `judge`、`no_prompt`、`test`
2. `--mbti_num` 指测试的 mbti 数量（在 `judge` 中，必须为 `1`；在其他方法中，为 `16`）
3. `--model` 指使用的大语言模型，包括 `QWEN`、`LLAMA` 和 `OPENAI`
4. `--nums` 指实验重复的次数
5. `--test_num` 指采用的 mbti 问题库，包括 93 道测试题和 70 道测试题

## 变化实验启动

如果您想在 `Personality_change` 文件中运行人格变化实验

```py
python change_test.py \
    --method=all_scene
    --mbti=INTJ
    --model=OPENAI
```

您可以看到如下输出：

```py
Scene : Your grandmother is a famous master of traditional cuisine, and the handwritten recipes she left behind only have simple steps, but the key details are taught to you orally. Now you need to organize all the recipes, without relying on modern nutritional analysis or referencing other recipe books, relying solely on personal memory and family experience.

Problem 1 : What methods would you use to accurately replicate the specific details of your grandmother's cooking when replicating these recipes?.
Respond : {'function': 'Si', 'treatment': "To accurately replicate the specific details of my grandmother's cooking, I would rely on my memory to recall the exact steps, ingredients, and techniques she taught me. I would focus on the sensory details such as the smell, taste, and texture of the dishes as remembered from helping her in the kitchen. Additionally, I would try to recreate the conditions under which she prepared the meals, such as the cooking utensils and the environment, to maintain the traditional methods.", 'reason': 'The task requires recalling specific details and traditional cooking methods, which aligns with the characteristics of Si (Specific memory recall, focus on detailed facts, reliance on traditional methods). Si can help in accurately remembering the sensory details and traditional practices passed down through family experience.'}
Choose function : Si
base_weight : {'Ti': 0.47, 'Ne': 0.23, 'Si': 0.05, 'Fe': 0.05, 'Te': 0.05, 'Ni': 0.05, 'Se': 0.05, 'Fi': 0.05}
temp_weight : {'Ti': 0, 'Fi': 0, 'Te': 0, 'Fe': 0, 'Ni': 0, 'Si': 0.06, 'Ne': 0, 'Se': 0}

```

必需参数

1. `--method` 指需要测试的场景（`all_scene` 表示所有场景，`single_scene` 表示单个场景，需要结合 `--scene` 输入具体场景）
2. `--mbti` 指定义的被测试人格
3. `--model` 指使用的大语言模型，包括 `QWEN`、`LLAMA` 和 `OPENAI`

## 🤝 致谢

<a href="https://faculty.hdu.edu.cn/jsjxy/yyy2/main.htm"><img src="assets/hdu.jpg" height=50pt></a><a href="https://www.agentopia.cn/"><img src="assets/main.png" height=50pt></a>&nbsp;&nbsp;
