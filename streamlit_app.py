import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
#from gsheetsdb import connect #<-works
#from shillelagh.backends.apsw.db import connect as ctsh
from shillelagh.backends.apsw.db import connect  #<-works also for reading
from google.oauth2 import service_account
from google.cloud import storage


#USEFUL LINKS
#https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs
#https://github.com/betodealmeida/shillelagh/
#https://github.com/betodealmeida/shillelagh/blob/main/examples/gsheets.py
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


#st.set_page_config(page_title="MyGasApp", page_icon="🤖")
st.set_page_config(page_title="MyGasApp", page_icon=":fuelpump:")
st.title("Get gas prices in Valdepeñas")


# Create a connection object. gsheet
####conn = connect()                                   #<-works
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)                                 #<-works
@st.cache(suppress_st_warning=True)                #<-works


#---------- GOOGLE CLOUD
# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)


#------------


def fetchdf(session, url):
    try:
        result = session.get(url)
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


def run_query(query): #  based on gsheets
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


def googlesheetsdf(sheet_url):  #based on gsheets
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    # Print results.
    for row in rows:
        st.write(row.Rótulo)
    
    return



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

    session = requests.Session()
   
    with st.form("my_form"):
        #index = st.number_input("ID", min_value=0, max_value=100, key="index")
        submitted = st.form_submit_button("Submit")

        if submitted:
            url = 'https://geoportalgasolineras.es/geoportalmovil/eess/search.do?tipoCarburante=4&rotulo=&venta=P&provincia=13&localidad=7339&tipoDestinatarioPlan=&operador=&nombrePlan=&calle=&numero=&codPostal='
            st.text(url)
            st.write("Result")
            res = fetchdf(session, url )
            st.text(res.status_code)
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
                
        sheet_url = st.secrets["public_gsheets_url"]   #gsheets
        ###googlesheetsdf(sheet_url)                      #gsheets
        
        

        #------------GOOGLE OATUH code
        #---GOOGLE CLOUD -----------
        
        def read_file( bucket_name, file_path):
            bucket = client.bucket(bucket_name)
            content = bucket.blob(file_path).download_as_string().decode("utf-8")
            return content

        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
        client = storage.Client(credentials=credentials)
        st.write('my client on GCP is:')
        st.write(client)
        
          
        bucket_name = "streamlit-bucket-gasolinera"
        file_path = "GasolinerasVDP.csv"
        content = read_file(bucket_name, file_path)
        
        # Print results.
        st.write(content)
        for line in content.strip().split("\n"):
            st.write(line)
        #------------------------
        
       
        
        
        #----------- new code SQL  #shillelagh
        connection = connect(":memory:")
        cursor = connection.cursor()
 
        #READ TABLE - works
        #SQL2= str(f'SELECT * FROM "{sheet_url}"')
        #st.write(SQL2)
        #for row in cursor.execute(SQL2):
        #    st.write(row)
        
        
        SQL3 = 'INSERT INTO "{}" VALUES ("{}", "{}", "{}", "{}")'.format(sheet_url, 'FAST', 'CIAO', '99', '20220625') 
        st.write(SQL3)
        
        #cursor.execute(SQL3)
            
        #-----------------  #shillelagh
    
    
        savefile = st.form_submit_button('save csv')
        if savefile:
            hist_df.to_csv('gasolineras_ciudad_real.csv', index=False)  
             

if __name__ == '__main__':
    main()
 
####---------OLD CODE--------
#        SQL = """
#        SELECT *
#        FROM "url here"  
#        """
#        st.write('this is the query')
#        st.write(SQL)

