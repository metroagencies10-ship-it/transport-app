import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator
import io

# 1. SETUP TRANSLATOR
translator = GoogleTranslator(source='en', target='gu')

def translate_text(text):
    if not text: return ""
    return translator.translate(text)

# 2. COORDINATES (Adjust these to move text on the lines)
# (Left/Right, Up/Down)
COORDS = {
    'transport': (350, 115),
    'date': (1270, 122),
    'seller': (360, 215),
    'buyer': (300, 330),
    'dest': (370, 440)
}

st.set_page_config(page_title="Transport Form")

st.title("📦 Transport Form Generator")
st.write("Enter details in English; it will translate and fill the Gujarati form.")

# 3. INPUT FORM
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        t_name = st.text_input("Transport Name")
        s_name = st.text_input("Seller Name")
        b_name = st.text_input("Buyer Name")
    with col2:
        date_val = st.date_input("Date").strftime("%d/%m/%Y")
        dest_val = st.text_input("Destination (from Sarkhej to...)")

if st.button("Generate & Translate Form"):
    # Load Image
    try:
        img = Image.open("template.jpg")
        draw = ImageDraw.Draw(img)
        
        # Load Gujarati Font
        # Note: Size 30 is a starting point, change as needed
        font = ImageFont.truetype("NotoSansGujarati-Regular.ttf", 60)
        
        # Translation Logic
        st.write("Translating...")
        t_gu = translate_text(t_name)
        s_gu = translate_text(s_name)
        b_gu = translate_text(b_name)
        d_gu = translate_text(dest_val)

        # Draw on Image
        draw.text(COORDS['transport'], t_gu, font=font, fill="black")
        draw.text(COORDS['date'], date_val, font=font, fill="black")
        draw.text(COORDS['seller'], s_gu, font=font, fill="black")
        draw.text(COORDS['buyer'], b_gu, font=font, fill="black")
        draw.text(COORDS['dest'], d_gu, font=font, fill="black")

        # Convert to PDF
        pdf_img = img.convert('RGB')
        buf = io.BytesIO()
        pdf_img.save(buf, format="PDF")
        byte_im = buf.getvalue()

        # Show Preview
        st.image(img, caption="Preview", use_column_width=True)

        # Download Button
        st.download_button(
            label="Download Printable PDF",
            data=byte_im,
            file_name="transport_form.pdf",
            mime="application/pdf"
        )
    except FileNotFoundError:
        st.error("Error: Ensure template.jpg and NotoSansGujarati-Regular.ttf are in the folder.")