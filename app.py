import streamlit as st

from agent import process_email


st.set_page_config(
    page_title="AI Email Management Agent",
    page_icon="📧"
)


st.title("📧 AI Email Management Agent")

st.write(
    "Analyze an email, identify its priority and required action, "
    "extract tasks and deadlines, and generate a reply."
)


email = st.text_area(
    "Paste Email",
    height=250,
    placeholder="Paste an email here..."
)


if st.button("Analyze Email"):

    if not email.strip():

        st.warning("Please paste an email.")

    else:

        with st.spinner("Agent is analyzing the email..."):

            result = process_email(email)

        st.subheader("📊 Email Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Category",
                result["category"]
            )

        with col2:
            st.metric(
                "Priority",
                result["priority"]
            )

        st.subheader("🎯 Required Action")

        st.write(result["action"])

        st.subheader("✅ Tasks")

        st.write(result["tasks"])

        st.subheader("📅 Deadline")

        st.write(result["deadline"])

        st.subheader("✉️ Suggested Reply")

        st.info(result["reply"])
