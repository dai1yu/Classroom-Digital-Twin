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
def add_box(fig, x, y, z, dx, dy, dz, color, name, opacity=1.0, edge="#8bb7c3"):
    """Add a cuboid with clean edges to the Plotly 3D scene."""
    xs=[x,x+dx,x+dx,x,x,x+dx,x+dx,x]
    ys=[y,y,y+dy,y+dy,y,y,y+dy,y+dy]
    zs=[z,z,z,z,z+dz,z+dz,z+dz,z+dz]
    ii=[0,0,0,1,1,2,4,4,5,5,6,3]
    jj=[1,2,4,2,5,3,5,6,6,7,7,7]
    kk=[2,3,5,3,6,7,6,7,7,4,4,0]
    fig.add_trace(go.Mesh3d(x=xs,y=ys,z=zs,i=ii,j=jj,k=kk,
        color=color,opacity=opacity,flatshading=True,name=name,showlegend=False,
        lighting=dict(ambient=0.62,diffuse=0.72,specular=0.22,roughness=0.72),
        hovertemplate=f"{name}<extra></extra>"))
    # subtle outline edges make the equipment read as solid objects
    edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    ex=[]; ey=[]; ez=[]
    for a,b in edges:
        ex += [xs[a],xs[b],None]; ey += [ys[a],ys[b],None]; ez += [zs[a],zs[b],None]
    fig.add_trace(go.Scatter3d(x=ex,y=ey,z=ez,mode="lines",line=dict(color=edge,width=2),
        showlegend=False,hoverinfo="skip"))


def add_ball(fig, x, y, z, color, size=5, name="部件"):
    fig.add_trace(go.Scatter3d(x=[x],y=[y],z=[z],mode="markers",
        marker=dict(size=size,color=color,line=dict(color="#d6f7ff",width=.7),
                    opacity=1,symbol="circle"),
        name=name,showlegend=False,hovertemplate=f"{name}<extra></extra>"))


def add_line(fig, x, y, z, color="#4d8190", width=2, name=None):
    fig.add_trace(go.Scatter3d(x=x,y=y,z=z,mode="lines",
        line=dict(color=color,width=width),showlegend=False,hoverinfo="skip",name=name))


def make_lab_scene():
    """A fuller classroom scene: room shell, windows, lighting, consoles, desks and CCTV."""
    fig=go.Figure()

    # --- Room floor and industrial safety markings ---
    add_box(fig,-12.4,-9.2,-0.18,24.8,18.4,.18,"#203f4d","实训室防滑地面",edge="#527987")
    # floor tile grid
    for x in range(-12,13):
        add_line(fig,[x,x],[-9,9],[.012,.012],"#456875",1)
    for y in range(-9,10):
        add_line(fig,[-12,12],[y,y],[.014,.014],"#456875",1)
    # yellow safety walkways and machine bays
    for x in [-10.9,10.9]:
        add_line(fig,[x,x],[-8,8],[.04,.04],"#f0ca45",5)
    add_line(fig,[-10,10],[-7.4,-7.4],[.045,.045],"#f0ca45",5)
    add_line(fig,[-10,10],[7.2,7.2],[.045,.045],"#f0ca45",5)
    # machine bay boundary stripes
    for x in [-8.4,-2.8,2.8,8.4]:
        add_line(fig,[x,x],[-5.7,5.7],[.035,.035],"#c3a943",2)

    # --- Back and side walls ---
    add_box(fig,-12.4,8.75,0,24.8,.22,6.5,"#183746","后墙",opacity=.92,edge="#4a7785")
    add_box(fig,-12.4,-9.0,0,.22,18,6.5,"#173645","左侧墙",opacity=.72,edge="#426d7a")
    add_box(fig,12.18,-9.0,0,.22,18,6.5,"#173645","右侧墙",opacity=.72,edge="#426d7a")
    # wall cladding panels and skirting
    for x in range(-11,12,2):
        add_line(fig,[x,x],[8.61,8.61],[.2,6.2],"#315d6b",2)
    add_box(fig,-12.2,8.48,0,24.4,.18,.42,"#294e5c","后墙踢脚线",edge="#7199a4")

    # --- Windows along the rear wall ---
    for x in [-8.7,-3.0,2.7,8.4]:
        add_box(fig,x,8.48,3.45,4.35,.08,2.15,"#0b2d42","高窗玻璃",opacity=.96,edge="#56a4b7")
        add_box(fig,x,8.39,4.42,4.35,.10,.08,"#5d8793","窗框横梁",edge="#9ac4ce")
        add_box(fig,x+2.05,8.39,3.45,.08,.10,2.15,"#5d8793","窗框竖梁",edge="#9ac4ce")
        # cool daylight reflection
        add_line(fig,[x+.2,x+1.7],[8.34,8.34],[5.35,5.35],"#3b93a8",3)

    # --- Door, wall sign and electrical trunking ---
    add_box(fig,9.55,8.42,.05,2.0,.14,2.75,"#102a38","实训室安全门",edge="#7ba6b1")
    add_box(fig,9.72,8.32,.25,1.65,.08,2.35,"#234d5c","安全门门板",edge="#a1c8d0")
    add_box(fig,9.83,8.22,1.25,.12,.08,.12,"#d6c36a","门把手",edge="#fff0a8")
    add_box(fig,-10.8,8.40,2.35,3.2,.10,.72,"#12384b","安全管理标牌",edge="#32c9dc")
    add_line(fig,[-11.8,11.7],[8.30,8.30],[6.12,6.12],"#b34e39",4)
    add_line(fig,[-11.8,11.7],[8.26,8.26],[5.85,5.85],"#d4a34a",2)

    # --- Ceiling structure: open rafters keep the classroom visible ---
    for x in [-11,-7,-3,1,5,9,11]:
        add_box(fig,x,-9,6.15,.20,18,.20,"#466875","天花板横梁",edge="#82aab4")
    for y in [-8,-4,0,4,8]:
        add_box(fig,-12.2,y,6.30,24.4,.16,.16,"#345764","天花板纵梁",edge="#7096a2")
    # industrial LED light strips
    for x in [-8,-2,4,9]:
        add_box(fig,x-1.15,-.12,6.02,2.3,.42,.10,"#9ac4cc","LED工业灯具",edge="#d6fbff")
        add_box(fig,x-.95,-.06,5.98,1.9,.30,.035,"#38d9ec","灯光发光面",opacity=.95,edge="#8effff")
    # visible suspended ventilation ducts
    add_box(fig,-11.7,5.8,5.25,23.4,.48,.48,"#385d6b","主通风管道",edge="#8eb5bf")
    for x in [-8,-2,4,9]:
        add_box(fig,x,5.88,4.88,.32,.32,.42,"#527987","通风支管",edge="#9bc5cf")

    # --- Training stations: three at rear, four at front ---
    positions=[(-7.6,2.2),(-2.55,2.2),(2.55,2.2),(7.6,2.2),
               (-7.6,-3.25),(-2.55,-3.25),(2.55,-3.25)]
    for idx,(x,y) in enumerate(positions,1):
        # base plinth and cabinet body
        add_box(fig,x-1.12,y-.82,.08,2.24,1.64,.24,"#1b3440",f"实训台{idx}底座",edge="#7d9da7")
        add_box(fig,x-1.02,y-.72,.32,2.04,1.44,2.42,"#567f8d",f"HPY-RS03控制柜{idx}",edge="#b2d2d8")
        # top cap and side service panel
        add_box(fig,x-1.08,y-.76,2.73,2.16,1.52,.16,"#789eaa",f"实训台{idx}顶部盖板",edge="#d0e7eb")
        add_box(fig,x+.77,y-.66,.52,.20,1.28,1.92,"#294b5a",f"实训台{idx}侧检修板",edge="#8bb3bd")
        # front access door, darker viewing window and vertical handles
        add_box(fig,x- .82,y-.755,.55,1.18,.055,1.92,"#315e6e",f"实训台{idx}前门",edge="#a9cbd2")
        add_box(fig,x-.70,y-.79,1.08,.94,.035,1.12,"#0b2637",f"实训台{idx}观察窗",edge="#64a2b1")
        add_line(fig,[x-.22,x-.22],[y-.81,y-.81],[1.18,2.10],"#6fa4b1",2)
        add_box(fig,x+.52,y-.80,.80,.055,.07,.17,"#d6e6e9",f"实训台{idx}门把手",edge="#f1ffff")
        # upper display housing with cyan screen
        add_box(fig,x-.70,y-.91,2.02,1.18,.18,.62,"#142c3a",f"实训台{idx}显示器外壳",edge="#9bc5cf")
        add_box(fig,x-.60,y-1.015,2.12,.98,.035,.40,"#08202f",f"实训台{idx}显示屏",edge="#20c8df")
        # screen UI traces
        add_line(fig,[x-.48,x-.18,x+.12,x+.42],[y-1.06]*4,[2.38,2.46,2.40,2.52],"#25d9e9",3)
        add_line(fig,[x-.48,x-.18,x+.12,x+.42],[y-1.065]*4,[2.25,2.30,2.27,2.35],"#3a8da7",2)
        # control keypad plate and key buttons
        add_box(fig,x+.48,y-.93,1.35,.42,.17,.78,"#172c38",f"实训台{idx}按键面板",edge="#aacbd2")
        for r in range(3):
            for c in range(3):
                col=["#c9e8eb","#27c9dc","#e3bd51"][(r+c)%3]
                add_ball(fig,x+.55+c*.13,y-1.045,1.94-r*.17,col,3.2,"操作按键")
        # emergency stop: yellow collar + red mushroom
        add_ball(fig,x+.67,y-1.08,1.47,"#e8b83d",7,"急停按钮保护圈")
        add_ball(fig,x+.67,y-1.105,1.52,"#f0444e",5.5,"红色急停按钮")
        # manual pulse generator handwheel, ring and hub
        add_ball(fig,x+.94,y-1.02,1.03,"#182a34",8,"手轮外圈")
        add_ball(fig,x+.94,y-1.07,1.03,"#c4dce1",3.4,"手轮中心")
        add_line(fig,[x+.94,x+.94],[y-1.08,y-1.08],[.88,1.18],"#b5d4dc",2)
        # status stack light on top, red / amber / green
        add_box(fig,x-.84,y-.52,2.89,.08,.08,.36,"#253e49","三色灯灯杆",edge="#b1cbd0")
        add_ball(fig,x-.80,y-.48,3.30,"#f34c58",5.5,"红色信号灯")
        add_ball(fig,x-.80,y-.48,3.43,"#ffc24e",5.5,"黄色信号灯")
        add_ball(fig,x-.80,y-.48,3.56,"#20e5a6",5.5,"绿色信号灯")
        # lower ventilation grille and feet
        for k in range(4):
            add_line(fig,[x-.62+k*.16,x-.62+k*.16],[y-.80,y-.80],[.48,.76],"#9bbcc5",1)
        for fx in [x-.82,x+.72]:
            add_box(fig,fx,y-.56,.02,.16,.92,.10,"#101f29","设备支脚",edge="#5b7e89")
        # floor position label
        add_box(fig,x-1.0,y-1.18,.025,2.0,.20,.025,"#d6b94a",f"工位{idx:02d}地标线",edge="#f8e28a")

    # --- Work tables, chairs and instructor station ---
    def furniture_table(tx,ty,label):
        add_box(fig,tx-.95,ty-.48,.78,1.9,.96,.12,"#527887",label+"桌面",edge="#b1d0d7")
        for lx in [tx-.82,tx+.72]:
            for ly in [ty-.35,ty+.28]:
                add_box(fig,lx,ly,.08,.10,.10,.70,"#304d5a",label+"桌腿",edge="#6f929d")
        add_box(fig,tx-.52,ty-.24,.91,1.05,.05,.46,"#102c3b",label+"桌面显示器",edge="#7fb0bc")
        add_box(fig,tx-.42,ty-.30,.99,.85,.035,.32,"#071a29",label+"屏幕",edge="#27bcd2")
    furniture_table(-10.0,1.5,"学生讨论桌A")
    furniture_table(10.0,1.5,"学生讨论桌B")
    # chairs with seat, back and four legs
    for cx,cy in [(-10.2,-.3),(-8.7,-.3),(8.7,-.3),(10.2,-.3),(-10.2,3.1),(10.2,3.1)]:
        add_box(fig,cx-.28,cy-.25,.48,.56,.52,.13,"#315a6a","实训椅坐垫",edge="#8fb4bf")
        add_box(fig,cx-.28,cy+.18,.62,.56,.12,.72,"#426e7d","实训椅靠背",edge="#9bc1ca")
        for lx in [cx-.20,cx+.18]:
            for ly in [cy-.16,cy+.12]:
                add_box(fig,lx,ly,.08,.07,.07,.42,"#243d49","椅腿",edge="#688995")
    # instructor desk at front-left side
    add_box(fig,-10.8,-6.25,.10,3.0,1.25,.95,"#385f70","教师讲台",edge="#9fc2ca")
    add_box(fig,-10.3,-6.42,1.08,1.65,.16,.82,"#102a39","教师电脑显示器",edge="#7db5c3")
    add_box(fig,-10.22,-6.52,1.18,1.48,.04,.62,"#061b2a","教师显示屏",edge="#27c6dc")
    add_box(fig,-9.65,-5.95,1.03,.8,.48,.08,"#263f4b","键盘",edge="#8caeb8")

    # --- CCTV cameras mounted high in corners with brackets ---
    for cx,cy in [(-11.5,7.8),(11.5,7.8),(-11.5,-7.8),(11.5,-7.8)]:
        add_box(fig,cx-.12,cy-.12,5.65,.24,.24,.42,"#536f7a","摄像头支架",edge="#a6c6ce")
        add_box(fig,cx-.30,cy-.35,5.48,.60,.52,.24,"#a2c3ca","监控摄像头",edge="#d9f4f7")
        add_ball(fig,cx,cy-.38,5.59,"#f34e5a",3.4,"摄像头指示灯")
        add_line(fig,[cx,cx],[cy-.4,cy-1.1],[5.5,4.65],"#317e91",1)

    # subtle room labels
    fig.add_trace(go.Scatter3d(x=[-10.5],y=[8.28],z=[3.0],mode="text",
        text=["智能制造实训区"],textfont=dict(color="#c4f4fb",size=11),showlegend=False,hoverinfo="skip"))
    fig.update_layout(
        height=650, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="#041725",
            xaxis=dict(visible=False,range=[-13,13]),
            yaxis=dict(visible=False,range=[-10,10]),
            zaxis=dict(visible=False,range=[0,7]),
            camera=dict(eye=dict(x=1.62,y=-2.25,z=1.32),center=dict(x=0,y=0,z=0.34),up=dict(x=0,y=0,z=1)),
            aspectmode="manual",aspectratio=dict(x=1.72,y=1.30,z=.78),
            dragmode="orbit"
        ),showlegend=False,
        font=dict(color="#c9edf4")
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
    st.caption("完整实训室空间｜7 台 HPY-RS03 恒佩优立式一体化实训控制台｜桌椅、讲台、门窗、顶棚灯具、通风管道及 CCTV")
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
