#!/usr/bin/env python3
"""
OpenLens - Multi-Modal AI Creation Platform
============================================
Version: 1.0.4
Features: Text-to-Image, Text-to-Video, Image-to-Video, Video-to-Video
Deploy: Streamlit Cloud | OpenClaw Skill

i18n Support: English, 简体中文, 日本語
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime

# ============================================================
# Step 1: Translation Dictionary (i18n)
# ============================================================
TRANSLATIONS = {
    "en": {
        # Age Verification
        "age_title": "OpenLens",
        "age_subtitle": "Age Verification Required",
        "age_description": "This platform provides multi-modal AI generation services. By proceeding, you confirm:",
        "age_check_1": "I am 18 years or older",
        "age_check_2": "I will use this platform legally",
        "age_check_3": "I accept full responsibility for generated content",
        "age_warning": "Any illegal or harmful content generation is strictly prohibited",
        "age_enter": "I am 18+ - Enter",
        "age_exit": "Exit",
        "age_redirecting": "Redirecting...",
        
        # Main UI
        "main_title": "OpenLens",
        "main_subtitle": "Multi-Modal AI Creation Platform | T2I · T2V · I2V · V2V",
        
        # Configuration Panel
        "config_title": "⚙️ Configuration",
        "global_settings": "🌐 Global Settings",
        "global_api_url": "Global API Base URL",
        "global_api_url_placeholder": "https://api.openai.com/v1",
        
        "text_model": "✏️ Text Model (Prompt Optimization)",
        "text_api_key": "Text API Key",
        "text_api_key_placeholder": "sk-...",
        "text_model_name": "Text Model Name",
        "text_model_placeholder": "gpt-4o, claude-3, etc.",
        
        "t2i_model": "🖼️ Image Generation (T2I)",
        "t2i_api_key": "T2I API Key",
        "t2i_api_key_placeholder": "sk-...",
        "t2i_model_name": "T2I Model Name",
        "t2i_model_placeholder": "dall-e-3, midjourney, etc.",
        
        "t2v_model": "🎬 Text-to-Video (T2V)",
        "t2v_api_key": "T2V API Key",
        "t2v_api_key_placeholder": "sk-...",
        "t2v_model_name": "T2V Model Name",
        "t2v_model_placeholder": "wan2.2, seedance1.5, kling, etc.",
        
        "i2v_model": "📸 Image-to-Video (I2V)",
        "i2v_api_key": "I2V API Key",
        "i2v_api_key_placeholder": "sk-...",
        "i2v_model_name": "I2V Model Name",
        "i2v_model_placeholder": "wan2.2, anyvideo, etc.",
        
        "v2v_model": "🎥 Video-to-Video (V2V)",
        "v2v_api_key": "V2V API Key",
        "v2v_api_key_placeholder": "sk-...",
        "v2v_model_name": "V2V Model Name",
        "v2v_model_placeholder": "wan2.2, etc.",
        
        "save_config": "💾 Save Configuration",
        "save_config_success": "✅ Configuration saved to session",
        
        # Creation Panel
        "create_title": "🎨 Creation",
        "step_1": "1. Select Mode",
        "mode_t2i": "Text-to-Image",
        "mode_t2v": "Text-to-Video",
        "mode_i2v": "Image-to-Video",
        "mode_v2v": "Video-to-Video",
        
        "step_2": "2. Enter Prompt",
        "prompt_label": "Describe what you want to generate",
        "prompt_placeholder": "E.g., A cat sleeping lazily in the sunlight...",
        "use_ai_optimize": "✨ Use AI to optimize prompt",
        
        "step_3": "3. Media Input",
        "upload_image": "Upload Image",
        "or_image_url": "Or Image URL",
        "image_url_placeholder": "https://example.com/image.jpg",
        "upload_video": "Upload Video",
        "or_video_url": "Or Video URL",
        "video_url_placeholder": "https://example.com/video.mp4",
        
        # Generate
        "generate": "🚀 Start Generation",
        "generating": "🎬 Generating... Please wait...",
        
        # Validation Errors
        "error_no_prompt": "❌ Please enter a prompt",
        "error_text_api": "❌ Please fill in Text API Key and Model Name in Configuration",
        "error_t2i_api": "❌ Please fill in T2I API Key and Model Name",
        "error_t2v_api": "❌ Please fill in T2V API Key and Model Name",
        "error_i2v_api": "❌ Please fill in I2V API Key and Model Name",
        "error_i2v_media": "❌ Please upload an image or enter an image URL",
        "error_v2v_api": "❌ Please fill in V2V API Key and Model Name",
        "error_v2v_media": "❌ Please upload a video or enter a video URL",
        
        # Success Messages
        "optimize_title": "✨ Optimizing prompt...",
        "optimize_success": "✅ Prompt optimized!",
        "enhanced_prompt": "Enhanced:",
        
        # Result
        "result_title": "🎉 Result",
        "result_image": "Generated Image",
        "result_video": "Generated Video",
        "download_prompt": "📥 Download Prompt (JSON)",
        
        # Footer
        "footer_title": "OpenLens | Multi-Modal AI Creation Platform",
        "footer_disclaimer": "⚠️ Disclaimer: This tool is a transparent gateway only. We do not store any API Keys.",
        
        # Language
        "language": "🌍 Language",
    },
    
    "zh": {
        # Age Verification
        "age_title": "OpenLens",
        "age_subtitle": "需要年龄验证",
        "age_description": "本平台提供多模态AI生成服务。继续即表示您确认：",
        "age_check_1": "我已年满 18 岁",
        "age_check_2": "我将合法使用本平台",
        "age_check_3": "我对生成内容承担全部责任",
        "age_warning": "任何违法或有害内容生成均被严格禁止",
        "age_enter": "我已满18岁 - 进入",
        "age_exit": "离开",
        "age_redirecting": "正在跳转...",
        
        # Main UI
        "main_title": "OpenLens",
        "main_subtitle": "多模态AI创作平台 | T2I · T2V · I2V · V2V",
        
        # Configuration Panel
        "config_title": "⚙️ 配置",
        "global_settings": "🌐 全局设置",
        "global_api_url": "Global API 基础URL",
        "global_api_url_placeholder": "https://api.openai.com/v1",
        
        "text_model": "✏️ 文本模型 (提示词优化)",
        "text_api_key": "文本 API Key",
        "text_api_key_placeholder": "sk-...",
        "text_model_name": "文本模型名称",
        "text_model_placeholder": "gpt-4o, claude-3 等",
        
        "t2i_model": "🖼️ 图像生成 (T2I)",
        "t2i_api_key": "T2I API Key",
        "t2i_api_key_placeholder": "sk-...",
        "t2i_model_name": "T2I 模型名称",
        "t2i_model_placeholder": "dall-e-3, midjourney 等",
        
        "t2v_model": "🎬 文生视频 (T2V)",
        "t2v_api_key": "T2V API Key",
        "t2v_api_key_placeholder": "sk-...",
        "t2v_model_name": "T2V 模型名称",
        "t2v_model_placeholder": "wan2.2, seedance1.5, kling 等",
        
        "i2v_model": "📸 图生视频 (I2V)",
        "i2v_api_key": "I2V API Key",
        "i2v_api_key_placeholder": "sk-...",
        "i2v_model_name": "I2V 模型名称",
        "i2v_model_placeholder": "wan2.2, anyvideo 等",
        
        "v2v_model": "🎥 视频生视频 (V2V)",
        "v2v_api_key": "V2V API Key",
        "v2v_api_key_placeholder": "sk-...",
        "v2v_model_name": "V2V 模型名称",
        "v2v_model_placeholder": "wan2.2 等",
        
        "save_config": "💾 保存配置",
        "save_config_success": "✅ 配置已保存到会话",
        
        # Creation Panel
        "create_title": "🎨 创作",
        "step_1": "1. 选择模式",
        "mode_t2i": "文生图",
        "mode_t2v": "文生视频",
        "mode_i2v": "图生视频",
        "mode_v2v": "视频生视频",
        
        "step_2": "2. 输入提示词",
        "prompt_label": "描述你想要生成的内容",
        "prompt_placeholder": "例如：一只猫咪在阳光下懒洋洋地睡觉...",
        "use_ai_optimize": "✨ 使用AI优化提示词",
        
        "step_3": "3. 媒体输入",
        "upload_image": "上传图片",
        "or_image_url": "或图片URL",
        "image_url_placeholder": "https://example.com/image.jpg",
        "upload_video": "上传视频",
        "or_video_url": "或视频URL",
        "video_url_placeholder": "https://example.com/video.mp4",
        
        # Generate
        "generate": "🚀 开始生成",
        "generating": "🎬 正在生成，请稍候...",
        
        # Validation Errors
        "error_no_prompt": "❌ 请输入提示词",
        "error_text_api": "❌ 请在配置区填写文本API Key和模型名称",
        "error_t2i_api": "❌ 请填写T2I API Key和模型名称",
        "error_t2v_api": "❌ 请填写T2V API Key和模型名称",
        "error_i2v_api": "❌ 请填写I2V API Key和模型名称",
        "error_i2v_media": "❌ 请上传图片或输入图片URL",
        "error_v2v_api": "❌ 请填写V2V API Key和模型名称",
        "error_v2v_media": "❌ 请上传视频或输入视频URL",
        
        # Success Messages
        "optimize_title": "✨ 正在优化提示词...",
        "optimize_success": "✅ 提示词优化完成！",
        "enhanced_prompt": "优化后：",
        
        # Result
        "result_title": "🎉 结果",
        "result_image": "生成的图片",
        "result_video": "生成的视频",
        "download_prompt": "📥 下载提示词 (JSON)",
        
        # Footer
        "footer_title": "OpenLens | 多模态AI创作平台",
        "footer_disclaimer": "⚠️ 免责声明：本工具仅作为透明网关，不存储任何API Key。",
        
        # Language
        "language": "🌍 语言",
    },
    
    "ja": {
        # Age Verification
        "age_title": "OpenLens",
        "age_subtitle": "年齢確認",
        "age_description": "このプラットフォームはマルチモーダルAI生成サービスを提供します。続行することで以下を確認：",
        "age_check_1": "私は18歳以上です",
        "age_check_2": "私はこのプラットフォームを合法的に使用します",
        "age_check_3": "生成されたコンテンツに対して全責任を負います",
        "age_warning": "違法または有害なコンテンツ生成は厳密に禁止されています",
        "age_enter": "18歳以上 - 進む",
        "age_exit": "退出",
        "age_redirecting": "リダイレクト中...",
        
        # Main UI
        "main_title": "OpenLens",
        "main_subtitle": "マルチモーダルAI作成プラットフォーム | T2I · T2V · I2V · V2V",
        
        # Configuration Panel
        "config_title": "⚙️ 設定",
        "global_settings": "🌐 グローバル設定",
        "global_api_url": "グローバルAPI Base URL",
        "global_api_url_placeholder": "https://api.openai.com/v1",
        
        "text_model": "✏️ テキストモデル（プロンプト最適化）",
        "text_api_key": "テキストAPI Key",
        "text_api_key_placeholder": "sk-...",
        "text_model_name": "テキストモデル名",
        "text_model_placeholder": "gpt-4o, claude-3 など",
        
        "t2i_model": "🖼️ 画像生成 (T2I)",
        "t2i_api_key": "T2I API Key",
        "t2i_api_key_placeholder": "sk-...",
        "t2i_model_name": "T2I モデル名",
        "t2i_model_placeholder": "dall-e-3, midjourney など",
        
        "t2v_model": "🎬 テキストから動画 (T2V)",
        "t2v_api_key": "T2V API Key",
        "t2v_api_key_placeholder": "sk-...",
        "t2v_model_name": "T2V モデル名",
        "t2v_model_placeholder": "wan2.2, seedance1.5, kling など",
        
        "i2v_model": "📸 画像から動画 (I2V)",
        "i2v_api_key": "I2V API Key",
        "i2v_api_key_placeholder": "sk-...",
        "i2v_model_name": "I2V モデル名",
        "i2v_model_placeholder": "wan2.2, anyvideo など",
        
        "v2v_model": "🎥 動画から動画 (V2V)",
        "v2v_api_key": "V2V API Key",
        "v2v_api_key_placeholder": "sk-...",
        "v2v_model_name": "V2V モデル名",
        "v2v_model_placeholder": "wan2.2 など",
        
        "save_config": "💾 設定を保存",
        "save_config_success": "✅ 設定がセッションに保存されました",
        
        # Creation Panel
        "create_title": "🎨 作成",
        "step_1": "1. モードを選択",
        "mode_t2i": "画像生成",
        "mode_t2v": "動画生成",
        "mode_i2v": "画像から動画",
        "mode_v2v": "動画から動画",
        
        "step_2": "2. プロンプトを入力",
        "prompt_label": "生成したい内容を描述",
        "prompt_placeholder": "例：阳光下でのんびりと眠る猫...",
        "use_ai_optimize": "✨ AIでプロンプトを最適化",
        
        "step_3": "3. メディア入力",
        "upload_image": "画像をアップロード",
        "or_image_url": "または画像URL",
        "image_url_placeholder": "https://example.com/image.jpg",
        "upload_video": "動画をアップロード",
        "or_video_url": "または動画URL",
        "video_url_placeholder": "https://example.com/video.mp4",
        
        # Generate
        "generate": "🚀 生成開始",
        "generating": "🎬 生成中...お待ちください...",
        
        # Validation Errors
        "error_no_prompt": "❌ プロンプトを入力してください",
        "error_text_api": "❌ 設定でテキストAPI Keyとモデル名を入力してください",
        "error_t2i_api": "❌ T2I API Keyとモデル名を入力してください",
        "error_t2v_api": "❌ T2V API Keyとモデル名を入力してください",
        "error_i2v_api": "❌ I2V API Keyとモデル名を入力してください",
        "error_i2v_media": "❌ 画像をアップロードするか画像URLを入力してください",
        "error_v2v_api": "❌ V2V API Keyとモデル名を入力してください",
        "error_v2v_media": "❌ 動画をアップロードするか動画URLを入力してください",
        
        # Success Messages
        "optimize_title": "✨ プロンプトを最適化中...",
        "optimize_success": "✅ プロンプトが最適化されました！",
        "enhanced_prompt": "最適化後：",
        
        # Result
        "result_title": "🎉 結果",
        "result_image": "生成された画像",
        "result_video": "生成された動画",
        "download_prompt": "📥 プロンプトをダウンロード (JSON)",
        
        # Footer
        "footer_title": "OpenLens | マルチモーダルAI作成プラットフォーム",
        "footer_disclaimer": "⚠️ 免責事項：このツールは透明なゲートウェイです。API Keyは保存しません。",
        
        # Language
        "language": "🌍 言語",
    }
}

# ============================================================
# Step 2: Translation Function
# ============================================================
def t(key):
    """Translate a key based on current language"""
    lang = st.session_state.get("current_lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))

# ============================================================
# Session State Initialization
# ============================================================
if 'age_verified' not in st.session_state:
    st.session_state.age_verified = False

if 'current_lang' not in st.session_state:
    st.session_state.current_lang = "en"

# ============================================================
# Age Verification Gate
# ============================================================
if not st.session_state.age_verified:
    st.set_page_config(
        page_title="OpenLens - Age Verification",
        page_icon="🎬",
        layout="centered"
    )
    
    st.markdown("""
    <style>
    .stApp { background: #0a0a0a; }
    .age-box { background: #1a1a1a; border: 2px solid #667eea; border-radius: 20px; padding: 50px; max-width: 550px; margin: 80px auto; text-align: center; }
    .age-title { font-size: 32px; font-weight: bold; color: #fff; margin-bottom: 25px; }
    .age-text { color: #aaa; font-size: 15px; line-height: 1.8; }
    .age-check { color: #fff; margin: 20px 0; text-align: left; padding: 0 40px; }
    .age-warning { color: #ef4444; font-size: 13px; padding: 12px; background: rgba(239,68,68,0.15); border-radius: 8px; margin-top: 20px; }
    .stButton > button { width: 100%; margin: 8px 0; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="age-box">
        <div class="age-title">🎬 {t('age_title')}</div>
        <div class="age-text">
            <strong>{t('age_subtitle')}</strong><br><br>
            {t('age_description')}
        </div>
        <div class="age-check">
            ✅ {t('age_check_1')}<br>
            ✅ {t('age_check_2')}<br>
            ✅ {t('age_check_3')}
        </div>
        <div class="age-warning">
            ⚠️ {t('age_warning')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button(t("age_enter"), type="primary", key="age_confirm"):
            st.session_state.age_verified = True
            st.rerun()
    
    with col2:
        if st.button(t("age_exit"), key="age_exit"):
            st.markdown("""
            <script>window.parent.location.href = "https://www.google.com";</script>
            """, unsafe_allow_html=True)
            st.warning(t("age_redirecting"))
    
    st.stop()

# ============================================================
# Main App Config
# ============================================================
st.set_page_config(
    page_title="OpenLens - AI Multi-Modal Creation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Session State - API Config
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
    st.session_state.generation_mode = "Text-to-Image"

# ============================================================
# CSS
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
# Language Switcher (Top of Sidebar)
# ============================================================
with st.sidebar:
    st.markdown("---")
    lang = st.selectbox(t("language"), ["en", "zh", "ja"], 
                        format_func=lambda x: {"en": "English", "zh": "简体中文", "ja": "日本語"}[x],
                        index=["en", "zh", "ja"].index(st.session_state.current_lang))
    if lang != st.session_state.current_lang:
        st.session_state.current_lang = lang
        st.rerun()

# ============================================================
# API Functions (TODO: Add real API calls)
# ============================================================

def call_text_api(prompt, api_key, model, api_url):
    """Text Model API for Prompt Optimization"""
    time.sleep(1)
    return f"【Enhanced】{prompt} - High quality cinematic footage, soft lighting, detailed, 4K, smooth animation"

def call_t2i_api(prompt, api_key, model, api_url):
    """Text-to-Image API"""
    time.sleep(2)
    return {"url": "https://via.placeholder.com/1024x1024/667eea/ffffff?text=AI+Generated+Image", "type": "image", "prompt": prompt}

def call_t2v_api(prompt, api_key, model, api_url, **kwargs):
    """Text-to-Video API"""
    time.sleep(3)
    return {"url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "type": "video", "prompt": prompt}

def call_i2v_api(prompt, image_data, api_key, model, api_url):
    """Image-to-Video API"""
    time.sleep(3)
    return {"url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "type": "video", "prompt": prompt}

def call_v2v_api(prompt, video_data, api_key, model, api_url):
    """Video-to-Video API"""
    time.sleep(4)
    return {"url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "type": "video", "prompt": prompt}

# ============================================================
# Main Interface
# ============================================================

st.markdown(f'<p class="main-title">🎬 {t("main_title")}</p>', unsafe_allow_html=True)
st.markdown(f"### {t('main_subtitle')}")
st.markdown("---")

# Two Columns
col_config, col_create = st.columns([1, 2])

# ============================================================
# Left: Configuration Panel
# ============================================================
with col_config:
    st.header(t("config_title"))
    
    with st.expander(t("global_settings"), expanded=True):
        st.session_state.global_api_url = st.text_input(
            t("global_api_url"), 
            value=st.session_state.global_api_url, 
            placeholder=t("global_api_url_placeholder")
        )
    
    with st.expander(t("text_model")):
        st.session_state.text_api_key = st.text_input(
            t("text_api_key"), 
            value=st.session_state.text_api_key, 
            type="password", 
            placeholder=t("text_api_key_placeholder")
        )
        st.session_state.text_model = st.text_input(
            t("text_model_name"), 
            value=st.session_state.text_model, 
            placeholder=t("text_model_placeholder")
        )
    
    with st.expander(t("t2i_model")):
        st.session_state.t2i_api_key = st.text_input(
            t("t2i_api_key"), 
            value=st.session_state.t2i_api_key, 
            type="password", 
            placeholder=t("t2i_api_key_placeholder")
        )
        st.session_state.t2i_model = st.text_input(
            t("t2i_model_name"), 
            value=st.session_state.t2i_model, 
            placeholder=t("t2i_model_placeholder")
        )
    
    with st.expander(t("t2v_model")):
        st.session_state.t2v_api_key = st.text_input(
            t("t2v_api_key"), 
            value=st.session_state.t2v_api_key, 
            type="password", 
            placeholder=t("t2v_api_key_placeholder")
        )
        st.session_state.t2v_model = st.text_input(
            t("t2v_model_name"), 
            value=st.session_state.t2v_model, 
            placeholder=t("t2v_model_placeholder")
        )
    
    with st.expander(t("i2v_model")):
        st.session_state.i2v_api_key = st.text_input(
            t("i2v_api_key"), 
            value=st.session_state.i2v_api_key, 
            type="password", 
            placeholder=t("i2v_api_key_placeholder")
        )
        st.session_state.i2v_model = st.text_input(
            t("i2v_model_name"), 
            value=st.session_state.i2v_model, 
            placeholder=t("i2v_model_placeholder")
        )
    
    with st.expander(t("v2v_model")):
        st.session_state.v2v_api_key = st.text_input(
            t("v2v_api_key"), 
            value=st.session_state.v2v_api_key, 
            type="password", 
            placeholder=t("v2v_api_key_placeholder")
        )
        st.session_state.v2v_model = st.text_input(
            t("v2v_model_name"), 
            value=st.session_state.v2v_model, 
            placeholder=t("v2v_model_placeholder")
        )
    
    if st.button(t("save_config"), use_container_width=True):
        st.success(t("save_config_success"))

# ============================================================
# Right: Creation Panel
# ============================================================
with col_create:
    st.header(t("create_title"))
    
    # Step 1: Mode Selection
    st.subheader(t("step_1"))
    mode = st.radio(
        "Mode", 
        ["Text-to-Image", "Text-to-Video", "Image-to-Video", "Video-to-Video"], 
        horizontal=True, 
        label_visibility="collapsed",
        format_func=lambda x: {
            "Text-to-Image": t("mode_t2i"),
            "Text-to-Video": t("mode_t2v"),
            "Image-to-Video": t("mode_i2v"),
            "Video-to-Video": t("mode_v2v")
        }[x]
    )
    st.session_state.generation_mode = mode
    
    # Step 2: Prompt Input
    st.subheader(t("step_2"))
    prompt = st.text_area(
        t("prompt_label"), 
        height=120, 
        placeholder=t("prompt_placeholder")
    )
    
    # Prompt Optimization
    use_optimize = st.checkbox(t("use_ai_optimize"))
    
    # Step 3: Media Input
    media_input = None
    media_url = ""
    
    st.subheader(t("step_3"))
    
    if mode == "Image-to-Video":
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            uploaded_image = st.file_uploader(t("upload_image"), type=['jpg', 'jpeg', 'png', 'webp'])
        with col_img2:
            media_url = st.text_input(t("or_image_url"), placeholder=t("image_url_placeholder"))
        if uploaded_image:
            import base64
            media_input = base64.b64encode(uploaded_image.read()).decode()
    
    elif mode == "Video-to-Video":
        col_vid1, col_vid2 = st.columns(2)
        with col_vid1:
            uploaded_video = st.file_uploader(t("upload_video"), type=['mp4', 'mov', 'avi'])
        with col_vid2:
            media_url = st.text_input(t("or_video_url"), placeholder=t("video_url_placeholder"))
        if uploaded_video:
            import base64
            media_input = base64.b64encode(uploaded_video.read()).decode()
    
    # Generate Button
    st.markdown("---")
    
    if st.button(t("generate"), type="primary", use_container_width=True):
        # Basic Validation
        if not prompt:
            st.error(t("error_no_prompt"))
            st.stop()
        
        final_prompt = prompt
        
        # Prompt Optimization
        if use_optimize:
            if not st.session_state.text_api_key or not st.session_state.text_model:
                st.error(t("error_text_api"))
                st.stop()
            
            with st.spinner(t("optimize_title")):
                final_prompt = call_text_api(prompt, st.session_state.text_api_key, st.session_state.text_model, st.session_state.global_api_url)
            
            st.success(t("optimize_success"))
            st.info(f"{t('enhanced_prompt')} {final_prompt}")
        
        # Mode-specific Validation
        if mode == "Text-to-Image" and (not st.session_state.t2i_api_key or not st.session_state.t2i_model):
            st.error(t("error_t2i_api"))
            st.stop()
        elif mode == "Text-to-Video" and (not st.session_state.t2v_api_key or not st.session_state.t2v_model):
            st.error(t("error_t2v_api"))
            st.stop()
        elif mode == "Image-to-Video" and (not st.session_state.i2v_api_key or not st.session_state.i2v_model):
            st.error(t("error_i2v_api"))
            st.stop()
        elif mode == "Image-to-Video" and not media_input and not media_url:
            st.error(t("error_i2v_media"))
            st.stop()
        elif mode == "Video-to-Video" and (not st.session_state.v2v_api_key or not st.session_state.v2v_model):
            st.error(t("error_v2v_api"))
            st.stop()
        elif mode == "Video-to-Video" and not media_input and not media_url:
            st.error(t("error_v2v_media"))
            st.stop()
        
        # Generate
        with st.spinner(t("generating")):
            result = None
            if mode == "Text-to-Image":
                result = call_t2i_api(final_prompt, st.session_state.t2i_api_key, st.session_state.t2i_model, st.session_state.global_api_url)
            elif mode == "Text-to-Video":
                result = call_t2v_api(final_prompt, st.session_state.t2v_api_key, st.session_state.t2v_model, st.session_state.global_api_url)
            elif mode == "Image-to-Video":
                result = call_i2v_api(final_prompt, media_input or media_url, st.session_state.i2v_api_key, st.session_state.i2v_model, st.session_state.global_api_url)
            elif mode == "Video-to-Video":
                result = call_v2v_api(final_prompt, media_input or media_url, st.session_state.v2v_api_key, st.session_state.v2v_model, st.session_state.global_api_url)
        
        # Display Result
        st.markdown("---")
        st.subheader(t("result_title"))
        
        if result:
            if result["type"] == "image":
                st.image(result["url"], caption=t("result_image"))
            elif result["type"] == "video":
                st.video(result["url"])
            
            # Download
            prompt_json = json.dumps({
                "prompt": result.get("prompt", final_prompt),
                "mode": mode,
                "timestamp": datetime.now().isoformat()
            }, ensure_ascii=False, indent=2)
            
            st.download_button(t("download_prompt"), prompt_json, "openlens_prompt.json", "application/json")

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>🎬 {t('footer_title')}</p>
    <p><strong>{t('footer_disclaimer')}</strong></p>
</div>
""", unsafe_allow_html=True)
