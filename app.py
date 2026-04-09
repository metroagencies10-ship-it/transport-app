import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import io
import os

# 1. TRANSLATION FUNCTION WITH CORRECTIONS
def get_gujarati_translation(text):
    if not text: return ""
    
    # Custom dictionary for common business words
    # You can add more words here!
    corrections = {
        "shri": "શ્રી",
        "fortune": "ફોર્ચ્યુન",
        "spring": "સ્પ્રિંગ"
    }
    
    clean_text = text.lower().strip()
    
    # If it's a simple business word, use our correction
    if clean_text in corrections:
        return corrections[clean_text]
    
    # Otherwise, let Google Translate handle it
    try:
        translated = GoogleTranslator(source='en', target='gu').translate(text)
        return translated
    except:
        return text # Return original if internet fails

# 2. SETTINGS
COORDS = {
    'transport': (350, 120),
    'date': (1280, 110),
    'seller': (350, 222),
    'buyer': (290, 324),
    'dest': (370, 435)
}
FONT_SIZE = 50 

st.set_page_config(page_title="Transport Form A5", layout="centered")
st.title("📦 Transport Form (Google Translate)")
st.info("Enter details in English. The app will translate them to Gujarati and format the PDF.")

# 3. INPUTS
col1, col2 = st.columns(2)
with col1:
    t_name = st.text_input("Transport Name")
    s_name = st.text_input("Seller Name")
    b_name = st.text_input("Buyer Name")
with col2:
    date_val = st.date_input("Date").strftime("%d/%m/%Y")
    dest_val = st.text_input("Destination (From Sarkhej to...)")

if st.button("Generate A5 PDF"):
    try:
        # Load Files
        base_dir = os.path.dirname(__file__)
        img = Image.open(os.path.join(base_dir, "template.jpg"))
        font_path = os.path.join(base_dir, "NotoSansGujarati-Regular.ttf")
        font = ImageFont.truetype(font_path, FONT_SIZE)
        draw = ImageDraw.Draw(img)

        # Translation
        with st.spinner('Translating...'):
            t_gu = get_gujarati_translation(t_name)
            s_gu = get_gujarati_translation(s_name)
            b_gu = get_gujarati_translation(b_name)
            d_gu = get_gujarati_translation(dest_val)

        # Draw text
        draw.text(COORDS['transport'], t_gu, font=font, fill="black")
        draw.text(COORDS['date'], date_val, font=font, fill="black")
        draw.text(COORDS['seller'], s_gu, font=font, fill="black")
        draw.text(COORDS['buyer'], b_gu, font=font, fill="black")
        draw.text(COORDS['dest'], d_gu, font=font, fill="black")

        # --- A5 HALF PAGE LOGIC ---
        a5_width, a5_height = 1748, 2480 
        a5_canvas = Image.new('RGB', (a5_width, a5_height), 'white')
        
        # Resize form to fit A5 width
        w_percent = (a5_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        resized_form = img.resize((a5_width, h_size), Image.Resampling.LANCZOS)
        
        # Paste on Top Half
        a5_canvas.paste(resized_form, (0, 0))

        # Show Preview
        st.image(img, caption="Preview", use_column_width=True)

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
        st.error(f"Something went wrong: {e}")
