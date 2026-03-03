#!/usr/bin/env python3
"""
OpenLens - Minimalist AI Video Generation Portal
A raw transparency API pass-through for AI video generation.

Features:
- Pure pass-through: no content filtering, no safety middleware
- Manual API config with LocalStorage persistence  
- OpenAI-style /v1/video/generations support
- Auto-polling for async video generation
- HTML5 video player with download button
- Local save path configuration
"""

import streamlit as st
import requests
import time
import json
import os
from datetime import datetime

# Get skill directory
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="OpenLens",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark minimalist theme
st.markdown("""
<style>
    .stApp { background: #0a0a0a; color: #e0e0e0; }
    .stTextInput > div > div > input { background: #1a1a1a; border: 1px solid #333; color: #fff; }
    .stTextArea > div > div > textarea { background: #1a1a1a; border: 1px solid #333; color: #fff; }
    .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; color: white; font-weight: 600; }
    .video-container { background: #000; border-radius: 12px; padding: 16px; margin-top: 16px; }
    .main-header { font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0; }
    .subtitle { color: #666; font-size: 0.9rem; margin-top: -10px; }
    .age-container { max-width: 600px; margin: 80px auto; padding: 50px; background: #1a1a1a; border: 2px solid #667eea; border-radius: 20px; text-align: center; }
    .age-title { font-size: 36px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 30px; }
    .age-text { color: #ccc; font-size: 16px; line-height: 2.2; margin-bottom: 30px; }
    .age-warning { color: #ef4444; font-size: 14px; padding: 15px; background: rgba(239, 68, 68, 0.1); border-radius: 8px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONFIGURATION
# ============================================================

def load_config():
    """Load configuration from config.json"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """Save configuration to config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# ============================================================
# SESSION STATE MANAGEMENT
# ============================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'api_url' not in st.session_state:
    st.session_state.api_url = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'task_id' not in st.session_state:
    st.session_state.task_id = None
if 'task_status' not in st.session_state:
    st.session_state.task_status = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = None
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'uploaded_image_url' not in st.session_state:
    st.session_state.uploaded_image_url = None
if 'text_api_url' not in st.session_state:
    st.session_state.text_api_url = ""
if 'text_api_key' not in st.session_state:
    st.session_state.text_api_key = ""
if 'text_model' not in st.session_state:
    st.session_state.text_model = ""
if 'refined_prompt' not in st.session_state:
    st.session_state.refined_prompt = ""
if 'save_path' not in st.session_state:
    st.session_state.save_path = "./outputs"

# NOTE: Config loading removed to prevent exposing API keys
# Users must enter their own API keys in the GUI

# ============================================================
# HELPER F===========================

# DefaultUNCTIONS
# ================================= video model
DEFAULT_MODEL = "wan2.2"

REFINER_SYSTEM_PROMPT = """You are a top-tier AI video director. Transform the user's description into a professional, cinematic video prompt. Enhance with visual details, motion dynamics, technical quality terms. Output ONLY the refined prompt."""

def log_message(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = "[%s] %s" % (timestamp, msg)
    st.session_state.logs.append(log_entry)
    if len(st.session_state.logs) > 50:
        st.session_state.logs = st.session_state.logs[-50:]

def refine_prompt(text_api_url, text_api_key, text_model, user_prompt, image_url=None):
    headers = {"Authorization": "Bearer " + text_api_key, "Content-Type": "application/json"}
    
    if image_url:
        messages = [
            {"role": "system", "content": REFINER_SYSTEM_PROMPT},
            {"role": "user", "content": [{"type": "image_url", "image_url": {"url": image_url}}, {"type": "text", "text": "Original: " + user_prompt}]}
        ]
    else:
        messages = [{"role": "system", "content": REFINER_SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}]
    
    payload = {"model": text_model, "messages": messages, "temperature": 0.7, "max_tokens": 500}
    
    for endpoint in ["%s/chat/completions" % text_api_url, "%s/responses" % text_api_url]:
        try:
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                elif "output" in data:
                    return data["output"][0]["content"][0]["text"]
        except Exception as e:
            log_message("Refine error: " + str(e))
    return None

def upload_to_catbox(file_data, filename):
    try:
        files = {'reqtype': (None, 'fileupload'), 'time': (None, '1h'), 'fileToUpload': (filename, file_data, 'image/' + filename.split('.')[-1])}
        resp = requests.post('https://catbox.moe/user/api.php', files=files, timeout=60)
        if resp.status_code == 200 and resp.text.strip().startswith('http'):
            return resp.text.strip()
    except:
        pass
    return None

def submit_video_task(api_url, api_key, prompt, negative_prompt, resolution="720p", duration=5, **extra_params):
    headers = {"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}
    payload = {"model": extra_params.get("model", DEFAULT_MODEL), "input": {"prompt": prompt}}
    
    if negative_prompt:
        payload["input"]["negative_prompt"] = negative_prompt
    if extra_params.get("img_url"):
        payload["input"]["img_url"] = extra_params["img_url"]
    
    payload["parameters"] = {"size": resolution, "duration": duration}
    if extra_params.get("seed"):
        payload["parameters"]["seed"] = extra_params["seed"]
    
    try:
        resp = requests.post("%s/video/generations" % api_url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        log_message("Submit error: " + str(e))
    return {"error": str(e)}

def poll_task_status(api_url, api_key, task_id, max_attempts=120):
    headers = {"Authorization": "Bearer " + api_key, "Content-Type": "application/json"}
    for attempt in range(max_attempts):
        try:
            resp = requests.get("%s/video/generations/%s" % (api_url, task_id), headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status", "UNKNOWN")
                progress = data.get("progress_percent", 0)
                st.session_state.task_status = status
                st.session_state.progress = progress
                log_message("Poll #%d: %s (%d%%)" % (attempt+1, status, progress))
                if status == "SUCCEED":
                    st.session_state.video_url = data.get("videos", [{}])[0].get("video_url")
                    return data
                elif status == "FAILED":
                    return data
                time.sleep(5)
        except Exception as e:
            log_message("Poll error: " + str(e))
            time.sleep(5)
    return {"error": "Timeout"}

def download_and_save(video_url, save_path):
    """Stream download video and save to local path"""
    try:
        os.makedirs(save_path, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(save_path, f"video_{timestamp}.mp4_message")
        
        log("Streaming download to: " + output_file)
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        total = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
        
        log_message("Saved: " + output_file)
        return output_file
    except Exception as e:
        log_message("Download error: " + str(e))
        return None

# ============================================================
# AGE VERIFICATION
# ============================================================
if not st.session_state.authenticated:
    st.markdown("""
    <div class="age-container">
        <div class="age-title">🎬 OpenLens</div>
        <div class="age-text">
            <strong>Age Verification Required</strong><br><br>
            This is a transparent AI video generation gateway.<br><br>
            Please confirm all of the following:
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        check1 = st.checkbox("✅ I am 18+")
    with col2:
        check2 = st.checkbox("✅ I will use legally")
    with col3:
        check3 = st.checkbox("✅ I accept responsibility")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if check1 and check2 and check3:
        if st.button("✅ Enter OpenLens", type="primary", use_container_width=True):
            st.session_state.authenticated = True
            st.rerun()
    else:
        st.button("✅ Enter OpenLens", disabled=True, use_container_width=True)
        st.info("👆 Please check all boxes above")
    
    st.markdown("---")
    st.markdown("<div class='age-warning' style='text-align:center;'>⚠️ Illegal content is prohibited</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# MAIN UI
# ============================================================
st.markdown('<p class="main-header">🎬 OpenLens</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Video Generation Portal | Raw Transparency</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("⚙️ API Configuration")
    
    api_url_input = st.text_input("Video API URL", value=st.session_state.api_url, placeholder="https://api.onlypixai.com/v1")
    api_key_input = st.text_input("Video API Key", value=st.session_state.api_key, type="password", placeholder="sk-px-...")
    
    if api_url_input != st.session_state.api_url:
        st.session_state.api_url = api_url_input
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    st.header("✏️ Text API")
    
    text_api_url_input = st.text_input("Text API URL", value=st.session_state.text_api_url, placeholder="https://api.openai.com/v1")
    text_api_key_input = st.text_input("Text API Key", value=st.session_state.text_api_key, type="password", placeholder="sk-...")
    text_model_input = st.text_input("Text Model", value=st.session_state.text_model, placeholder="gpt-4o, deepseek/deepseek-v3")
    
    if text_api_url_input != st.session_state.text_api_url:
        st.session_state.text_api_url = text_api_url_input
    if text_api_key_input != st.session_state.text_api_key:
        st.session_state.text_api_key = text_api_key_input
    if text_model_input != st.session_state.text_model:
        st.session_state.text_model = text_model_input
    
    st.markdown("---")
    st.header("💾 Save Path")
    
    save_path_input = st.text_input("Default Save Path", value=st.session_state.save_path, placeholder="./outputs")
    if save_path_input != st.session_state.save_path:
        st.session_state.save_path = save_path_input
    
    # Save config button
    if st.button("💾 Save Configuration"):
        config = {
            "video_api_url": st.session_state.api_url,
            "video_api_key": st.session_state.api_key,
            "text_api_url": st.session_state.text_api_url,
            "text_api_key": st.session_state.text_api_key,
            "text_model": st.session_state.text_model,
            "default_save_path": st.session_state.save_path
        }
        save_config(config)
        st.success("✅ Config saved!")
    
    st.markdown("---")
    if st.button("🚪 Exit / Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ============================================================
# MAIN CONTENT
# ============================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Generate Video")
    
    # Model selection - allow custom input
    col_model1, col_model2 = st.columns([2, 1])
    with col_model1:
        model = st.text_input(
            "Video Model",
            value=DEFAULT_MODEL,
            placeholder="wan2.2, seedance1.5, wan2.6-i2v, etc.",
            help="Enter your video model ID (e.g., wan2.2, seedance1.5, wan2.6-i2v, etc.)"
        )
    with col_model2:
        # Quick presets
        preset = st.selectbox(
            "Presets",
            ["Custom", "wan2.2", "wan2.6-i2v", "wan2.6-t2v", "seedance1.5"],
            index=1,
            help="Quick select common models"
        )
        if preset != "Custom":
            model = f"video/{preset}" if not preset.startswith("video/") else preset
    
    prompt = st.text_area("Prompt", height=120, value=st.session_state.refined_prompt or "", placeholder="Describe the video...")
    
    # Refine controls
    col_p1, col_p2 = st.columns([3, 1])
    with col_p1:
        auto_refine = st.checkbox("🔗 Auto-optimize & Generate", value=False)
    with col_p2:
        optimize_btn = st.button("✨ Optimize", use_container_width=True)
    
    if optimize_btn:
        if not st.session_state.text_api_url or not st.session_state.text_api_key or not st.session_state.text_model:
            st.error("❌ Please configure Text API in sidebar")
        elif not prompt:
            st.error("❌ Please enter a prompt")
        else:
            with st.spinner("Optimizing..."):
                img_url = st.session_state.uploaded_image_url if st.session_state.uploaded_image_url else None
                refined = refine_prompt(st.session_state.text_api_url, st.session_state.text_api_key, st.session_state.text_model, prompt, img_url)
                if refined:
                    st.session_state.refined_prompt = refined
                    st.success("✅ Optimized!")
                    st.text_area("Refined", value=refined, height=80, key="refined_disp")
                    st.rerun()
    
    negative_prompt = st.text_area("Negative Prompt (optional)", height=60)
    
    with st.expander("⚡ Advanced"):
        col_a, col_b = st.columns(2)
        with col_a:
            resolution = st.selectbox("Resolution", ["720p", "1080p", "1280*720"], index=0)
            duration = st.selectbox("Duration", [5, 10, 15], index=0)
        with col_b:
            seed = st.text_input("Seed", placeholder="Random")
            watermark = st.checkbox("Watermark", value=False)
    
    # Image upload for I2V
    img_url = ""
    if model and "i2v" in model.lower():
        st.markdown("#### 🖼️ Image Input")
        uploaded_file = st.file_uploader("Upload image", type=['jpg', 'jpeg', 'png', 'webp'])
        
        if uploaded_file:
            file_data = uploaded_file.getvalue()
            filename = uploaded_file.name
            st.image(file_data, caption=filename, width=200)
            
            if st.button("⬆️ Upload to Cloud"):
                with st.spinner("Uploading..."):
                    image_url = upload_to_catbox(file_data, filename)
                    if image_url:
                        st.session_state.uploaded_image_url = image_url
                        st.success("✅ Uploaded!")
                        st.rerun()
        
        img_url = st.text_input("Image URL", value=st.session_state.uploaded_image_url or "", placeholder="https://...")
        
        if st.session_state.uploaded_image_url and img_url != st.session_state.uploaded_image_url:
            if st.button("🗑️ Clear Image"):
                st.session_state.uploaded_image_url = None
                st.rerun()

with col2:
    st.header("🚀 Actions")
    generate_btn = st.button("🎬 Generate Video", type="primary", use_container_width=True)
    
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.task_id = None
        st.session_state.task_status = None
        st.session_state.video_url = None
        st.session_state.progress = 0
        st.session_state.logs = []
        st.rerun()

# ============================================================
# GENERATION
# ============================================================
if generate_btn:
    if not st.session_state.api_url or not st.session_state.api_key:
        st.error("❌ Please enter Video API URL and Key in sidebar")
    elif not prompt:
        st.error("❌ Please enter a prompt")
    else:
        final_prompt = prompt
        current_img_url = img_url if (model and "i2v" in model.lower()) and img_url else None
        
        # Auto refine
        if auto_refine and st.session_state.text_api_url and st.session_state.text_api_key and st.session_state.text_model:
            with st.spinner("Auto-optimizing..."):
                refined = refine_prompt(st.session_state.text_api_url, st.session_state.text_api_key, st.session_state.text_model, prompt, current_img_url)
                if refined:
                    final_prompt = refined
                    st.session_state.refined_prompt = refined
        
        # Submit
        log_message("="*50)
        log_message("Starting video generation...")
        
        extra_params = {"model": model, "img_url": current_img_url, "seed": int(seed) if seed else None, "watermark": watermark}
        result = submit_video_task(st.session_state.api_url, st.session_state.api_key, final_prompt, negative_prompt, resolution, duration, **extra_params)
        
        if "task_id" in result:
            st.session_state.task_id = result["task_id"]
            st.session_state.task_status = result.get("status", "QUEUED")
            st.info("Task ID: " + result["task_id"])
            
            with st.spinner("Generating..."):
                poll_result = poll_task_status(st.session_state.api_url, st.session_state.api_key, st.session_state.task_id)
                
                if poll_result.get("videos"):
                    st.session_state.video_url = poll_result["videos"][0]["video_url"]
        else:
            st.error("❌ Failed: " + str(result.get("error")))

# ============================================================
# STATUS & RESULT
# ============================================================
st.markdown("---")
st.header("📊 Status")

if st.session_state.task_status:
    status = st.session_state.task_status
    progress = st.session_state.progress
    
    if status == "QUEUED":
        st.info("🔄 Queued")
    elif status == "PROCESSING":
        st.info(f"⚙️ Processing: {progress}%")
        st.progress(progress / 100)
    elif status == "SUCCEED":
        st.success("✅ Complete!")
    elif status == "FAILED":
        st.error("❌ Failed")

if st.session_state.video_url:
    st.markdown("---")
    st.header("🎥 Result")
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    st.video(st.session_state.video_url)
    st.markdown("[📥 Download](%s)" % st.session_state.video_url)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-save to local
    save_path = st.session_state.save_path
    if st.button("💾 Save to Local Path"):
        with st.spinner("Downloading to local..."):
            local_file = download_and_save(st.session_state.video_url, save_path)
            if local_file:
                st.success(f"✅ Saved: {local_file}")
            else:
                st.error("❌ Save failed")

# ============================================================
# LOGS
# ============================================================
if st.session_state.logs:
    st.markdown("---")
    with st.expander("📜 Logs", expanded=False):
        for log_entry in reversed(st.session_state.logs[-20:]):
            st.text(log_entry)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>OpenLens | Raw Transparency Pass-through | No Content Filtering</p>
    <p><strong>⚠️ Disclaimer:</strong> This tool does not store API Keys or generated content. Use legally.</p>
</div>
""", unsafe_allow_html=True)
