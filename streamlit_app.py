import streamlit as st
from openai import OpenAI
import json

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="AI Design System Generator",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🎨 AI Design System Generator")
st.caption("Generate colors, tokens, and preview UI components")

# -----------------------------------
# API KEY
# -----------------------------------
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

if not openai_api_key:
    st.info("Please enter your OpenAI API key.", icon="🔑")
    st.stop()

# -----------------------------------
# OPENAI CLIENT
# -----------------------------------
client = OpenAI(api_key=openai_api_key)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("Design Options")

style = st.sidebar.selectbox(
    "Style",
    [
        "Minimal",
        "Modern",
        "Brutalist",
        "Luxury",
        "Glassmorphism"
    ]
)

theme_mode = st.sidebar.selectbox(
    "Theme",
    [
        "Light",
        "Dark"
    ]
)

radius = st.sidebar.slider(
    "Radius",
    0,
    32,
    16
)

# -----------------------------------
# INPUT
# -----------------------------------
prompt = st.text_area(
    "Describe your product",
    placeholder="Modern fintech app for Gen Z",
    height=120
)

generate = st.button("Generate Design System")

# -----------------------------------
# GENERATE
# -----------------------------------
if generate and prompt:

    system_prompt = f"""
    You are a senior UI/UX designer.

    Generate:
    1. Modern UI color palette
    2. Design tokens

    Style: {style}
    Theme: {theme_mode}

    Return ONLY valid JSON.

    Format:
    {{
      "brand_name": "",
      "concept": "",
      "colors": [
        {{
          "name": "",
          "hex": "",
          "usage": ""
        }}
      ],
      "tokens": {{
        "primary": "",
        "secondary": "",
        "background": "",
        "surface": "",
        "text": "",
        "border": "",
        "accent": ""
      }}
    }}
    """

    with st.spinner("Generating Design System..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.9
        )

        result = response.choices[0].message.content

        try:
            data = json.loads(result)

            tokens = data["tokens"]

            # -----------------------------------
            # BRAND INFO
            # -----------------------------------
            st.divider()

            st.subheader(f"✨ {data['brand_name']}")
            st.write(data["concept"])

            # -----------------------------------
            # COLOR PALETTE
            # -----------------------------------
            st.divider()

            st.subheader("🎨 Color Palette")

            cols = st.columns(len(data["colors"]))

            for idx, color in enumerate(data["colors"]):

                with cols[idx]:

                    st.markdown(
                        f"""
                        <div style="
                            background:{color['hex']};
                            height:140px;
                            border-radius:{radius}px;
                            border:1px solid #e5e7eb;
                        "></div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(f"### {color['name']}")
                    st.code(color["hex"])
                    st.caption(color["usage"])

            # -----------------------------------
            # TOKENS
            # -----------------------------------
            st.divider()

            st.subheader("📦 Design Tokens")

            st.json(tokens)

            # -----------------------------------
            # COMPONENT PREVIEW
            # -----------------------------------
            st.divider()

            st.subheader("🧩 Component Preview")

            preview_html = f"""
            <div style="
                background:{tokens['background']};
                padding:40px;
                border-radius:24px;
                border:1px solid {tokens['border']};
                font-family:Inter, sans-serif;
            ">

                <h3 style="
                    color:{tokens['text']};
                    margin-bottom:24px;
                ">
                    Button
                </h3>

                <div style="
                    display:flex;
                    gap:16px;
                    margin-bottom:40px;
                    flex-wrap:wrap;
                ">

                    <button style="
                        background:{tokens['primary']};
                        color:white;
                        border:none;
                        padding:14px 24px;
                        border-radius:{radius}px;
                        font-size:16px;
                        font-weight:600;
                        cursor:pointer;
                    ">
                        Primary Button
                    </button>

                    <button style="
                        background:{tokens['surface']};
                        color:{tokens['text']};
                        border:1px solid {tokens['border']};
                        padding:14px 24px;
                        border-radius:{radius}px;
                        font-size:16px;
                        font-weight:600;
                        cursor:pointer;
                    ">
                        Secondary Button
                    </button>

                </div>

                <h3 style="
                    color:{tokens['text']};
                    margin-bottom:24px;
                ">
                    TextField
                </h3>

                <div style="
                    display:flex;
                    flex-direction:column;
                    gap:20px;
                    max-width:420px;
                ">

                    <input
                        placeholder="Email Address"
                        style="
                            background:{tokens['surface']};
                            color:{tokens['text']};
                            border:1px solid {tokens['border']};
                            padding:16px;
                            border-radius:{radius}px;
                            font-size:16px;
                            outline:none;
                        "
                    />

                    <input
                        placeholder="Password"
                        type="password"
                        style="
                            background:{tokens['surface']};
                            color:{tokens['text']};
                            border:1px solid {tokens['border']};
                            padding:16px;
                            border-radius:{radius}px;
                            font-size:16px;
                            outline:none;
                        "
                    />

                </div>

            </div>
            """

            st.components.v1.html(
                preview_html,
                height=500
            )

            # -----------------------------------
            # DOWNLOAD
            # -----------------------------------
            st.divider()

            st.download_button(
                "Download Tokens JSON",
                data=json.dumps(tokens, indent=2),
                file_name="design-tokens.json",
                mime="application/json"
            )

        except Exception as e:

            st.error("Failed to parse AI response.")
            st.code(result)
            st.exception(e)
