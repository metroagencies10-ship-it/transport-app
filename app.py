import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import io
import os

# 1. TRANSLATION FUNCTION WITH CORRECTIONS
def get_gujarati_translation(text):
    if not text: return ""
    
    # 1. Your custom business dictionary
    # Keep these in lowercase for easier matching
    corrections = {
        "shri": "શ્રી",
        "fortune": "ફોર્ચ્યુન",
        "spring": "સ્પ્રિંગ",
        "limited": "લિમિટેડ",
        "pvt": "પ્રા. લિ."
    }
    
    # 2. First, let's replace the specific words in your English input
    # so Google doesn't mess them up.
    words = text.split()
    processed_words = []
    
    for word in words:
        # Clean the word (remove dots or commas for the check)
        clean_word = word.lower().strip().replace(".", "").replace(",", "")
        
        if clean_word in corrections:
            # If it's in our dictionary, use our word
            processed_words.append(corrections[clean_word])
        else:
            # Otherwise, keep it as is for Google to translate later
            processed_words.append(word)
    
    # 3. Join them back together
    # If the text is now all Gujarati (e.g. "શ્રી ફોર્ચ્યુન"), 
    # Google Translate will just return it as is.
    final_input = " ".join(processed_words)
    
    try:
        translated = GoogleTranslator(source='en', target='gu').translate(final_input)
        return translated
    except:
        return final_input
        
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
