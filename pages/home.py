# pages/home.py
import streamlit as st

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #080b14 !important; color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.hero-wrap {
    min-height: 100vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 60px 24px 40px;
    background:
        radial-gradient(ellipse 80% 60% at 20% 30%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 70%, rgba(16,185,129,0.12) 0%, transparent 55%),
        #080b14;
    text-align: center;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3);
    border-radius: 999px; padding: 5px 16px;
    font-size: 0.72rem; font-weight: 500; color: #a5b4fc;
    letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 28px;
}
.hero-title {
    font-size: clamp(2.4rem, 5vw, 4rem); font-weight: 800; line-height: 1.15;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 40%, #34d399 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 20px;
}
.hero-sub {
    font-size: 1.05rem; color: rgba(226,232,240,0.5);
    max-width: 520px; line-height: 1.8; margin: 0 auto 40px;
}
.input-label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: rgba(226,232,240,0.28);
    margin-bottom: 10px; display: block; text-align: left;
    width: 100%;
}

/* ── 把按钮本身做成卡片 ── */
div[data-testid="stButton"].card-wc-btn > button,
div[data-testid="stButton"].card-vos-btn > button {
    width: 100% !important;
    height: auto !important;
    min-height: 320px !important;
    border-radius: 20px !important;
    padding: 36px 32px !important;
    text-align: left !important;
    white-space: pre-wrap !important;
    line-height: 1.6 !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    transition: transform 0.25s, box-shadow 0.25s, border-color 0.25s !important;
    position: relative !important;
    overflow: hidden !important;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: rgba(226,232,240,0.45) !important;
    cursor: pointer !important;
}
div[data-testid="stButton"].card-wc-btn > button {
    border-top: 2px solid #6366f1 !important;
}
div[data-testid="stButton"].card-vos-btn > button {
    border-top: 2px solid #10b981 !important;
}
div[data-testid="stButton"].card-wc-btn > button:hover {
    transform: translateY(-6px) !important;
    border-color: #818cf8 !important;
    box-shadow: 0 24px 60px rgba(99,102,241,0.2) !important;
    background: rgba(255,255,255,0.05) !important;
}
div[data-testid="stButton"].card-vos-btn > button:hover {
    transform: translateY(-6px) !important;
    border-color: #34d399 !important;
    box-shadow: 0 24px 60px rgba(16,185,129,0.2) !important;
    background: rgba(255,255,255,0.05) !important;
}

/* 文本框 */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-size: 0.9rem !important; line-height: 1.7 !important;
    width: 100% !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

.flow-bar {
    display: flex; align-items: center; justify-content: center;
    gap: 0; margin-top: 64px; flex-wrap: wrap; padding-bottom: 60px;
}
.flow-step { display: flex; flex-direction: column; align-items: center; padding: 0 20px; text-align: center; }
.flow-num {
    width: 36px; height: 36px; border-radius: 50%;
    background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 600; color: #a5b4fc; margin-bottom: 8px;
}
.flow-label { font-size: 0.75rem; color: rgba(226,232,240,0.35); line-height: 1.5; }
.flow-arrow { color: rgba(255,255,255,0.12); font-size: 1.1rem; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">✦ Academic Visualization Toolkit</div>
  <div class="hero-title">学术可视化工具箱</div>
  <div class="hero-sub">
    为科研论文设计的专业可视化套件<br/>
    从词频分析到知识图谱，一站式生成顶刊级图表
  </div>
</div>
""", unsafe_allow_html=True)

# ── 文本输入 ──────────────────────────────────────────────────
_, col_input, _ = st.columns([1, 20, 1])
with col_input:
    st.markdown('<span class="input-label">粘贴文本内容</span>', unsafe_allow_html=True)
    default_text = "Ageing is accompanied by declining memory function, with extremely heterogeneous manifestation in the human population. Brain-extrinsic factors influencing cognitive decline, such as gastrointestinal signals, have emerged as attractive targets for peripheral interventions, but the underlying mechanisms remain largely unclear. Here, by charting a high-resolution map of microbiome ageing and its functional consequences throughout the lifespan of mice, we identify a mechanism by which inhibition of gut–brain signalling during ageing results in impaired neuronal activation in the hippocampus and loss of memory encoding."
    text_input = st.text_area(
        label="text", label_visibility="collapsed",
        height=180, value=st.session_state.get("shared_text", default_text),
        placeholder="在此粘贴论文摘要、正文或任意文字内容..."
    )
    st.session_state["shared_text"] = text_input

# ── 功能卡片（按钮即卡片）────────────────────────────────────
_, col_cards, _ = st.columns([1, 20, 1])
with col_cards:
    col1, col2 = st.columns(2, gap="large")

    wc_label = "☁️  词云生成器\n\n输入任意文本，自动分词并生成高清词云图。支持自定义形状掩码、多种配色方案，以及 AI 智能生成专属剪影轮廓，一键导出 PNG / PDF。\n\n自动分词   AI 生成掩码   8 种配色   PNG / PDF"
    vos_label = "🕸️  VOSviewer 知识图谱\n\n自动计算关键词共现矩阵，生成符合 VOSviewer 标准的网络数据集，直接在页面内嵌的交互式图谱中可视化词与词之间的语义关联。\n\n共现矩阵   网络可视化   JSON 导出   交互式图谱"

    with col1:
        st.markdown('<div class="card-wc-btn">', unsafe_allow_html=True)
        if st.button(wc_label, key="btn_wc", use_container_width=True):
            st.session_state["shared_text"] = text_input
            st.switch_page("pages/wordcloud_page.py")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card-vos-btn">', unsafe_allow_html=True)
        if st.button(vos_label, key="btn_vos", use_container_width=True):
            st.session_state["shared_text"] = text_input
            st.switch_page("pages/vosviewer_page.py")
        st.markdown('</div>', unsafe_allow_html=True)

# ── 流程条 ───────────────────────────────────────────────────
st.markdown("""
<div class="flow-bar">
  <div class="flow-step"><div class="flow-num">1</div><div class="flow-label">粘贴文本</div></div>
  <div class="flow-arrow">›</div>
  <div class="flow-step"><div class="flow-num">2</div><div class="flow-label">选择功能<br/>与参数</div></div>
  <div class="flow-arrow">›</div>
  <div class="flow-step"><div class="flow-num">3</div><div class="flow-label">AI 智能<br/>处理分析</div></div>
  <div class="flow-arrow">›</div>
  <div class="flow-step"><div class="flow-num">4</div><div class="flow-label">预览并<br/>下载成果</div></div>
</div>
""", unsafe_allow_html=True)
