import streamlit as st
import pitch
import pandas as pd

df = pd.read_csv('base_formation.csv')

formation = st.selectbox("Pilih Formasi",
                         ('4-2-3-1','4-1-2-1-2','3-4-2-1', '4-3-1-2', '4-4-2', '4-3-3','4-2-2-2', '4-4-1-1'))

st.pyplot(pitch.createPitch(df, formation=formation))