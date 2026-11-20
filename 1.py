# -*- coding: utf-8 -*-
"""
课堂数字孪生可视化大屏（Streamlit 云端版）
部署方式：
1. 将本文件命名为 app.py
2. 将 requirements.txt 一并上传到 GitHub 仓库根目录
3. Streamlit Community Cloud 选择 app.py 作为启动文件
本版本不依赖 pygame，适用于 Streamlit Cloud。
"""

import math
import random
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="课堂数字孪生可视化平台",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans SC', sans-serif; }
.stApp {
  background: radial-gradient(ellipse at 50% 25%, #092a40 0%, #041725 48%, #020b14 100%);
  color: #d9f7ff;
}
.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
header, footer {visibility: hidden;}
h1,h2,h3,p,label,span { color: #d9f7ff; }
.topbar {
  border-bottom: 1px solid #0d718c; padding: 8px 4px 14px 4px; margin-bottom: 12px;
  background: linear-gradient(90deg, rgba(4,30,47,.95), rgba(3,18,31,.6));
}
.brand {font-size: 28px; font-weight: 900; letter-spacing: 3px; color:#d9fbff;
 text-shadow: 0 0 12px #00cde8;}
.en {font-family: Orbitron,sans-serif; font-size:9px; letter-spacing:2px; color:#30b7ce;}
.panel {
 background: linear-gradient(145deg, rgba(6,38,57,.96), rgba(3,22,37,.96));
 border: 1px solid #11647b; border-radius: 7px; padding: 13px 15px;
 box-shadow: 0 0 15px rgba(0,190,220,.07), inset 0 0 18px rgba(0,120,150,.04);
 margin-bottom: 12px;
}
.panel-title {font-size:16px; font-weight:700; color:#c9f7ff; border-bottom:1px solid #174b60;
 padding-bottom:9px; margin-bottom:10px;}
.panel-title small {float:right; font-size:9px; color:#38b7c8; letter-spacing:1px; font-weight:400;}
.metric {
 background: linear-gradient(135deg, #0a3449, #082638); border:1px solid #14536a;
 border-radius:5px; padding:10px 12px; min-height:78px;
}
.metric-label {font-size:11px;color:#82b9c8;}
.metric-value {font-size:25px;font-weight:800;color:#d8faff;margin-top:2px;}
.metric-unit {font-size:10px;color:#34d5e5;margin-left:4px;}
.device-row {padding:8px 7px; border:1px solid #12455a; border-radius:4px;
 background:#062538; margin:5px 0; font-size:11px;}
.dot {display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:8px;background:#23e4ae;
 box-shadow:0 0 8px #23e4ae;}
.dot-warn {background:#ffbd4c;box-shadow:0 0 8px #ffbd4c;}
.status {float:right;color:#2de4bd;font-weight:700;}
.alert {border-left:3px solid #ffbd4c;background:#102c3b;padding:8px 9px;margin:6px 0;
 font-size:11px;border-radius:3px;}
.alert-ok {border-left-color:#21dba9;}
button[kind="secondary"], .stButton button {
 background:linear-gradient(135deg,#073d59,#07516b)!important;
 color:#d8fbff!important;border:1px solid #1a9db7!important;border-radius:4px!important;
 font-weight:700!important;
}
.stButton button:hover {border-color:#4cf2ff!important;box-shadow:0 0 12px #087b96!important;}
div[data-testid="stPlotlyChart"] {border:1px solid #124c63;border-radius:5px;overflow:hidden;}
div[data-testid="stMetric"] {background:#08283a;border:1px solid #14536a;padding:10px;border-radius:5px;}
div[data-testid="stMetricLabel"] {color:#8fc4d2;}
div[data-testid="stMetricValue"] {color:#d9fbff;}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
h1, h2 = st.columns([3, 2])
with h1:
    st.markdown('<div class="topbar"><div class="brand">智能制造课堂数字孪生平台</div><div class="en">INTELLIGENT MANUFACTURING · DIGITAL TWIN TRAINING CENTER</div></div>', unsafe_allow_html=True)
with h2:
    st.markdown(f'<div style="text-align:right;padding-top:14px;color:#58c9d8;font-size:12px;">实训总览　　设备管理　　数据分析　　视频监控<br><br>{datetime.now().strftime("%Y/%m/%d　%H:%M:%S")}</div>', unsafe_allow_html=True)

# ---------- State / interactions ----------
if "alarm_on" not in st.session_state: st.session_state.alarm_on = False
if "patrol_on" not in st.session_state: st.session_state.patrol_on = False
if "task_no" not in st.session_state: st.session_state.task_no = 28
if "camera" not in st.session_state: st.session_state.camera = "实训室全景"

# ---------- 3D scene ----------
def add_box(fig, x, y, z, dx, dy, dz, color, name, opacity=1.0):
    # Eight vertices and twelve triangles for a cuboid
    xs=[x,x+dx,x+dx,x,x,x+dx,x+dx,x]
    ys=[y,y,y+dy,y+dy,y,y,y+dy,y+dy]
    zs=[z,z,z,z,z+dz,z+dz,z+dz,z+dz]
    ii=[0,0,0,1,1,2,4,4,5,5,6,3]
    jj=[1,2,4,2,5,3,5,6,6,7,7,7]
    kk=[2,3,5,3,6,7,6,7,7,4,4,0]
    fig.add_trace(go.Mesh3d(x=xs,y=ys,z=zs,i=ii,j=jj,k=kk,
        color=color,opacity=opacity,flatshading=True,name=name,showlegend=False,
        hovertemplate=f"{name}<extra></extra>"))

def make_lab_scene():
    fig=go.Figure()
    # Floor plane
    fig.add_trace(go.Mesh3d(x=[-12,12,12,-12],y=[-8,-8,8,8],z=[0,0,0,0],
        i=[0,0],j=[1,2],k=[2,3],color="#183b4a",opacity=1,showlegend=False,hoverinfo="skip"))
    # Floor grid
    for x in range(-12,13,1):
        fig.add_trace(go.Scatter3d(x=[x,x],y=[-8,8],z=[.025,.025],mode="lines",
            line=dict(color="#315c68",width=1),showlegend=False,hoverinfo="skip"))
    for y in range(-8,9,1):
        fig.add_trace(go.Scatter3d(x=[-12,12],y=[y,y],z=[.025,.025],mode="lines",
            line=dict(color="#315c68",width=1),showlegend=False,hoverinfo="skip"))
    # Safety lanes
    for x in [-10.5,10.5]:
        fig.add_trace(go.Scatter3d(x=[x,x],y=[-7,7],z=[.05,.05],mode="lines",
            line=dict(color="#e4c64b",width=5),showlegend=False,hoverinfo="skip"))
    # Training consoles, arranged in two rows
    positions=[(-8,-3),(-4,-3),(0,-3),(4,-3),(8,-3),(-5,3),(2,3)]
    for idx,(x,y) in enumerate(positions,1):
        add_box(fig,x-.9,y-.65,.08,1.8,1.3,2.15,"#527d8b",f"HPY-RS03 实训控制台 {idx}")
        # dark screen panel
        add_box(fig,x-.52,y-.68,1.48,1.05,.055,.48,"#071b2a",f"控制屏 {idx}")
        add_box(fig,x-.4,y-.735,1.57,.8,.025,.27,"#13a9c2",f"显示区域 {idx}")
        # front button plate and emergency stop
        add_box(fig,x+.37,y-.75,1.05,.22,.10,.20,"#142a36",f"按键面板 {idx}")
        fig.add_trace(go.Scatter3d(x=[x+.48],y=[y-.82],z=[1.18],mode="markers",
            marker=dict(size=5,color="#ff4d59"),name="急停按钮",showlegend=False,
            hovertemplate="红色急停按钮<extra></extra>"))
        # handwheel on right side
        fig.add_trace(go.Scatter3d(x=[x+.94,x+.94],y=[y-.12,y-.12],z=[1.45,1.45],
            mode="markers",marker=dict(size=[7,3],color=["#1b2730","#c4e4ed"]),
            showlegend=False,hoverinfo="skip"))
        # stack light (red / amber / green)
        for z,c in [(2.55,"#ff4e57"),(2.68,"#ffc04e"),(2.81,"#25e7a8")]:
            fig.add_trace(go.Scatter3d(x=[x-.72],y=[y-.42],z=[z],mode="markers",
                marker=dict(size=5,color=c),showlegend=False,hoverinfo="skip"))
        # console foot glow
        fig.add_trace(go.Scatter3d(x=[x],y=[y],z=[.06],mode="markers",
            marker=dict(size=14,color="#00bcd4",opacity=.18),showlegend=False,hoverinfo="skip"))
    # Tables and chairs
    for x,y in [(-10,1),(10,1),(-9,5),(9,5)]:
        add_box(fig,x-.7,y-.45,.08,1.4,.9,.85,"#416778","实训桌")
        add_box(fig,x+.85,y-.2,.08,.55,.55,.48,"#294a5a","实训椅")
        add_box(fig,x+.85,y-.2,.56,.55,.12,.62,"#365c6b","椅背")
    # Instructor desk
    add_box(fig,-1,6,.08,2.2,1.0,.95,"#345e70","教师讲台")
    add_box(fig,-.65,5.92,1.05,1.5,.08,.65,"#071b2a","教师显示器")
    # CCTV cameras
    for x,y in [(-11,-6),(11,-6),(-11,6),(11,6)]:
        fig.add_trace(go.Scatter3d(x=[x],y=[y],z=[4.7],mode="markers",
            marker=dict(size=7,color="#9ed9e6",symbol="diamond"),name="监控摄像头",
            showlegend=False,hovertemplate="监控摄像头<extra></extra>"))
    fig.update_layout(
        height=580, margin=dict(l=0,r=0,t=5,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="#041725",
            xaxis=dict(visible=False,range=[-13,13]),
            yaxis=dict(visible=False,range=[-9,9]),
            zaxis=dict(visible=False,range=[0,5.5]),
            camera=dict(eye=dict(x=1.55,y=-1.9,z=1.15),center=dict(x=0,y=0,z=.15)),
            aspectmode="manual",aspectratio=dict(x=1.65,y=1.1,z=.62)
        ),
        showlegend=False
    )
    return fig

# ---------- Layout ----------
left, center, right = st.columns([.95, 2.45, .95], gap="small")

with left:
    st.markdown('<div class="panel"><div class="panel-title">设备统计卡片 <small>DEVICE MONITOR</small></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="metric"><div class="metric-label">设备总数</div><div class="metric-value">07<span class="metric-unit">台</span></div></div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric"><div class="metric-label">在线设备</div><div class="metric-value">06<span class="metric-unit">台</span></div></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="metric"><div class="metric-label">设备运行率</div><div class="metric-value">85.7<span class="metric-unit">%</span></div></div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric"><div class="metric-label">今日实训</div><div class="metric-value">128<span class="metric-unit">人次</span></div></div>',unsafe_allow_html=True)
    st.markdown('<br><div class="panel-title">实训设备列表</div>',unsafe_allow_html=True)
    for i in range(1,8):
        status="待检查" if i==4 else "运行中"
        dot="dot-warn" if i==4 else "dot"
        st.markdown(f'<div class="device-row"><span class="{dot}"></span>HPY-RS03 实训台 {i:02d}<span class="status">{status}</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">实训负荷折线图 <small>TRAINING LOAD</small></div>',unsafe_allow_html=True)
    hours=[f"{8+i//2:02d}:{'00' if i%2==0 else '30'}" for i in range(17)]
    load=[38,42,55,61,58,68,73,65,78,82,75,69,84,88,72,76,81]
    df_load=pd.DataFrame({"时间":hours,"实训负荷":load})
    fig_line=px.line(df_load,x="时间",y="实训负荷",markers=True)
    fig_line.update_traces(line_color="#18d8e6",marker_color="#b4fbff",line_width=3,fill="tozeroy",
        fillcolor="rgba(10,190,210,.12)")
    fig_line.update_layout(height=210,margin=dict(l=0,r=0,t=8,b=0),paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",font_color="#a9dce6",font_size=9,
        xaxis=dict(showgrid=False),yaxis=dict(range=[0,100],gridcolor="#17475a",title=None))
    st.plotly_chart(fig_line,use_container_width=True,config={"displayModeBar":False})
    st.markdown('</div>',unsafe_allow_html=True)

with center:
    st.markdown('<div class="panel"><div class="panel-title">智能制造实训室三维场景 <small>FACTORY 3D DIGITAL TWIN</small></div>',unsafe_allow_html=True)
    st.caption("HPY-RS03 恒佩优立式一体化实训控制台　·　实训工位三维分布　·　设备状态可视化")
    st.plotly_chart(make_lab_scene(),use_container_width=True,config={"displayModeBar":True,"displaylogo":False})
    st.markdown('</div>',unsafe_allow_html=True)
    m1,m2,m3=st.columns(3)
    m1.metric("当前实训任务",f"TASK-{st.session_state.task_no:03d}","智能制造基础实训")
    m2.metric("设备综合健康度","96.8%","+1.2%")
    m3.metric("今日实训人数","128 人次","+12")

with right:
    st.markdown('<div class="panel"><div class="panel-title">实训数据对比 <small>DATA ANALYSIS</small></div>',unsafe_allow_html=True)
    df_bar=pd.DataFrame({"工位":["01","02","03","04","05","06","07"],"实训完成率":[82,91,76,64,88,95,79]})
    fig_bar=px.bar(df_bar,x="工位",y="实训完成率",text="实训完成率")
    fig_bar.update_traces(marker_color="#10b9ce",texttemplate="%{text}%",textposition="outside")
    fig_bar.update_layout(height=245,margin=dict(l=0,r=0,t=18,b=0),paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",font_color="#a9dce6",font_size=9,
        xaxis=dict(title=None,showgrid=False),yaxis=dict(title=None,range=[0,110],gridcolor="#17475a"))
    st.plotly_chart(fig_bar,use_container_width=True,config={"displayModeBar":False})
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">视频监控窗口 <small>LIVE CAMERA</small></div>',unsafe_allow_html=True)
    st.markdown("""
    <div style="height:160px;background:linear-gradient(145deg,#071b29,#102f3d);border:1px solid #1b7185;position:relative;overflow:hidden;">
      <div style="position:absolute;inset:0;background-image:linear-gradient(#1b5360 1px,transparent 1px),linear-gradient(90deg,#1b5360 1px,transparent 1px);background-size:24px 24px;opacity:.45;"></div>
      <div style="position:absolute;left:12%;bottom:17%;width:22%;height:42%;background:#426c7b;border:1px solid #7fc6d2;"></div>
      <div style="position:absolute;left:43%;bottom:17%;width:22%;height:42%;background:#426c7b;border:1px solid #7fc6d2;"></div>
      <div style="position:absolute;right:10%;bottom:17%;width:18%;height:42%;background:#426c7b;border:1px solid #7fc6d2;"></div>
      <div style="position:absolute;top:8px;left:10px;color:#ff6b76;font-size:10px;">● LIVE  CAM-01</div>
      <div style="position:absolute;bottom:7px;left:10px;color:#bcebf3;font-size:10px;">实训室全景监控 · 信号正常</div>
    </div>
    """,unsafe_allow_html=True)
    st.selectbox("监控画面",["实训室全景","工位01","工位02","工位03"],label_visibility="collapsed")
    st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">告警预警列表 <small>ALARM CENTER</small></div>',unsafe_allow_html=True)
    if st.session_state.alarm_on:
        st.markdown('<div class="alert" style="border-left-color:#ff5964;">10:16:08　工位04 设备状态待确认</div>',unsafe_allow_html=True)
    st.markdown('<div class="alert">10:12:08　工位04 急停状态待确认</div><div class="alert alert-ok">09:48:21　工位02 实训任务完成</div><div class="alert alert-ok">09:32:06　网络连接状态正常</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

# ---------- Bottom action bar ----------
st.markdown("---")
b1,b2,b3,b4,sp=st.columns([1,1,1,1,2.4])
with b1:
    if st.button("⚠ 设备告警",use_container_width=True):
        st.session_state.alarm_on=not st.session_state.alarm_on
        st.rerun()
with b2:
    if st.button("✓ 一键巡检",use_container_width=True):
        st.session_state.patrol_on=True
        st.toast("巡检已启动：正在检查 7 个实训工位")
with b3:
    if st.button("◎ 视角复位",use_container_width=True):
        st.toast("三维场景视角已复位")
with b4:
    if st.button("⇧ 实训任务下发",use_container_width=True):
        st.session_state.task_no+=1
        st.toast(f"实训任务 TASK-{st.session_state.task_no:03d} 已下发")
        st.rerun()
with sp:
    st.markdown('<div style="text-align:right;color:#4da9bb;font-size:10px;padding-top:10px;">DIGITAL TWIN SYSTEM　|　数据模拟演示版　|　HPY-RS03</div>',unsafe_allow_html=True)
