# -*- coding: utf-8 -*-
"""
智能制造实训室数字孪生服务平台
运行方式：streamlit run app.py
"""

import random
import datetime as dt

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ------------------------------ 页面配置 ------------------------------
st.set_page_config(
    page_title="实训室数字孪生服务平台",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------ 全局样式 ------------------------------
st.markdown(
    """
    <style>
    .main { background-color: #0a1428; }
    div[data-testid="stMetric"] {
        background-color: #12233f;
        border: 1px solid #1f3b66;
        border-radius: 10px;
        padding: 12px 16px;
    }
    div[data-testid="stMetricLabel"] p { color: #7fb2ff; font-size: 14px; }
    div[data-testid="stMetricValue"] { color: #ffffff; font-size: 26px; }
    .block-container { padding-top: 1rem; }
    h1 { color: #e8f1ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------ 模拟数据 ------------------------------
# 实训控制台（立式一体化实训控制台）
CONSOLES = [
    {"id": "HPY-RS03-01", "status": "在线", "task": "零件缺陷检测", "lamp": "绿"},
    {"id": "HPY-RS03-02", "status": "在线", "task": "数控编程实训", "lamp": "绿"},
    {"id": "HPY-RS03-03", "status": "在线", "task": "数字孪生调试", "lamp": "黄"},
    {"id": "HPY-RS03-04", "status": "故障", "task": "急停触发", "lamp": "红"},
    {"id": "HPY-RS03-05", "status": "在线", "task": "零件缺陷检测", "lamp": "绿"},
    {"id": "HPY-RS03-06", "status": "离线", "task": "—", "lamp": "灰"},
]

# 人员统计
TEACHER_ONLINE = 2
STUDENT_ONLINE = 18
STUDENT_TRAINING = 15

# 告警列表
ALERTS = [
    ("10:24:31", "HPY-RS03-04", "急停按钮被按下", "高危"),
    ("10:18:05", "HPY-RS03-03", "三色灯黄灯：参数越界风险", "警告"),
    ("09:57:42", "HPY-RS03-01", "检出缺陷零件 1 件（YOLO 检测）", "提示"),
    ("09:40:11", "HPY-RS03-06", "设备离线失联", "警告"),
]

# 实训任务负荷（近 12 个时间点）
hours = [(dt.datetime.now() - dt.timedelta(hours=i)).strftime("%H:%M") for i in range(11, -1, -1)]
load_df = pd.DataFrame(
    {
        "时间": hours,
        "零件缺陷检测": [random.randint(1, 5) for _ in hours],
        "数控编程实训": [random.randint(2, 6) for _ in hours],
        "数字孪生调试": [random.randint(0, 4) for _ in hours],
    }
)

# 本周 / 上周实训数据对比
compare_df = pd.DataFrame(
    {
        "指标": ["完成实训组数", "零件检测成功数", "模型训练次数"],
        "本周": [42, 138, 9],
        "上周": [35, 121, 7],
    }
)


# ------------------------------ 图表 ------------------------------
def line_chart() -> go.Figure:
    fig = px.line(
        load_df,
        x="时间",
        y=["零件缺陷检测", "数控编程实训", "数字孪生调试"],
        markers=True,
        title="实训任务负荷监测",
        color_discrete_sequence=["#36a3ff", "#2ee6a8", "#ffb84d"],
    )
    fig.update_layout(
        paper_bgcolor="#12233f",
        plot_bgcolor="#12233f",
        font_color="#dbe9ff",
        legend_title_text="任务类型",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def bar_chart() -> go.Figure:
    fig = px.bar(
        compare_df,
        x="指标",
        y=["本周", "上周"],
        barmode="group",
        title="实训数据周对比",
        color_discrete_sequence=["#36a3ff", "#5c7db5"],
    )
    fig.update_layout(
        paper_bgcolor="#12233f",
        plot_bgcolor="#12233f",
        font_color="#dbe9ff",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


# ------------------------------ 页面渲染 ------------------------------
# 顶部标题
st.title("🏭 智能制造实训室数字孪生服务平台")
st.caption("Smart Manufacturing Training Room Digital Twin Service Platform")

# 第一行：设备统计 / 三维场景 / 人员统计
col_l, col_m, col_r = st.columns([1.1, 2.0, 1.1])

with col_l:
    st.subheader("设备规模统计")
    total = len(CONSOLES)
    online = sum(1 for c in CONSOLES if c["status"] == "在线")
    fault = sum(1 for c in CONSOLES if c["status"] == "故障")
    offline = sum(1 for c in CONSOLES if c["status"] == "离线")
    m1, m2, m3, m4 = st.columns(2)
    m1.metric("实训台总数", total)
    m2.metric("在线设备", online)
    m3.metric("故障告警", fault)
    m4.metric("离线设备", offline)

    st.markdown("**设备状态明细**")
    for c in CONSOLES:
        lamp = {"绿": "🟢", "黄": "🟡", "红": "🔴", "灰": "⚪"}[c["lamp"]]
        st.write(f"{lamp} `{c['id']}` ｜ {c['status']} ｜ {c['task']}")

with col_m:
    st.subheader("三维孪生场景")
    # 场景占位：后续可替换为 Three.js / Unity 导出的网页模型
    st.image(
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=1200&q=60",
        caption="实训室三维场景（占位图，可替换为实训控制台 3D 模型）",
        use_container_width=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.button("🔄 视角复位")
    c2.button("🚶 一键巡检")
    c3.button("📡 设备告警")
    c4.button("📤 任务下发")

with col_r:
    st.subheader("人员状态")
    st.metric("在线老师", TEACHER_ONLINE)
    st.metric("在线学生", STUDENT_ONLINE)
    st.metric("正在实训", STUDENT_TRAINING)

    st.markdown("**当前工位**")
    st.write("👨‍🏫 指导老师：2 人在岗")
    st.write("🧑‍🎓 实训学生：15 人操作中，3 人待命")

# 第二行：折线图 / 视频监控 / 柱状图
col_a, col_b, col_c = st.columns([1.2, 1.0, 1.2])

with col_a:
    st.plotly_chart(line_chart(), use_container_width=True)

with col_b:
    st.subheader("视频监控")
    st.image(
        "https://images.unsplash.com/photo-1558002038-1055907df827?w=600&q=60",
        caption="实训室实时监控（占位，可接入摄像头流）",
        use_container_width=True,
    )
    cam = st.selectbox("切换机位", ["机位 1（主入口）", "机位 2（实训台区）", "机位 3（设备区）"])

with col_c:
    st.plotly_chart(bar_chart(), use_container_width=True)

# 第三行：告警预警列表
st.subheader("⚠️ 告警预警列表")
alert_df = pd.DataFrame(ALERTS, columns=["时间", "设备编号", "告警内容", "级别"])
level_color = {"高危": "#ff4d4f", "警告": "#ffb84d", "提示": "#36a3ff"}
st.dataframe(
    alert_df.style.applymap(lambda v: f"color: {level_color.get(v, '#dbe9ff')}", subset=["级别"]),
    use_container_width=True,
    hide_index=True,
)

# 底部说明
st.caption("说明：本页面数据为演示模拟数据，可对接设备采集接口与 YOLO 缺陷检测结果实时刷新。")
