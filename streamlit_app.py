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
st.caption("Generate colors, design tokens, and UI components with AI")

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
        "Glassmorphism",
        "Neumorphism"
    ]
)

theme_mode = st.sidebar.selectbox(
    "Theme Mode",
    [
        "Light",
        "Dark"
    ]
)

radius = st.sidebar.slider(
    "Border Radius",
    0,
    32,
    16
)

# -----------------------------------
# USER INPUT
# -----------------------------------
prompt = st.text_area(
    "Describe your product",
    placeholder="AI productivity tool for Gen Z designers",
    height=120
)

generate = st.button("Generate Design System")

# -----------------------------------
# GENERATE
# -----------------------------------
if generate and prompt:

    system_prompt = f"""
    You are a senior product designer and design system engineer.

    Generate:
    1. Color palette
    2. Design tokens
    3. Tailwind theme
    4. React Button component

    Style: {style}
    Theme: {theme_mode}
    Radius: {radius}px

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
        "accent": ""
      }},
      "tailwind": "",
      "component": ""
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

            st.json(data["tokens"])

            # -----------------------------------
            # TAILWIND CONFIG
            # -----------------------------------
            st.divider()

            st.subheader("⚡ Tailwind Theme")

            st.code(
                data["tailwind"],
                language="javascript"
            )

            # -----------------------------------
            # COMPONENT
            # -----------------------------------
            st.divider()

            st.subheader("🧩 React Component")

            st.code(
                data["component"],
                language="tsx"
            )

            # -----------------------------------
            # DOWNLOAD TOKENS
            # -----------------------------------
            st.divider()

            st.download_button(
                "Download Design Tokens",
                data=json.dumps(data["tokens"], indent=2),
                file_name="design-tokens.json",
                mime="application/json"
            )

        except Exception as e:

            st.error("Failed to parse AI response.")
            st.code(result)
            st.exception(e)
