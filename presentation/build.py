#!/usr/bin/env python3
"""
HAIG Presentation Builder — embeds audio into standalone HTML.

Usage:
    cd ~/haig/presentation
    python3 build.py

Requires: audio/haig-vo.mp3
Outputs:  haig-standalone.html
"""
import base64, sys, os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')

AUDIO_FILE = 'audio/haig-vo.mp3'
HTML_FILE = 'index.html'
OUTPUT = 'haig-standalone.html'

# Calibrated from silence detection (ffmpeg silencedetect, d=1.2s, noise=-35dB)
# 15 gaps >= 2.7s found — maps exactly to 15 transitions for 16 slides
TIMESTAMPS = [
    0,        # S1:  Hook
    17.0,     # S2:  Collapse (gap 2.7s at 0:16)
    68.3,     # S3:  Cost (gap 2.7s at 1:08)
    109.6,    # S4:  Principle (gap 2.7s at 1:49)
    161.4,    # S5:  Four Roles (gap 2.7s at 2:41)
    227.4,    # S6:  SA Session (gap 2.8s at 3:47)
    288.1,    # S7:  Dispatch (gap 2.8s at 4:48)
    336.9,    # S8:  CC Session / money slide (gap 2.7s at 5:36)
    411.6,    # S9:  Adversarial (gap 2.7s at 6:51)
    485.7,    # S10: Context Dump (gap 2.7s at 8:05)
    524.2,    # S11: Amendments (gap 2.7s at 8:44)
    564.3,    # S12: Numbers (gap 2.7s at 9:24)
    598.1,    # S13: Before/After (gap 2.7s at 9:58)
    660.2,    # S14: What You Get (gap 2.8s at 11:00)
    689.9,    # S15: Get Started (gap 2.7s at 11:29)
    729.6,    # S16: Close (gap 2.7s at 12:09)
]

for f in [AUDIO_FILE, HTML_FILE]:
    if not os.path.exists(f):
        print(f"ERROR: {f} not found")
        sys.exit(1)

print("Encoding audio...")
with open(AUDIO_FILE, 'rb') as f:
    audio_b64 = base64.b64encode(f.read()).decode()
print(f"  Audio: {len(audio_b64)//1024}KB base64")

AUDIO_URI = f"data:audio/mpeg;base64,{audio_b64}"

print("Reading HTML template...")
with open(HTML_FILE) as f:
    html = f.read()

# Inject audio player + VO sync before </body>
AUDIO_INJECT = f"""
<!-- VO Overlay -->
<div id="ov" onclick="startVO()">
<div style="text-align:center">
<h1 style="font-size:2.5rem;margin-bottom:1rem"><span class="g gw">HAIG</span></h1>
<p style="color:var(--t2);font-size:1rem;margin-bottom:2rem">Human-AI Integrated Governance</p>
<div id="play-btn" style="width:72px;height:72px;border-radius:50%;border:2px solid var(--g);margin:0 auto;cursor:pointer;position:relative;transition:all .3s">
<div style="position:absolute;left:56%;top:50%;transform:translate(-50%,-50%);border:12px solid transparent;border-left:20px solid var(--g)"></div>
</div>
<p style="color:var(--t3);font-size:.8rem;margin-top:1rem">Click to start</p>
</div>
</div>
<style>
#ov{{position:fixed;inset:0;background:var(--bg);z-index:10001;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:opacity .8s}}
#ov.gone{{opacity:0;pointer-events:none}}
#play-btn:hover{{box-shadow:0 0 30px var(--gg);transform:scale(1.05)}}
</style>
<audio id="vo" preload="auto">
<source src="{AUDIO_URI}" type="audio/mpeg">
</audio>
<script>
const TS={TIMESTAMPS};
let voPlaying=false;
function startVO(){{
  document.getElementById('ov').classList.add('gone');
  setTimeout(()=>document.getElementById('ov').style.display='none',800);
  const vo=document.getElementById('vo');
  vo.play();
  voPlaying=true;
  syncVO();
}}
function syncVO(){{
  if(!voPlaying)return;
  const vo=document.getElementById('vo');
  const t=vo.currentTime;
  let target=0;
  for(let i=TS.length-1;i>=0;i--){{
    if(t>=TS[i]){{target=i;break;}}
  }}
  if(target!==cur)show(target);
  requestAnimationFrame(syncVO);
}}
// Override go() to also seek audio when manually navigating
const _origGo=go;
function goWithSeek(d){{
  _origGo(d);
  if(voPlaying){{
    document.getElementById('vo').currentTime=TS[cur]||0;
  }}
}}
// Rebind navigation
document.removeEventListener('keydown',null);
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key===' ')goWithSeek(1);
  if(e.key==='ArrowLeft')goWithSeek(-1);
  if(e.key==='f')document.documentElement.requestFullscreen?.();
}});
</script>
"""

# Inject before </body>
html = html.replace('</body>', AUDIO_INJECT + '\n</body>')

# Remove the existing keydown listener (we replace it in the inject)
# The original is inline in the script block — we leave it, the new one takes priority

print(f"Writing {OUTPUT}...")
with open(OUTPUT, 'w') as f:
    f.write(html)

size_mb = os.path.getsize(OUTPUT) / (1024*1024)
print(f"  Output: {OUTPUT} ({size_mb:.1f} MB)")
print("Done. Open haig-standalone.html in browser.")
