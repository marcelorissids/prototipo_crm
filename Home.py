import base64
import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO
from PIL import Image

st.title('Análise RFM')

#image_path = 'logo.png'
image = Image.open('logo.png')

st.set_page_config(page_title='Home')

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Análise RFM')
st.sidebar.markdown('## A melhor para seu ecommerce')
st.sidebar.markdown("""---""")

st.write('# FM Company')

st.markdown(
    """
    A melhor maneira de segmentar seus clientes!
    ### Ask for Help
    - Time de Data Science no Discord
        - @MarceloRissi
""")