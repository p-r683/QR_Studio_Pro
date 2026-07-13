import random
import streamlit as st

st.set_page_config(
    page_title="QR Studio Pro",
    page_icon="▩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def generate_qr_pattern(size: int = 16, seed: int = 7):
    """Generate a pseudo QR-code style boolean grid with real finder patterns
    (the nested squares) forced into three corners, like an actual QR code."""
    rng = random.Random(seed)
    grid = [[rng.random() > 0.56 for _ in range(size)] for _ in range(size)]

    def stamp_finder(top, left):
        for r in range(7):
            for c in range(7):
                on = (
                    r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4)
                )
                grid[top + r][left + c] = on

    stamp_finder(0, 0)
    stamp_finder(0, size - 7)
    stamp_finder(size - 7, 0)
    return grid


def render_qr_html(grid, cell=12, on_color="var(--accent)", off_color="transparent"):
    size = len(grid)
    rows_html = []
    for row in grid:
        cells = "".join(
            f'<div class="qr-cell" style="background:{on_color if v else off_color}"></div>'
            for v in row
        )
        rows_html.append(f'<div class="qr-row">{cells}</div>')
    return (
        f'<div class="qr-grid" style="--cell:{cell}px;">' + "".join(rows_html) + "</div>"
    )


# ----------------------------------------------------------------------------
# Theme
# ----------------------------------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');

:root{
  --bg:#060911;
  --bg-alt:#0A0F1A;
  --surface:#10151F;
  --surface-2:#151D2C;
  --border:#232C3F;
  --accent:#39FF9E;
  --accent-dim:#1F8F5C;
  --violet:#8B7FFF;
  --sky:#38BDF8;
  --amber:#FFB84D;
  --text:#EDEFF3;
  --muted:#8A93A8;
}

html, body, [class*="css"]{
  font-family:'Inter', sans-serif;
}

.stApp{
  background:
    radial-gradient(circle at 12% -10%, rgba(57,255,158,0.08), transparent 40%),
    radial-gradient(circle at 90% 0%, rgba(139,127,255,0.10), transparent 45%),
    var(--bg);
  color:var(--text);
}

section[data-testid="stSidebar"]{
  background:var(--bg-alt);
  border-right:1px solid var(--border);
}

#MainMenu, footer{visibility:hidden;}

/* ---------- Hero ---------- */
.hero-wrap{
  position:relative;
  border:1px solid var(--border);
  border-radius:22px;
  padding:44px 40px;
  background:linear-gradient(160deg, var(--surface) 0%, var(--surface-2) 100%);
  overflow:hidden;
  display:flex;
  align-items:center;
  gap:40px;
  flex-wrap:wrap;
}

.hero-wrap::before{
  content:"";
  position:absolute;
  top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg, transparent, var(--accent), transparent);
  animation:scan-x 3.5s linear infinite;
}

@keyframes scan-x{
  0%{transform:translateX(-100%);}
  100%{transform:translateX(100%);}
}

.hero-left{flex:1 1 380px;}

.eyebrow{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  letter-spacing:.14em;
  color:var(--accent);
  text-transform:uppercase;
  display:flex;
  align-items:center;
  gap:8px;
  margin-bottom:14px;
}

.eyebrow .dot{
  width:7px;height:7px;border-radius:50%;
  background:var(--accent);
  box-shadow:0 0 8px var(--accent);
  animation:pulse 1.6s ease-in-out infinite;
}

@keyframes pulse{
  0%,100%{opacity:1;}
  50%{opacity:.35;}
}

.hero-title{
  font-family:'Space Grotesk', sans-serif;
  font-weight:700;
  font-size:44px;
  line-height:1.08;
  margin:0 0 14px 0;
  letter-spacing:-0.01em;
}

.hero-title span{color:var(--accent);}

.hero-sub{
  font-size:16px;
  color:var(--muted);
  max-width:480px;
  line-height:1.55;
  margin-bottom:22px;
}

.hero-tags{display:flex; gap:8px; flex-wrap:wrap;}

.tag{
  font-family:'JetBrains Mono', monospace;
  font-size:11.5px;
  padding:6px 12px;
  border-radius:999px;
  border:1px solid var(--border);
  color:var(--muted);
  background:rgba(255,255,255,0.02);
}

/* ---------- QR visual ---------- */
.qr-frame{
  position:relative;
  padding:18px;
  background:#000;
  border-radius:16px;
  border:1px solid var(--border);
  box-shadow:0 0 0 1px rgba(57,255,158,0.06), 0 20px 60px -20px rgba(57,255,158,0.25);
}

.qr-grid{display:flex; flex-direction:column; gap:2px;}
.qr-row{display:flex; gap:2px;}
.qr-cell{width:var(--cell); height:var(--cell); border-radius:2px;}

.qr-frame::after{
  content:"";
  position:absolute;
  left:18px; right:18px; height:3px;
  top:18px;
  background:linear-gradient(90deg, transparent, var(--accent), transparent);
  box-shadow:0 0 14px 2px var(--accent);
  animation:scan-y 2.8s ease-in-out infinite;
}

@keyframes scan-y{
  0%{top:18px; opacity:0;}
  10%{opacity:1;}
  90%{opacity:1;}
  100%{top:calc(100% - 18px); opacity:0;}
}

/* ---------- Section headers ---------- */
.section-eyebrow{
  font-family:'JetBrains Mono', monospace;
  font-size:12px;
  color:var(--accent);
  letter-spacing:.12em;
  text-transform:uppercase;
  margin-bottom:6px;
}

.section-title{
  font-family:'Space Grotesk', sans-serif;
  font-weight:700;
  font-size:26px;
  margin:0 0 22px 0;
}

/* ---------- Feature cards ---------- */
.qcard{
  position:relative;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:16px;
  padding:20px 20px 18px 20px;
  height:100%;
  transition:transform .18s ease, border-color .18s ease, box-shadow .18s ease;
}

.qcard:hover{
  transform:translateY(-3px);
  border-color:rgba(57,255,158,0.35);
  box-shadow:0 14px 34px -18px rgba(0,0,0,0.6);
}

.qcard .bar{
  position:absolute; top:0; left:18px; right:18px; height:2px;
  background:var(--accent-color, var(--accent));
  border-radius:2px;
  opacity:.85;
}

.qcard .icon{font-size:22px; margin-bottom:10px; display:block;}
.qcard .title{font-family:'Space Grotesk', sans-serif; font-weight:600; font-size:16px; margin-bottom:6px;}
.qcard .desc{color:var(--muted); font-size:13.5px; line-height:1.5;}

/* ---------- Status chips (feature availability) ---------- */
.chip-row{display:flex; align-items:center; justify-content:space-between;
  padding:11px 14px; border:1px solid var(--border); border-radius:12px;
  background:var(--surface); margin-bottom:8px;}

.chip-row .label{font-size:14px; color:var(--text);}

.chip{
  font-family:'JetBrains Mono', monospace;
  font-size:10.5px;
  letter-spacing:.05em;
  padding:4px 10px;
  border-radius:999px;
  text-transform:uppercase;
}

.chip.live{background:rgba(57,255,158,0.12); color:var(--accent); border:1px solid rgba(57,255,158,0.3);}
.chip.soon{background:rgba(138,147,168,0.12); color:var(--muted); border:1px solid var(--border);}

/* ---------- Buttons ---------- */
.stButton>button{
  background:linear-gradient(135deg, var(--accent), #1FD98A);
  color:#04140C;
  font-weight:600;
  border:none;
  border-radius:10px;
  padding:0.55em 1.4em;
  font-family:'Space Grotesk', sans-serif;
  transition:filter .15s ease, transform .15s ease;
}
.stButton>button:hover{filter:brightness(1.08); transform:translateY(-1px);}

.stButton [kind="secondary"] button, .stButton>button:focus{outline:none;}

/* ---------- Divider ---------- */
hr, [data-testid="stDivider"]{border-color:var(--border) !important;}

/* ---------- Footer ---------- */
.qfooter{
  margin-top:10px;
  padding:18px 4px;
  color:var(--muted);
  font-size:12.5px;
  font-family:'JetBrains Mono', monospace;
  display:flex;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:10px;
  border-top:1px solid var(--border);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="eyebrow"><span class="dot"></span>QR STUDIO PRO</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Navigation")
    st.caption("v2.4.0 · Build · All systems operational")

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------

qr_grid = generate_qr_pattern(size=16, seed=11)
qr_html = render_qr_html(qr_grid, cell=11)

st.markdown(
    f"""
<div class="hero-wrap">
  <div class="hero-left">
    <div class="eyebrow"><span class="dot"></span>LIVE · GENERATING QR CODES SINCE 2024</div>
    <div class="hero-title">Every link,<br><span>one scan away.</span></div>
    <div class="hero-sub">
      Create, customize, and track QR codes for websites, WiFi, email, phone
      and WhatsApp — with logo embedding, gradients, and analytics built in.
    </div>
    <div class="hero-tags">
      <span class="tag">⚡ Instant generation</span>
      <span class="tag">🎨 Custom branding</span>
      <span class="tag">📊 Scan analytics</span>
    </div>
  </div>
  <div class="qr-frame">{qr_html}</div>
</div>
""",
    unsafe_allow_html=True,
)

c_a, c_b, _ = st.columns([1, 1, 3])
with c_a:
    st.button("Generate a QR code →", type="primary")
with c_b:
    st.button("View documentation")

st.write("")
st.write("")

# ----------------------------------------------------------------------------
# QR type cards
# ----------------------------------------------------------------------------

st.markdown('<div class="section-eyebrow">Generate</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Pick a QR code type</div>', unsafe_allow_html=True)

cards = [
    ("🌐", "Website QR", "Point straight to any URL — landing pages, portfolios or shops.", "var(--accent)"),
    ("📶", "WiFi QR", "Share network access without anyone typing a password.", "var(--sky)"),
    ("📧", "Email QR", "Pre-filled email drafts, ready to send in one scan.", "var(--amber)"),
    ("📞", "Phone QR", "Dial a number instantly from any camera app.", "var(--violet)"),
    ("💬", "WhatsApp QR", "Open a chat pre-loaded with your starting message.", "var(--accent)"),
    ("📷", "QR Scanner", "Decode any QR code straight from your browser.", "var(--sky)"),
]

row1 = st.columns(3)
row2 = st.columns(3)
for col, (icon, title, desc, color) in zip(row1 + row2, cards):
    with col:
        st.markdown(
            f"""
            <div class="qcard">
              <div class="bar" style="--accent-color:{color}"></div>
              <span class="icon">{icon}</span>
              <div class="title">{title}</div>
              <div class="desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.divider()

# ----------------------------------------------------------------------------
# Features status
# ----------------------------------------------------------------------------

st.markdown('<div class="section-eyebrow">Roadmap</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Features</div>', unsafe_allow_html=True)

left, right = st.columns(2)

live_features = ["Website QR", "WiFi QR", "Email QR", "Phone QR", "WhatsApp QR","Logo Embedding","QR Scanner", "History", "Analytics"]
soon_features = ["Gradient QR"]

with left:
    st.markdown("**Available now**")
    for f in live_features:
        st.markdown(
            f'<div class="chip-row"><span class="label">{f}</span>'
            f'<span class="chip live">Live</span></div>',
            unsafe_allow_html=True,
        )

with right:
    st.markdown("**Coming soon**")
    for f in soon_features:
        st.markdown(
            f'<div class="chip-row"><span class="label">{f}</span>'
            f'<span class="chip soon">Soon</span></div>',
            unsafe_allow_html=True,
        )

st.divider()
st.success("👈 Select a page from the sidebar to begin.")

st.markdown(
    """
    <div class="qfooter">
      <span>© 2026 QR Studio Pro</span>
      <span>Built with Streamlit · Python</span>
      <span>Status: <span style="color:var(--accent)">● Operational</span></span>
    </div>
    """,
    unsafe_allow_html=True,
)
