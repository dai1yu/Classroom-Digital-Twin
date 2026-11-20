import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ---------------------- 页面基础配置 ----------------------
st.set_page_config(
    page_title="智能制造实训室数字孪生服务平台",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 全局深色样式
st.markdown("""
<style>
    .main {background-color:#0b101c;}
    .stMetric {background:#101a30;border-radius:8px;padding:10px;color:#fff;}
    .block-container {padding-top:10px; padding-left:20px; padding-right:20px;}
    h1,h2,h3,h4 {color:#40b8ff;}
</style>
""", unsafe_allow_html=True)

# ---------------------- 模拟基础数据 ----------------------
console_data = {
    "总数":6,
    "在线":5,
    "故障":1,
    "离线":0,
    "摄像头":3,
    "巡检锚点":8
}
person_data = {
    "教师":2,
    "学生":24,
    "实训中":18
}

alert_list = [
    "2号实训台：急停按钮按下",
    "4号实训台：三色灯异常",
    "1号实训台：YOLO检出零件缺陷",
    "3号实训台：参数越界告警"
]

# 实训负荷数据
load_df = pd.DataFrame({
    "时间":["11:00","12:00","13:00","14:00","15:00","16:00"],
    "数控任务":[6,8,4,9,7,5],
    "检测任务":[3,5,7,4,6,8],
    "仿真任务":[4,3,6,5,3,6]
})

# 周对比数据
compare_df = pd.DataFrame({
    "月份":["08周","09周","10周","11周","12周"],
    "本周":[32,45,38,52,60],
    "上周":[22,28,30,36,41]
})

# ---------------------- 标题栏 ----------------------
st.markdown("<h1 style='text-align:center;'>智能制造实训室数字孪生服务平台</h1>",unsafe_allow_html=True)

# 分三栏布局
col_left, col_center, col_right = st.columns([1,2,1])

# ========== 左侧面板 ==========
with col_left:
    st.subheader("📊 设备规模")
    for k,v in console_data.items():
        st.metric(k, v)

    st.subheader("👥 人员统计")
    for k,v in person_data.items():
        st.metric(k, v)

    st.subheader("📈 实训负荷监测")
    fig_load = px.line(load_df, x="时间", y=["数控任务","检测任务","仿真任务"])
    fig_load.update_layout(paper_bgcolor="#101a30", plot_bgcolor="#101a30", font_color="white")
    st.plotly_chart(fig_load, use_container_width=True)

# ========== 中间主场景区域 ==========
with col_center:
    st.subheader("🖥️ 实训室三维孪生场景")
    st.info("【三维场景占位】此处嵌入实训室+HPY-RS03实训控制台3D模型，支持旋转缩放、点击设备查看详情")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.button("🔔 设备告警")
    with c2:
        st.button("🚶 一键巡检")
    with c3:
        st.button("🔄 视角复位")
    with c4:
        st.button("📝 实训任务下发")

# ========== 右侧面板 ==========
with col_right:
    st.subheader("📊 实训数据对比")
    fig_bar = px.bar(compare_df, x="月份", y=["本周","上周"], barmode="group")
    fig_bar.update_layout(paper_bgcolor="#101a30", plot_bgcolor="#101a30", font_color="white")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🎥 视频监控")
    st.info("监控画面窗口，可切换机位")

    st.subheader("⚠️ 预警情况")
    for msg in alert_list:
        st.warning(msg)
