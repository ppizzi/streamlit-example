import streamlit as st
import requests
import pandas as pd


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

    
def fetchdf(session, url):
    try:
        result = session.get(url)
        return result
    except Exception:
        return {}

def main():
    st.set_page_config(page_title="Example App", page_icon="🤖")
    st.title("Get Image by Id")
    session = requests.Session()
    with st.form("my_form"):
        index = st.number_input("ID", min_value=0, max_value=100, key="index")

        submitted = st.form_submit_button("Submit")

        if submitted:
            st.write("Result")
            data = fetch(session, f"https://picsum.photos/id/{index}/info")
            url1 = 'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal='
            data1 = fetchdf(session1, url1)
            if data:
                st.image(data['download_url'], caption=f"Author: {data['author']}")
            else:
                st.error("Error")

            if data1:
                df=data[0]
                df

if __name__ == '__main__':
    main()
