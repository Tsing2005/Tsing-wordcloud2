# utils/styles.py

COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #080b14 !important;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

.block-container {
    padding: 2.5rem 4rem !important;
    max-width: 1100px !important;
}

/* ── 顶部导航栏 ── */
.topbar {
    display: flex; align-items: center; gap: 20px;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 36px;
}
.page-title {
    font-size: 1.5rem; font-weight: 800; line-height: 1;
    background: linear-gradient(90deg, #e0e7ff, #a5b4fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.page-title-green {
    font-size: 1.5rem; font-weight: 800; line-height: 1;
    background: linear-gradient(90deg, #d1fae5, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── 通用标签 ── */
.label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: rgba(226,232,240,0.28);
    margin-bottom: 10px; margin-top: 24px; display: block;
}

/* ── 玻璃卡片 ── */
.glass-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px; padding: 28px;
    margin-bottom: 20px;
}
.glass-card-indigo {
    background: rgba(99,102,241,0.05);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 18px; padding: 28px;
    margin-bottom: 20px;
}
.glass-card-green {
    background: rgba(16,185,129,0.05);
    border: 1px solid rgba(16,185,129,0.12);
    border-radius: 18px; padding: 28px;
    margin-bottom: 20px;
}

/* ── 文本预览条 ── */
.text-preview {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid rgba(99,102,241,0.5);
    border-radius: 10px; padding: 14px 18px;
    font-size: 0.82rem; color: rgba(226,232,240,0.38);
    line-height: 1.65; margin-bottom: 28px;
    max-height: 68px; overflow: hidden; position: relative;
}
.text-preview::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 26px; background: linear-gradient(transparent, #080b14);
}

/* ── 渐变色条 ── */
.gradient-bar {
    width: 100%; height: 8px; border-radius: 6px;
    margin-top: -4px; margin-bottom: 14px;
}

/* ── 分割线 ── */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 28px 0;
}

/* ── 按钮全局覆写 ── */
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 11px 20px !important;
    transition: all 0.2s ease !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #e2e8f0 !important;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(255,255,255,0.08) !important;
    transform: translateY(-1px) !important;
}

/* ── 主操作按钮（indigo） ── */
.btn-primary div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border: none !important; color: #fff !important;
    font-size: 0.95rem !important; padding: 14px 0 !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
}
.btn-primary div[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 28px rgba(99,102,241,0.45) !important;
}

/* ── 主操作按钮（green） ── */
.btn-primary-green div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #059669, #0d9488) !important;
    border: none !important; color: #fff !important;
    font-size: 0.95rem !important; padding: 14px 0 !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.3) !important;
}

/* ── 输入框 ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-size: 0.9rem !important; line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* ── selectbox / slider / radio ── */
div[data-testid="stSelectbox"] > div,
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
}
.stRadio > div { gap: 8px !important; }
.stRadio label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important; padding: 6px 14px !important;
    font-size: 0.82rem !important; color: rgba(226,232,240,0.6) !important;
}

/* ── expander ── */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
}
div[data-testid="stExpander"] summary {
    font-size: 0.88rem !important; font-weight: 600 !important;
    color: rgba(226,232,240,0.6) !important;
}

/* ── 下载按钮 ── */
div[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-weight: 600 !important; width: 100% !important;
    padding: 12px 0 !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,255,255,0.08) !important;
}

/* ── success / info / warning ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}
</style>
"""
