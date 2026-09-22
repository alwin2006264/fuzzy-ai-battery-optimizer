import os

import streamlit as st


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fuzzy AI Battery Optimizer",
    page_icon="🔋",
    layout="centered"
)


# ============================================================
# LOAD GEMINI API KEY FROM STREAMLIT SECRETS
# ============================================================

try:

    if "GEMINI_API_KEY" in st.secrets:

        os.environ["GEMINI_API_KEY"] = (
            st.secrets["GEMINI_API_KEY"]
        )

except Exception:

    pass


# Import after loading Streamlit secrets
from main import analyze_battery


# ============================================================
# PAGE TITLE
# ============================================================

st.title(
    "🔋 Fuzzy AI Battery Optimizer"
)

st.write(
    "Describe your phone's current battery usage "
    "and the AI + fuzzy logic system will analyze it."
)


# ============================================================
# USER INPUT
# ============================================================

user_text = st.text_area(
    "Describe your battery usage:",
    height=180,
    placeholder=(
        "Example: My battery is 18%. "
        "I've been playing games for two hours, "
        "brightness is high, mobile data is on "
        "and my phone is getting very hot."
    )
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "⚡ Analyze Battery Usage",
    use_container_width=True
):

    # --------------------------------------------------------
    # CHECK INPUT
    # --------------------------------------------------------

    if not user_text.strip():

        st.warning(
            "Please enter a description first."
        )

    else:

        # ----------------------------------------------------
        # RUN ANALYSIS
        # ----------------------------------------------------

        with st.spinner(
            "Analyzing battery usage..."
        ):

            try:

                analysis = analyze_battery(
                    user_text
                )


                # ------------------------------------------------
                # GET RESULTS
                # ------------------------------------------------

                ai_inputs = analysis[
                    "ai_inputs"
                ]

                fuzzy_result = analysis[
                    "fuzzy_result"
                ]


                # ------------------------------------------------
                # SUCCESS MESSAGE
                # ------------------------------------------------

                st.success(
                    "Battery analysis completed!"
                )


                # =================================================
                # AI EXTRACTED INPUTS
                # =================================================

                st.subheader(
                    "🤖 AI Extracted Inputs"
                )

                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Battery",
                        f"{ai_inputs['battery_level']}%"
                    )

                    st.metric(
                        "App Usage",
                        f"{ai_inputs['app_usage']}%"
                    )

                    st.metric(
                        "Screen Usage",
                        f"{ai_inputs['screen_usage']}%"
                    )


                with col2:

                    st.metric(
                        "Network Usage",
                        f"{ai_inputs['network_usage']}%"
                    )

                    st.metric(
                        "Temperature",
                        f"{ai_inputs['temperature']}°C"
                    )


                # =================================================
                # FUZZY LOGIC RESULT
                # =================================================

                st.subheader(
                    "🧠 Fuzzy Logic Analysis"
                )


                score = fuzzy_result.get(
                    "score"
                )


                if score is not None:

                    st.metric(
                        "Power-Saving Score",
                        f"{float(score):.2f} / 100"
                    )

                    st.progress(
                        min(
                            max(
                                float(score) / 100,
                                0.0
                            ),
                            1.0
                        )
                    )


                # =================================================
                # MEMBERSHIP VALUES
                # =================================================

                membership = fuzzy_result.get(
                    "membership"
                )


                if membership:

                    st.subheader(
                        "📊 Membership Values"
                    )

                    st.json(
                        membership
                    )


                # =================================================
                # FUZZY RULE ACTIVATION
                # =================================================

                rule_activation = fuzzy_result.get(
                    "rule_activation"
                )


                if rule_activation:

                    st.subheader(
                        "⚙️ Rule Activation"
                    )

                    st.json(
                        rule_activation
                    )


                # =================================================
                # COMPLETE ANALYSIS
                # =================================================

                with st.expander(
                    "View complete analysis"
                ):

                    st.json(
                        fuzzy_result
                    )


            # ----------------------------------------------------
            # ERROR HANDLING
            # ----------------------------------------------------

            except Exception as error:

                st.error(
                    "❌ Analysis failed."
                )

                st.exception(
                    error
                )