import streamlit as st
import os
import pandas as pd 
import numpy as np


if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled=True

def process(art):  
    st.warning("Yout text is being processed",)



title = st.text_input('Titel des Artikels',)
article  = st.text_area('Artikel', key="art")
clicked=st.button("Artikel überprüfen", disabled=st.session_state.button_disabled, key="b_check", )

if st.session_state["art"]=="":
    st.session_state.button_disabled= not st.session_state.button_disabled

if clicked:
    process(st.session_state["art"])

