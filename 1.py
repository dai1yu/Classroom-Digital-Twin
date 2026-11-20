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
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#020916;color:#eaf7ff;font-family:"Microsoft YaHei",Arial,sans-serif}
#wrap{position:relative;width:100%;height:780px;overflow:hidden;border:1px solid rgba(38,165,255,.7);border-radius:7px;background:radial-gradient(ellipse at 50% 44%,#163b5b 0%,#07192b 56%,#020814 100%);box-shadow:inset 0 0 55px #0876bd33,0 0 22px #008bff22}
#view{width:100%;height:100%;display:block}
.hud{position:absolute;z-index:4;pointer-events:none;text-shadow:0 2px 6px #000}
.hud.top{left:17px;top:14px;color:#8cddff;font-size:13px;letter-spacing:2px}
.hud.tip{right:16px;top:14px;color:#a4cde8;font-size:11px}
#legend{position:absolute;left:17px;top:43px;font-size:11px;color:#c1e6ff;line-height:2}
.pulse{display:inline-block;width:7px;height:7px;border-radius:50%;background:#36edb6;box-shadow:0 0 9px #36edb6;margin-right:6px}
#info{position:absolute;left:16px;bottom:16px;z-index:5;width:258px;min-height:98px;padding:12px 14px;background:linear-gradient(135deg,rgba(3,27,49,.94),rgba(3,12,25,.92));border:1px solid #168bc7;border-left:3px solid #26c5ff;border-radius:5px;box-shadow:0 0 20px #0068a655}
#info strong{color:#5bd8ff;font-size:14px}
#info p{font-size:11px;line-height:1.8;color:#d0e9fa;margin:7px 0 0}
#tools{position:absolute;right:13px;bottom:14px;z-index:6;display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
#tools button{background:rgba(4,43,73,.94);border:1px solid #168bc7;color:#e1f6ff;padding:8px 11px;border-radius:4px;cursor:pointer;font-size:11px}
#tools button:hover{background:#087bb4;box-shadow:0 0 12px #16aaff77}
#scan{position:absolute;inset:0;pointer-events:none;z-index:2;background:repeating-linear-gradient(0deg,transparent 0px,transparent 5px,rgba(65,174,255,.025) 6px)}
</style></head><body>
<div id="wrap">
<canvas id="view"></canvas><div id="scan"></div>
<div class="hud top"><span class="pulse"></span>CLASSROOM DIGITAL TWIN / LIVE SCENE</div>
<div class="hud tip">拖动旋转 · 滚轮缩放 · 点击模型查看孪生数据</div>
<div id="legend">● 设备在线　<span style="color:#ffc65c">●</span> 待检设备　<span style="color:#42aaff">●</span> 学生　<span style="color:#ff9d62">●</span> 教师</div>
<div id="info"><strong id="infoTitle">三维教室数字孪生</strong><p id="infoText">场景已加载。点击立式一体化实训控制台、学生或教师模型，查看对象状态、位置及任务信息。</p></div>
<div id="tools">
<button onclick="setMode('all')">教室全景</button><button onclick="setMode('devices')">设备视角</button>
<button onclick="setMode('people')">人员视角</button><button onclick="setMode('top')">俯视视角</button><button onclick="resetCamera()">视角复位</button>
</div></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const canvas=document.getElementById('view'),wrap=document.getElementById('wrap');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.8));renderer.setSize(wrap.clientWidth,wrap.clientHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const scene=new THREE.Scene();scene.background=new THREE.Color(0x061525);scene.fog=new THREE.Fog(0x061525,28,62);
const camera=new THREE.PerspectiveCamera(43,wrap.clientWidth/wrap.clientHeight,.1,120);
let target=new THREE.Vector3(0,2.1,-1),radius=28,theta=.18,phi=1.12;
function updateCamera(){camera.position.set(target.x+radius*Math.sin(phi)*Math.sin(theta),target.y+radius*Math.cos(phi),target.z+radius*Math.sin(phi)*Math.cos(theta));camera.lookAt(target)}
updateCamera();
scene.add(new THREE.HemisphereLight(0xc4eaff,0x142337,2.0));
const key=new THREE.DirectionalLight(0xffffff,2.4);key.position.set(-10,18,10);key.castShadow=true;key.shadow.mapSize.set(2048,2048);scene.add(key);
const rim=new THREE.PointLight(0x168dff,42,42);rim.position.set(0,8,-7);scene.add(rim);
const fill=new THREE.PointLight(0x28c9ff,24,30);fill.position.set(8,5,8);scene.add(fill);
function mat(color,rough=.62,metal=0,emissive=0x000000){return new THREE.MeshStandardMaterial({color,roughness:rough,metalness:metal,emissive,emissiveIntensity:.35})}
function box(w,h,d,x,y,z,m,parent=scene){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o}
function cylinder(rt,rb,h,x,y,z,m,parent=scene){const o=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,20),m);o.position.set(x,y,z);o.castShadow=true;parent.add(o);return o}
const floorMat=mat(0x26384a,.88),wallMat=mat(0x526273,.9),trim=mat(0x1b9bd2,.32,.35,0x063c65);
box(26,.32,34,0,-.22,0,floorMat);
const floorGrid=new THREE.GridHelper(26,52,0x1688bc,0x31536c);floorGrid.position.y=-.045;scene.add(floorGrid);
// 房间墙体：后墙、左右墙和蓝色踢脚线
box(26,8,.35,0,3.8,-17,wallMat);box(.35,8,34,-13,3.8,0,mat(0x354b5f));box(.35,8,34,13,3.8,0,mat(0x354b5f));
box(26,.12,.16,0,.16,-16.78,trim);box(.16,.12,34,-12.78,.16,0,trim);box(.16,.12,34,12.78,.16,0,trim);
// 后墙窗户、窗框和顶灯
for(let i=0;i<6;i++){let x=-10.4+i*4.15;box(2.65,1.8,.07,x,4.8,-16.78,mat(0x75b7d7,.22,.25,0x102c45));box(2.75,.09,.12,x,3.86,-16.68,mat(0x9eb5c4));box(.08,1.9,.12,x-1.34,4.8,-16.65,trim);box(.08,1.9,.12,x+1.34,4.8,-16.65,trim)}
for(let x of [-8,0,8]){box(.22,.08,24,x,7.55,-1,mat(0x43c8ff,.2,.2,0x0879c5));}
for(let z of [-10,-2,6]){box(18,.04,.05,0,7.25,z,mat(0x2e9bc9,.3,.2,0x073e66));}
// 前方教学区与讲台
box(7,.28,1.7,0,.15,-13.6,mat(0x536b7d));box(3.2,1.25,.35,0,.9,-14.25,mat(0x14283b));
box(2.5,1.35,.08,0,1.9,-14.32,mat(0x071b2e));box(2.35,1.18,.025,0,1.9,-14.25,mat(0x0b3450,.2,.2,0x0b5a86));
// 场景对象和可点击对象
const clickable=[],animated=[];
function makeTag(text,position,color='#25bfff'){
 const c=document.createElement('canvas');c.width=512;c.height=112;const ctx=c.getContext('2d');
 ctx.fillStyle='rgba(3,22,42,.91)';ctx.fillRect(0,0,512,112);ctx.strokeStyle=color;ctx.lineWidth=5;ctx.strokeRect(3,3,506,106);
 ctx.fillStyle='#e8f8ff';ctx.font='bold 39px Arial,"Microsoft YaHei"';ctx.fillText(text,20,72);
 const tex=new THREE.CanvasTexture(c),sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true,depthTest:false}));
 sp.scale.set(3.6,.78,1);sp.position.copy(position);scene.add(sp);return sp;
}
function addRing(parent,y,r,color){const ring=new THREE.Mesh(new THREE.TorusGeometry(r,.018,8,64),new THREE.MeshBasicMaterial({color,transparent:true,opacity:.85}));ring.rotation.x=Math.PI/2;ring.position.y=y;parent.add(ring);return ring}
// 立式一体化实训控制台：白色立式机身、上置大屏、操作台、按钮、键盘、侧面通风口和脚轮
function makeConsole(x,z,index){
 const g=new THREE.Group();g.position.set(x,0,z);g.rotation.y=Math.PI;scene.add(g);
 const white=mat(0xe9eef1,.42,.08),edge=mat(0xb8c7d0,.38,.25),black=mat(0x101b27,.28,.22),screenMat=new THREE.MeshStandardMaterial({color:0x061827,roughness:.18,metalness:.22,emissive:0x07304a,emissiveIntensity:.8}),silver=mat(0x8496a4,.3,.65);
 // 底盘与主机立柱
 box(1.95,.18,1.22,0,.22,0,white,g);box(1.78,.08,1.08,0,.12,0,edge,g);
 box(1.32,2.25,.94,0,1.38,.02,white,g);
 // 前面机身装饰面板
 box(1.16,1.72,.035,0,1.48,-.465,white,g);
 // 大尺寸上部显示屏与外框
 box(1.38,1.12,.15,0,2.92,-.43,black,g);
 box(1.22,.91,.035,0,2.94,-.525,screenMat,g);
 // 屏幕数字界面细节
 for(let j=0;j<4;j++){box(.78,.025,.008,0,3.22-j*.15,-.545,mat(0x27aee7,.3,.1,0x0879c5),g)}
 // 倾斜操作台
 let deck=box(1.72,.18,.88,0,2.22,.03,white,g);deck.rotation.x=-.08;
 let control=box(1.48,.08,.64,0,2.34,-.02,black,g);control.rotation.x=-.08;
 // 操作按钮、旋钮和急停按钮
 for(let i=0;i<6;i++){let bx=-.57+(i%3)*.28,by=2.39-Math.floor(i/3)*.19;let b=cylinder(.065,.065,.045,bx,by,-.27,i===0?mat(0xe43c39,.3,0,0x9b100c):silver,g);b.rotation.x=Math.PI/2}
 let stop=cylinder(.105,.105,.08,-.52,2.46,-.19,mat(0xf02c25,.25,0,0x7e0905),g);stop.rotation.x=Math.PI/2;
 // 键盘托板与键盘
 box(1.35,.055,.48,0,1.96,.55,edge,g);box(1.12,.055,.34,0,2.02,.55,black,g);
 for(let r=0;r<3;r++)for(let c=0;c<13;c++)box(.065,.018,.055,-.48+c*.08,2.06,.42+r*.085,silver,g);
 // 下部散热格栅
 for(let i=0;i<7;i++)box(.62,.025,.018,0,.62+i*.09,-.49,silver,g);
 // 侧面立柱和透明线缆软管
 box(.055,1.5,.06,.69,1.15,.49,edge,g);
 // 脚轮
 for(let xx of [-.72,.72])for(let zz of [-.42,.42]){let w=cylinder(.095,.095,.09,xx,.10,zz,black,g);w.rotation.z=Math.PI/2}
 const halo=addRing(g,.035,1.12,index===3?0xffbd52:0x27dfff);
 const data={obj:g,title:'立式一体化实训控制台 '+String(index).padStart(2,'0'),text:'设备型号：HPY-RS03 智能制造综合实训平台\\n设备类型：立式一体化实训控制台\\n运行状态：'+(index===3?'待巡检':'在线运行')+'\\n当前任务：智能制造综合实训\\n设备工位：'+index+'号工位\\n连接状态：数字孪生已连接'};
 clickable.push(data);makeTag('实训控制台 '+index,new THREE.Vector3(x,4.35,z),index===3?'#ffbd52':'#25bfff');
 animated.push({obj:halo,phase:index*.7});
 return g;
}
let consoles=[];
const positions=[[-8,5],[-2.7,5],[2.7,5],[8,5],[-5.3,-3],[0,-3],[5.3,-3]];
positions.forEach((p,i)=>consoles.push(makeConsole(p[0],p[1],i+1)));
// 工位桌、显示器与椅子
const deskMat=mat(0x40566b),chairMat=mat(0x233c52);
for(let row=0;row<3;row++)for(let col=0;col<4;col++){
 const x=-9+col*6,z=9-row*5.2;
 box(2.15,.15,1.25,x,.86,z,deskMat);
 for(let xx of [-.88,.88])for(let zz of [-.48,.48])box(.1,.82,.1,x+xx,.4,z+zz,chairMat);
 box(.72,.5,.08,x,.0+1.2,z-.48,mat(0x142c43),scene);
 box(.64,.4,.025,x,1.22,z-.425,mat(0x071d32,.2,.2,0x073c60),scene);
}
// 人员三维模型，衣服、头部、手臂、腿部和脚
function person(x,z,isTeacher=false,n=0){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 const shirt=mat(isTeacher?0xe18a42:0x238bc5),skin=mat(0xe4b99a),pants=mat(0x1b2c40),shoe=mat(0x101b29);
 let torso=new THREE.Mesh(new THREE.CapsuleGeometry(.27,.52,5,10),shirt);torso.position.y=1.18;g.add(torso);
 let head=new THREE.Mesh(new THREE.SphereGeometry(.22,16,12),skin);head.position.y=1.82;g.add(head);
 let hair=new THREE.Mesh(new THREE.SphereGeometry(.225,16,8,0,Math.PI*2,0,Math.PI*.52),mat(0x20252b));hair.position.y=1.9;g.add(hair);
 for(let side of [-1,1]){
  let arm=new THREE.Mesh(new THREE.CapsuleGeometry(.075,.48,4,8),shirt);arm.position.set(side*.32,1.22,-.01);arm.rotation.z=side*.22;g.add(arm);
  let leg=new THREE.Mesh(new THREE.CapsuleGeometry(.09,.48,4,8),pants);leg.position.set(side*.12,.43,0);g.add(leg);
  box(.18,.1,.29,side*.12,.12,-.035,shoe,g);
 }
 const title=isTeacher?'授课教师':'学生 '+String(n).padStart(2,'0');
 clickable.push({obj:g,title,text:isTeacher?'人员类型：授课教师\\n当前状态：正在授课\\n负责课程：智能制造综合实训\\n所在位置：教师讲台':'人员类型：实训学生\\n学号：STU-'+String(240100+n)+'\\n考勤状态：已签到\\n当前状态：设备操作训练\\n所在位置：'+(n)+'号学习工位'});
 if(isTeacher)makeTag('授课教师',new THREE.Vector3(x,2.8,z),'#ff9d62');
 return g;
}
person(-1,-11.6,true);let students=[];
for(let i=0;i<16;i++){let row=Math.floor(i/4),col=i%4;students.push(person(-8.5+col*5.6,8-row*4.7,false,i+1));}
// 工位定位点、地面路径和动态数据流线
const pathMat=new THREE.MeshBasicMaterial({color:0x148dcc,transparent:true,opacity:.65});
for(let i=0;i<4;i++){let line=box(.08,.018,17,-10+i*6.7,.0,-1,pathMat);line.material=pathMat}
for(let i=0;i<12;i++){let marker=new THREE.Mesh(new THREE.CircleGeometry(.12,20),new THREE.MeshBasicMaterial({color:0x28caff,transparent:true,opacity:.6}));marker.rotation.x=-Math.PI/2;marker.position.set(-9+(i%4)*6,0.015,8-Math.floor(i/4)*5);scene.add(marker);}
// 点选、旋转、缩放
const ray=new THREE.Raycaster(),mouse=new THREE.Vector2();let down=false,px=0,py=0,moved=false;
canvas.addEventListener('pointerdown',e=>{down=true;moved=false;px=e.clientX;py=e.clientY;canvas.setPointerCapture(e.pointerId)});
canvas.addEventListener('pointerup',()=>{down=false});
canvas.addEventListener('pointermove',e=>{if(!down)return;let dx=e.clientX-px,dy=e.clientY-py;if(Math.abs(dx)+Math.abs(dy)>2)moved=true;px=e.clientX;py=e.clientY;theta-=dx*.006;phi=Math.max(.28,Math.min(1.49,phi+dy*.005));updateCamera()});
canvas.addEventListener('wheel',e=>{radius=Math.max(13,Math.min(42,radius+e.deltaY*.018));updateCamera()},{passive:true});
canvas.addEventListener('click',e=>{
 if(moved)return;let r=canvas.getBoundingClientRect();mouse.x=((e.clientX-r.left)/r.width)*2-1;mouse.y=-((e.clientY-r.top)/r.height)*2+1;
 ray.setFromCamera(mouse,camera);const hits=ray.intersectObjects(clickable.map(x=>x.obj),true);
 if(hits.length){let root=hits[0].object;while(root.parent&&!clickable.some(x=>x.obj===root))root=root.parent;let d=clickable.find(x=>x.obj===root);
 if(d){document.getElementById('infoTitle').textContent=d.title;document.getElementById('infoText').innerHTML=d.text.replaceAll('\\n','<br>')}}
});
window.setMode=function(mode){
 if(mode==='devices'){target.set(0,1.8,1);radius=21;theta=.05;phi=1.12}
 else if(mode==='people'){target.set(0,1.4,2);radius=23;theta=-.2;phi=.95}
 else if(mode==='top'){target.set(0,0,0);radius=34;theta=.01;phi=.25}
 else{target.set(0,2.1,-1);radius=28;theta=.18;phi=1.12}
 updateCamera()
};
window.resetCamera=()=>setMode('all');
let clock=new THREE.Clock();
function animate(){requestAnimationFrame(animate);let t=clock.getElapsedTime();
 animated.forEach((a,i)=>{a.obj.material.opacity=.55+.35*Math.sin(t*2+a.phase);a.obj.scale.setScalar(1+.035*Math.sin(t*2+a.phase))});
 renderer.render(scene,camera)}
animate();
window.addEventListener('resize',()=>{renderer.setSize(wrap.clientWidth,wrap.clientHeight);camera.aspect=wrap.clientWidth/wrap.clientHeight;camera.updateProjectionMatrix()});
</script></body></html>
"""


left, center, right = st.columns([1.05, 3.9, 1.05], gap="small")

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
