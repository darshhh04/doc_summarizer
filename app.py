import streamlit as st

from src.ingestion import extract_text, normalize_transcript, word_count
from src.pipeline import process_transcript
from src.export import to_json, create_pdf

st.set_page_config(page_title="DocuSummarizer", page_icon="📝", layout="wide")
st.title("📝Darshan's DocuSummarizer")
st.caption("Upload a meeting transcript to get a summary, decisions, action items and risks.")


uploaded = st.file_uploader("Upload transcript (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"])


if uploaded and st.button("Process transcript"):
    try:
        raw = extract_text(uploaded.getvalue(), uploaded.name)
        text = normalize_transcript(raw)
        words = word_count(text)

        if words == 0:
            st.error("The file has no readable text.")
        else:
            if words > 50000:
                st.warning("This transcript is over 50,000 words. It may be slow.")
            st.info(f"Transcript loaded: {words} words")

            bar = st.progress(0, text="Starting...")

            def update(fraction, message):
                bar.progress(fraction, text=message)

            result, usage = process_transcript(text, uploaded.name, progress=update)
            st.session_state["result"] = result
            st.session_state["usage"] = usage
    except Exception as error:
        st.error(f"Something went wrong: {error}")


if "result" in st.session_state:
    result = st.session_state["result"]
    usage = st.session_state["usage"]

    tab_summary, tab_decisions, tab_actions, tab_risks = st.tabs(
        ["Summary", "Decisions", "Actions", "Risks"]
    )

    with tab_summary:
        st.write(result.summary)
        st.subheader("Topics")
        for topic in result.topics:
            st.markdown(f"**{topic.name}**")
            for point in topic.points:
                st.markdown(f"- {point}")

    with tab_decisions:
        if result.decisions:
            st.table([d.model_dump() for d in result.decisions])
        else:
            st.write("No decisions found.")

    with tab_actions:
        if result.action_items:
            st.table([a.model_dump() for a in result.action_items])
        else:
            st.write("No action items found.")

    with tab_risks:
        if result.risks:
            st.table([r.model_dump() for r in result.risks])
        else:
            st.write("No risks found.")

    
    st.caption(
        f"API calls: {usage['calls']} | "
        f"Tokens: {usage['input_tokens'] + usage['output_tokens']} | "
        f"Estimated cost: ${usage['estimated_cost_usd']}"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇ Download JSON", data=to_json(result),
                           file_name="meeting_summary.json", mime="application/json")
    with col2:
        st.download_button("⬇ Download PDF report", data=create_pdf(result, usage),
                           file_name="meeting_report.pdf", mime="application/pdf")