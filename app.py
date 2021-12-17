import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image




st.set_page_config(page_title='Data Produksi Minyak Mentah')
st.header('Data Produksi Minyak Mentah')

### --- LOAD DATAFRAME
json_file = 'kode_negara_lengkap.json'
csv_file = 'produksi_minyak_mentah.csv'

df_negara = pd.read_json(json_file)

df = pd.read_csv(csv_file)


df['nama_negara'] = df.kode_negara.map(df_negara.set_index('alpha-3')['name'].to_dict())

ng = df['nama_negara']
df.drop(labels=['nama_negara'], axis=1,inplace = True)
df.insert(0, 'nama_negara', ng)

df_participants = pd.read_csv(csv_file)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
kd_negara = df['kode_negara'].unique().tolist()
nm_negara = df['nama_negara'].unique().tolist()
years = df['tahun'].unique().tolist()

year_selection = st.select_slider('Tahun:',options=years)

nm_negara_selection = st.multiselect('Nama Negara:',
                                    nm_negara,
                                    default='Indonesia')

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['tahun'] == year_selection) & (df['nama_negara'].isin(nm_negara_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask]
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
st.subheader('Bar Chart Data Produksi Negara')
if(len(df_grouped) != 0):
        bar_chart = px.bar(df_grouped,
                title='Bar Chart Data Produksi Negara Tahun {y}'.format(y = year_selection),
                x='nama_negara',
                y='produksi',
                text='nama_negara',
                color='nama_negara',
                # color_discrete_sequence = ['#0294e8']*len(df_grouped),
                template= 'plotly_white')
        st.plotly_chart(bar_chart)


# --- PLOT PIE CHART
st.subheader('Pie Chart Data Produksi Negara')
pie_chart = px.pie(df_grouped,
                title='Pie Chart Data Produksi Negara Tahun {y}'.format(y = year_selection),
                values='produksi',
                names='nama_negara')
st.plotly_chart(pie_chart)


#besar negara
# vm = df['produksi'].unique().tolist()
# vmax = max(vm)
# big_selection = st.slider('Besar:',
#                         min_value= 0, 
#                         max_value= 50000)
big_selection = st.selectbox('Besar Negara:',(1,2,3,4,5,6,7,8,9,10))
# --- FILTER DATAFRAME BASED ON SELECTION

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped2 = df[(df['tahun'] == year_selection)]
df_grouped2 = df_grouped2.reset_index()

st.subheader('Bar Chart Data Produksi {big} Terbesar'.format(big = big_selection))
bar_chart2 = px.bar(df_grouped2.loc[df_grouped2['nama_negara'].notna()].sort_values('produksi',ascending=False).head(big_selection),
        title='Bar Chart Data Produksi {big} Terbesar Tahun {y}'.format(big = big_selection,y = year_selection),
        x='nama_negara',
        y='produksi',
        text='nama_negara',
        color='nama_negara'
        # color_discrete_sequence = ['#03fc6b']*len(df_grouped2))
        )
st.plotly_chart(bar_chart2)

df = pd.merge(df_negara[['region','sub-region','alpha-3']], df, left_on='alpha-3', right_on='kode_negara', how='right')


#line chart
st.subheader('Line Chart Data Kumulatif Produksi {big} Terbesar'.format(big = big_selection))
lc = df.loc[df['nama_negara'].notna()]
lc.sort_values('produksi',ascending=False).groupby(['kode_negara']).head(10)
a = df.groupby(['nama_negara','kode_negara']).sum()

a = a.sort_values('produksi', ascending=False).head(big_selection)
a = a.reset_index()

fig2 = px.line(df.loc[df['nama_negara'].isin(a['nama_negara'])].sort_values('tahun',ascending=False), 
                title='Line Chart Data Produksi Dari Tahun {start_y} Sampai {end_y}'.format(start_y = min(years), end_y = max(years)),
                x='tahun',
                y="produksi",
                color='nama_negara',
                markers=True)
st.plotly_chart(fig2,use_container_width=True)


#hapus alpha-3 karena sudah ada kode negara
df.drop(labels=['alpha-3'], axis=1,inplace = True)

#atur posisi column agar nama negara dan kode negara berada di depan
ng = df['kode_negara']
df.drop(labels=['kode_negara'], axis=1,inplace = True)
df.insert(0, 'kode_negara', ng)
ng = df['nama_negara']
df.drop(labels=['nama_negara'], axis=1,inplace = True)
df.insert(0, 'nama_negara', ng)

#hapus index pada dataframe
hide_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_row_index, unsafe_allow_html=True)


#Nilai produksi terbesar
st.subheader('Data Max Produksi Minyak Mentah')
st.write("Tahun "+str(year_selection))
df_temp = df.loc[(df['tahun'] == year_selection) & (df['nama_negara'].notna())]
st.table(df_temp.loc[df_temp['produksi'] == df_temp['produksi'].max()] )

#Nilai produksi terkecil
st.subheader('Data Min Produksi Minyak Mentah')
st.write("Tahun "+str(year_selection))
df_temp2 = df_temp.loc[df_temp['produksi'] != 0]
st.table(df_temp2.loc[df_temp2['produksi'] == df_temp2['produksi'].min()])

#Nilai produksi sama dengan 0
st.subheader('Data Produksi Minyak Mentah Dengan Jumlah 0')
st.write("Tahun "+str(year_selection))
df_temp2 = df_temp.loc[df_temp['produksi'] == 0]
st.dataframe(df_temp2)
