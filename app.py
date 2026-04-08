import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import io
import os

# 1. TRANSLITERATION FUNCTION (Sound-based)
def get_gujarati_sound(text):
    if not text: return ""
    # Converts phonetic English to Gujarati Script
    return transliterate(text.lower(), sanscript.ITRANS, sanscript.GUJARATI)

# 2. COORDINATES & SETTINGS
COORDS = {
    'transport': (340, 110),
    'date': (1300, 115),
    'seller': (330, 215),
    'buyer': (265, 335),
    'dest': (345, 435)
}
FONT_SIZE = 50 # Adjusted to be larger as requested

st.set_page_config(page_title="Transport Form A5", layout="centered")
st.title("📦 Phonetic Transport Form")
st.info("Type using sounds (e.g., 'Sarkhej' or 'Mahavir'). It will convert to Gujarati script.")

# 3. INPUTS
col1, col2 = st.columns(2)
with col1:
    t_name = st.text_input("Transport Name (e.g. mahavir)")
    s_name = st.text_input("Seller Name")
    b_name = st.text_input("Buyer Name")
with col2:
    date_val = st.date_input("Date").strftime("%d/%m/%Y")
    dest_val = st.text_input("Destination (e.g. baroda)")

if st.button("Generate A5 PDF"):
    try:
        # Load Image and Font
        base_dir = os.path.dirname(__file__)
        img = Image.open(os.path.join(base_dir, "template.jpg"))
        font_path = os.path.join(base_dir, "NotoSansGujarati-Regular.ttf")
        font = ImageFont.truetype(font_path, FONT_SIZE)
        draw = ImageDraw.Draw(img)

        # Process Sound-based Typing
        t_gu = get_gujarati_sound(t_name)
        s_gu = get_gujarati_sound(s_name)
        b_gu = get_gujarati_sound(b_name)
        d_gu = get_gujarati_sound(dest_val)

        # Draw text on original image
        draw.text(COORDS['transport'], t_gu, font=font, fill="black")
        draw.text(COORDS['date'], date_val, font=font, fill="black")
        draw.text(COORDS['seller'], s_gu, font=font, fill="black")
        draw.text(COORDS['buyer'], b_gu, font=font, fill="black")
        draw.text(COORDS['dest'], d_gu, font=font, fill="black")

        # --- A5 HALF PAGE LOGIC ---
        a5_width, a5_height = 1748, 2480 # 300 DPI
        a5_canvas = Image.new('RGB', (a5_width, a5_height), 'white')
        
        # Resize form to fit A5 width
        w_percent = (a5_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        resized_form = img.resize((a5_width, h_size), Image.Resampling.LANCZOS)
        
        # Paste on Top Half
        a5_canvas.paste(resized_form, (0, 0))

        # Show Preview
        st.image(img, caption="Filled Form Preview", use_column_width=True)

        # Save to PDF
        buf = io.BytesIO()
        a5_canvas.save(buf, format="PDF")
        
        st.download_button(
            label="Download A5 PDF",
            data=buf.getvalue(),
            file_name=f"form_{t_name}.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Error: {e}")
