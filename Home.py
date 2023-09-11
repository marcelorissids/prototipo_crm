import base64
import numpy as np
import pandas as pd
import datetime as dt
import streamlit as st
from io import BytesIO

st.title('Análise RFM')

st.sidebar.markdown('# Análise RFM')
st.sidebar.markdown('## A melhor para seu ecommerce')
st.sidebar.markdown("""---""")

st.write('# FM Company')

st.markdown(
    """
    A melhor maneira de segmentar seus clientes!
    ### Ask for Help
    - Time de Data Science no Discord
        - @MarceloRissi
""")

def analise_rfm(df):
    df.columns = ['PedidoNum', 'ProdutoCod', 'ProdutoDesc', 'Qtd', 'PedidoData', 'PrecoUnit', 'ClienteID', 'Pais']
    df.info()
    df = df[df['PedidoNum'].str[0] != 'C']
    df = df[df['ClienteID'].notnull()]
    df = df.drop_duplicates()
    df[df['PrecoUnit']==0].head()
    df['PrecoTotal'] = df['PrecoUnit']*df['Qtd']
    df['PedidoData'] = pd.to_datetime(df['PedidoData'])
    dia_do_hit = df['PedidoData'].max() + dt.timedelta(days=1)
    rfm = df.groupby(['ClienteID']).agg({'PedidoData': lambda x: (dia_do_hit - x.max()).days, 'PedidoNum':'count','PrecoTotal':'sum'})
    rfm = rfm.rename(columns={'PedidoData':'Recência','PedidoNum':'Frequência','PrecoTotal':'ValorMonetário'})
    # Criando os níveis de R, F e M - 5 níveis
    niveis_r = range(5, 0, -1)
    niveis_f = range(1, 6)
    niveis_m = range(1, 6)

    # Dividindo a lista de cliente em 5 quintis (dividindo nos quaartis)
    r_quintis = pd.qcut(rfm['Recência'], q= 5, labels = niveis_r)
    f_quintis = pd.qcut(rfm['Frequência'], q= 5, labels = niveis_f)
    m_quintis = pd.qcut(rfm['ValorMonetário'], q= 5, labels = niveis_m)
    rfm = rfm.assign ( R=r_quintis, F=f_quintis, M=m_quintis)

    # Criando tabela atribuindo níveis RFM e pontuação RFM (coma dos níveis)
    def add_rfm(x): return str(x['R']) + str(x['F']) + str(x['M'])
    rfm['RFM_cluster'] = rfm.apply(add_rfm, axis=1)
    rfm['RFM_score'] = rfm[['R', 'F', 'M']].sum(axis=1)
    rfm[['F', 'M']] = rfm[['F', 'M']].astype(float)
    rfm['FM_media'] = rfm[['F', 'M']].mean(axis=1).round()
    rfm = rfm.reset_index()

    pivot_rfm = rfm.pivot_table(values='ClienteID', index='FM_media', columns='R', aggfunc = 'count', fill_value=0)
    pivot_rfm = pivot_rfm.loc[[5.0, 4.0, 3.0, 2.0, 1.0],[1,2,3,4,5]]

    rfm['R'] = rfm['R'].astype('int64')
    rfm['FM_media'] = rfm['FM_media'].astype('int64')

    def classificar(df):
        if (df['FM_media'] == 5) and (df['R'] == 1):
            return 'Não posso perdê-lo'
        elif (df['FM_media'] == 5) and ((df['R'] == 3) or (df['R'] == 4)):
            return 'Cliente leal'
        elif (df['FM_media'] == 5) and (df['R'] == 5):
            return 'Campeão'
        elif (df['FM_media'] == 4) and (df['R'] >= 3):
            return 'Cliente leal'    
        elif (df['FM_media'] == 3) and (df['R'] == 3):
            return 'Precisa de atenção'    
        elif ((df['FM_media'] == 3) or (df['FM_media'] == 2))  and (df['R'] > 3):
            return 'Lealdade potencial' 
        elif ((df['FM_media'] == 2) or (df['FM_media'] == 1)) and (df['R'] == 1):
            return 'Perdido'     
        elif (df['FM_media'] == 2) and (df['R'] == 2):
            return 'Hibernando'     
        elif ((df['FM_media'] == 2) or (df['R'] == 1)) and (df['R'] == 3):
            return 'Prestes a hibernar'
        elif (df['FM_media'] == 1) and (df['R'] == 2):
            return 'Perdido'
        elif (df['FM_media'] == 1) and (df['R'] == 4):
            return 'Promissor'       
        elif (df['FM_media'] == 1) and (df['R'] == 5):
            return 'Recentes'  
        else:
            return 'Em risco'

    rfm['Classe'] = rfm.apply(classificar,axis=1)

    return rfm

# Upload csv
arquivo = st.file_uploader('Faça o upload do seu arquivo csv',type=['csv'])

if arquivo is not None:
    df = pd.read_csv(arquivo)
    st.write('Dados carregados:')
    st.write(df)

    # botão para realizar a analise
    if st.button('Realizar Análise'):
        with st.spinner('Realizando análise...'):
            df1 = analise_rfm(df)

        st.write('Resultado da análise:')
        st.write(df1)
        

        # botão para exportar
        csv = df1.to_csv(index=False, sep=';', encoding='utf-8')
        href = f'<a href="data:file/csv" download="df1.csv">Baixar Resultado CSV</a>'
        st.markdown(href, unsafe_allow_html=True)