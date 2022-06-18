import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd

#import matplotlib.pyplot as plt



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
    
    
    
def update_hist(df, hist_df):
    #hist_df.head(5)
    st.write('new shape: ', hist_df.shape)
    hist_df.dtypes
    #hist_df.date = hist_df.date.astype('datetime')
    #hist_df = hist_df.append(df, ignore_index=True)
    #hist_df.sort_values(by=['Rótulo', 'Dirección','date'], ascending=[True, True, True], ignore_index=True, inplace=True)
    #hist_df.drop_duplicates(subset=['Rótulo','Dirección','date'], keep='first', inplace=True, ignore_index=True)
    #hist_df
    #st.write('f1')
    #st.dataframe( hist_df.tail(5))
    #st.write('f2')
    #st.write(hist_df)
    return hist_df



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
                df.Precio = df.Precio.str.replace('€', '').str.replace(',','.').astype('float')
                date=pd.to_datetime('today').strftime("%Y%m%d")
                df['date']=date
                df
                
                try: 
                    hist_df = pd.read_csv('gasolineras_ciudad_real.csv') 
                    st.write('loaded shape', hist_df.shape)
                    hist_df = update_hist(df,hist_df)
                    #hist_df
                except:
                    st.text('file not found')
                    
                hist_df
        
                    
        savefile = st.form_submit_button('save csv')
        if savefile:
            hist_df.to_csv('gasolineras_ciudad_real.csv', index=False)  
             

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


