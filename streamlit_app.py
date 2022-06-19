import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from gsheetsdb import connect


# Create a connection object.
conn = connect() 

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
    st.write(row)


#USEFUL LINKS
#https://discuss.streamlit.io/t/after-upgrade-to-the-latest-version-now-this-error-id-showing-up-arrowinvalid/15794/26
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

    #hist_df = hist_df.astype(str)
    hist_df.date = hist_df.date.astype(str)
    hist_df = hist_df.append(df, ignore_index=True)
    st.write('new shape: ', hist_df.shape)
    hist_df.sort_values(by=['Rótulo', 'Dirección','date'], ascending=[True, True, True], ignore_index=True, inplace=True)
    hist_df.drop_duplicates(subset=['Rótulo','Dirección','date'], keep='first', inplace=True, ignore_index=True)

    return hist_df


def plot_hist(hist_df):
    hist_df.Precio = hist_df.Precio.astype(float)
    #hist_df.date = hist_df.date.astype(datetime)
    hist_df.date = pd.to_datetime(hist_df.date,format='%Y%m%d')
    st.write('dtypes new df with date: ', hist_df.dtypes.astype(str))
    hist_df = hist_df.set_index('date')
    #st.line_chart(hist_df.loc[hist_df['Rótulo'] == 'FAST FUEL', ['date','Precio'] ]) 
    st.line_chart(hist_df.loc[hist_df['Rótulo'] == 'FAST FUEL', ['Precio'] ]) 
    
    return



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
                st.write('dtypes new df with date: ', df.dtypes.astype(str))
                df
                
                try: 
                    hist_df = pd.read_csv('gasolineras_ciudad_real.csv') 
                    st.write('dtypes hist_df as loaded: ', hist_df.dtypes.astype(str))
                    st.write('loaded shape', hist_df.shape)
                    hist_df = update_hist(df,hist_df)
                    #hist_df
                except:
                    st.text('file not found')
                    
                # hist_df2 = hist_df.astype(str)
                st.write('dtypes hist_df: ', hist_df.dtypes.astype(str))
                #st.write('hist_df.to_list: ', hist_df.to_list())
                hist_df
                
                plot_hist(hist_df)
                    
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


