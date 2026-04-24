# pages/vosviewer_page.py
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(layout="centered", page_title="VOSviewer 知识图谱")

import jieba
from collections import Counter
from utils.shared import generate_vosviewer_json

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #080b14 !important; color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 40px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1100px !important;
    margin: 0 auto !important;
}

.page-header-outer {
    position: relative;
    left: 50%; right: 50%;
    margin-left: -50vw; margin-right: -50vw;
    width: 100vw;
    padding: 28px 10vw;
    background:
        radial-gradient(ellipse 70% 80% at 10% 50%, rgba(16,185,129,0.1) 0%, transparent 60%),
        #080b14;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center;
    box-sizing: border-box;
}
.page-header-left { display: flex; align-items: center; gap: 20px; }
.page-header-icon {
    font-size: 2rem;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.22);
    border-radius: 14px; width: 56px; height: 56px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.page-header-title {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(90deg, #d1fae5, #34d399);
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
.info-card {
    background: rgba(16,185,129,0.04);
    border: 1px solid rgba(16,185,129,0.13);
    border-left: 3px solid rgba(16,185,129,0.45);
    border-radius: 14px; padding: 18px 22px; margin-bottom: 28px;
    font-size: 0.87rem; color: rgba(226,232,240,0.5); line-height: 1.75;
}
.info-card b { color: rgba(226,232,240,0.8); }
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
    background: linear-gradient(135deg, #059669, #0d9488) !important;
    border: none !important; color: #fff !important;
    font-size: 1rem !important; padding: 14px 0 !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.3) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(16,185,129,0.45) !important;
    transform: translateY(-2px) !important;
}
div[data-testid="stAlert"] { border-radius: 12px !important; border: none !important; }
.iframe-wrap {
    border-radius: 16px; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.07); margin-top: 8px;
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
        <div class="page-header-icon">🕸️</div>
        <div>
          <div class="page-header-title">VOSviewer 知识图谱</div>
          <div class="page-header-sub">计算共现矩阵 · 生成网络数据集 · 交互式可视化</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_back:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if st.button("← 返回首页", use_container_width=True):
        st.switch_page("pages/home.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
  如果说词云反映的是「词频」，那么这里的知识图谱反映的是「<b>词与词之间的联系</b>」。
  程序会自动计算文本中的共现关系并生成符合 VOSviewer 标准的网络数据集。
</div>
""", unsafe_allow_html=True)

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

# ── 分词（直接用全量，不做筛选）────────────────────────────
seg_list = jieba.lcut(text_area)
counts = dict(Counter([w for w in seg_list if len(w) > 1 and w.strip()]).most_common())

if not counts:
    st.info("文本分词结果为空，请检查输入内容。")
    st.stop()

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
if st.button("🚀 生成 VOSviewer 网络视图", type="primary", use_container_width=True):
    with st.spinner("正在计算词汇共现矩阵并打包 VOSviewer 数据..."):
        vos_json_str = generate_vosviewer_json(text_area, counts)
        st.success("✅ 图谱数据计算完成！")

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <script src="https://unpkg.com/vosviewer-online@1.1.4/dist/vosviewer-online.umd.js"></script>
          <link rel="stylesheet" href="https://unpkg.com/vosviewer-online@1.1.4/dist/vosviewer-online.css">
          <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ background: #080b14; }}
            #vos-container {{ width: 100%; height: 700px; }}
          </style>
        </head>
        <body>
          <div id="vos-container"></div>
          <script>
            const vosData = {vos_json_str};
            new VOSviewer(document.getElementById("vos-container"), {{
              json: vosData,
              dark_ui: true,
            }});
          </script>
        </body>
        </html>
        """

        st.markdown('<div class="iframe-wrap">', unsafe_allow_html=True)
        st.components.v1.html(
            html_content,
            height=700,
            scrolling=False
        )
        st.markdown('</div>', unsafe_allow_html=True)
