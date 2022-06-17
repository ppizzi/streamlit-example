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
url = 'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal='


#resp = requests.get(url)
#print(resp.status_code)


#data = pd.read_html(url)
#data



def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

def next_step(df):
    df.dtypes
    df.Precio = df.Precio.str.replace('€', '').str.replace(',','.').astype('float')
    df.Precio
    date=pd.to_datetime('today').strftime("%Y%m%d")
    df['date']=date
    # df['date']=(pd.DatetimeIndex(df['date']) + pd.DateOffset(-1)).strftime("%Y%m%d") #add or reduce days
    df    
    
    return
    

def main():
    st.set_page_config(page_title="Pietro s App", page_icon="🤖")
    st.title("Get Gas price Valdepenas")
    session = requests.Session()
    with st.form("my_form"):
        index = st.number_input("ID", min_value=0, max_value=100, key="index")

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.write("Result")
            #data = fetch(session, f"https://picsum.photos/id/{index}/info")
            data = fetch(session, url)

            if data:
                df = data[0] 
                df
                #st.image(data['download_url'], caption=f"Author: {data['author']}")
                next_step(df)
            else:
                st.error("Error")

                
                
                


if __name__ == '__main__':
    main()









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
