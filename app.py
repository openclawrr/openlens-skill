#!/usr/bin/env python3
"""
OpenLens - 多模态 AI 创作前端
===================================
作者: OpenLens Team
版本: 1.0.2
功能: 文生图、文生视频、图生视频、视频生视频
部署: Streamlit Cloud
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime

# ============================================================
# 第 1 步：Session State 初始化（必须在最前面）
# ============================================================
if 'age_verified' not in st.session_state:
    st.session_state.age_verified = False

# ============================================================
# 第 2 步：18禁拦截逻辑（必须在渲染任何内容之前）
# ============================================================
if not st.session_state.age_verified:
    # 页面配置
    st.set_page_config(
        page_title="OpenLens - 年龄验证",
        page_icon="🎬",
        layout="centered"
    )
    
    # CSS 样式
    st.markdown("""
    <style>
    .stApp { background: #0a0a0a; }
    .age-box {
        background: #1a1a1a;
        border: 2px solid #667eea;
        border-radius: 20px;
        padding: 50px;
        max-width: 600px;
        margin: 100px auto;
        text-align: center;
    }
    .age-title {
        font-size: 36px;
        font-weight: bold;
        color: #fff;
        margin-bottom: 30px;
    }
    .age-text { color: #ccc; font-size: 16px; line-height: 2; }
    .age-warning { color: #ef4444; font-size: 14px; padding: 15px; background: rgba(239,68,68,0.1); border-radius: 8px; margin-top: 20px; }
    .stButton > button { width: 100%; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)
    
    # 18禁弹窗 HTML
    st.markdown("""
    <div class="age-box">
        <div class="age-title">🎬 OpenLens</div>
        <div class="age-text">
            <strong>年龄验证 Required</strong><br><br>
            本平台支持多模态 AI 创作功能。<br>
            请确认以下条件：
        </div>
        <div style="color: #fff; margin: 30px 0; text-align: left; padding: 0 50px;">
            ✅ 我已年满 <strong>18 岁</strong><br>
            ✅ 我将 <strong>合法合规</strong> 使用本平台<br>
            ✅ 我确认对生成内容 <strong>承担全部责任</strong>
        </div>
        <div class="age-warning">
            ⚠️ 任何违法或有害内容生成均被严格禁止
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按钮列 - 使用 key 确保状态正确
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("✅ 我已满18岁 - 进入", type="primary", key="age_confirm_btn"):
            st.session_state.age_verified = True
            st.rerun()
    
    with col2:
        if st.button("❌ 离开", key="age_exit_btn"):
            # 使用 JavaScript 跳转
            st.markdown("""
            <script>
            window.parent.location.href = "https://www.google.com";
            </script>
            """, unsafe_allow_html=True)
            st.warning("正在跳转...")
    
    # 第 5 步：阻断后续执行
    st.stop()

# ============================================================
# 验证通过后的配置
# ============================================================
st.set_page_config(
    page_title="OpenLens - AI 多模态创作平台",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 其他 Session State 初始化
# ============================================================
if 'global_api_url' not in st.session_state:
    st.session_state.global_api_url = "https://api.openai.com/v1"
if 'text_api_key' not in st.session_state:
    st.session_state.text_api_key = ""
if 'text_model' not in st.session_state:
    st.session_state.text_model = "gpt-4o"
if 't2i_api_key' not in st.session_state:
    st.session_state.t2i_api_key = ""
if 't2i_model' not in st.session_state:
    st.session_state.t2i_model = "dall-e-3"
if 't2v_api_key' not in st.session_state:
    st.session_state.t2v_api_key = ""
if 't2v_model' not in st.session_state:
    st.session_state.t2v_model = "wan2.2"
if 'i2v_api_key' not in st.session_state:
    st.session_state.i2v_api_key = ""
if 'i2v_model' not in st.session_state:
    st.session_state.i2v_model = "wan2.2"
if 'v2v_api_key' not in st.session_state:
    st.session_state.v2v_api_key = ""
if 'v2v_model' not in st.session_state:
    st.session_state.v2v_model = "wan2.2"
if 'generated_media' not in st.session_state:
    st.session_state.generated_media = None
if 'final_prompt' not in st.session_state:
    st.session_state.final_prompt = ""
if 'generation_mode' not in st.session_state:
    st.session_state.generation_mode = "文生图"

# ============================================================
# CSS 样式
# ============================================================
st.markdown("""
<style>
.stApp { background: #0a0a0a; color: #e0e0e0; }
.stTextInput > div > div > input { background: #1a1a1a; border: 1px solid #333; color: #fff; }
.stTextArea > div > div > textarea { background: #1a1a1a; border: 1px solid #333; color: #fff; }
.stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; color: white; font-weight: 600; }
.main-title { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# API 调用函数
# ============================================================

def call_text_api(prompt, api_key, model, api_url):
    """文本模型 API (Prompt 优化)"""
    # TODO: 填入真实 API 调用代码
    time.sleep(1)
    return f"【优化后】{prompt} - 高品质电影感画面，柔和灯光，细节丰富，4K超清"

def call_t2i_api(prompt, api_key, model, api_url):
    """文生图 API"""
    # TODO: 填入真实 API 调用代码
    time.sleep(2)
    return {"url": "https://via.placeholder.com/1024x1024/667eea/ffffff?text=AI+Image", "type": "image", "prompt": prompt}

def call_t2v_api(prompt, api_key, model, api_url, **kwargs):
    """文生视频 API"""
    # TODO: 填入真实 API 调用代码
    time.sleep(3)
    return {"url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "type": "video", "prompt": prompt}

def call_i2v_api(prompt, image_data, api_key, model, api_url):
    """图生视频 API"""
    # TODO: 填入真实 API 调用代码
    time.sleep(3)
    return {"url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "type": "video", "prompt": prompt}

def call_v2v_api(prompt, video_data, api_key, model, api_url):
    """视频生视频 API"""
    # TODO: 填入真实 API 调用代码
    time.sleep(4)
    return {"url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "type": "video", "prompt": prompt}

# ============================================================
# 第 6 步：主界面（验证通过后才执行）
# ============================================================

st.markdown('<p class="main-title">🎬 OpenLens</p>', unsafe_allow_html=True)
st.markdown("### 多模态 AI 创作平台 | 文生图 · 文生视频 · 图生视频 · 视频生视频")
st.markdown("---")

# 左右分栏
col_config, col_create = st.columns([1, 2])

# 配置区
with col_config:
    st.header("⚙️ 配置区")
    
    with st.expander("🌐 全局配置", expanded=True):
        st.session_state.global_api_url = st.text_input("Global API Base URL", value=st.session_state.global_api_url, placeholder="https://api.openai.com/v1")
    
    with st.expander("✏️ 文本模型 (Prompt 优化)"):
        st.session_state.text_api_key = st.text_input("Text API Key", value=st.session_state.text_api_key, type="password", placeholder="sk-...")
        st.session_state.text_model = st.text_input("Text Model Name", value=st.session_state.text_model, placeholder="gpt-4o")
    
    with st.expander("🖼️ 图像生成 (T2I)"):
        st.session_state.t2i_api_key = st.text_input("T2I API Key", value=st.session_state.t2i_api_key, type="password", placeholder="sk-...")
        st.session_state.t2i_model = st.text_input("T2I Model Name", value=st.session_state.t2i_model, placeholder="dall-e-3")
    
    with st.expander("🎬 文生视频 (T2V)"):
        st.session_state.t2v_api_key = st.text_input("T2V API Key", value=st.session_state.t2v_api_key, type="password", placeholder="sk-...")
        st.session_state.t2v_model = st.text_input("T2V Model Name", value=st.session_state.t2v_model, placeholder="wan2.2")
    
    with st.expander("📸 图生视频 (I2V)"):
        st.session_state.i2v_api_key = st.text_input("I2V API Key", value=st.session_state.i2v_api_key, type="password", placeholder="sk-...")
        st.session_state.i2v_model = st.text_input("I2V Model Name", value=st.session_state.i2v_model, placeholder="wan2.2")
    
    with st.expander("🎥 视频生视频 (V2V)"):
        st.session_state.v2v_api_key = st.text_input("V2V API Key", value=st.session_state.v2v_api_key, type="password", placeholder="sk-...")
        st.session_state.v2v_model = st.text_input("V2V Model Name", value=st.session_state.v2v_model, placeholder="wan2.2")
    
    if st.button("💾 保存配置", use_container_width=True):
        st.success("✅ 配置已保存")

# 创作区
with col_create:
    st.header("🎨 创作区")
    
    # 模式选择
    st.subheader("1. 选择创作模式")
    mode = st.radio("模式", ["文生图", "文生视频", "图生视频", "视频生视频"], horizontal=True, label_visibility="collapsed")
    st.session_state.generation_mode = mode
    
    # 提示词
    st.subheader("2. 输入提示词")
    prompt = st.text_area("描述你想要生成的内容", height=120, placeholder="例如：一只猫咪在阳光下懒洋洋地睡觉...")
    
    # Prompt 优化
    use_optimize = st.checkbox("✨ 使用 AI 优化提示词")
    
    # 动态媒体输入
    media_input = None
    media_url = ""
    
    st.subheader("3. 媒体输入")
    
    if mode == "图生视频":
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            uploaded_image = st.file_uploader("上传图片", type=['jpg', 'jpeg', 'png', 'webp'])
        with col_img2:
            media_url = st.text_input("或图片 URL", placeholder="https://example.com/image.jpg")
        if uploaded_image:
            import base64
            media_input = base64.b64encode(uploaded_image.read()).decode()
    
    elif mode == "视频生视频":
        col_vid1, col_vid2 = st.columns(2)
        with col_vid1:
            uploaded_video = st.file_uploader("上传视频", type=['mp4', 'mov', 'avi'])
        with col_vid2:
            media_url = st.text_input("或视频 URL", placeholder="https://example.com/video.mp4")
        if uploaded_video:
            import base64
            media_input = base64.b64encode(uploaded_video.read()).decode()
    
    # 生成按钮
    st.markdown("---")
    
    if st.button("🚀 开始生成", type="primary", use_container_width=True):
        # 基础校验
        if not prompt:
            st.error("❌ 请输入提示词")
            st.stop()
        
        final_prompt = prompt
        
        # Prompt 优化
        if use_optimize:
            if not st.session_state.text_api_key or not st.session_state.text_model:
                st.error("❌ 请填写【文本模型 API Key】和【Model Name】")
                st.stop()
            
            with st.spinner("✨ 正在优化提示词..."):
                final_prompt = call_text_api(prompt, st.session_state.text_api_key, st.session_state.text_model, st.session_state.global_api_url)
            
            st.success("✅ 优化完成!")
            st.info(f"优化后: {final_prompt}")
        
        # 模式校验
        if mode == "文生图" and (not st.session_state.t2i_api_key or not st.session_state.t2i_model):
            st.error("❌ 请填写【T2I API Key】和【T2I Model Name】")
            st.stop()
        elif mode == "文生视频" and (not st.session_state.t2v_api_key or not st.session_state.t2v_model):
            st.error("❌ 请填写【T2V API Key】和【T2V Model Name】")
            st.stop()
        elif mode == "图生视频" and (not st.session_state.i2v_api_key or not st.session_state.i2v_model):
            st.error("❌ 请填写【I2V API Key】和【I2V Model Name】")
            st.stop()
        elif mode == "图生视频" and not media_input and not media_url:
            st.error("❌ 请上传图片或输入图片 URL")
            st.stop()
        elif mode == "视频生视频" and (not st.session_state.v2v_api_key or not st.session_state.v2v_model):
            st.error("❌ 请填写【V2V API Key】和【V2V Model Name】")
            st.stop()
        elif mode == "视频生视频" and not media_input and not media_url:
            st.error("❌ 请上传视频或输入视频 URL")
            st.stop()
        
        # 生成
        with st.spinner("🎬 正在生成..."):
            result = None
            if mode == "文生图":
                result = call_t2i_api(final_prompt, st.session_state.t2i_api_key, st.session_state.t2i_model, st.session_state.global_api_url)
            elif mode == "文生视频":
                result = call_t2v_api(final_prompt, st.session_state.t2v_api_key, st.session_state.t2v_model, st.session_state.global_api_url)
            elif mode == "图生视频":
                result = call_i2v_api(final_prompt, media_input or media_url, st.session_state.i2v_api_key, st.session_state.i2v_model, st.session_state.global_api_url)
            elif mode == "视频生视频":
                result = call_v2v_api(final_prompt, media_input or media_url, st.session_state.v2v_api_key, st.session_state.v2v_model, st.session_state.global_api_url)
        
        # 结果展示
        st.markdown("---")
        st.subheader("🎉 生成结果")
        
        if result:
            if result["type"] == "image":
                st.image(result["url"], caption="生成的图片")
            elif result["type"] == "video":
                st.video(result["url"])
            
            # 下载
            prompt_json = json.dumps({"prompt": result.get("prompt", final_prompt), "mode": mode, "timestamp": datetime.now().isoformat()}, ensure_ascii=False, indent=2)
            st.download_button("📥 下载提示词 (JSON)", prompt_json, "openlens_prompt.json", "application/json")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>🎬 OpenLens | 多模态 AI 创作平台</p>
    <p><strong>⚠️ 免责声明：</strong>本工具仅作为透明网关，不存储任何 API Key。</p>
</div>
""", unsafe_allow_html=True)
