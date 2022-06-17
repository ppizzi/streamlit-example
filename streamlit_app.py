import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd

import matplotlib.pyplot as plt



#USEFUL LINKS
#https://discuss.streamlit.io/t/rendering-data-frames-from-an-html-code/14843/4
#https://betterprogramming.pub/how-to-make-http-requests-in-streamlit-app-f22a77fd1ed7
#https://share.streamlit.io/gerardrbentley/streamlit-random/main/pandas_power.py
#https://discuss.streamlit.io/t/no-module-named-lxml/25251
#https://stackoverflow.com/questions/44954802/python-importerror-lxml-not-found-please-install-it
#https://github.com/gerardrbentley/streamlit-random/blob/9711973519977960365df32f077b58f31277c732/pandas_power.py#L104
#https://discuss.streamlit.io/t/pandas-read-html-as-a-web-app-scrape-tables-from-urls/23565
#https://betterprogramming.pub/how-to-make-http-requests-in-streamlit-app-f22a77fd1ed7
#https://docs.streamlit.io/library/api-reference/data/st.dataframe





    
def fetchdf(session, url):
    try:
        st.text(url)
        result = session.get(url)
        st.text(result.status_code)
        return result
    except Exception:
        return {}

def main():
    #st.set_page_config(page_title="MyGasApp", page_icon="🤖")
    st.set_page_config(page_title="MyGasApp", page_icon=":fuelpump:")
    st.title("Get gas prices in Valdepeñas")
    session = requests.Session()
   
    with st.form("my_form"):
        #index = st.number_input("ID", min_value=0, max_value=100, key="index")
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.write("Result")
            res = fetchdf(session, f'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal=' )
            if res:
                df=pd.read_html(res.text)[0]
                df
                
                try: 
                    hist_df = pd.read_csv('gasolineras_ciudad_real.csv') 
                    hist_df.shape
                    #hist_df.head(5)
                    hist_df = hist_df.append(df, ignore_index=True)
                    st.text('shape: ', hist_df.shape)
                    st.dataframe( hist_df.tail(5) )
                    hist_df.sort_values(by=['Rótulo', 'Dirección','date'], ascending=[True, True, True], ignore_index=True, inplace=True)
                    hist_df.drop_duplicates(subset=['Rótulo','Dirección','date'], keep='first', inplace=True, ignore_index=True)
                    st.text('shape: ', hist_df.shape)
                    #hist_df.head(20)
                    hist_df.to_csv('gasolineras_ciudad_real.csv', index=False)
                    gasolineras = list(hist_df.Dirección.unique() )
                    gasolineras
                    gasolineras_ID = ['A','B','C','D','E','F','G','H','I','J','L','M','N','O','P']
                    if not(len(gasolineras) == len(gasolineras_ID)) :
                        input('there is a mismatch between the two lists')
                    else:
                        gas_df = pd.DataFrame( {'gasolineras': gasolineras, 'ID':gasolineras_ID})
                        gas_df
                    
                    hist_df['ID'] = list(map(lambda x: gasolineras_ID[gasolineras.index(x)], hist_df['Dirección'] ) )
                    hist_df
                    hist_df.date = pd.to_datetime(hist_df.date,format='%Y%m%d')
                    hist_df.head(5)
                    hist_df['address']=hist_df.Rótulo + ' ' + hist_df.Dirección
                    hist_df
                    hist_df_hor = hist_df.pivot(index = 'date' , columns = ['ID'], values ='Precio')
                    hist_df_hor.head(5)
                    hist_df_hor.reset_index(inplace=True)
                    print(hist_df_hor.dtypes)
                    hist_df_hor.head()
                    legenda = hist_df[['ID', 'Rótulo', 'Dirección']].drop_duplicates(subset='ID')
                    legenda
                    
                    fig, ax = plt.subplots()
                    ax.plot(hist_df_hor.date, hist_df_hor.H, color='green', marker='x', label='Fast Fuel')
                    ax.plot(hist_df_hor.date, hist_df_hor.B, color='red', marker='x', label='Cepsa')
                    plt.grid(True)
                    ax.set_xlabel("Time")
                    ax.set_ylabel("Price")
                    fig.suptitle("Precio gasoleo Valdepenas")
                    plt.legend(loc='upper left')
                 except:
                    st.text('file not found')

                

                

if __name__ == '__main__':
    main()
    
    
#--- old code

#def fetch(session, url):
#    try:
#        result = session.get(url)
#        return result.json()
#    except Exception:
#        return {}


#data = fetch(session, f"https://picsum.photos/id/{index}/info")
#url1 = 'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal='
#st.text(url1)

#if data:
#    st.image(data['download_url'], caption=f"Author: {data['author']}")
#else:
#    st.error("Error")


