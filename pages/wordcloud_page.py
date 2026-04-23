# pages/wordcloud_page.py
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(layout="centered", page_title="词云生成器")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import jieba
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import io
from collections import Counter
from utils.shared import (
    get_default_font, process_mask_to_array,
    ai_match_mask_filename, generate_mask_image_by_ai
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #080b14 !important;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 40px !important;
}

.page-header-outer {
    position: relative;
    left: 50%; right: 50%;
    margin-left: -50vw; margin-right: -50vw;
    width: 100vw;
    padding: 28px 10vw;
    background:
        radial-gradient(ellipse 70% 80% at 10% 50%, rgba(99,102,241,0.13) 0%, transparent 60%),
        #080b14;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center; justify-content: space-between;
    box-sizing: border-box;
}
.page-header-left { display: flex; align-items: center; gap: 20px; }
.page-header-icon {
    font-size: 2rem;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px; width: 56px; height: 56px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.page-header-title {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(90deg, #e0e7ff, #a5b4fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.page-header-sub {
    font-size: 0.82rem; color: rgba(226,232,240,0.35); line-height: 1.5;
}
.section-label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: rgba(226,232,240,0.28);
    margin-bottom: 10px; margin-top: 28px; display: block;
}
.gradient-bar {
    width: 100%; height: 8px; border-radius: 6px;
    margin-top: -2px; margin-bottom: 14px;
}
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important; overflow: hidden;
}
div[data-testid="stExpander"] summary {
    font-size: 0.9rem !important; font-weight: 600 !important;
    color: rgba(226,232,240,0.55) !important; padding: 16px 20px !important;
}
div[data-testid="stExpander"] summary:hover { color: rgba(226,232,240,0.85) !important; }
div[data-testid="stButton"] > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-size: 0.85rem !important; font-weight: 600 !important;
    padding: 10px 18px !important; transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(255,255,255,0.08) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border: none !important; color: #fff !important;
    font-size: 1rem !important; padding: 14px 0 !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(99,102,241,0.5) !important;
    transform: translateY(-2px) !important;
}
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: rgba(99,102,241,0.45) !important;
}
.stRadio > div { gap: 6px !important; flex-direction: column !important; }
.stRadio label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important; padding: 8px 14px !important;
    font-size: 0.82rem !important; color: rgba(226,232,240,0.5) !important;
    transition: all 0.15s !important;
}
.stRadio label:hover {
    background: rgba(99,102,241,0.08) !important;
    border-color: rgba(99,102,241,0.25) !important;
}
div[data-testid="stSlider"] > div > div > div {
    background: rgba(99,102,241,0.6) !important;
}
div[data-baseweb="tag"] {
    background: rgba(99,102,241,0.18) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 6px !important;
}
.dl-section {
    background: rgba(99,102,241,0.05);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 16px; padding: 28px; margin-top: 28px;
}
.dl-title {
    font-size: 0.8rem; font-weight: 700; color: #a5b4fc;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 16px;
}
div[data-testid="stDownloadButton"] > button {
    background: rgba(99,102,241,0.1) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important; color: #c7d2fe !important;
    font-weight: 600 !important; width: 100% !important;
    padding: 12px 0 !important; transition: all 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(99,102,241,0.2) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stAlert"] { border-radius: 12px !important; border: none !important; }
div[data-testid="stImage"] img { border-radius: 14px !important; }
.mask-preview-card {
    background: rgba(16,185,129,0.04);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 14px; padding: 20px; margin-top: 16px;
}
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 0 0 28px 0;
}
</style>
""", unsafe_allow_html=True)

# ── 页头 + 返回按钮 ──────────────────────────────────────────
col_header, col_back = st.columns([6, 1])

with col_header:
    st.markdown("""
    <div class="page-header-outer">
      <div class="page-header-left">
        <div class="page-header-icon">☁️</div>
        <div>
          <div class="page-header-title">词云生成器</div>
          <div class="page-header-sub">配置参数 · 一键生成高清词云图 · 导出 PNG / PDF</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_back:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.switch_page("pages/home.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 读取首页传入的文本 ────────────────────────────────────────
text_area = st.session_state.get("shared_text", "")

if not text_area:
    st.markdown("""
    <div style="text-align:center;padding:60px 24px;">
      <div style="font-size:2.5rem;margin-bottom:16px;">📋</div>
      <div style="font-size:1rem;color:rgba(226,232,240,0.4);margin-bottom:24px;">
        还没有输入文本，请先返回首页粘贴内容
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("← 返回首页输入文本", use_container_width=True):
        st.switch_page("pages/home.py")
    st.stop()

# 文本预览
st.markdown('<span class="section-label">当前文本</span>', unsafe_allow_html=True)
preview = text_area[:200] + "..." if len(text_area) > 200 else text_area
st.markdown(f"""
<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
border-radius:14px;padding:18px 22px;margin-bottom:24px;font-size:0.85rem;
color:rgba(226,232,240,0.45);line-height:1.7;position:relative;max-height:100px;overflow:hidden;">
  {preview}
  <div style="position:absolute;bottom:0;left:0;right:0;height:36px;
  background:linear-gradient(transparent,rgba(8,11,20,0.95));border-radius:0 0 14px 14px;"></div>
</div>
""", unsafe_allow_html=True)

# ── 参数配置 ─────────────────────────────────────────────────
with st.expander("🎨 设计参数配置", expanded=True):
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<span class="section-label">字体</span>', unsafe_allow_html=True)
        fonts_dir = os.path.join(ROOT_DIR, "fonts")
        font_files = [f for f in os.listdir(fonts_dir)
                      if f.lower().endswith(('.ttf', '.otf', '.ttc'))] if os.path.exists(fonts_dir) else []
        if font_files:
            selected_font = st.selectbox("选择字体", font_files, label_visibility="collapsed")
            font_p = os.path.join(fonts_dir, selected_font)
        else:
            st.warning("⚠️ 未检测到 fonts 文件夹中的字体")
            font_p = st.text_input("字体路径", value=get_default_font())

        st.markdown('<span class="section-label">字体大小</span>', unsafe_allow_html=True)
        min_f_size = st.slider("最小字体", 4, 100, 12)
        max_f_size = st.slider("最大字体", 50, 500, 200)

    with c2:
        st.markdown('<span class="section-label">色彩方案</span>', unsafe_allow_html=True)
        bg_color          = st.color_picker("画布外部背景", "#FFFFFF")
        shape_inner_color = st.color_picker("形状内部底色", "#FDF5E6")
        color_options = ["viridis","Set1","plasma","Dark2","spring","magma","coolwarm","rainbow"]
        text_colormap = st.selectbox("文字颜色主题", color_options)
        colormap_gradients = {
            "viridis":  "linear-gradient(to right,#440154,#31688e,#35b779,#fde725)",
            "Set1":     "linear-gradient(to right,#e41a1c,#377eb8,#4daf4a,#984ea3,#ff7f00)",
            "plasma":   "linear-gradient(to right,#0d0887,#9c179e,#ed7953,#f0f921)",
            "Dark2":    "linear-gradient(to right,#1b9e77,#d95f02,#7570b3,#e7298a,#66a61e)",
            "spring":   "linear-gradient(to right,#ff00ff,#ffff00)",
            "magma":    "linear-gradient(to right,#000004,#51127c,#b73779,#fc8961,#fcfdbf)",
            "coolwarm": "linear-gradient(to right,#3b4cc0,#dddddd,#b40426)",
            "rainbow":  "linear-gradient(to right,#ff0000,#ff7f00,#ffff00,#00ff00,#0000ff,#4b0082,#8b00ff)"
        }
        st.markdown(
            f'<div class="gradient-bar" style="background:{colormap_gradients[text_colormap]};"></div>',
            unsafe_allow_html=True)

    with c3:
        st.markdown('<span class="section-label">掩码模版</span>', unsafe_allow_html=True)
        mask_threshold = st.slider("抠图白底容差", 150, 255, 180, step=5,
                                   help="若形状中间有空洞，请调大此值")
        mask_mode = st.radio(
            "获取方式",
            ["手动选择本地模版", "上传自定义照片", "AI匹配本地模版", "AI生成新掩码图"],
            label_visibility="collapsed"
        )

# ── 掩码来源处理 ─────────────────────────────────────────────
supported_formats = ('.png', '.jpg', '.jpeg', '.webp')
mask_image_to_use = None

# 高清放大倍数：把 mask 放大到此目标边长再生成词云
TARGET_LONG_SIDE = 3000

def upscale_mask_array(arr: np.ndarray, target: int = TARGET_LONG_SIDE) -> np.ndarray:
    """将 mask 数组等比放大到长边=target，保持内容不失真。"""
    h, w = arr.shape[:2]
    scale = target / max(h, w)
    if scale <= 1.0:
        return arr
    new_w, new_h = int(w * scale), int(h * scale)
    img = Image.fromarray(arr)
    img = img.resize((new_w, new_h), Image.NEAREST)
    return np.array(img)

if mask_mode == "手动选择本地模版":
    mask_dir = os.path.join(ROOT_DIR, "masks")
    if os.path.exists(mask_dir):
        # 第一级：列出所有直接子文件夹
        sub_folders = sorted([
            d for d in os.listdir(mask_dir)
            if os.path.isdir(os.path.join(mask_dir, d))
        ])
        if sub_folders:
            selected_folder = st.selectbox("📂 选择分类文件夹：", sub_folders)
            folder_path = os.path.join(mask_dir, selected_folder)
            # 第二级：列出该文件夹下的图片
            folder_files = sorted([
                f for f in os.listdir(folder_path)
                if f.lower().endswith(supported_formats)
            ])
            if folder_files:
                selected_file = st.selectbox("🖼️ 选择模版图片：", folder_files)
                mask_image_to_use = Image.open(os.path.join(folder_path, selected_file))
                st.image(mask_image_to_use, caption="当前图形预览", width=120)
            else:
                st.warning(f"文件夹 '{selected_folder}' 下没有找到图片。")
        else:
            # 没有子文件夹，直接扫描根目录图片（兼容旧结构）
            root_files = sorted([
                f for f in os.listdir(mask_dir)
                if f.lower().endswith(supported_formats)
            ])
            if root_files:
                selected_file = st.selectbox("🖼️ 选择模版图片：", root_files)
                mask_image_to_use = Image.open(os.path.join(mask_dir, selected_file))
                st.image(mask_image_to_use, caption="当前图形预览", width=120)
            else:
                st.warning("目录 'masks' 下没有找到图片或子文件夹。")
    else:
        st.warning("未找到 masks 文件夹。")

elif mask_mode == "上传自定义照片":
    uploaded = st.file_uploader("点击上传图片 (支持 WebP, PNG, JPG)", type=["png","jpg","jpeg","webp"])
    if uploaded:
        mask_image_to_use = Image.open(uploaded)
        st.image(mask_image_to_use, caption="上传成功", width=120)

# ── 分词与词频 ────────────────────────────────────────────────
seg_list = jieba.lcut(text_area)
counts = dict(Counter([w for w in seg_list if len(w) > 1 and w.strip()]).most_common())

if not counts:
    st.info("文本分词结果为空，请检查输入内容。")
    st.stop()

st.markdown('<span class="section-label">词汇筛选</span>', unsafe_allow_html=True)
max_words = st.slider("选择展示词语的数量：", min_value=1, max_value=len(counts),
                      value=min(50, len(counts)), label_visibility="collapsed")
words_to_show = st.multiselect(
    "筛选词汇：",
    options=list(counts.keys()),
    default=list(counts.keys())[:max_words],
    format_func=lambda w: f"{w} ({counts[w]})"
)

mask_display_container = st.container()

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
if st.button("🚀 生成高清词云", type="primary", use_container_width=True):
    if not words_to_show:
        st.error("词汇列表为空")
    else:
        try:
            with st.spinner("正在执行高精度抠图与图层合成..."):
                filtered_data = {w: counts[w] for w in words_to_show}

                if mask_mode == "AI匹配本地模版":
                    mask_dir = os.path.join(ROOT_DIR, "masks")
                    if not os.path.exists(mask_dir):
                        st.error("未找到 'masks' 文件夹。"); st.stop()
                    # 递归扫描所有子文件夹
                    all_mask_files = []
                    for root, dirs, files_in_dir in os.walk(mask_dir):
                        for f in files_in_dir:
                            if f.lower().endswith(supported_formats):
                                rel_path = os.path.relpath(os.path.join(root, f), mask_dir)
                                all_mask_files.append(rel_path)
                    if not all_mask_files:
                        st.error("目录 'masks' 及其子文件夹下没有找到图片。"); st.stop()
                    cache_hit = (st.session_state.get("ai_cache_text") == text_area and
                                 st.session_state.get("ai_cache_mode") == mask_mode and
                                 st.session_state.get("ai_cache_image") is not None)
                    if cache_hit:
                        mask_image_to_use = st.session_state["ai_cache_image"]
                        matched_file = st.session_state["ai_cache_filename"]
                    else:
                        matched_file = ai_match_mask_filename(text_area, all_mask_files)
                        mask_image_to_use = Image.open(os.path.join(mask_dir, matched_file))
                        st.session_state["ai_cache_text"]     = text_area
                        st.session_state["ai_cache_mode"]     = mask_mode
                        st.session_state["ai_cache_image"]    = mask_image_to_use
                        st.session_state["ai_cache_filename"] = matched_file

                elif mask_mode == "AI生成新掩码图":
                    cache_hit = (st.session_state.get("ai_cache_text") == text_area and
                                 st.session_state.get("ai_cache_mode") == mask_mode and
                                 st.session_state.get("ai_cache_image") is not None)
                    if cache_hit:
                        mask_image_to_use = st.session_state["ai_cache_image"]
                    else:
                        mask_image_to_use = generate_mask_image_by_ai(text_area)
                        st.session_state["ai_cache_text"]  = text_area
                        st.session_state["ai_cache_mode"]  = mask_mode
                        st.session_state["ai_cache_image"] = mask_image_to_use

                mask_array = None
                if mask_image_to_use:
                    raw_array  = process_mask_to_array(mask_image_to_use, threshold=mask_threshold)
                    # ↓ 关键：放大到高分辨率，解决模糊问题
                    mask_array = upscale_mask_array(raw_array, TARGET_LONG_SIDE)

                wc = WordCloud(
                    font_path=font_p,
                    background_color=None,
                    mode="RGBA",
                    mask=mask_array,
                    colormap=text_colormap,
                    width=1000  if mask_array is None else mask_array.shape[1],
                    height=1000 if mask_array is None else mask_array.shape[0],
                    contour_width=0,
                    relative_scaling=0.15,
                    min_font_size=min_f_size,
                    max_font_size=max_f_size
                )
                wc.generate_from_frequencies(filtered_data)
                wc_layer = wc.to_image()
                w, h = wc_layer.size

                final_canvas = Image.new("RGBA", (w, h), bg_color)
                if mask_array is not None:
                    inner_layer     = Image.new("RGBA", (w, h), shape_inner_color)
                    shape_mask_data = 255 - mask_array[:, :, 0]
                    shape_mask_img  = Image.fromarray(shape_mask_data, mode="L")
                    final_canvas    = Image.composite(inner_layer, final_canvas, shape_mask_img)

                final_result = Image.alpha_composite(final_canvas, wc_layer)
                st.image(final_result, caption="渲染结果", use_container_width=True)

                st.markdown('<div class="dl-section">', unsafe_allow_html=True)
                st.markdown('<div class="dl-title">📥 下载中心</div>', unsafe_allow_html=True)
                dc1, dc2 = st.columns(2)
                png_buf = io.BytesIO()
                final_result.save(png_buf, format="PNG")
                dc1.download_button("🖼️ 下载 PNG", data=png_buf.getvalue(), file_name="cloud_star.png")
                pdf_buf = io.BytesIO()
                final_result.convert("RGB").save(pdf_buf, format="PDF", resolution=300)
                dc2.download_button("📩 下载 PDF", data=pdf_buf.getvalue(), file_name="cloud_star.pdf")
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"渲染失败: {e}")

# ── AI 掩码预览面板 ──────────────────────────────────────────
with mask_display_container:
    if (mask_mode == "AI生成新掩码图" and
            st.session_state.get("ai_cache_text") == text_area and
            st.session_state.get("ai_cache_mode") == mask_mode and
            st.session_state.get("ai_cache_image") is not None):
        st.markdown('<div class="mask-preview-card">', unsafe_allow_html=True)
        st.success("当前缓存的 AI 掩码图如下（随意调整上方参数，该图不会消失）：")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(st.session_state["ai_cache_image"], width=200)
        with col2:
            st.markdown("##### ✏️ 对生成的掩码图不满意？")
            modify_prompt = st.text_input("输入修改指令（例如：换成大脑的形状、线条更简单等）：")
            if st.button("🔄 根据指令重新生成掩码图"):
                with st.spinner("AI 正在根据您的指令重新作画..."):
                    combined_text = f"原始文本内容：{text_area}\n\n【用户特别修改指令，请务必优先满足】：{modify_prompt}"
                    new_img = generate_mask_image_by_ai(combined_text)
                    st.session_state["ai_cache_image"] = new_img
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif (mask_mode == "AI匹配本地模版" and
          st.session_state.get("ai_cache_text") == text_area and
          st.session_state.get("ai_cache_mode") == mask_mode and
          st.session_state.get("ai_cache_image") is not None):
        st.markdown('<div class="mask-preview-card">', unsafe_allow_html=True)
        st.success(f"当前缓存的 AI 匹配掩码文件：{st.session_state.get('ai_cache_filename')}（随意调整上方参数，该图不会消失）")
        st.image(st.session_state["ai_cache_image"], width=200)
        st.markdown('</div>', unsafe_allow_html=True)
