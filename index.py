import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


nav = st.container()
konten = st.container()

dataMinyakCsv = pd.read_csv('produksi_minyak_mentah.csv')
dataNegaraJson = pd.read_json('kode_negara_lengkap.json')


with nav:
    menu = st.selectbox('Pilih menu', (
        'Data Berdasarkan Nama',
        'Data Banyak Negara Terbesar Berdasarkan Tahun',
        'Data Kumulatif Berdasarkan Tahun',
        'Data Informasi Negara Berdasarkan Tahun'
    ))

with konten:
    if menu == 'Data Berdasarkan Nama':
        inputNegara = st.text_input('Input Nama Negara')

        if inputNegara!='':
            cariNegara = dataNegaraJson[dataNegaraJson.name==inputNegara]
            if not (cariNegara.empty):
                kodeNegara = cariNegara['alpha-3'].iloc[0]

                dataNegara = pd.DataFrame(dataMinyakCsv[dataMinyakCsv['kode_negara']==kodeNegara])
                dataNegara.index = dataNegara['tahun']

                st.markdown('Tampilan')
                
                grafik = st.checkbox('Grafik', value=True)
                ket = st.checkbox('Tabel')

                if grafik:
                    st.subheader(f"Grafik Produksi Minyak Mentah Negara {inputNegara}")

                    fig = px.bar(
                    dataNegara.produksi)
                    
                    st.plotly_chart(fig)
                

                if ket:
                    st.subheader(f"Tabel Keterangan negara {inputNegara}")
            
                    tabel = pd.DataFrame({
                        'Tahun': dataNegara.tahun,
                        'Jumlah Minyak': dataNegara.produksi
                    })
                    tabel.index = np.arange(1, len(tabel)+1)

                    st.table(tabel)
                
            else:
                st.warning('Pencarian Gagal!')
    
    elif menu == 'Data Banyak Negara Terbesar Berdasarkan Tahun':
        inputTahun = st.slider('Input Tahun', 1971, 2015)
        inputBanyak = st.slider('Input Jumlah Data', 0, 100)

        if inputTahun > 0 and inputBanyak > 0:
            produksiUrut = pd.DataFrame(dataMinyakCsv[dataMinyakCsv['tahun']==inputTahun].sort_values(['produksi'], ascending=False))
            produksiUrut = produksiUrut.head(inputBanyak)
            produksiUrut.index = np.arange(1, len(produksiUrut)+1)

            grafikTabel = pd.DataFrame()

            for x in range(len(produksiUrut)):
                kodeNegara = produksiUrut['kode_negara'].iloc[x]
                alphaJson = dataNegaraJson[dataNegaraJson['alpha-3']== kodeNegara]

                if not (alphaJson.empty):
                    kodeBaru = alphaJson['name'].iloc[0]
                else:
                    kodeBaru = kodeNegara
                
                tumpukRow = {
                            'nama negara':kodeBaru, 
                            'produksi': produksiUrut['produksi'].iloc[x]
                            }
                grafikTabel =grafikTabel.append(tumpukRow, ignore_index=True)
            
            st.subheader(f"{inputBanyak} Besar Negara Produksi Minyak Mentah Tahun {inputTahun}")
            col1, col2 = st.columns([3,1])
            grafikTabel.index = produksiUrut['kode_negara']
            produksiUrut.index = produksiUrut['kode_negara']

            fig = plt.figure(figsize = (16, 10))
            plt.title(f'{inputBanyak} Besar Negara Produksi Minyak Mentah', fontsize=22)
            plt.plot(produksiUrut['produksi'], marker = 'o')
            plt.grid()
            plt.xlabel('Negara', fontsize=20)
            plt.ylabel('Jumlah', fontsize=20)

            
            col1.pyplot(fig)

            col2.write(grafikTabel)

    elif menu == 'Data Kumulatif Berdasarkan Tahun':
        inputBanyak = st.slider('Input Jumlah Data', 0, 100)

        if inputBanyak > 0:
            dataKumulatif = dataMinyakCsv.groupby('kode_negara').sum().sort_values(['produksi'], ascending=False)
            dataKumulatif = dataKumulatif.head(inputBanyak)
            dataKumulatif = dataKumulatif.reset_index()

            grafikTabel = pd.DataFrame()

            for x in range(len(dataKumulatif)):
                kodeNegara = dataKumulatif['kode_negara'].iloc[x]
                alphaJson = dataNegaraJson[dataNegaraJson['alpha-3']== kodeNegara]

                if not (alphaJson.empty):
                    kodeBaru = alphaJson['name'].iloc[0]
                else:
                    kodeBaru = kodeNegara
                
                tumpukRow = {
                            'nama negara':kodeBaru, 
                            'produksi': dataKumulatif['produksi'].iloc[x]
                            }
                grafikTabel = grafikTabel.append(tumpukRow, ignore_index=True)
            
            st.subheader(f"{inputBanyak} Besar Negara Produksi Minyak Mentah Kumulatif")

            col1, col2 = st.columns([3,1])
            grafikTabel.index = dataKumulatif['kode_negara']
            dataKumulatif.index = dataKumulatif['kode_negara']
            fig = plt.figure(figsize = (16, 10))

            plt.title('Grafik Data Negara Kumulatif', fontsize=22)
            plt.plot(dataKumulatif['produksi'], marker = 'o')
            plt.grid()
            plt.xlabel('Negara', fontsize=20)
            plt.ylabel('Jumlah', fontsize=20)

            

            col1.pyplot(fig)

            col2.write(grafikTabel)

    elif menu == 'Data Informasi Negara Berdasarkan Tahun':
        inputTahun = st.slider('Input Tahun', 1971, 2015)
    
        radio = st.radio("Tampilan", ('Informasi Negara', 'Tabel Negara'))

        dataTahun = pd.DataFrame(dataMinyakCsv[dataMinyakCsv['tahun']==inputTahun])

        dataUrutDepan = dataTahun.sort_values(['produksi'], ascending=False)
        dataNol = dataUrutDepan[dataUrutDepan['produksi'] == 0]
        dataUrutDepan = dataUrutDepan[dataUrutDepan['produksi'] != 0]
        dataUrutBelakang = dataUrutDepan.sort_values(['produksi'], ascending=True)

        if radio == 'Informasi Negara':
            # Data Terbesar
            dataKode = dataUrutDepan['kode_negara'].iloc[0]
            dataNegara = dataNegaraJson[dataNegaraJson['alpha-3'] == dataKode]

            if not dataNegara.empty:
                namaNegara = dataNegara['name'].iloc[0]
                regionNegara = dataNegara['region'].iloc[0]
                subNegara = dataNegara['sub-region'].iloc[0]
                kodeNegara = dataNegara['country-code'].iloc[0]
            else:
                namaNegara = dataKode
                regionNegara = '-'
                subNegara = '-'
                kodeNegara = dataKode

            
            st.subheader(f'Data Negara dengan Jumlah Produksi Terbesar pada Tahun {inputTahun}')

            totalProduksi = dataUrutDepan['produksi'].iloc[0]
            dataNegara = pd.DataFrame(dataMinyakCsv[dataMinyakCsv['kode_negara']==dataKode])
            dataNegara.index = dataNegara['tahun']

            col1, col2 = st.columns([2,4])

            col1.markdown('Nama Negara')
            col2.markdown(f': {namaNegara}')

            col1.markdown('Kode Negara')
            col2.markdown(f': {kodeNegara}')

            col1.markdown('Region')
            col2.markdown(f': {regionNegara}')

            col1.markdown('Sub Region')
            col2.markdown(f': {subNegara}')

            col1.markdown('Total Produksi')
            col2.markdown(f': {totalProduksi}')

            st.markdown(f"**Grafik Produksi Minyak Mentah Negara** **{namaNegara}** ")
            fig = px.bar(
            dataNegara.produksi)
                        
            st.plotly_chart(fig)
           

        
            # Data Terkecil
            dataKode = dataUrutBelakang['kode_negara'].iloc[0]
            dataNegara = dataNegaraJson[dataNegaraJson['alpha-3'] == dataKode]

            if not dataNegara.empty:
                namaNegara = dataNegara['name'].iloc[0]
                regionNegara = dataNegara['region'].iloc[0]
                subNegara = dataNegara['sub-region'].iloc[0]
                kodeNegara = dataNegara['country-code'].iloc[0]
            else:
                namaNegara = dataKode
                regionNegara = '-'
                subNegara = '-'
                kodeNegara = dataKode

            st.subheader(f'Data Negara dengan Jumlah Produksi Terkecil pada Tahun {inputTahun}')
            
            totalProduksi = dataUrutBelakang['produksi'].iloc[0]
            dataNegara = pd.DataFrame(dataMinyakCsv[dataMinyakCsv['kode_negara']==dataKode])
            dataNegara.index = dataNegara['tahun']

            col1, col2 = st.columns([2,4])

            col1.markdown('Nama Negara')
            col2.markdown(f': {namaNegara}')

            col1.markdown('Kode Negara')
            col2.markdown(f': {kodeNegara}')

            col1.markdown('Region')
            col2.markdown(f': {regionNegara}')

            col1.markdown('Sub Region')
            col2.markdown(f': {subNegara}')

            col1.markdown('Total Produksi')
            col2.markdown(f': {totalProduksi}')

            st.markdown(f"**Grafik Produksi Minyak Mentah Negara** **{namaNegara}** ")
            fig = px.bar(
            dataNegara.produksi)
                        
            st.plotly_chart(fig)



            #Data Nol
            dataKode = dataNol['kode_negara'].iloc[0]
            dataNegara = dataNegaraJson[dataNegaraJson['alpha-3'] == dataKode]

            if not dataNegara.empty:
                namaNegara = dataNegara['name'].iloc[0]
                regionNegara = dataNegara['region'].iloc[0]
                subNegara = dataNegara['sub-region'].iloc[0]
                kodeNegara = dataNegara['country-code'].iloc[0]
            else:
                namaNegara = dataKode
                regionNegara = '-'
                subNegara = '-'
                kodeNegara = dataKode

            st.subheader(f'Data Negara dengan Jumlah Produksi Nol pada Tahun {inputTahun}')

            totalProduksi = dataNol['produksi'].iloc[0]
            dataNegara = pd.DataFrame(dataMinyakCsv[dataMinyakCsv['kode_negara']==dataKode])
            dataNegara.index = dataNegara['tahun']

            col1, col2 = st.columns([2,4])

            col1.markdown('Nama Negara')
            col2.markdown(f': {namaNegara}')

            col1.markdown('Kode Negara')
            col2.markdown(f': {kodeNegara}')

            col1.markdown('Region')
            col2.markdown(f': {regionNegara}')

            col1.markdown('Sub Region')
            col2.markdown(f': {subNegara}')

            col1.markdown('Total Produksi')
            col2.markdown(f': {totalProduksi}')

            st.markdown(f"**Grafik Produksi Minyak Mentah Negara** **{namaNegara}** ")
            fig = px.bar(
            dataNegara.produksi)
                        
            st.plotly_chart(fig)
            


        if radio == 'Tabel Negara':
            cetakTabelBesar = pd.DataFrame()

            for x in range (len(dataUrutDepan)):
                dataKode = dataUrutDepan['kode_negara'].iloc[x]
                dataNegara = dataNegaraJson[dataNegaraJson['alpha-3'] == dataKode]

                if not dataNegara.empty:
                    namaNegara = dataNegara['name'].iloc[0]
                    regionNegara = dataNegara['region'].iloc[0]
                    subNegara = dataNegara['sub-region'].iloc[0]
                    kodeNegara = dataNegara['country-code'].iloc[0]
                else:
                    namaNegara = dataKode
                    regionNegara = '-'
                    subNegara = '-'
                    kodeNegara = dataKode

                tumpukData = {
                    'nama':namaNegara, 
                    'kode': kodeNegara, 
                    'region':regionNegara,
                    'sub-region':subNegara,
                    'total':dataUrutDepan['produksi'].iloc[x]
                    }

                cetakTabelBesar = cetakTabelBesar.append(tumpukData, ignore_index=True)

            cetakTabelBesar.index = np.arange(1, len(cetakTabelBesar)+1)
                    
            st.subheader(f'Data Produksi Negara Terbesar tahun {inputTahun}')
            test = cetakTabelBesar.astype(str)
            st.write(test)

            # 
            cetakTabelKecil = pd.DataFrame()


            for x in range (len(dataUrutBelakang)):
                dataKode = dataUrutBelakang['kode_negara'].iloc[x]
                dataNegara = dataNegaraJson[dataNegaraJson['alpha-3'] == dataKode]

                if not dataNegara.empty:
                    namaNegara = dataNegara['name'].iloc[0]
                    regionNegara = dataNegara['region'].iloc[0]
                    subNegara = dataNegara['sub-region'].iloc[0]
                    kodeNegara = dataNegara['country-code'].iloc[0]
                else:
                    namaNegara = dataKode
                    regionNegara = '-'
                    subNegara = '-'
                    kodeNegara = dataKode

                tumpukData = {
                    'nama':namaNegara, 
                    'kode': kodeNegara, 
                    'region':regionNegara,
                    'sub-region':subNegara,
                    'total':dataUrutBelakang['produksi'].iloc[x]
                    }

                cetakTabelKecil = cetakTabelKecil.append(tumpukData, ignore_index=True)

            cetakTabelKecil.index = np.arange(1, len(cetakTabelKecil)+1)
                    
            st.subheader(f'Data Produksi Negara Terkecil tahun {inputTahun}')
            test = cetakTabelKecil.astype(str)
            st.write(test)

            #
            catakTabelNol = pd.DataFrame()


            for x in range (len(dataNol)):
                dataKode = dataNol['kode_negara'].iloc[x]
                dataNegara = dataNegaraJson[dataNegaraJson['alpha-3'] == dataKode]

                if not dataNegara.empty:
                    namaNegara = dataNegara['name'].iloc[0]
                    regionNegara = dataNegara['region'].iloc[0]
                    subNegara = dataNegara['sub-region'].iloc[0]
                    kodeNegara = dataNegara['country-code'].iloc[0]
                else:
                    namaNegara = dataKode
                    regionNegara = '-'
                    subNegara = '-'
                    kodeNegara = dataKode

                tumpukData = {
                    'nama':namaNegara, 
                    'kode': kodeNegara, 
                    'region':regionNegara,
                    'sub-region':subNegara,
                    'total':dataNol['produksi'].iloc[x]
                    }

                catakTabelNol = catakTabelNol.append(tumpukData, ignore_index=True)

            catakTabelNol.index = np.arange(1, len(catakTabelNol)+1)
                    
            st.subheader(f'Data Produksi Negara Nol tahun {inputTahun}')
            test = catakTabelNol.astype(str)
            st.write(test)
