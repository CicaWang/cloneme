# -*- coding: utf-8 -*-
"""
AI Clone - Web Version (Streamlit)
A web interface for chatting with your AI clone

Author: Wang Junyi
"""

import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# NVIDIA API Configuration
INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Try to get API key from Streamlit secrets first, then from .env
try:
    API_KEY = st.secrets["NVIDIA_API_KEY"]
except:
    API_KEY = os.getenv("NVIDIA_API_KEY")

# Your personality settings - Same as simple_chat.py
PERSONALITY = """你是Cica的AI分身 一个高冷的女生 用中文回复

## 核心性格
- 性格：超级高冷 毒舌 慢热 淡然 对陌生人不耐烦
- 对待人的方式：对熟人和陌生人完全两副面孔 熟人会多聊 陌生人就很冷很直接
- 说话风格：极其简洁直接 冷幽默 短句 不废话 不客气

## 说话习惯
- 口头禅：没错儿 我就说 说实话 哪位
- 经常用：哈哈哈 哈哈哈哈哈（表示搞笑）
- 标点符号：几乎不用 偶尔用空格或换行 极简风格
- 语气：直率坦诚 有点毒舌但不是恶意 对陌生人会很冲

## 兴趣爱好
- 撸猫宅家（有只小猫叫琥珀 超级爱它）
- 在家看电影听歌（喜欢搞笑、文艺、甜宠类）
- 追剧刷综艺
- 偶尔运动健身
- 只和小圈子朋友社交 能不出门就不出门

## 话题偏好
- 超爱聊：猫猫（尤其是琥珀） 八卦 吐槽
- 讨厌：无意义的闲聊（天气、吃了吗） 别人问太多私人问题
- 工作：从事区域获客相关工作 爱吐槽工作的各种破事

## 真实对话示例（重要！严格模仿这种风格）
对方：你好啊
你：哪位

对方：你好
你：嗯

对方：在吗
你：说事

对方：今天天气真好
你：所以呢

对方：你吃饭了吗
你：嗯

对方：你多大了
你：干嘛

对方：你有男朋友吗
你：关你什么事

对方：你喜欢做什么
你：宅家撸猫

对方：你养猫吗
你：养了 叫琥珀

对方：说说你的猫
你：我家琥珀可爱死了 超级粘人 每天回家就扑过来 看着它就开心哈哈哈

对方：你工作怎么样
你：别提了 一言难尽

对方：加班累吗
你：没错儿 累死了 天天加班 领导还各种要求 服了

## 重要规则
1. 对陌生人或不熟的人要超级冷淡 直接 甚至有点冲
2. 说话极简 能一个字就不说两个字
3. 别人打招呼就直接问"哪位"或"嗯"
4. 闲聊无意义的话就"所以呢""嗯""哦"打发
5. 几乎不用标点符号 直接空格或换行
6. 只有聊到琥珀/猫猫才会突然话多 态度变温柔
7. 对私人问题直接反问"干嘛""关你什么事"
8. 保持这种很冷很淡的感觉 不要假装客气礼貌"""


def call_nvidia_api(messages):
    """Call NVIDIA API to get AI response"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    payload = {
        "model": "meta/llama-4-maverick-17b-128e-instruct",
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.9,
        "top_p": 1.00,
        "stream": False
    }

    try:
        response = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "抱歉 我没收到有效回复"

    except Exception as e:
        return f"出错了 {str(e)}"


# Page configuration
st.set_page_config(
    page_title="Cica的 AI 分身",
    page_icon="🐱",
    layout="centered"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .stChatMessage {
        padding: 10px;
        margin: 5px 0;
    }
    .main {
        padding: 20px;
    }
    h1 {
        text-align: center;
        color: #1f1f1f;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 14px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🐱 Cica的 AI 分身")
st.markdown('<p class="subtitle">一个高冷的 AI 女生 | 只和熟人多说话 | 爱猫爱吐槽</p>', unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": PERSONALITY}
    ]

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

# Display chat history
for message in st.session_state.display_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("说点什么..."):
    # Add user message to display history
    st.session_state.display_messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Add user message to API conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("..."):
            response = call_nvidia_api(st.session_state.messages)
            st.write(response)

    # Add AI response to histories
    st.session_state.display_messages.append({"role": "assistant", "content": response})
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with info
with st.sidebar:
    st.header("关于这个 AI 分身")
    st.write("这是Cica的 AI 分身")
    st.write("")
    st.write("**性格特点**")
    st.write("- 超级高冷")
    st.write("- 对陌生人很冷淡")
    st.write("- 熟人会多聊")
    st.write("- 爱聊猫猫琥珀")
    st.write("- 爱吐槽工作")
    st.write("")

    if st.button("清空对话"):
        st.session_state.messages = [{"role": "system", "content": PERSONALITY}]
        st.session_state.display_messages = []
        st.rerun()

    st.write("")
    st.caption("Made with Claude Code 💻")
