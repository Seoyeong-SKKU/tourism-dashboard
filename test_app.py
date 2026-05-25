
import streamlit as st
import plotly.express as px
import pandas as pd
st.title('test')
df = pd.DataFrame({'x':[1,2,3],'y':[10,20,30]})
fig = px.line(df, x='x', y='y')
st.plotly_chart(fig)
