function rand(a,b){ return Math.random()*(b-a)+a; }

function bubbles(container, n=12, dur=[1,2]){
  const wrap=document.createElement("div");
  wrap.className="mix-bubble-container";
  container.appendChild(wrap);
  for(let i=0;i<n;i++){
    const d=document.createElement("div");
    d.className="mix-bubble";
    const s=rand(6,16);
    d.style.width=`${s}px`; d.style.height=`${s}px`;
    d.style.left=`${rand(8,92)}%`;
    d.style.animationDuration=`${rand(dur[0],dur[1])}s`;
    d.style.opacity=String(rand(0.6,0.95));
    wrap.appendChild(d);
    d.addEventListener("animationend", ()=>d.remove());
  }
  setTimeout(()=>wrap.remove(), Math.ceil(dur[1]*1000)+800);
}

function pulse(el, cls="mix-pulse", t=500){
  if(!el) return; el.classList.add(cls); setTimeout(()=>el.classList.remove(cls), t);
}

function sparkOn(el){ if(el) el.style.opacity="1"; }
function sparkOff(el){ if(el) el.style.opacity="0"; }

function pour(liquidEl){
  if(!liquidEl) return;
  liquidEl.style.filter="brightness(1.1) saturate(1.1)";
  setTimeout(()=>{ liquidEl.style.filter=""; }, 300);
}

function cloud(el, density=1){
  if(!el) return;
  const fog=document.createElement("div");
  fog.style.position="absolute";
  fog.style.inset="0";
  fog.style.pointerEvents="none";
  fog.style.background=`radial-gradient(180px 120px at 50% 70%, rgba(255,255,255,${0.08*density}), transparent 60%),
                        radial-gradient(220px 160px at 40% 80%, rgba(255,255,255,${0.06*density}), transparent 60%)`;
  fog.style.opacity="0";
  fog.style.transition="opacity .5s ease";
  el.appendChild(fog);
  requestAnimationFrame(()=>{ fog.style.opacity="1"; });
  setTimeout(()=>{ fog.style.opacity="0"; setTimeout(()=>fog.remove(),300); }, 1200);
}

function fadeColor(liquidEl, to, ms=1200){
  if(!liquidEl) return;
  liquidEl.style.transition="background .6s ease";
  liquidEl.style.background = `linear-gradient(180deg, ${to}, rgba(255,255,255,0.08))`;
}

function swirl(el){
  if(!el) return;
  el.style.transition="transform .6s ease";
  el.style.transform="rotate(2deg) scale(1.01)";
  setTimeout(()=>{ el.style.transform=""; }, 600);
}

function smoke(el){
  if(!el) return;
  const s=document.createElement("div");
  s.style.position="absolute"; s.style.bottom="50%"; s.style.left="50%";
  s.style.width="8px"; s.style.height="8px"; s.style.borderRadius="50%";
  s.style.background="rgba(255,255,255,.85)"; s.style.filter="blur(2px)";
  s.style.transform="translate(-50%,0)";
  s.style.opacity="0.9";
  el.appendChild(s);
  const a= s.animate([
    { transform:"translate(-50%,0) scale(1)", opacity:0.9 },
    { transform:"translate(-60%,-80px) scale(1.8)", opacity:0 }
  ], { duration:1200, easing:"ease-out" });
  a.onfinish=()=>s.remove();
}

function triggerReactionFX(beaker, sparkEl, name){
  if(name==="pulse-bubbles"){ pulse(beaker, "mix-pulse", 900); bubbles(beaker, 16, [0.8,1.6]); sparkOn(sparkEl); setTimeout(()=>sparkOff(sparkEl), 500); }
  else if(name==="pulse-strong"){ pulse(beaker, "mix-pulse", 1200); bubbles(beaker, 22, [0.6,1.2]); cloud(beaker, 1); }
  else if(name==="fizz-fast"){ bubbles(beaker, 26, [0.5,1.0]); pulse(beaker, "mix-pulse", 500); }
  else if(name==="fizz-soft"){ bubbles(beaker, 18, [0.8,1.6]); }
  else if(name==="cloudy-fall"){ cloud(beaker, 1.2); }
  else if(name==="cloudy-dense"){ cloud(beaker, 1.6); }
  else if(name==="swirl-color"){ swirl(beaker); bubbles(beaker, 10, [0.8,1.5]); }
  else if(name==="swirl-deep"){ swirl(beaker); bubbles(beaker, 14, [0.8,1.5]); }
  else if(name==="fade-out"){ fadeColor(document.getElementById("liquid"), "rgba(255,255,255,0.12)"); }
  else if(name==="fade-green"){ fadeColor(document.getElementById("liquid"), "rgba(140,220,160,0.45)"); }
  else if(name==="smoke-line"){ smoke(beaker); }
  else if(name==="milk-cloud"){ cloud(beaker, 1.8); }
}

/* --- NEW: show/hide loader overlay on the beaker --- */
function showLoader(beaker){
  if(!beaker) return;
  let overlay = beaker.querySelector(".mix-loading");
  if(!overlay){
    overlay = document.createElement("div");
    overlay.className = "mix-loading";
    beaker.appendChild(overlay);
  }
}
function hideLoader(beaker){
  const overlay = beaker?.querySelector(".mix-loading");
  if(overlay) overlay.remove();
}

window.triggerReactionFX = triggerReactionFX;
window.pulse = pulse;
window.pour = pour;
/* expose new helpers */
window.showLoader = showLoader;
window.hideLoader = hideLoader;
