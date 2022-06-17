from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Pietro Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""




#------ new code 

import re
import requests
import numpy as np
import json
import os

#Ciudad Real - valdepeñas - gasoleo A habitual - 
url1 = 'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal='


resp = requests.get(url1)
print(resp.status_code)


data = pd.read_html(url1)
data

df = data[0] 
df

df.dtypes

df.Precio = df.Precio.str.replace('€', '').str.replace(',','.').astype('float')
df.Precio


date=pd.to_datetime('today').strftime("%Y%m%d")
df['date']=date
# df['date']=(pd.DatetimeIndex(df['date']) + pd.DateOffset(-1)).strftime("%Y%m%d") #add or reduce days
df












#------------- original code of the app


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
