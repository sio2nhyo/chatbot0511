```python
import streamlit as st
from openai import OpenAI
import json

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Color Generator",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("🎨 AI Color System Generator")
st.caption("Generate modern design system color palettes using AI")

st.write(
    """
    Describe the brand, mood, or product you want to design for.
    
    Examples:
    - "Fintech app for Gen Z"
    - "Luxury fashion brand"
    - "Minimal productivity tool"
    - "AI startup with futuristic feeling"
    """
)

# -----------------------------
# API KEY
# -----------------------------
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="sk-..."
)

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
    st.stop()

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI(api_key=openai_api_key)

# -----------------------------
# Session State
# -----------------------------
if "palette" not in st.session_state:
    st.session_state.palette = None

# -----------------------------
# User Input
# -----------------------------
prompt = st.text_area(
    "Describe your brand or UI",
    placeholder="Example: Modern fintech app with trust, premium, and clean feeling",
    height=120
)

generate = st.button("Generate Color System")

# -----------------------------
# Generate Colors
# -----------------------------
if generate and prompt:

    system_prompt = """
    You are a senior UI/UX designer and design system expert.

    Your task is to generate a modern UI color system.

    Return ONLY valid JSON.

    Format:
    {
      "brand_name": "",
      "concept": "",
      "colors": [
        {
          "name": "",
          "hex": "",
          "usage": ""
        }
      ]
    }

    Requirements:
    - Generate 6 colors
    - Include:
      - Primary
      - Secondary
      - Background
      - Surface
      - Text
      - Accent
    - Colors should feel cohesive
    - Use modern startup-style palettes
    """

    with st.spinner("Generating design system colors..."):

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
            palette = json.loads(result)
            st.session_state.palette = palette

        except:
            st.error("Failed to parse AI response.")
            st.code(result)

# -----------------------------
# Display Palette
# -----------------------------
if st.session_state.palette:

    palette = st.session_state.palette

    st.divider()

    st.subheader(f"✨ {palette['brand_name']}")
    st.write(palette["concept"])

    cols = st.columns(len(palette["colors"]))

    for idx, color in enumerate(palette["colors"]):

        with cols[idx]:

            st.markdown(
                f"""
                <div style="
                    background:{color['hex']};
                    height:140px;
                    border-radius:20px;
                    border:1px solid #e5e7eb;
                "></div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(f"### {color['name']}")
            st.code(color["hex"])
            st.caption(color["usage"])

    st.divider()

    st.subheader("📦 JSON Tokens")

    st.json(palette)
```
