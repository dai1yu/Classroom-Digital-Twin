# -*- coding: utf-8 -*-
"""
智能制造课堂数字孪生可视化大屏
参考用户提供的“智能工厂数字孪生平台.py”大屏布局与科技UI风格重构。
部署：GitHub 根目录放置 1.py 和 requirements.txt，Streamlit Cloud 启动文件设为 1.py。
仅依赖 streamlit；三维场景由浏览器端 Three.js CDN 渲染，不依赖 pygame / plotly / pandas。
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="课堂教学数字孪生平台",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{visibility:hidden!important;height:0!important}
.stApp{background:#04131e!important}
.block-container{padding:0!important;max-width:100%!important}
iframe{border:0!important}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>课堂数字孪生平台</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#04131e;color:#d9faff;font-family:"Microsoft YaHei","Noto Sans SC",Arial,sans-serif}
:root{--cyan:#16d9df;--blue:#168ba8;--line:rgba(26,220,230,.48);--panel:rgba(3,24,34,.86)}
#app{position:relative;width:100vw;height:100vh;min-height:680px;overflow:hidden;background:radial-gradient(ellipse at 50% 48%,rgba(0,111,132,.20),transparent 56%),linear-gradient(180deg,#061724 0%,#06121b 100%)}
#scene{position:absolute;inset:0;width:100%;height:100%;z-index:0;display:block}
.topbar{position:absolute;z-index:5;left:0;right:0;top:0;height:68px;background:linear-gradient(180deg,rgba(3,19,29,.98),rgba(3,19,29,.62));border-bottom:1px solid rgba(31,214,224,.35);display:flex;align-items:center;justify-content:space-between;padding:0 22px}
.brand{font-size:23px;font-weight:800;letter-spacing:4px;color:#dffcff;text-shadow:0 0 15px #00d9e9}
.brand small{display:block;font-size:9px;letter-spacing:2.5px;color:#56b8c4;margin-top:4px;font-weight:400}
.top-actions{display:flex;align-items:center;gap:8px}
.top-btn{border:1px solid rgba(31,219,226,.55);background:rgba(0,128,145,.18);color:#9ffaff;padding:8px 13px;cursor:pointer;font-size:11px;letter-spacing:1px;clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%,0 8px)}
.top-btn.active,.top-btn:hover{background:rgba(0,205,210,.35);box-shadow:0 0 14px rgba(0,224,230,.28)}
.clock{font-size:11px;color:#83cbd2;margin-left:10px;min-width:135px;text-align:right}
.corner{position:absolute;z-index:2;top:78px;left:50%;transform:translateX(-50%);font-size:9px;letter-spacing:2px;color:#3295a7;text-shadow:0 0 8px #087b8e;white-space:nowrap}
.panel{position:absolute;z-index:3;width:248px;background:linear-gradient(135deg,rgba(3,26,37,.93),rgba(3,18,29,.82));border:1px solid var(--line);box-shadow:0 0 20px rgba(0,207,222,.10),inset 0 0 22px rgba(0,150,170,.08);padding:12px 13px 11px;backdrop-filter:blur(8px)}
.panel:before,.panel:after{content:"";position:absolute;width:34px;height:2px;background:var(--cyan);box-shadow:0 0 8px var(--cyan)}
.panel:before{left:-1px;top:-1px}.panel:after{right:-1px;bottom:-1px}
.left{left:15px;top:88px;bottom:108px;overflow:auto;scrollbar-width:thin;scrollbar-color:#176477 transparent}
.right{right:15px;top:88px;bottom:108px;overflow:auto;scrollbar-width:thin;scrollbar-color:#176477 transparent}
.panel-title{font-size:14px;letter-spacing:1px;color:#b8faff;border-bottom:1px solid rgba(38,211,221,.32);padding:0 0 9px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
.panel-title span{font-size:9px;color:#5bcbd3;letter-spacing:1px;font-weight:400}
.section-label{font-size:10px;color:#57c8d1;margin:11px 0 7px;display:flex;align-items:center;gap:7px}
.section-label:before{content:"";width:5px;height:5px;background:#19dce2;box-shadow:0 0 8px #19dce2}
.device{display:flex;justify-content:space-between;align-items:center;padding:7px 7px;margin:5px 0;border:1px solid rgba(27,170,185,.18);background:rgba(12,73,86,.18);font-size:10px;color:#b8dfe3;cursor:pointer}
.device:hover,.device.selected{border-color:#14dce3;background:rgba(0,175,190,.22);color:#e1ffff}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:7px;background:#23e7a5;box-shadow:0 0 8px #23e7a5}
.dot.warn{background:#ffba45;box-shadow:0 0 8px #ffba45}.dot.off{background:#768a91;box-shadow:none}
.status{color:#39e9bd;font-size:9px}.status.warn{color:#ffc15b}.status.off{color:#a1afb4}
.metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.metric{padding:8px 8px;background:rgba(10,72,86,.28);border:1px solid rgba(27,184,195,.23);min-height:61px}
.metric label{display:block;color:#6dbbc4;font-size:9px;margin-bottom:6px}
.metric strong{font-size:18px;color:#d7ffff;font-weight:600}.metric em{font-size:9px;color:#4de0d9;font-style:normal;margin-left:3px}
.bar-row{margin:9px 0;font-size:9px;color:#8ecbd0;display:grid;grid-template-columns:55px 1fr 30px;gap:6px;align-items:center}
.bar{height:5px;background:rgba(125,190,197,.18);overflow:hidden}.bar i{display:block;height:100%;background:linear-gradient(90deg,#087c9b,#22e6d9);box-shadow:0 0 8px #14cfd9}
.ring-wrap{display:flex;align-items:center;gap:11px;padding:5px 1px}
.ring{width:72px;height:72px;flex:none;border-radius:50%;display:grid;place-items:center;background:conic-gradient(#14d9db 0 94%,#16667a 94% 100%);position:relative}
.ring:after{content:"";position:absolute;inset:7px;background:#09202a;border-radius:50%}.ring b{z-index:1;font-size:17px;color:#e1ffff;font-weight:600}
.ring-info{font-size:9px;color:#7fc4cb;line-height:1.9}.ring-info strong{font-size:13px;color:#d9ffff}
.chart{height:112px;width:100%;display:block}
.chart-labels{display:flex;justify-content:space-between;color:#5d9eaa;font-size:8px;margin-top:-2px}
.alert{border-left:3px solid #ffba45;background:rgba(16,44,59,.75);padding:7px 7px;margin:6px 0;font-size:9px;color:#a9d5dc;line-height:1.5}
.alert.ok{border-left-color:#21dba9}.alert.red{border-left-color:#ff5964}
.camera{height:150px;border:1px solid rgba(31,214,224,.48);position:relative;overflow:hidden;background:linear-gradient(180deg,#1d3944 0%,#36545a 46%,#172d37 47%,#0b202b 100%);box-shadow:inset 0 0 24px rgba(0,0,0,.55)}
.camera:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(39,130,146,.22) 1px,transparent 1px),linear-gradient(90deg,rgba(39,130,146,.22) 1px,transparent 1px);background-size:19px 19px}
.cam-machine{position:absolute;bottom:22px;width:24%;height:58px;background:linear-gradient(135deg,#b9c8c9 0%,#627c84 42%,#243e49 100%);border:1px solid #9acbd2;box-shadow:0 0 12px rgba(0,220,230,.15);clip-path:polygon(8% 0,92% 0,100% 100%,0 100%)}
.cam-machine:after{content:"";position:absolute;left:16%;right:16%;top:8px;height:27px;background:linear-gradient(145deg,#102d39,#06151e);border:2px solid #9bb8bd;box-shadow:inset 0 0 8px #08788c}
.cam-label{position:absolute;top:7px;left:8px;font-size:8px;color:#ff6975;text-shadow:0 0 5px #ff2438}.cam-time{position:absolute;bottom:5px;right:8px;font-size:8px;color:#a5dce2}
.bottom{position:absolute;z-index:4;left:15px;right:15px;bottom:10px;height:78px;display:grid;grid-template-columns:1.25fr 1fr 1fr 1fr 1.25fr;gap:8px}
.bottom-card{background:linear-gradient(135deg,rgba(3,28,41,.94),rgba(4,22,34,.86));border:1px solid rgba(28,179,195,.38);padding:10px 12px;position:relative;box-shadow:0 0 12px rgba(0,180,200,.06)}
.bottom-card label{display:block;color:#6dbbc4;font-size:9px;margin-bottom:7px}.bottom-card strong{font-size:20px;color:#d9ffff;font-weight:600}.bottom-card small{font-size:9px;color:#45c9d6;margin-left:4px}
.bottom-card:first-child strong{font-size:19px}.bottom-card:last-child strong{color:#39e8b6}
.bottom-card .spark{position:absolute;right:14px;top:27px;color:#18d9df;font-size:20px}
.actionbar{position:absolute;z-index:6;left:50%;transform:translateX(-50%);bottom:105px;display:flex;gap:7px}
.action{border:1px solid rgba(31,219,226,.62);background:rgba(3,38,54,.92);color:#bffaff;padding:8px 14px;font-size:10px;letter-spacing:1px;cursor:pointer}
.action:hover,.action.active{background:rgba(0,173,190,.35);box-shadow:0 0 12px rgba(0,220,230,.25)}
.toast{position:absolute;z-index:10;left:50%;top:82px;transform:translateX(-50%);padding:9px 18px;background:rgba(4,42,55,.96);border:1px solid #1bbdca;color:#cfffff;font-size:11px;opacity:0;pointer-events:none;transition:opacity .2s}
.toast.show{opacity:1}
.legend{position:absolute;z-index:2;left:50%;top:112px;transform:translateX(-50%);font-size:9px;color:#77b9c4;letter-spacing:1px;white-space:nowrap}
.modal-mask{display:none;position:absolute;z-index:20;inset:0;background:rgba(0,8,14,.72);align-items:center;justify-content:center}
.modal-mask.show{display:flex}.modal{width:min(520px,90vw);background:#082638;border:1px solid #20c9d6;box-shadow:0 0 30px #08798b;padding:18px}
.modal-head{display:flex;justify-content:space-between;border-bottom:1px solid #1b6677;padding-bottom:10px;color:#cfffff}
.modal-body{font-size:12px;line-height:2;color:#a9d5dc}.close-btn{background:none;border:0;color:#8fefff;font-size:18px;cursor:pointer}
@media(max-width:1050px){.panel{width:220px}.left{left:8px}.right{right:8px}.top-actions{gap:4px}.top-btn{padding:7px 8px;font-size:9px}.brand{font-size:18px}.bottom{left:8px;right:8px;gap:5px}.bottom-card{padding:8px}.bottom-card strong{font-size:16px}}
@media(max-width:760px){.topbar{height:58px;padding:0 10px}.brand{font-size:14px;letter-spacing:1px}.brand small{font-size:7px}.top-actions .top-btn{display:none}.clock{font-size:9px;min-width:110px}.panel{width:185px;padding:9px}.left{top:76px;bottom:100px}.right{top:76px;bottom:100px}.panel-title{font-size:11px}.device{font-size:8px;padding:5px}.metric strong{font-size:14px}.bottom{height:70px;bottom:8px}.bottom-card label{font-size:7px}.bottom-card strong{font-size:12px}.bottom-card small{font-size:7px}.actionbar{bottom:83px}.action{padding:6px 8px;font-size:8px}.corner,.legend{display:none}}
</style>
</head>
<body>
<div id="app">
<canvas id="scene"></canvas>
<div class="topbar">
  <div class="brand">课堂教学数字孪生平台<small>CLASSROOM DIGITAL TWIN · INTELLIGENT TRAINING CENTER</small></div>
  <div class="top-actions">
    <button class="top-btn" onclick="showPanel('overview')">实训总览</button>
    <button class="top-btn" onclick="showPanel('devices')">设备管理</button>
    <button class="top-btn" onclick="showPanel('data')">数据分析</button>
    <button class="top-btn" onclick="showPanel('camera')">视频监控</button>
    <button class="top-btn" onclick="resetCameraView()">视角复位</button>
    <div class="clock" id="clock"></div>
  </div>
</div>
<div class="corner">CLASSROOM 3D VISUALIZATION　/　智能制造实训教学空间</div>
<div class="legend">HPY-RS03 恒佩优立式一体化实训控制台　·　3D DIGITAL TWIN</div>

<div class="panel left">
  <div class="panel-title">设备运行监控 <span>DEVICE MONITOR</span></div>
  <div class="section-label">实训设备列表</div>
  <div class="device selected" onclick="selectDevice(this,1)"><span><i class="dot"></i>HPY-RS03 实训台 01</span><b class="status">运行中</b></div>
  <div class="device" onclick="selectDevice(this,2)"><span><i class="dot"></i>HPY-RS03 实训台 02</span><b class="status">运行中</b></div>
  <div class="device" onclick="selectDevice(this,3)"><span><i class="dot"></i>HPY-RS03 实训台 03</span><b class="status">运行中</b></div>
  <div class="device" onclick="selectDevice(this,4)"><span><i class="dot warn"></i>HPY-RS03 实训台 04</span><b class="status warn">待检查</b></div>
  <div class="device" onclick="selectDevice(this,5)"><span><i class="dot"></i>HPY-RS03 实训台 05</span><b class="status">运行中</b></div>
  <div class="device" onclick="selectDevice(this,6)"><span><i class="dot"></i>HPY-RS03 实训台 06</span><b class="status">运行中</b></div>
  <div class="device" onclick="selectDevice(this,7)"><span><i class="dot"></i>HPY-RS03 实训台 07</span><b class="status">运行中</b></div>
  <div class="section-label">设备实时参数</div>
  <div class="metric-grid">
    <div class="metric"><label>主轴转速</label><strong id="rpm">3200</strong><em>rpm</em></div>
    <div class="metric"><label>主轴负载</label><strong id="load">68</strong><em>%</em></div>
    <div class="metric"><label>设备温度</label><strong id="temp">36.5</strong><em>℃</em></div>
    <div class="metric"><label>运行时长</label><strong>08:26</strong><em>h</em></div>
  </div>
  <div class="section-label">实训运行状态</div>
  <div class="bar-row"><span>运行时间</span><div class="bar"><i style="width:86%"></i></div><b>86%</b></div>
  <div class="bar-row"><span>实训进度</span><div class="bar"><i style="width:72%"></i></div><b>72%</b></div>
  <div class="bar-row"><span>健康指数</span><div class="bar"><i style="width:96%"></i></div><b>96%</b></div>
  <div class="section-label">实训负荷趋势</div>
  <canvas id="loadChart" class="chart" width="420" height="150"></canvas>
  <div class="chart-labels"><span>08:00</span><span>10:00</span><span>12:00</span><span>14:00</span><span>16:00</span></div>
</div>

<div class="panel right">
  <div class="panel-title">实训数据分析 <span>DATA ANALYSIS</span></div>
  <div class="section-label">实训运行总览</div>
  <div class="ring-wrap"><div class="ring"><b>93.8%</b></div><div class="ring-info">设备综合运行率<br><strong>正常运行</strong><br>实训状态良好</div></div>
  <div class="section-label">关键实训指标</div>
  <div class="metric-grid">
    <div class="metric"><label>今日实训人次</label><strong id="output">128</strong><em>人次</em></div>
    <div class="metric"><label>完成任务数</label><strong id="goodCount">86</strong><em>项</em></div>
    <div class="metric"><label>待完成任务</label><strong id="badCount">12</strong><em>项</em></div>
    <div class="metric"><label>任务完成率</label><strong id="yieldRate">87.8</strong><em>%</em></div>
  </div>
  <div class="section-label">各工位实训效率对比</div>
  <canvas id="effChart" class="chart" width="420" height="150"></canvas>
  <div class="section-label">视频监控窗口 <span style="margin-left:auto;color:#55b9c7">CAM-01 ONLINE</span></div>
  <div class="camera">
    <div class="cam-label">● LIVE / 实训室全景</div>
    <div class="cam-machine" style="left:7%"></div><div class="cam-machine" style="left:38%"></div><div class="cam-machine" style="left:69%"></div><div style="position:absolute;bottom:22px;left:27%;width:12px;height:37px;background:#203e4b;border-radius:7px 7px 2px 2px;box-shadow:0 -10px 0 -1px #c79d7a,0 0 0 1px #7ba5ae"></div><div style="position:absolute;bottom:22px;left:60%;width:12px;height:37px;background:#4a596a;border-radius:7px 7px 2px 2px;box-shadow:0 -10px 0 -1px #c79d7a,0 0 0 1px #7ba5ae"></div>
    <div class="cam-time" id="camTime">CAM-01　--:--:--</div>
  </div>
  <div class="section-label">告警预警列表</div>
  <div class="alert red">10:16:08　工位04 设备状态待确认</div>
  <div class="alert">10:12:08　工位04 急停状态待确认</div>
  <div class="alert ok">09:48:21　工位02 实训任务完成</div>
  <div class="alert ok">09:32:06　监控网络连接正常</div>
</div>

<div class="actionbar">
  <button class="action" id="alarmBtn" onclick="toggleAlarm()">⚠ 设备告警</button>
  <button class="action" id="patrolBtn" onclick="runPatrol()">✓ 一键巡检</button>
  <button class="action" onclick="resetCameraView()">◎ 视角复位</button>
  <button class="action" onclick="dispatchTask()">⇧ 实训任务下发</button>
</div>
<div class="bottom">
 <div class="bottom-card"><label>当前实训任务</label><strong id="task">实训任务 #0826</strong><span class="spark">▰</span></div>
 <div class="bottom-card"><label>设备总数 / 在线设备</label><strong>07 / 06</strong><small>台</small></div>
 <div class="bottom-card"><label>今日实训人数</label><strong id="bottomOutput">128</strong><small>人次</small></div>
 <div class="bottom-card"><label>平均实训效率</label><strong>96.8</strong><small>%</small></div>
 <div class="bottom-card"><label>系统运行状态</label><strong id="systemState">正常</strong><small>教学实训运行中</small></div>
</div>
<div class="modal-mask" id="modalMask" onclick="closePanel(event)"><div class="modal" onclick="event.stopPropagation()"><div class="modal-head"><b id="modalTitle">模块详情</b><button class="close-btn" onclick="closePanel()">✕</button></div><div id="modalBody" class="modal-body"></div></div></div>
<div class="toast" id="toast"></div>
</div>

<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js';

const canvas=document.getElementById('scene');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.8));
renderer.setSize(innerWidth,innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.32;

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x061724);
scene.fog=new THREE.Fog(0x061724,42,105);
const camera=new THREE.PerspectiveCamera(39,innerWidth/innerHeight,.1,150);
camera.position.set(16.2,9.1,21.8);
const controls=new OrbitControls(camera,renderer.domElement);
controls.target.set(0,1.95,-0.5);
controls.enableDamping=true;controls.dampingFactor=.055;
controls.minDistance=12;controls.maxDistance=39;
controls.maxPolarAngle=Math.PI*.46;
controls.minPolarAngle=.18;
controls.update();
const defaultPos=new THREE.Vector3(16.2,9.1,21.8);
const defaultTarget=new THREE.Vector3(0,1.95,-0.5);

scene.add(new THREE.HemisphereLight(0xc8f3ff,0x253b45,2.45));
const key=new THREE.DirectionalLight(0xf1fbff,3.25);key.position.set(-12,24,15);key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-24;key.shadow.camera.right=24;key.shadow.camera.top=24;key.shadow.camera.bottom=-24;scene.add(key);
const cyanLight=new THREE.PointLight(0x00d9e8,52,46);cyanLight.position.set(-9,6,0);scene.add(cyanLight);
const blueLight=new THREE.PointLight(0x168cff,34,40);blueLight.position.set(10,5,-8);scene.add(blueLight);

const mat=(color,metalness=.25,roughness=.55,emissive=0x000000)=>new THREE.MeshStandardMaterial({color,metalness,roughness,emissive});
const floorMat=mat(0x687d83,.12,.78);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(34,25),floorMat);floor.rotation.x=-Math.PI/2;floor.position.y=-.08;floor.receiveShadow=true;scene.add(floor);
const grid=new THREE.GridHelper(34,34,0x64818a,0x354f59);grid.position.y=-.055;scene.add(grid);
const safety=mat(0xe3c34b,.12,.8);
function box(parent,x,y,z,w,h,d,material,cast=true,receive=true){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);m.position.set(x,y,z);m.castShadow=cast;m.receiveShadow=receive;parent.add(m);return m;}
function cylinder(parent,x,y,z,r1,r2,h,material,segments=24){const m=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,segments),material);m.position.set(x,y,z);m.castShadow=true;parent.add(m);return m;}
function line(parent,a,b,color=0x4b8290,r=.025){const d=new THREE.Vector3(...b).sub(new THREE.Vector3(...a));const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,d.length(),8),new THREE.MeshBasicMaterial({color}));m.position.copy(new THREE.Vector3(...a).add(new THREE.Vector3(...b)).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());parent.add(m);return m;}

// Room shell: walls, windows, door, ceiling beams and industrial lighting
const wall=mat(0x234958,.24,.62), trim=mat(0x9ab7bf,.62,.38), glass=new THREE.MeshPhysicalMaterial({color:0x28718a,metalness:.28,roughness:.12,transparent:true,opacity:.72});
box(scene,0,3.35,-10.7,34,6.8,.28,wall);
box(scene,-16.85,3.35,0,.28,6.8,21.6,wall);
box(scene,16.85,3.35,0,.28,6.8,21.6,wall);
// Back wall window row
for(const x of [-11,-5,1,7]){
 box(scene,x,4.15,-10.52,4.7,2.15,.08,glass,false);
 box(scene,x,5.24,-10.44,4.85,.10,.12,trim);
 box(scene,x,3.06,-10.44,4.85,.10,.12,trim);
 box(scene,x,4.15,-10.43,.10,2.25,.12,trim);
}
// Teaching display wall: large interactive board, side rails and status strip
box(scene,-1.8,2.55,-10.43,7.4,2.45,.16,mat(0x0b202c,.45,.25),false);
box(scene,-1.8,2.55,-10.32,7.08,2.12,.035,mat(0x102f40,.25,.2,0x062b3a),false);
for(let i=0;i<7;i++)box(scene,-4.7+i*.88,3.18,-10.285,.62,.035,.018,mat(0x21c6d5,.1,.25,0x087e92),false);
for(let i=0;i<4;i++)box(scene,-4.65,2.72-i*.28,-10.285,2.1-i*.25,.025,.018,mat(0x5b9eaa,.1,.35,0x092b38),false);
box(scene,-1.8,1.28,-10.31,7.5,.08,.10,trim,false);
// right rear entry door
box(scene,14.9,1.55,-10.48,2.2,3.05,.12,mat(0x234b5b),false);
box(scene,14.25,1.55,-10.38,.08,2.6,.08,trim,false);
cylinder(scene,15.55,1.5,-10.25,.055,.055,.12,mat(0xd8c77b));
// ceiling rafters and roof ribs
for(const z of [-9,-5,-1,3,7,10])box(scene,0,6.45,z,34,.18,.18,trim,false);
for(const x of [-16,-11,-6,-1,4,9,14])box(scene,x,6.42,0,.16,.16,21,trim,false);
// ventilation ducts
box(scene,-12,5.95,-1,1.0,.62,18,mat(0x526f79,.65,.5));
for(const z of [-7,-2,3,8]){box(scene,-12,5.55,z,.52,.62,.52,trim);}
// LED fixtures
for(const x of [-10,-3,4,11])for(const z of [-6,2,8]){
 box(scene,x,6.13,z,3.2,.13,.48,mat(0xd7f6fa,.18,.22,0x2c7788),false);
 const lamp=new THREE.PointLight(0xb8f5ff,7.5,10);lamp.position.set(x,5.85,z);scene.add(lamp);
}
// Yellow walkway and station outlines
for(const x of [-14,14])box(scene,x,.015,0,.10,.025,19,safety,false);
box(scene,0,.018,9,27,.025,.10,safety,false);
box(scene,0,.018,-8.9,27,.025,.10,safety,false);
for(const x of [-11,-6,-1,4,9])box(scene,x,.02,0,.045,.025,16,safety,false);
// Individual machine work bays, aisle arrows and floor reflectors
for(const x of [-9,-3,3,9]){
 box(scene,x,.028,-4.8,3.25,.028,2.45,mat(0x78969b,.1,.8),false);
 box(scene,x,.035,-6.05,2.7,.025,.045,safety,false);
 box(scene,x,.035,-3.55,2.7,.025,.045,safety,false);
}
for(const z of [6.5,7.2])box(scene,0,.028,z,25,.025,.035,safety,false);

// Console materials and equipment groups
const cabinet=mat(0xa9bec3,.66,.31), cabinetDark=mat(0x344f5b,.72,.30), black=mat(0x101d26,.52,.32), screenMat=new THREE.MeshStandardMaterial({color:0x061a27,emissive:0x079bb7,emissiveIntensity:.82,metalness:.25,roughness:.16}), keyMat=mat(0xd5e4e6,.42,.26), red=mat(0xf0444e,.18,.24,0x79151c), green=mat(0x24e6a5,.12,.2,0x08754d), amber=mat(0xffbf4b,.12,.22,0x7b4a0a);
const stations=[];
function makeConsole(x,z,index){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 // HPY-RS03: white one-piece mobile training console, based on the supplied reference photos
 const white=new THREE.MeshStandardMaterial({color:0xe8e9e6,metalness:.16,roughness:.34});
 const whiteSide=new THREE.MeshStandardMaterial({color:0xd8dcda,metalness:.20,roughness:.42});
 const blackGlass=new THREE.MeshPhysicalMaterial({color:0x07131b,metalness:.42,roughness:.12,clearcoat:.9,clearcoatRoughness:.08});
 const darkPanel=new THREE.MeshStandardMaterial({color:0x171e23,metalness:.38,roughness:.34});
 const silver=new THREE.MeshStandardMaterial({color:0x9da8aa,metalness:.78,roughness:.25});
 const rubber=new THREE.MeshStandardMaterial({color:0x171b1e,metalness:.12,roughness:.72});
 const redButton=new THREE.MeshStandardMaterial({color:0xe51d25,metalness:.12,roughness:.28,emissive:0x370000});
 const greenLed=new THREE.MeshStandardMaterial({color:0x26e5a5,emissive:0x087a54,emissiveIntensity:.8});
 const amberLed=new THREE.MeshStandardMaterial({color:0xffc34b,emissive:0x754000,emissiveIntensity:.7});
 const blueLed=new THREE.MeshStandardMaterial({color:0x2ac6ef,emissive:0x075b88,emissiveIntensity:.8});
 // Low, wide wheeled base and broad white cabinet body
 box(g,0,.12,0,2.55,.20,1.72,rubber);
 for(const xx of [-1.02,1.02])for(const zz of [-.62,.62]){
   const caster=cylinder(g,xx,.10,zz,.105,.105,.10,silver,18);caster.rotation.x=Math.PI/2;
   cylinder(g,xx,.055,zz,.055,.055,.08,rubber,16);
 }
 box(g,0,.94,-.02,2.35,1.58,1.48,white);
 // front lower access panel, seams and vent grille
 box(g,0,.91,.735,2.12,1.38,.035,whiteSide,false);
 box(g,.52,.91,.765,.72,.74,.025,white,false);
 for(let i=0;i<9;i++)box(g,.20+i*.075,.52,.789,.045,.018,.012,silver,false);
 box(g,-.78,1.48,.765,.06,.23,.035,silver,false);
 // upper sloped monitor housing: angled rear spine with large framed widescreen
 const back=box(g,0,2.30,-.28,2.18,1.54,.18,white);back.rotation.x=-.17;
 // screen frame tilted slightly backward
 const frame=box(g,0,2.52,.00,2.02,1.25,.16,blackGlass);frame.rotation.x=-.12;
 const screen=box(g,0,2.53,.092,1.78,1.00,.025,new THREE.MeshStandardMaterial({color:0x102b36,emissive:0x063344,emissiveIntensity:.48,metalness:.22,roughness:.18}));screen.rotation.x=-.12;
 // screen content lines and status blocks
 for(let i=0;i<5;i++)box(g,-.70+i*.30,2.91,.113,.22,.025,.008,mat(0x4ac5d4,.05,.3,0x0a4b5b),false);
 for(let i=0;i<4;i++)box(g,-.69,2.73-i*.13,.115,.42-i*.035,.018,.008,mat(0x73aeb8,.05,.4,0x092e3a),false);
 box(g,.48,2.70,.116,.42,.38,.012,mat(0x123f50,.1,.25,0x07556b),false);
 // HPY-RS03 model name strip above screen
 box(g,0,3.18,-.005,1.92,.19,.10,whiteSide,false);
 // desk / operator shelf projecting forward
 box(g,0,1.72,.86,2.78,.18,1.02,white);
 box(g,0,1.615,.91,2.70,.055,.94,mat(0x262b2e,.28,.5),false);
 // angled black control deck, with dense real-world button layout
 const deck=box(g,0,1.91,.93,1.78,.10,.68,darkPanel);deck.rotation.x=-.16;
 // panel border
 box(g,0,1.975,.93,1.82,.025,.72,silver,false).rotation.x=-.16;
 // rows of illuminated and physical keys
 for(let r=0;r<3;r++)for(let c=0;c<7;c++){
   const bx=-.68+c*.225, by=1.93-r*.105;
   const color=(r===2&&c===1)?redButton:((r===0&&c===5)?amberLed:((c===0&&r===1)?greenLed:keyMat));
   box(g,bx,by,1.245,.115,.055,.065,color,false);
   box(g,bx,by+.035,1.282,.09,.012,.012,black,false);
 }
 // rotary selectors and knobs (cylinders face forward)
 for(const [kx,ky,rr] of [[-.64,2.09,.095],[-.28,2.09,.105],[.12,2.09,.085],[.48,2.09,.085],[.72,2.09,.075]]){
   const collar=cylinder(g,kx,ky,1.20,rr*1.28,rr*1.28,.07,silver,24);collar.rotation.x=Math.PI/2;
   const knob=cylinder(g,kx,ky,1.25,rr,rr,.10,black,24);knob.rotation.x=Math.PI/2;
   box(g,kx,ky+rr*.55,1.31,.018,rr*.48,.018,white,false);
 }
 // large emergency stop with yellow safety collar
 const collar=cylinder(g,-.70,1.79,1.22,.19,.19,.09,amberLed,32);collar.rotation.x=Math.PI/2;
 const eStop=cylinder(g,-.70,1.79,1.30,.135,.135,.12,redButton,32);eStop.rotation.x=Math.PI/2;
 // separate manual pulse handwheel mounted on right side of control deck
 const wheel=new THREE.Mesh(new THREE.TorusGeometry(.19,.027,12,36),silver);wheel.position.set(1.05,1.91,1.13);wheel.rotation.x=Math.PI/2;g.add(wheel);
 const hub=cylinder(g,1.05,1.91,1.16,.065,.065,.10,black,24);hub.rotation.x=Math.PI/2;
 const spoke1=box(g,1.05,1.91,1.19,.025,.32,.025,silver,false);const spoke2=box(g,1.05,1.91,1.19,.32,.025,.025,silver,false);
 // keyboard on the work shelf, separate keycaps and space bar
 box(g,-.40,1.69,1.24,1.16,.055,.40,rubber,false);
 for(let r=0;r<4;r++)for(let c=0;c<13;c++)box(g,-.91+c*.085,1.73-r*.025,1.39-r*.085,.064,.018,.055,mat(0x9ca8aa,.12,.45),false);
 box(g,-.42,1.655,1.13,.38,.025,.07,mat(0xb8c0c0,.12,.55),false);
 // side-mounted coiled cable and protective conduit, routed down cabinet
 const cableCurve=new THREE.CatmullRomCurve3([new THREE.Vector3(1.12,2.95,-.30),new THREE.Vector3(1.28,2.72,-.12),new THREE.Vector3(1.28,2.15,.15),new THREE.Vector3(1.30,1.25,.34),new THREE.Vector3(1.28,.35,.48)]);
 const cable=new THREE.Mesh(new THREE.TubeGeometry(cableCurve,42,.035,8,false),rubber);g.add(cable);
 // top mast and three-colour stack light
 cylinder(g,-.86,3.34,-.34,.045,.045,.24,silver,16);
 for(const [yy,material] of [[3.48,redButton],[3.62,amberLed],[3.76,greenLed]]){
   const lamp=cylinder(g,-.86,yy,-.34,.085,.085,.115,material,20);stations.push(lamp);
 }
 // ventilation slots, tiny screws and feet detail
 for(let i=0;i<8;i++)box(g,.48+i*.09,.40,.777,.055,.018,.012,black,false);
 for(const xx of [-.95,.95])for(const yy of [.30,1.55]){const screw=cylinder(g,xx,yy,.79,.025,.025,.018,silver,12);screw.rotation.x=Math.PI/2;}
 // small manufacturer badge on cabinet front
 box(g,0,1.12,.795,.72,.20,.025,white,false);
 box(g,0,1.13,.815,.58,.09,.012,mat(0x174a7a,.2,.3),false);
 // subtle side service panel
 box(g,1.185,1.02,-.12,.035,.68,.68,whiteSide,false);
 for(let i=0;i<6;i++)box(g,1.21,.78+i*.085,-.12,.018,.025,.44,silver,false);
 stations.push(g);return g;
}
// 7 machines arranged in two orderly rows, leaving central aisle
const pos=[[-9,-4.8],[-3,-4.8],[3,-4.8],[9,-4.8],[-6,3.0],[0,3.0],[6,3.0]];
pos.forEach((p,i)=>makeConsole(p[0],p[1],i+1));

// Student work tables, chairs and instructor desk
function makeDesk(x,z){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 box(g,0,1.02,0,2.0,.14,1.1,mat(0x5d8490,.5,.48));
 for(const xx of [-.82,.82])for(const zz of [-.38,.38])box(g,xx,.50,zz,.10,1.0,.10,black);
 box(g,0,1.48,-.32,.82,.62,.10,black);box(g,0,1.48,-.255,.72,.48,.025,screenMat,false);
 box(g,0,1.10,.22,.70,.035,.34,mat(0x273d48),false);
}
function makeChair(x,z){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 box(g,0,.58,0,.58,.14,.58,mat(0x315b6b));
 box(g,0,.96,-.24,.58,.68,.13,mat(0x416f7e));
 for(const xx of [-.22,.22])for(const zz of [-.22,.22])box(g,xx,.29,zz,.055,.55,.055,trim);
}
makeDesk(-12,1);makeDesk(12,1);makeDesk(-12,-4);makeDesk(12,-4);
[[-12,2.2],[-10.3,2.2],[10.3,2.2],[12,2.2],[-12,-2.3],[12,-2.3],[-12,-5.5],[12,-5.5]].forEach(p=>makeChair(...p));
// student terminal keyboards, desktop lamps and stools
for(const [x,z] of [[-12,1],[12,1],[-12,-4],[12,-4]]){
 box(scene,x,1.12,z+.23,.72,.045,.28,mat(0x172d38,.45,.35),false);
 for(let k=0;k<5;k++)box(scene,x-.27+k*.135,1.15,z+.23,.09,.018,.13,mat(0x6d8990,.35,.4),false);
 cylinder(scene,x+.72,1.28,z-.25,.055,.055,.34,trim,12);
 const glow=new THREE.PointLight(0x39cfe0,1.2,2);glow.position.set(x+.72,1.55,z-.25);scene.add(glow);
}
// teacher podium
box(scene,-13,.72,7,2.6,1.4,1.5,mat(0x3d6675));box(scene,-13,1.65,6.6,1.0,.65,.12,black);box(scene,-13,1.65,6.53,.88,.52,.025,screenMat,false);
// CCTV cameras with bracket and lens
function makeCCTV(x,z,rot=0){
 const g=new THREE.Group();g.position.set(x,5.4,z);g.rotation.y=rot;scene.add(g);
 box(g,0,.15,0,.48,.16,.42,trim);line(g,[0,.1,0],[0,-.08,.38],0x8bb6c0,.035);
 box(g,0,-.16,.55,.42,.26,.52,black);cylinder(g,0,-.16,.83,.12,.12,.10,mat(0x8fbcc7),20);
 const lens=new THREE.Mesh(new THREE.CircleGeometry(.085,20),new THREE.MeshBasicMaterial({color:0x15ddec}));lens.position.set(0,-.16,.89);g.add(lens);
}
makeCCTV(-15,-9,.6);makeCCTV(15,-9,2.5);makeCCTV(-15,9,-.6);makeCCTV(15,9,-2.5);

// Human silhouettes for classroom scale
function limbBetween(parent,a,b,radius,material){
 const A=new THREE.Vector3(...a),B=new THREE.Vector3(...b),d=B.clone().sub(A);
 const mesh=new THREE.Mesh(new THREE.CylinderGeometry(radius*.82,radius,d.length(),12),material);
 mesh.position.copy(A.add(B).multiplyScalar(.5));mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),d.normalize());mesh.castShadow=true;parent.add(mesh);
 const joint=new THREE.Mesh(new THREE.SphereGeometry(radius*1.02,12,10),material);joint.position.set(...b);joint.castShadow=true;parent.add(joint);return mesh;
}
function makePerson(x,z,shirt=0x286b87,pose='standing'){
 const g=new THREE.Group();g.position.set(x,0,z);scene.add(g);
 const skin=new THREE.MeshStandardMaterial({color:0xc99573,roughness:.78});
 const top=new THREE.MeshStandardMaterial({color:shirt,roughness:.72});
 const pants=new THREE.MeshStandardMaterial({color:0x263744,roughness:.82});
 const shoe=new THREE.MeshStandardMaterial({color:0x151e24,roughness:.8});
 const hair=new THREE.MeshStandardMaterial({color:0x20252a,roughness:.9});
 // human proportions, layered torso, neck, head and face
 const torso=new THREE.Mesh(new THREE.CapsuleGeometry(.235,.48,7,14),top);torso.position.set(0,1.16,0);torso.castShadow=true;g.add(torso);
 const collar=new THREE.Mesh(new THREE.TorusGeometry(.105,.025,8,18),mat(0xd6dfe0,.05,.75));collar.position.set(0,1.40,.02);collar.rotation.x=Math.PI/2;g.add(collar);
 const neck=new THREE.Mesh(new THREE.CylinderGeometry(.075,.085,.16,14),skin);neck.position.y=1.53;g.add(neck);
 const head=new THREE.Mesh(new THREE.SphereGeometry(.17,24,20),skin);head.scale.set(.91,1.12,.90);head.position.set(0,1.75,.015);head.castShadow=true;g.add(head);
 // ears, hair cap, brows and eyes add facial definition
 for(const side of [-1,1]){
  const ear=new THREE.Mesh(new THREE.SphereGeometry(.035,12,10),skin);ear.position.set(side*.16,1.75,.005);g.add(ear);
  const eye=new THREE.Mesh(new THREE.SphereGeometry(.014,10,8),black);eye.position.set(side*.055,1.78,.164);g.add(eye);
  const brow=new THREE.Mesh(new THREE.BoxGeometry(.045,.012,.012),hair);brow.position.set(side*.055,1.81,.16);g.add(brow);
 }
 const hairCap=new THREE.Mesh(new THREE.SphereGeometry(.174,20,12,0,Math.PI*2,0,Math.PI*.58),hair);hairCap.position.set(0,1.82,-.008);g.add(hairCap);
 const nose=new THREE.Mesh(new THREE.SphereGeometry(.022,10,8),skin);nose.position.set(0,1.735,.17);g.add(nose);
 // trousers, knees and shoes; two articulated legs
 for(const side of [-1,1]){
  const hip=[side*.105,.91,0],knee=[side*.13,.49,.025],ankle=[side*.14,.13,.05];
  limbBetween(g,hip,knee,.095,pants);limbBetween(g,knee,ankle,.075,pants);
  const foot=new THREE.Mesh(new THREE.BoxGeometry(.16,.09,.28),shoe);foot.position.set(side*.14,.075,.13);foot.castShadow=true;g.add(foot);
 }
 // arms with shoulder, elbow, forearm and hands; relaxed / operating pose
 for(const side of [-1,1]){
  const shoulder=[side*.22,1.35,0];
  const elbow=pose==='operating'?[side*.36,1.12,.28]:[side*.36,1.05,.04];
  const hand=pose==='operating'?[side*.28,1.12,.55]:[side*.43,.78,.08];
  limbBetween(g,shoulder,elbow,.075,top);limbBetween(g,elbow,hand,.055,top);
  const palm=new THREE.Mesh(new THREE.SphereGeometry(.065,12,10),skin);palm.position.set(...hand);g.add(palm);
  for(let f=0;f<3;f++)limbBetween(g,[hand[0]+(f-1)*.018,hand[1]-.015,hand[2]],[hand[0]+(f-1)*.022,hand[1]-.07,hand[2]+.015],.012,skin);
 }
 // safety helmet: hard shell + brim, not a floating sphere
 const helmetShell=new THREE.Mesh(new THREE.SphereGeometry(.205,24,14,0,Math.PI*2,0,Math.PI/2),amber);helmetShell.scale.set(1.05,.72,1.0);helmetShell.position.set(0,1.91,0);g.add(helmetShell);
 const brim=new THREE.Mesh(new THREE.CylinderGeometry(.225,.225,.025,24),amber);brim.position.set(0,1.88,0);g.add(brim);
 // small reflective vest strips
 for(const yy of [1.05,1.24]){const strip=new THREE.Mesh(new THREE.BoxGeometry(.40,.035,.012),mat(0xe7d27b,.1,.45));strip.position.set(0,yy,.225);g.add(strip);}
 return g;
}
const people=[makePerson(-10,-1.2,0x286b87,'operating'),makePerson(10,-1.5,0x6a596f,'standing'),makePerson(-13,4,0x326e63,'standing')];
// Ceiling-mounted camera viewing frustum hints
const frustumMat=new THREE.LineBasicMaterial({color:0x16d9df,transparent:true,opacity:.18});
for(const [x,z] of [[-15,-9],[15,-9]]){const geo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x,5.3,z),new THREE.Vector3(x-2,1.0,z+3),new THREE.Vector3(x+2,1.0,z+3),new THREE.Vector3(x,5.3,z)]);scene.add(new THREE.Line(geo,frustumMat));}

let patrol=false, alarm=false, taskNo=826;
window.addEventListener('reset-twin-camera',()=>{camera.position.copy(defaultPos);controls.target.copy(defaultTarget);controls.update();});
window.addEventListener('twin-patrol',e=>{patrol=!!e.detail;});
let last=0;
function animate(t){
 requestAnimationFrame(animate);
 const sec=t*.001;
 stations.forEach((lamp,i)=>{if(lamp.material && lamp.material.emissive) lamp.material.emissiveIntensity=.55+.25*Math.sin(sec*2+i*.4);});
 if(patrol){people[0].position.x=-10+Math.sin(sec*.55)*2.3;people[0].position.z=-1.2+Math.cos(sec*.55)*1.0;}
 controls.update();renderer.render(scene,camera);
}
requestAnimationFrame(animate);
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);});
</script>

<script>
function updateClock(){const d=new Date();document.getElementById('clock').textContent=d.toLocaleDateString('zh-CN')+' '+d.toLocaleTimeString('zh-CN',{hour12:false});document.getElementById('camTime').textContent='CAM-01　'+d.toLocaleTimeString('zh-CN',{hour12:false});}
updateClock();setInterval(updateClock,1000);
let alarmOn=false,patrolOn=false,taskNo=826;
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>t.classList.remove('show'),1900);}
function selectDevice(el,n){document.querySelectorAll('.device').forEach(x=>x.classList.remove('selected'));el.classList.add('selected');document.getElementById('modalTitle').textContent='HPY-RS03 实训台 '+String(n).padStart(2,'0');document.getElementById('modalBody').innerHTML='<p>设备型号：HPY-RS03 恒佩优立式一体化实训控制台</p><p>设备状态：'+(n===4?'待检查':'运行中')+'</p><p>控制组件：数控显示屏、实体按键、急停按钮、手轮、三色信号灯</p><p>当前主轴转速：3200 rpm　设备温度：36.5 ℃</p><p>说明：当前数据为演示数据，可接入实训设备控制系统获取实时状态。</p>';document.getElementById('modalMask').classList.add('show');}
function showPanel(type){const title=document.getElementById('modalTitle'),body=document.getElementById('modalBody');const data={overview:['实训总览','<p>实训室设备共 7 台，在线 6 台，设备综合运行率 93.8%。</p><p>当前课堂实训任务：智能制造基础操作与数控编程。</p>'],devices:['设备管理','<p>HPY-RS03 恒佩优立式一体化实训控制台共 7 台。</p><p>设备包含操作面板、急停按钮、手轮、三色信号灯与显示终端。</p>'],data:['实训数据分析','<p>今日实训 128 人次，已完成任务 86 项，待完成任务 12 项。</p><p>平均实训效率 96.8%，设备健康指数 96%。</p>'],camera:['视频监控','<p>CAM-01 实训室全景监控模拟窗口在线。</p><p>当前页面展示的是监控界面示意，并非真实摄像头视频流。</p>']}[type];title.textContent=data[0];body.innerHTML=data[1];document.getElementById('modalMask').classList.add('show');}
function closePanel(e){if(!e||e.target.id==='modalMask')document.getElementById('modalMask').classList.remove('show');}
function resetCameraView(){window.dispatchEvent(new Event('reset-twin-camera'));toast('三维视角已复位');}
function toggleAlarm(){alarmOn=!alarmOn;document.getElementById('alarmBtn').classList.toggle('active',alarmOn);toast(alarmOn?'已展开设备告警：工位04状态待确认':'设备告警提示已收起');}
function runPatrol(){patrolOn=!patrolOn;document.getElementById('patrolBtn').classList.toggle('active',patrolOn);window.dispatchEvent(new CustomEvent('twin-patrol',{detail:patrolOn}));toast(patrolOn?'一键巡检已启动，巡检人员开始移动':'巡检结束，人员返回待命位置');}
function dispatchTask(){taskNo++;document.getElementById('task').textContent='实训任务 #'+String(taskNo).padStart(4,'0');toast('实训任务已下发：#'+taskNo);}
function drawLineChart(id,values,color){const c=document.getElementById(id),ctx=c.getContext('2d'),w=c.width,h=c.height;ctx.clearRect(0,0,w,h);ctx.strokeStyle='rgba(60,135,151,.25)';ctx.lineWidth=1;for(let y=20;y<h;y+=30){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}const max=Math.max(...values)+10,min=Math.min(...values)-10;ctx.beginPath();values.forEach((v,i)=>{const x=15+i*(w-30)/(values.length-1),y=h-18-(v-min)/(max-min)*(h-38);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});ctx.strokeStyle=color;ctx.lineWidth=3;ctx.shadowColor=color;ctx.shadowBlur=8;ctx.stroke();ctx.shadowBlur=0;values.forEach((v,i)=>{const x=15+i*(w-30)/(values.length-1),y=h-18-(v-min)/(max-min)*(h-38);ctx.beginPath();ctx.arc(x,y,3.5,0,Math.PI*2);ctx.fillStyle='#b9ffff';ctx.fill();});}
function drawBars(id,values){const c=document.getElementById(id),ctx=c.getContext('2d'),w=c.width,h=c.height;ctx.clearRect(0,0,w,h);ctx.font='10px Arial';values.forEach((v,i)=>{const bw=31,gap=23,x=12+i*(bw+gap),bh=v/100*(h-35),y=h-22-bh;ctx.fillStyle='#12bfd2';ctx.shadowColor='#10cddd';ctx.shadowBlur=7;ctx.fillRect(x,y,bw,bh);ctx.shadowBlur=0;ctx.fillStyle='#9edee5';ctx.fillText(v+'%',x,y-5);});}
drawLineChart('loadChart',[38,45,57,53,69,74,66,82,88,73,79],'#22dce8');
drawBars('effChart',[82,91,76,64,88,95,79]);
setInterval(()=>{const rpm=3200+Math.floor(Math.random()*45-22),load=66+Math.floor(Math.random()*6),temp=(36.3+Math.random()*.6).toFixed(1);document.getElementById('rpm').textContent=rpm;document.getElementById('load').textContent=load;document.getElementById('temp').textContent=temp;},1800);
</script>
</body>
</html>
"""
components.html(html, height=960, scrolling=False)
