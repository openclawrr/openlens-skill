#!/usr/bin/env python3
"""
OpenLens - 多模态 AI 创作前端
===================================
作者: OpenLens Team
版本: 1.0.0
功能: 文生图、文生视频、图生视频、视频生视频

部署: Streamlit Cloud
后端: 连接 API 聚合服务

注意: 
- 用户必须输入自己的 API Key
- 所有 API Key 保存在 session_state 中，不会上传
- 18禁验证确保合规
"""

import streamlit as st
import requests
import json
import os
import time
from datetime import datetime

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="OpenLens - AI 多模态创作平台",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    /* 暗色主题 */
    .stApp {
        background: #0a0a0a;
        color: #e0e0e0;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input {
        background: #1a1a1a;
        border: 1px solid #333;
        color: #fff;
    }
    
    /* 文本域样式 */
    .stTextArea > div > div > textarea {
        background: #1a1a1a;
        border: 1px solid #333;
        color: #fff;
    }
    
    /* 按钮渐变 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
    }
    
    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 18禁弹窗样式 */
    .age-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.95);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    
    .age-box {
        background: #1a1a1a;
        border: 2px solid #667eea;
        border-radius: 20px;
        padding: 50px;
        max-width: 600px;
        text-align: center;
    }
    
    .age-title {
        font-size: 32px;
        font-weight: bold;
        color: #fff;
        margin-bottom: 30px;
    }
    
    .age-warning {
        color: #ef4444;
        font-size: 14px;
        padding: 15px;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 8px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Session State 初始化
# ============================================================

def init_session_state():
    """初始化所有 session state 变量"""
    
    # 18禁验证状态
    if 'age_verified' not in st.session_state:
        st.session_state.age_verified = False
    
    # ========== 全局配置 ==========
    if 'global_api_url' not in st.session_state:
        st.session_state.global_api_url = "https://api.openai.com/v1"
    
    # ========== 文本模型配置 (Prompt 优化) ==========
    if 'text_api_key' not in st.session_state:
        st.session_state.text_api_key = ""
    if 'text_model' not in st.session_state:
        st.session_state.text_model = "gpt-4o"
    
    # ========== 图像生成配置 (T2I) ==========
    if 't2i_api_key' not in st.session_state:
        st.session_state.t2i_api_key = ""
    if 't2i_model' not in st.session_state:
        st.session_state.t2i_model = "dall-e-3"
    
    # ========== 文生视频配置 (T2V) ==========
    if 't2v_api_key' not in st.session_state:
        st.session_state.t2v_api_key = ""
    if 't2v_model' not in st.session_state:
        st.session_state.t2v_model = "wan2.2"
    
    # ========== 图生视频配置 (I2V) ==========
    if 'i2v_api_key' not in st.session_state:
        st.session_state.i2v_api_key = ""
    if 'i2v_model' not in st.session_state:
        st.session_state.i2v_model = "wan2.2"
    
    # ========== 视频生视频配置 (V2V) ==========
    if 'v2v_api_key' not in st.session_state:
        st.session_state.v2v_api_key = ""
    if 'v2v_model' not in st.session_state:
        st.session_state.v2v_model = "wan2.2"
    
    # ========== 生成状态 ==========
    if 'generated_media' not in st.session_state:
        st.session_state.generated_media = None
    if 'final_prompt' not in st.session_state:
        st.session_state.final_prompt = ""
    if 'generation_mode' not in st.session_state:
        st.session_state.generation_mode = "文生图"

# ============================================================
# 18禁验证页面
# ============================================================

def show_age_verification():
    """显示 18禁验证界面"""
    
    st.markdown("""
    <div class="age-overlay">
        <div class="age-box">
            <div class="age-title">🎬 OpenLens</div>
            <div style="color: #ccc; font-size: 18px; line-height: 2;">
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
                ⚠️ 任何违法或有害内容生成均被严格禁止<br>
                平台运营方不对用户生成内容负责
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 按钮列
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("✅ 我已满18岁 - 进入", type="primary", use_container_width=True):
            st.session_state.age_verified = True
            st.rerun()
    
    with col2:
        if st.button("❌ 离开"):
            st.markdown("""
            <meta http-equiv="refresh" content="0;url=https://www.google.com">
            """, unsafe_allow_html=True)
    
    st.stop()

# ============================================================
# API 调用函数 (模拟/标准格式)
# ============================================================

def call_text_api(prompt: str, api_key: str, model: str, api_url: str) -> str:
    """
    调用文本模型 API (Prompt 优化)
    
    参数:
        prompt: 原始提示词
        api_key: API Key
        model: 模型名称
        api_url: API 基础 URL
    
    返回:
        优化后的提示词
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """你是一位专业的 AI 视频/图像导演。请将用户的原始描述改写为：
- 充满电影感
- 强调物理动态和光影细节
- 包含技术质量术语（高质量、细节、4K、电影感）
- 输出 ONLY 优化后的内容，不要有任何解释"""
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        # TODO: 在这里填入真实的 API 调用代码
        # resp = requests.post(f"{api_url}/chat/completions", headers=headers, json=payload, timeout=60)
        # data = resp.json()
        # return data["choices"][0]["message"]["content"]
        
        # 模拟返回
        time.sleep(1)  # 模拟 API 延迟
        return f"【优化后】{prompt} - 高品质电影感画面，柔和灯光，细节丰富，4K超清，流畅动画"
        
    except Exception as e:
        st.error(f"文本 API 调用失败: {str(e)}")
        return prompt


def call_t2i_api(prompt: str, api_key: str, model: str, api_url: str) -> dict:
    """
    调用文生图 API (T2I)
    
    参数:
        prompt: 提示词
        api_key: API Key
        model: 模型名称
        api_url: API 基础 URL
    
    返回:
        包含图片 URL 的字典
    """
    
    # TODO: 在这里填入真实的文生图 API 调用代码
    # headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # payload = {"model": model, "prompt": prompt, "n": 1, "size": "1024x1024"}
    # resp = requests.post(f"{api_url}/images/generations", headers=headers, json=payload)
    # data = resp.json()
    # return {"url": data["data"][0]["url"], "type": "image"}
    
    # 模拟返回
    time.sleep(2)
    return {
        "url": "https://via.placeholder.com/1024x1024/667eea/ffffff?text=AI+Generated+Image",
        "type": "image",
        "prompt": prompt
    }


def call_t2v_api(prompt: str, api_key: str, model: str, api_url: str, **kwargs) -> dict:
    """
    调用文生视频 API (T2V)
    
    参数:
        prompt: 提示词
        api_key: API Key
        model: 模型名称
        api_url: API 基础 URL
    
    返回:
        包含视频 URL 的字典
    """
    
    # TODO: 在这里填入真实的文生视频 API 调用代码
    # headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # payload = {"model": model, "prompt": prompt, "duration": 5}
    # resp = requests.post(f"{api_url}/video/generations", headers=headers, json=payload)
    # task_id = resp.json()["task_id"]
    # # 轮询等待生成完成...
    # return {"url": video_url, "type": "video", "task_id": task_id}
    
    # 模拟返回
    time.sleep(3)
    return {
        "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "type": "video",
        "prompt": prompt
    }


def call_i2v_api(prompt: str, image_data: str, api_key: str, model: str, api_url: str) -> dict:
    """
    调用图生视频 API (I2V)
    
    参数:
        prompt: 提示词
        image_data: 图片 URL 或 base64
        api_key: API Key
        model: 模型名称
        api_url: API 基础 URL
    
    返回:
        包含视频 URL 的字典
    """
    
    # TODO: 在这里填入真实的图生视频 API 调用代码
    
    time.sleep(3)
    return {
        "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "type": "video",
        "prompt": prompt
    }


def call_v2v_api(prompt: str, video_data: str, api_key: str, model: str, api_url: str) -> dict:
    """
    调用视频生视频 API (V2V)
    
    参数:
        prompt: 提示词
        video_data: 视频 URL 或 base64
        api_key: API Key
        model: 模型名称
        api_url: API 基础 URL
    
    返回:
        包含视频 URL 的字典
    """
    
    # TODO: 在这里填入真实的视频生视频 API 调用代码
    
    time.sleep(4)
    return {
        "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "type": "video",
        "prompt": prompt
    }

# ============================================================
# 主界面
# ============================================================

def main():
    """主界面"""
    
    # 初始化 session state
    init_session_state()
    
    # 页面标题
    st.markdown('<p class="main-title">🎬 OpenLens</p>', unsafe_allow_html=True)
    st.markdown("### 多模态 AI 创作平台 | 文生图 · 文生视频 · 图生视频 · 视频生视频")
    st.markdown("---")
    
    # ============================================================
    # 左右分栏布局
    # ============================================================
    col_config, col_create = st.columns([1, 2])
    
    # ============================================================
    # 左列: 配置区
    # ============================================================
    with col_config:
        st.header("⚙️ 配置区")
        
        # 全局配置
        with st.expander("🌐 全局配置", expanded=True):
            st.session_state.global_api_url = st.text_input(
                "Global API Base URL",
                value=st.session_state.global_api_url,
                placeholder="https://api.openai.com/v1"
            )
        
        # 文本模型配置 (Prompt 优化)
        with st.expander("✏️ 文本模型 (Prompt 优化)"):
            st.session_state.text_api_key = st.text_input(
                "Text API Key",
                value=st.session_state.text_api_key,
                type="password",
                placeholder="sk-..."
            )
            st.session_state.text_model = st.text_input(
                "Text Model Name",
                value=st.session_state.text_model,
                placeholder="gpt-4o, claude-3, etc."
            )
        
        # 图像生成配置 (T2I)
        with st.expander("🖼️ 图像生成 (T2I)"):
            st.session_state.t2i_api_key = st.text_input(
                "T2I API Key",
                value=st.session_state.t2i_api_key,
                type="password",
                placeholder="sk-..."
            )
            st.session_state.t2i_model = st.text_input(
                "T2I Model Name",
                value=st.session_state.t2i_model,
                placeholder="dall-e-3, midjourney, etc."
            )
        
        # 文生视频配置 (T2V)
        with st.expander("🎬 文生视频 (T2V)"):
            st.session_state.t2v_api_key = st.text_input(
                "T2V API Key",
                value=st.session_state.t2v_api_key,
                type="password",
                placeholder="sk-..."
            )
            st.session_state.t2v_model = st.text_input(
                "T2V Model Name",
                value=st.session_state.t2v_model,
                placeholder="wan2.2, seedance1.5, kling, etc."
            )
        
        # 图生视频配置 (I2V)
        with st.expander("📸 图生视频 (I2V)"):
            st.session_state.i2v_api_key = st.text_input(
                "I2V API Key",
                value=st.session_state.i2v_api_key,
                type="password",
                placeholder="sk-..."
            )
            st.session_state.i2v_model = st.text_input(
                "I2V Model Name",
                value=st.session_state.i2v_model,
                placeholder="wan2.2, anyvideo, etc."
            )
        
        # 视频生视频配置 (V2V)
        with st.expander("🎥 视频生视频 (V2V)"):
            st.session_state.v2v_api_key = st.text_input(
                "V2V API Key",
                value=st.session_state.v2v_api_key,
                type="password",
                placeholder="sk-..."
            )
            st.session_state.v2v_model = st.text_input(
                "V2V Model Name",
                value=st.session_state.v2v_model,
                placeholder="wan2.2, etc."
            )
        
        # 保存配置按钮
        st.markdown("---")
        if st.button("💾 保存配置", use_container_width=True):
            st.success("✅ 配置已保存到本地 session")
    
    # ============================================================
    # 右列: 创作区
    # ============================================================
    with col_create:
        st.header("🎨 创作区")
        
        # 模式选择
        st.subheader("1. 选择创作模式")
        mode = st.radio(
            "模式",
            ["文生图", "文生视频", "图生视频", "视频生视频"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.generation_mode = mode
        
        # 基础输入
        st.subheader("2. 输入提示词")
        prompt = st.text_area(
            "描述你想要生成的内容",
            height=120,
            placeholder="例如：一只猫咪在阳光下懒洋洋地睡觉..."
        )
        
        # Prompt 优化选项
        use_optimize = st.checkbox("✨ 使用 AI 优化提示词")
        
        # 动态媒体输入
        media_input = None
        media_url = ""
        
        st.subheader("3. 媒体输入")
        
        if mode == "图生视频":
            # 图片上传或 URL
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                uploaded_image = st.file_uploader(
                    "上传图片",
                    type=['jpg', 'jpeg', 'png', 'webp']
                )
            with col_img2:
                media_url = st.text_input(
                    "或图片 URL",
                    placeholder="https://example.com/image.jpg"
                )
            
            if uploaded_image:
                import base64
                media_input = base64.b64encode(uploaded_image.read()).decode()
        
        elif mode == "视频生视频":
            # 视频上传或 URL
            col_vid1, col_vid2 = st.columns(2)
            with col_vid1:
                uploaded_video = st.file_uploader(
                    "上传视频",
                    type=['mp4', 'mov', 'avi']
                )
            with col_vid2:
                media_url = st.text_input(
                    "或视频 URL",
                    placeholder="https://example.com/video.mp4"
                )
            
            if uploaded_video:
                import base64
                media_input = base64.b64encode(uploaded_video.read()).decode()
        
        # ============================================================
        # 生成按钮与校验
        # ============================================================
        st.markdown("---")
        
        if st.button("🚀 开始生成", type="primary", use_container_width=True):
            # 基础校验
            if not prompt:
                st.error("❌ 请输入提示词")
                st.stop()
            
            final_prompt = prompt
            
            # Prompt 优化校验
            if use_optimize:
                if not st.session_state.text_api_key or not st.session_state.text_model:
                    st.error("❌ 请在左侧配置区填写【文本模型 API Key】和【Model Name】")
                    st.stop()
                
                with st.spinner("✨ 正在优化提示词..."):
                    final_prompt = call_text_api(
                        prompt=prompt,
                        api_key=st.session_state.text_api_key,
                        model=st.session_state.text_model,
                        api_url=st.session_state.global_api_url
                    )
                
                st.success("✅ 提示词优化完成!")
                st.info(f"优化后: {final_prompt}")
            
            # 模式特定校验
            if mode == "文生图":
                if not st.session_state.t2i_api_key or not st.session_state.t2i_model:
                    st.error("❌ 请在左侧配置区填写【T2I API Key】和【T2I Model Name】")
                    st.stop()
            
            elif mode == "文生视频":
                if not st.session_state.t2v_api_key or not st.session_state.t2v_model:
                    st.error("❌ 请在左侧配置区填写【T2V API Key】和【T2V Model Name】")
                    st.stop()
            
            elif mode == "图生视频":
                if not st.session_state.i2v_api_key or not st.session_state.i2v_model:
                    st.error("❌ 请在左侧配置区填写【I2V API Key】和【I2V Model Name】")
                    st.stop()
                if not media_input and not media_url:
                    st.error("❌ 请上传图片或输入图片 URL")
                    st.stop()
            
            elif mode == "视频生视频":
                if not st.session_state.v2v_api_key or not st.session_state.v2v_model:
                    st.error("❌ 请在左侧配置区填写【V2V API Key】和【V2V Model Name】")
                    st.stop()
                if not media_input and not media_url:
                    st.error("❌ 请上传视频或输入视频 URL")
                    st.stop()
            
            # 执行生成
            with st.spinner("🎬 正在生成，请稍候..."):
                result = None
                
                if mode == "文生图":
                    result = call_t2i_api(
                        prompt=final_prompt,
                        api_key=st.session_state.t2i_api_key,
                        model=st.session_state.t2i_model,
                        api_url=st.session_state.global_api_url
                    )
                
                elif mode == "文生视频":
                    result = call_t2v_api(
                        prompt=final_prompt,
                        api_key=st.session_state.t2v_api_key,
                        model=st.session_state.t2v_model,
                        api_url=st.session_state.global_api_url
                    )
                
                elif mode == "图生视频":
                    result = call_i2v_api(
                        prompt=final_prompt,
                        image_data=media_input or media_url,
                        api_key=st.session_state.i2v_api_key,
                        model=st.session_state.i2v_model,
                        api_url=st.session_state.global_api_url
                    )
                
                elif mode == "视频生视频":
                    result = call_v2v_api(
                        prompt=final_prompt,
                        video_data=media_input or media_url,
                        api_key=st.session_state.v2v_api_key,
                        model=st.session_state.v2v_model,
                        api_url=st.session_state.global_api_url
                    )
                
                # 保存结果
                st.session_state.generated_media = result
                st.session_state.final_prompt = final_prompt
            
            # ============================================================
            # 结果展示
            # ============================================================
            st.markdown("---")
            st.subheader("🎉 生成结果")
            
            if result:
                if result["type"] == "image":
                    st.image(result["url"], caption="生成的图片")
                elif result["type"] == "video":
                    st.video(result["url"])
                
                # 下载按钮
                col_dl1, col_dl2 = st.columns(2)
                
                with col_dl1:
                    # 下载提示词
                    prompt_json = json.dumps({
                        "prompt": result.get("prompt", final_prompt),
                        "mode": mode,
                        "model": st.session_state.get(f"{mode.lower().replace(' ', '')}_model", "unknown"),
                        "timestamp": datetime.now().isoformat()
                    }, ensure_ascii=False, indent=2)
                    
                    st.download_button(
                        label="📥 下载提示词 (JSON)",
                        data=prompt_json,
                        file_name="openlens_prompt.json",
                        mime="application/json"
                    )
                
                with col_dl2:
                    st.info(f"📝 使用模型: {result.get('model', 'N/A')}")
    
    # ============================================================
    # 页脚
    # ============================================================
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        <p>🎬 OpenLens | 多模态 AI 创作平台</p>
        <p><strong>⚠️ 免责声明：</strong>本工具仅作为透明网关，不存储任何 API Key 或生成的内容。请合规使用。</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    # 初始化 session state
    init_session_state()
    
    # 18禁验证
    if not st.session_state.age_verified:
        show_age_verification()
    else:
        main()
