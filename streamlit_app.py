import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd


#https://betterprogramming.pub/how-to-make-http-requests-in-streamlit-app-f22a77fd1ed7

def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

    
def fetchdf(session, url):
    try:
        st.text(url)
        result = session.get(url)
        st.text(result.status_code)
        #result.data
        #result.text
        #data = pd.read_html(result.text)
        #data
        #components.html(result)
        #df=data[0]
        #df
                
        
        #st.text('hereA')
        #st.text(pd.read_html(url)[1])
        #df=data[0]
        #df
        #st.text(result)
        return result
        #return data
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
            #data = fetch(session, f"https://picsum.photos/id/{index}/info")
            #url1 = 'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal='
            #st.text(url1)
            res = fetchdf(session, f'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal=' )
            
            #if data:
            #    st.image(data['download_url'], caption=f"Author: {data['author']}")
            #else:
            #    st.error("Error")

            if res:
                df=pd.read_html(res.text)
                df[0]
                #st.text('here2')
                #st.dataframe(df)
                #st.text('here3')
                #st.write(df)

if __name__ == '__main__':
    main()
