import streamlit as st

from agent import process_email


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Email Management Agent",
    page_icon="📧",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("📧 AI Email Management Agent")

st.write(
    "Analyze an email, identify its priority and required action, "
    "extract tasks and deadlines, and generate a suggested reply."
)


# =========================================================
# EMAIL INPUT
# =========================================================

email = st.text_area(
    "Paste Email",
    height=300,
    placeholder="Paste your email here..."
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("Analyze Email"):

    if not email.strip():

        st.warning(
            "Please paste an email before analyzing."
        )

    else:

        with st.spinner(
            "Agent is analyzing the email..."
        ):

            try:

                result = process_email(email)

                # -----------------------------
                # Email Analysis
                # -----------------------------

                st.subheader("📊 Email Analysis")

                col1, col2 = st.columns(2)

                with col1:

                    st.write("**Category**")

                    st.write(
                        result["category"]
                    )

                with col2:

                    st.write("**Priority**")

                    st.write(
                        result["priority"]
                    )

                # -----------------------------
                # Required Action
                # -----------------------------

                st.subheader(
                    "🎯 Required Action"
                )

                st.write(
                    result["action"]
                )

                # -----------------------------
                # Tasks
                # -----------------------------

                st.subheader(
                    "✅ Tasks"
                )

                st.markdown(
                    result["tasks"]
                )

                # -----------------------------
                # Deadline
                # -----------------------------

                st.subheader(
                    "📅 Deadline"
                )

                st.write(
                    result["deadline"]
                )

                # -----------------------------
                # Suggested Reply
                # -----------------------------

                st.subheader(
                    "✉️ Suggested Reply"
                )

                st.info(
                    result["reply"]
                )

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "analyzing the email."
                )

                st.code(
                    str(e)
                )
