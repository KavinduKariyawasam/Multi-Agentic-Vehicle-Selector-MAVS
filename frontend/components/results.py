import streamlit as st
from utils.parsing import extract_structured_result

CARD_CSS = """
<style>
.card { border: 1px solid rgba(49,51,63,0.2); border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.card h3 { margin: 0 0 6px 0; font-size: 1.05rem; }
.card .price { font-weight: 600; margin: 6px 0; }
.card .reason { color: rgba(49,51,63,0.8); }
.badge { display:inline-block; background:rgba(2,121,255,.08); border:1px solid rgba(2,121,255,.25);
         color:rgb(2,121,255); padding:2px 8px; border-radius:999px; font-size:.8rem; margin-bottom:8px; }
</style>
"""

def _render_card(pick: dict):
    model = pick.get("model_name", "Unknown")
    trim = pick.get("trim", "-")
    price = pick.get("price", "-")
    reason = pick.get("key_reason", "")
    try:
        price_fmt = f"${int(float(price)):,}"
    except Exception:
        price_fmt = f"${price}"
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<span class="badge">Rank #{pick.get("rank","?")}</span>', unsafe_allow_html=True)
    st.markdown(f"<h3>{model} — {trim}</h3>", unsafe_allow_html=True)
    st.markdown(f'<div class="price">Price: {price_fmt}</div>', unsafe_allow_html=True)
    if reason:
        st.markdown(f'<div class="reason">{reason}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_results(data):
    st.markdown(CARD_CSS, unsafe_allow_html=True)

    # Normalize to dict
    if isinstance(data, str):
        data = {"ok": True, "result": data, "meta": {}}
    if not isinstance(data, dict):
        st.error("Unexpected response type from backend.")
        st.write(data)
        return

    if not data.get("ok"):
        st.error(f"Error: {data.get('error', 'Unknown error')}")
        # with st.expander("Debug: full response", expanded=True):
        #     st.json(data)
        return

    result = data.get("result")
    meta = data.get("meta", {})

    # Always show raw for debugging
    # with st.expander("Debug: raw `result` from backend", expanded=True):
    #     if isinstance(result, (dict, list)):
    #         st.json(result)
    #     else:
    #         st.code(str(result), language="markdown")

    # Parse!
    parsed = extract_structured_result(result)

    st.subheader("Top Vehicle Recommendations")

    # st.write(parsed)

    if parsed and parsed.get("top_picks"):
        # st.json(parsed["top_picks"])
        picks = parsed["top_picks"]
        cols = st.columns(min(3, len(picks)))
        for i, pick in enumerate(picks[:3]):
            with cols[i]:
                _render_card(pick)
    else:
        st.info("This is what printing.")

    if parsed and parsed.get("analysis"):
        st.markdown("### Analysis")
        st.write(parsed["analysis"])

    if meta:
        st.caption(f"Search criteria: location={meta.get('location')}, budget={meta.get('budget')}")
