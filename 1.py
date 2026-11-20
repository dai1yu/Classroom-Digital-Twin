# -*- coding: utf-8 -*-
"""
课堂数字孪生服务平台 - Streamlit 单文件版
运行：
    pip install streamlit streamlit-autorefresh
    streamlit run app.py

部署：
    将 app.py 上传 GitHub；仓库根目录添加 requirements.txt（内容见下方说明）。
    Streamlit Community Cloud 选择该仓库和 app.py 即可部署。
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import random

st.set_page_config(
    page_title="课堂数字孪生服务平台",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------- 模拟业务数据 ----------------------------
ROOMS = ["智能制造实训室 A", "智能制造实训室 B", "工业机器人实训室"]
students_total = 36
teachers_total = 2
devices_total = 12

if "room" not in st.session_state:
    st.session_state.room = ROOMS[0]
if "page" not in st.session_state:
    st.session_state.page = "智慧总览"

# ---------------------------- 页面样式 ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 50% 0%, #102b4c 0%, #061323 42%, #020812 100%);
    color: #eaf6ff;
    font-family: 'Noto Sans SC', sans-serif;
}
[data-testid="stHeader"] {background: transparent;}
.block-container {padding: .35rem .55rem .5rem; max-width: 100%;}
h1,h2,h3,p, label {color:#eaf6ff;}
.topbar {
    border:1px solid rgba(54,173,255,.55);
    background:linear-gradient(90deg,rgba(8,42,78,.95),rgba(8,22,42,.96),rgba(8,42,78,.95));
    box-shadow:0 0 22px rgba(0,150,255,.22), inset 0 0 20px rgba(0,140,255,.12);
    padding:13px 22px; border-radius:8px; text-align:center;
    font-size:27px; font-weight:900; letter-spacing:4px;
}
.subhead {font-size:11px; color:#7ccfff; letter-spacing:2px; margin-top:2px;}
.metric {
    background:linear-gradient(135deg,rgba(10,46,78,.88),rgba(4,19,36,.94));
    border:1px solid rgba(47,166,255,.45); border-radius:7px;
    padding:12px 14px; min-height:83px; box-shadow:inset 0 0 18px rgba(0,133,255,.08);
}
.metric .k {font-size:12px;color:#9bc9e8;}
.metric .v {font-family:Rajdhani,sans-serif;font-size:29px;font-weight:700;color:#fff;margin-top:3px;}
.metric .u {font-size:11px;color:#55d8ff;margin-left:5px;}
.panel {
    border:1px solid rgba(50,158,238,.45);
    background:linear-gradient(145deg,rgba(9,34,58,.94),rgba(3,14,28,.95));
    border-radius:8px; padding:13px 15px; margin-bottom:12px;
    box-shadow:0 0 16px rgba(0,110,210,.12), inset 0 0 16px rgba(0,110,210,.06);
}
.panel-title {font-weight:800;color:#e9f7ff;font-size:15px;border-left:3px solid #20baff;padding-left:9px;margin-bottom:10px;}
.small {font-size:12px;color:#8fb6d5;}
.status-ok {color:#35e0b0;font-weight:700;}
.status-warn {color:#ffc65c;font-weight:700;}
div[data-testid="stSelectbox"] label, div[data-testid="stRadio"] label {color:#b9dfff!important;}
.stButton>button {
    background:linear-gradient(100deg,#075a9d,#087fc1)!important;color:white!important;
    border:1px solid #31baff!important;border-radius:5px!important;font-weight:700!important;
}
[data-testid="stPlotlyChart"] {background:transparent;}
hr {border-color:rgba(57,158,228,.25);}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------- 顶部标题与导航 ----------------------------
st.markdown(
    '<div class="topbar">课堂数字孪生服务平台'
    '<div class="subhead">CLASSROOM DIGITAL TWIN SERVICE PLATFORM</div></div>',
    unsafe_allow_html=True,
)
nav_cols = st.columns([1,1,1,1,1,1,2])
nav_items = ["智慧总览", "教室管理", "学生管理", "教师管理", "设备管理", "教学分析"]
for i, item in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
with nav_cols[6]:
    st.selectbox("当前教室", ROOMS, key="room", label_visibility="collapsed")

st.markdown("<div style='height:7px'></div>", unsafe_allow_html=True)

# ---------------------------- 中央三维数字孪生场景 ----------------------------
scene_html = r"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box}body{margin:0;background:#020b16;color:#eaf7ff;font-family:Arial,"Microsoft YaHei",sans-serif;overflow:hidden}
#wrap{position:relative;width:100%;height:780px;background:radial-gradient(ellipse at center,#102b45,#020914 75%);border:1px solid #17649a;border-radius:8px;overflow:hidden}
#view{width:100%;height:100%;display:block}
.hud{position:absolute;z-index:3;pointer-events:none;text-shadow:0 1px 4px #000}
.hud.top{left:16px;top:13px;font-size:13px;color:#9edcff;letter-spacing:2px}
.hud.tip{right:15px;top:13px;font-size:11px;color:#83b8d8}
#info{position:absolute;left:16px;bottom:16px;z-index:4;width:245px;padding:12px;background:rgba(3,21,39,.88);border:1px solid #168bc7;border-radius:6px;box-shadow:0 0 18px #0068a655}
#info strong{color:#55d8ff;font-size:14px}#info p{font-size:12px;color:#c3dff2;margin:7px 0 0}
#tools{position:absolute;right:13px;bottom:14px;z-index:5;display:flex;gap:7px;flex-wrap:wrap;justify-content:flex-end}
#tools button{pointer-events:auto;background:rgba(4,48,78,.92);border:1px solid #168bc7;color:#dff6ff;padding:8px 11px;border-radius:4px;cursor:pointer;font-size:12px}
#tools button:hover{background:#087bb4}
#legend{position:absolute;left:16px;top:45px;z-index:3;font-size:11px;color:#a8d4ee;line-height:1.9}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px;background:#31e0b0}
</style></head><body>
<div id="wrap">
<canvas id="view"></canvas>
<div class="hud top">● DIGITAL TWIN / LIVE CLASSROOM</div>
<div class="hud tip">鼠标拖动旋转 · 滚轮缩放 · 点击设备查看详情</div>
<div id="legend"><span class="dot"></span>在线设备　<span style="color:#ffc65c">●</span> 待检设备　<span style="color:#42aaff">●</span> 学生位置</div>
<div id="info"><strong id="infoTitle">课堂三维实景</strong><p id="infoText">点击中央白色立式实训控制台、学生或教师模型，查看对象信息。</p></div>
<div id="tools">
<button onclick="setMode('all')">全景</button><button onclick="setMode('devices')">设备视角</button>
<button onclick="setMode('people')">人员视角</button><button onclick="resetCamera()">复位视角</button>
</div></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const canvas=document.getElementById('view'), wrap=document.getElementById('wrap');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.shadowMap.enabled=true;
renderer.setSize(wrap.clientWidth,wrap.clientHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace;
const scene=new THREE.Scene(); scene.background=new THREE.Color(0x061321); scene.fog=new THREE.Fog(0x061321,22,55);
const camera=new THREE.PerspectiveCamera(48,wrap.clientWidth/wrap.clientHeight,.1,100);
let target=new THREE.Vector3(0,2,0), radius=23, theta=.18, phi=1.05;
function updateCamera(){camera.position.set(target.x+radius*Math.sin(phi)*Math.sin(theta),target.y+radius*Math.cos(phi),target.z+radius*Math.sin(phi)*Math.cos(theta));camera.lookAt(target)}
updateCamera();
scene.add(new THREE.HemisphereLight(0x9fdcff,0x172333,2.0));
const key=new THREE.DirectionalLight(0xffffff,2.2);key.position.set(-8,16,10);key.castShadow=true;scene.add(key);
const blue=new THREE.PointLight(0x168cff,32,35);blue.position.set(0,8,-5);scene.add(blue);
function mat(color,rough=.7,metal=0){return new THREE.MeshStandardMaterial({color,roughness:rough,metalness:metal})}
function box(w,h,d,x,y,z,m, parent=scene){let o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o}
const floor=box(24,.35,30,0,-.25,0,mat(0x26384a));
const grid=new THREE.GridHelper(24,24,0x1b78a8,0x24465e);grid.position.y=-.06;scene.add(grid);
// 房间墙体、窗户和后墙
box(24,8,.35,0,3.8,-14.8,mat(0x34495b));box(.35,8,30,-12,3.8,0,mat(0x25394c));box(.35,8,30,12,3.8,0,mat(0x25394c));
for(let i=0;i<5;i++){box(2.2,1.65,.12,-9.6+i*4.7,4.5,-14.58,mat(0x75b9df,.25,.2));box(2.25,.08,.16,-9.6+i*4.7,3.65,-14.5,mat(0x9ab9cc));}
// 顶部灯带
for(let x of [-7,0,7]){box(.16,.08,22,x,7.65,0,mat(0x38bfff,.25,0.2));}
// 讲台
box(5,.35,1.5,0,.2,-11,mat(0x40556b));box(2.6,1.2,.35,0,.95,-11.55,mat(0x172c40));
// 设备对象可点击
const clickable=[];
function label(text,obj){const c=document.createElement('canvas');c.width=512;c.height=100;const ctx=c.getContext('2d');ctx.fillStyle='rgba(3,25,45,.85)';ctx.fillRect(0,0,512,100);ctx.strokeStyle='#29bfff';ctx.lineWidth=4;ctx.strokeRect(2,2,508,96);ctx.fillStyle='#dff7ff';ctx.font='bold 38px Arial';ctx.fillText(text,20,65);const tex=new THREE.CanvasTexture(c);const s=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true}));s.scale.set(3.2,.62,1);s.position.set(obj.position.x, obj.position.y+2.6,obj.position.z);scene.add(s);}
function makeConsole(x,z,index){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 const white=mat(0xe8edf0,.48),dark=mat(0x111c29,.35,.15),screen=mat(0x071d32,.2,.2),silver=mat(0x8798a5,.35,.55);
 // 宽底座和立式柜体
 let base=box(1.8,.18,1.15,0,.22,0,white,g);
 box(1.15,2.65,.85,0,1.58,0,white,g);
 // 上部倾斜控制面板、显示器、操作台
 let panel=box(1.03,1.0,.12,0,2.9,-.40,dark,g);panel.rotation.x=-.12;
 box(.91,.72,.035,0,2.95,-.475,screen,g);
 box(1.42,.18,.82,0,2.35,.05,white,g);
 box(1.25,.10,.55,0,2.48,.04,dark,g);
 for(let i=0;i<5;i++){let b=new THREE.Mesh(new THREE.CylinderGeometry(.07,.07,.05,20),i===0?mat(0xe63939):silver);b.rotation.x=Math.PI/2;b.position.set(-.48+i*.23,2.55,-.24);g.add(b)}
 box(.46,.08,.02,0,1.0,-.438,silver,g);
 // 侧边通风口
 for(let i=0;i<5;i++)box(.56,.035,.018,0,.62+i*.09,-.437,silver,g);
 // 轮子
 for(let xx of [-.62,.62])for(let zz of [-.36,.36]){let w=new THREE.Mesh(new THREE.CylinderGeometry(.09,.09,.07,16),dark);w.rotation.z=Math.PI/2;w.position.set(xx,.12,zz);g.add(w)}
 clickable.push({obj:g,title:'立式一体化实训控制台 '+String(index).padStart(2,'0'),text:'设备型号：HPY-RS03 智能制造综合实训平台\\n运行状态：在线\\n当前任务：综合实训操作\\n设备位置：'+(index)+'号实训工位'});
 label('实训控制台 '+index,g);
 return g;
}
let consoleObjs=[];
for(let row=0;row<2;row++)for(let col=0;col<3;col++){let x=-7+col*7,z=3+row*-7;consoleObjs.push(makeConsole(x,z,row*3+col+1));}
// 工位桌椅
for(let row=0;row<3;row++)for(let col=0;col<4;col++){let x=-9+col*6,z=7-row*5;box(2.3,.16,1.25,x,.85,z,mat(0x40566b));box(.12,.8,.12,x-.9,.4,z-.48,mat(0x24394c));box(.12,.8,.12,x+.9,.4,z-.48,mat(0x24394c));}
// 人物简模
function person(x,z,isTeacher=false,n=0){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 let shirt=mat(isTeacher?0x20a9db:0x2787c8),skin=mat(0xe0b99a),pants=mat(0x1d2c42);
 let body=new THREE.Mesh(new THREE.CylinderGeometry(.25,.32,.9,12),shirt);body.position.y=1.05;g.add(body);
 let head=new THREE.Mesh(new THREE.SphereGeometry(.23,16,12),skin);head.position.y=1.72;g.add(head);
 for(let dx of [-.13,.13]){let leg=box(.16,.65,.18,dx,.32,0,pants,g)}
 clickable.push({obj:g,title:isTeacher?'授课教师':'学生 '+String(n).padStart(2,'0'),text:isTeacher?'教师状态：正在授课\\n负责课程：智能制造综合实训\\n当前位置：讲台区域':'学生状态：实训中\\n考勤状态：已签到\\n当前任务：设备操作训练'});
 return g;
}
person(-1,-10,true);let people=[];for(let i=0;i<12;i++)people.push(person(-8+(i%4)*5.2,5-Math.floor(i/4)*4,false,i+1));
// 点选与拖动
const ray=new THREE.Raycaster(),mouse=new THREE.Vector2();let down=false,px=0,py=0;
canvas.addEventListener('pointerdown',e=>{down=true;px=e.clientX;py=e.clientY;canvas.setPointerCapture(e.pointerId)});
canvas.addEventListener('pointerup',e=>{down=false;});
canvas.addEventListener('pointermove',e=>{if(!down)return;let dx=e.clientX-px,dy=e.clientY-py;px=e.clientX;py=e.clientY;theta-=dx*.006;phi=Math.max(.25,Math.min(1.48,phi+dy*.005));updateCamera()});
canvas.addEventListener('wheel',e=>{radius=Math.max(11,Math.min(36,radius+e.deltaY*.015));updateCamera()},{passive:true});
canvas.addEventListener('click',e=>{let r=canvas.getBoundingClientRect();mouse.x=((e.clientX-r.left)/r.width)*2-1;mouse.y=-((e.clientY-r.top)/r.height)*2+1;ray.setFromCamera(mouse,camera);let hits=ray.intersectObjects(clickable.map(x=>x.obj),true);if(hits.length){let root=hits[0].object;while(root.parent&&!clickable.some(x=>x.obj===root))root=root.parent;let d=clickable.find(x=>x.obj===root);if(d){document.getElementById('infoTitle').textContent=d.title;document.getElementById('infoText').innerHTML=d.text.replaceAll('\\n','<br>')}}});
window.setMode=function(mode){if(mode==='devices'){target.set(0,1.8,0);radius=17;theta=.2;phi=1.1}else if(mode==='people'){target.set(0,1.2,1);radius=20;theta=-.2;phi=.9}else{target.set(0,2,0);radius=23;theta=.18;phi=1.05}updateCamera()};
window.resetCamera=()=>setMode('all');
function animate(){requestAnimationFrame(animate);renderer.render(scene,camera)}animate();
window.addEventListener('resize',()=>{renderer.setSize(wrap.clientWidth,wrap.clientHeight);camera.aspect=wrap.clientWidth/wrap.clientHeight;camera.updateProjectionMatrix()});
</script></body></html>
"""

left, center, right = st.columns([1.15, 3.5, 1.15], gap="small")

with left:
    st.markdown('<div class="panel"><div class="panel-title">教室运行总览</div>', unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.room}**")
    st.markdown('<span class="status-ok">● 正常授课中</span>', unsafe_allow_html=True)
    st.markdown("---")
    for title, value, unit in [
        ("教室总数", "03", "间"), ("在校学生", "036", "人"),
        ("授课教师", "02", "人"), ("实训设备", "12", "台")
    ]:
        st.markdown(f"<div style='display:flex;justify-content:space-between;margin:9px 0'><span class='small'>{title}</span><b style='color:#62d9ff;font-size:19px'>{value} <span class='small'>{unit}</span></b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">学生考勤统计</div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size:30px;color:#4fe0bd;font-weight:800'>94.4%</div><div class='small'>课堂实时出勤率</div>", unsafe_allow_html=True)
    st.progress(0.944)
    for label, value in [("已签到 34 人", "34"), ("迟到 1 人", "01"), ("缺勤 1 人", "01")]:
        st.markdown(f"<div style='display:flex;justify-content:space-between;margin-top:7px'><span class='small'>{label}</span><b>{value}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">教师授课信息</div>', unsafe_allow_html=True)
    st.markdown("**张老师**　<span class='status-ok'>● 在线</span>", unsafe_allow_html=True)
    st.caption("课程：智能制造综合实训")
    st.caption("班级：智能制造 2401 班")
    st.caption("课时：第 3 / 4 节")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**课堂任务进度**")
    for name, value in [("任务一", 0.90), ("任务二", 0.76), ("任务三", 0.62)]:
        st.caption(name)
        st.progress(value)
    st.markdown("</div>", unsafe_allow_html=True)

with center:
    st.markdown('<div class="panel-title">三维数字孪生教室 / 3D CLASSROOM</div>', unsafe_allow_html=True)
    components.html(scene_html, height=790, scrolling=False)
    st.caption("提示：在三维场景中拖动鼠标旋转视角，滚轮缩放；点击白色实训控制台或人物查看信息。")

with right:
    st.markdown('<div class="panel"><div class="panel-title">设备运行监测</div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size:28px;color:#4fe0bd;font-weight:800'>91.7%</div><div class='small'>设备在线率 · 11 / 12 台在线</div>", unsafe_allow_html=True)
    st.progress(0.917)
    for name, status, color in [
        ("控制台 01", "运行中", "status-ok"), ("控制台 02", "运行中", "status-ok"),
        ("控制台 03", "待巡检", "status-warn"), ("控制台 04", "运行中", "status-ok"),
        ("教学大屏", "在线", "status-ok"), ("环境传感器", "在线", "status-ok"),
    ]:
        st.markdown(f"<div style='display:flex;justify-content:space-between;margin:8px 0'><span class='small'>{name}</span><span class='{color}'>{status}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">学生实训状态</div>', unsafe_allow_html=True)
    for name, value, count in [("设备操作", 0.72, "26人"), ("任务学习", 0.18, "6人"), ("待机状态", 0.10, "4人")]:
        st.markdown(f"<div style='display:flex;justify-content:space-between'><span class='small'>{name}</span><b>{count}</b></div>", unsafe_allow_html=True)
        st.progress(value)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">异常预警信息</div>', unsafe_allow_html=True)
    st.markdown("<div class='status-warn'>● 03号实训控制台待巡检</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:7px 0'>", unsafe_allow_html=True)
    st.markdown("<div class='status-ok'>● 当前无安全告警</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:7px 0'>", unsafe_allow_html=True)
    st.markdown("<div class='status-ok'>● 学生身份核验正常</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-title">课堂关键指标</div>', unsafe_allow_html=True)
    for name, value in [("平均实训完成率", "76%"), ("设备平均利用率", "82%"), ("课堂互动次数", "28次")]:
        st.markdown(f"<div style='display:flex;justify-content:space-between;margin:10px 0'><span class='small'>{name}</span><b style='color:#65d7ff'>{value}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------- 大屏底部状态栏 ----------------------------
st.markdown(
    f"<div style='text-align:center;color:#557d9b;font-size:11px;padding:8px'>"
    f"课堂数字孪生服务平台 · 演示数据 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
    f"</div>", unsafe_allow_html=True
)
