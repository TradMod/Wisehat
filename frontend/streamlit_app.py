import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import generate_report, WiseHatReport


def rating_color(rating: float) -> tuple[str, str, str]:
    if rating >= 9.0:
        return "#1B7F4B", "#E6F4EA", "Excellent"
    if rating >= 8.0:
        return "#2E9E5B", "#E8F5E9", "Very Good"
    if rating >= 7.0:
        return "#B8860B", "#FFF8E1", "Good"
    if rating >= 5.0:
        return "#C2570A", "#FFF1E0", "Caution"
    return "#B3261E", "#FDECEA", "High Risk"


def pill(label: str, value: str, bg: str = "#F3F4F6", fg: str = "#1F2937") -> str:
    return f"""
    <div style="display:inline-flex;align-items:center;gap:8px;
                background:{bg};color:{fg};padding:8px 16px;border-radius:999px;
                font-size:14px;font-weight:600;">
      <span style="opacity:.7;font-weight:500;">{label}</span>
      <span>{value}</span>
    </div>
    """


def render_list(items: list[str]) -> None:
    if not items:
        st.markdown("_No items documented._")
        return
    for item in items:
        st.markdown(f"• &nbsp; {item}")


def render_section(title: str, items: list[str], expanded: bool = False) -> None:
    if not items:
        return
    with st.expander(f"{title} &nbsp; `({len(items)})`", expanded=expanded):
        render_list(items)


def render_report(report: WiseHatReport) -> None:
    rec = report.wisehat_recommendation
    fg, bg, tier = rating_color(rec.rating)

    st.markdown(
        pill("PLATFORM", report.platform_name) + pill("PROGRAM", report.program_name),
        unsafe_allow_html=True,
    )
    st.write("")

    rating, verdict = st.columns([1, 1])
    with rating:
        st.markdown(
            f"""
            <div style="background:{bg};border:1px solid {fg};border-radius:14px;
                        padding:18px 20px;text-align:center;">
              <div style="font-size:13px;color:#6B7280;letter-spacing:1px;">WISEHAT RATING</div>
              <div style="font-size:46px;font-weight:800;color:{fg};line-height:1.1;">
                {rec.rating:.1f}<span style="font-size:22px;opacity:.6;">/10</span>
              </div>
              <div style="font-size:14px;font-weight:700;color:{fg};margin-top:4px;">{tier}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with verdict:
        st.markdown(
            f"""
            <div style="background:#FFFFFF;border:1px solid #E5E7EB;border-radius:14px;
                        padding:18px 20px;height:100%;">
              <div style="font-size:13px;color:#6B7280;letter-spacing:1px;">VERDICT</div>
              <div style="font-size:18px;font-weight:700;color:#111827;margin-top:6px;">
                {rec.verdict}
              </div>
              <div style="font-size:13px;color:#374151;margin-top:10px;">{rec.summary}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### Program Overview")
    with st.container(border=True):
        st.write(report.program_overview)

    st.markdown("#### Flags at a Glance")
    green, red = st.columns(2)
    with green:
        with st.container(border=True):
            st.markdown(f"##### Green Flags `{len(report.green_flags)}`")
            render_list(report.green_flags)
    with red:
        with st.container(border=True):
            st.markdown(f"##### Red Flags `{len(report.red_flags)}`")
            render_list(report.red_flags)

    st.markdown("#### Deep Dive")
    render_section("Mandatory Requirements", report.mandatory_requirements)
    render_section("Scope & Impact Analysis", report.scope_and_impact_analysis)
    render_section("Other Things to Consider", report.other_things_to_consider)
    render_section("Hunter Tips", report.hunter_tips, expanded=True)

    st.markdown("#### Before You Hunt Checklist")
    with st.container(border=True):
        if not report.before_you_hunt_checklist:
            st.markdown("_No checklist items documented._")
        for idx, item in enumerate(report.before_you_hunt_checklist):
            st.checkbox(item, value=False, key=f"chk_{idx}")


st.set_page_config(page_title="WiseHat", layout="wide")

st.markdown(
    """
    <style>
      .block-container {max-width: 1100px; padding-top: 2rem;}
      .stCheckbox {font-size: 14px;}
      .stMarkdown p {font-size: 14px;}
    </style>
    """,
    unsafe_allow_html=True,
)

title, subtitle = st.columns([1, 2])
with title:
    st.markdown(
        """
        <div style="font-size:34px;font-weight:800;letter-spacing:-0.5px;">
          WiseHat
        </div>
        """,
        unsafe_allow_html=True,
    )
with subtitle:
    st.markdown(
        """
        <div style="color:#6B7280;font-size:14px;padding-top:14px;">
          AI-powered intelligence for bug bounty hunters — analyze any BBP
          before you spend a single hour hunting.
        </div>
        """,
        unsafe_allow_html=True,
    )
st.divider()

with st.container(border=True):
    st.markdown("##### Program Details")
    plat_col, name_col = st.columns([1, 2])
    with plat_col:
        platform = st.selectbox("BBP Platform", options=["Immunefi", "Hackenproof"])
    with name_col:
        program_name = st.text_input(
            "Program Name",
            placeholder="exact slug / username  (e.g. solana, aave-v3)",
        )
    generate = st.button("Generate Intelligence Report", type="primary", use_container_width=True)

if generate:
    if not program_name.strip():
        st.error("Please enter a program name.")
    else:
        with st.status("WiseHat is generating the intelligence report...", expanded=True) as status:
            st.write(f"Fetching program data from **{platform}**...")
            st.write(f"Analyzing **{program_name.strip()}**...")
            try:
                report = generate_report(platform, program_name.strip())
                st.session_state["report"] = report
                status.update(label="Report ready!", state="complete")
            except ValueError as e:
                status.update(label="Could not generate report", state="error")
                st.error(str(e))
            except Exception as e:
                status.update(label="Failed to generate report", state="error")
                st.exception(e)

if "report" in st.session_state:
    render_report(st.session_state["report"])
