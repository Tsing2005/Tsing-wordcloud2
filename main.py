# main.py
import streamlit as st

st.set_page_config(
    page_title="学术可视化工具箱",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏默认侧边栏导航和汉堡菜单
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

pg = st.navigation(
    [
        st.Page("pages/home.py",           title="首页",       icon="🏠", default=True),
        st.Page("pages/wordcloud_page.py", title="词云生成器", icon="☁️"),
        st.Page("pages/vosviewer_page.py", title="知识图谱",   icon="🕸️"),
    ],
    position="hidden"   # 不显示顶部导航栏，完全由按钮控制跳转
)
pg.run()
