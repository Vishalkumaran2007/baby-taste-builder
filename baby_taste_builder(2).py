import streamlit as st
import cohere
import os

st.set_page_config(page_title="Baby Taste Builder", page_icon="👶", layout="centered")

st.title("👶 Baby Taste Builder")
st.write("Help your child explore the world through your own taste — safely and age-appropriately.")

# ✅ Load Cohere API key from secrets
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
co = cohere.Client(COHERE_API_KEY)

# 🎯 Form
with st.form("taste_form"):
    music = st.text_input("🎵 Favorite Music Artist or Band", placeholder="e.g., Taylor Swift")
    movie = st.text_input("🎬 Favorite Movie", placeholder="e.g., Avatar")
    book = st.text_input("📘 Favorite Book", placeholder="e.g., Harry Potter")
    submitted = st.form_submit_button("Generate Kid-Friendly Taste Matches")

# 🧠 Prompt builder
def build_prompt(music, movie, book):
    return f"""
You are a cultural assistant that helps parents introduce their children to media that reflects their own tastes in a child-friendly way.

Here is a parent's input:
- Music: {music}
- Movie: {movie}
- Book: {book}

Suggest one kid-friendly recommendation for each category (music, movie, book). Match the emotional tone, theme, or artistic style of the parent's tastes while keeping it safe and suitable for young children.

Return the results like this:

🎬 Movie: [Title] – [Why it matches]

🎵 Music: [Title] – [Why it matches]

📖 Book: [Title] – [Why it matches]
"""

# 🔁 Generate on submit
if submitted:
    with st.spinner("Crafting taste-matched content for your child..."):
        try:
            prompt = build_prompt(music, movie, book)

            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=400,
                temperature=0.8
            )

            output = response.generations[0].text.strip()
            st.success("Here’s your kid-friendly culture pack:")
            st.markdown(output)

        except Exception as e:
            st.error("Something went wrong while contacting Cohere.")
            st.exception(e)
