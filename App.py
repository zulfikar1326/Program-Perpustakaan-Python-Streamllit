import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

from oop import Buku,BukuDigital,BukuFisik,Perpustakaan

# Membuat instance dari kelas Perpustakaan
perpustakaan = Perpustakaan()

# Fungsi untuk menyimpan data ke Excel
def simpan_data_ke_excel():
    df = perpustakaan.tampilkan_semua_buku()
    df.to_excel('data_perpustakaan.xlsx', index=False)

# Fungsi untuk memuat data dari Excel
def muat_data_dari_excel():
    try:
        df = pd.read_excel('data_perpustakaan.xlsx')
        for _, row in df.iterrows():
            if pd.notna(row['Ukuran File (MB)']):
                buku = BukuDigital(row['Judul'], row['Penulis'], row['Tahun Terbit'], row['Ukuran File (MB)'], row['Format File'])
            elif pd.notna(row['Jumlah Halaman']):
                buku = BukuFisik(row['Judul'], row['Penulis'], row['Tahun Terbit'], row['Jumlah Halaman'], row['Berat (gram)'])
            else:
                buku = Buku(row['Judul'], row['Penulis'], row['Tahun Terbit'])
            buku.status = row['Status']
            perpustakaan.tambah_buku(buku)
    except FileNotFoundError:
        pass

# Memuat data dari Excel saat aplikasi dimulai
muat_data_dari_excel()

# Layout Streamlit
st.title("Perpustakaan Merdeka")


menu = option_menu(None, ["Tambah Buku", "Cari Buku", "Tampilkan Semua Buku", "Pinjam Buku", "Kembalikan Buku", "Hapus Buku", "Update Info Buku", "Unduh Data"], icons=['book', 'search', 'list', 'bookmark', 'return', 'trash', 'edit', 'download'], default_index=0, orientation="horizontal")

if menu == "Tambah Buku":
    jenis_buku = st.selectbox("Pilih Jenis Buku", ["Buku", "Buku Digital", "Buku Fisik"])
    judul = st.text_input("Judul")
    penulis = st.text_input("Penulis")
    tahun_terbit = st.number_input("Tahun Terbit", min_value=0, max_value=9999, step=1)
    if jenis_buku == "Buku Digital":
        ukuran_file = st.number_input("Ukuran File (MB)", min_value=0.0, step=0.1)
        format_file = st.selectbox("Format File", ["PDF", "EPUB", "MOBI"])
        if st.button("Tambah Buku Digital"):
            buku = BukuDigital(judul, penulis, tahun_terbit, ukuran_file, format_file)
            perpustakaan.tambah_buku(buku)
            st.success(f"Buku Digital '{judul}' berhasil ditambahkan.")
            simpan_data_ke_excel()
    elif jenis_buku == "Buku Fisik":
        jumlah_halaman = st.number_input("Jumlah Halaman", min_value=1, step=1)
        berat = st.number_input("Berat (gram)", min_value=0.0, step=0.1)
        if st.button("Tambah Buku Fisik"):
            buku = BukuFisik(judul, penulis, tahun_terbit, jumlah_halaman, berat)
            perpustakaan.tambah_buku(buku)
            st.success(f"Buku Fisik '{judul}' berhasil ditambahkan.")
            simpan_data_ke_excel()
    else:
        if st.button("Tambah Buku"):
            buku = Buku(judul, penulis, tahun_terbit)
            perpustakaan.tambah_buku(buku)
            st.success(f"Buku '{judul}' berhasil ditambahkan.")
            simpan_data_ke_excel()

elif menu == "Cari Buku":
    judul = st.text_input("Judul Buku yang Ingin Dicari")
    if st.button("Cari"):
        buku = perpustakaan.cari_buku(judul)
        if buku:
            st.write(buku.info_buku())
        else:
            st.error(f"Buku '{judul}' tidak ditemukan.")

elif menu == "Tampilkan Semua Buku":
    df = perpustakaan.tampilkan_semua_buku()
    st.dataframe(df)

elif menu == "Pinjam Buku":
    judul = st.text_input("Judul Buku yang Ingin Dipinjam")
    if st.button("Pinjam"):
        if perpustakaan.pinjam_buku(judul):
            st.success(f"Buku '{judul}' berhasil dipinjam.")
            simpan_data_ke_excel()
        else:
            st.error(f"Buku '{judul}' tidak tersedia untuk dipinjam.")
    if st.button("Tampilkan Buku yang Dipinjam"):
        df_dipinjam = perpustakaan.tampilkan_buku_dipinjam()
        st.dataframe(df_dipinjam)
    if st.button("Tampilkan Buku Digital"):
        df_digital = perpustakaan.tampilkan_buku_digital()
        st.dataframe(df_digital)
    if st.button("Tampilkan Buku Fisik"):
        df_fisik = perpustakaan.tampilkan_buku_fisik()
        st.dataframe(df_fisik)

elif menu == "Kembalikan Buku":
    judul = st.text_input("Judul Buku yang Ingin Dikembalikan")
    if st.button("Kembalikan"):
        if perpustakaan.kembalikan_buku(judul):
            st.success(f"Buku '{judul}' berhasil dikembalikan.")
            simpan_data_ke_excel()
        else:
            st.error(f"Buku '{judul}' tidak sedang dipinjam.")
    if st.button("Tampilkan Buku Digital"):
        df_digital = perpustakaan.tampilkan_buku_digital()
        st.dataframe(df_digital)
    if st.button("Tampilkan Buku Fisik"):
        df_fisik = perpustakaan.tampilkan_buku_fisik()
        st.dataframe(df_fisik)

elif menu == "Hapus Buku":
    judul = st.text_input("Judul Buku yang Ingin Dihapus")
    if st.button("Hapus"):
        if perpustakaan.hapus_buku(judul):
            st.success(f"Buku '{judul}' berhasil dihapus.")
            simpan_data_ke_excel()
        else:
            st.error(f"Buku '{judul}' tidak ditemukan.")
    if st.button("Tampilkan Buku Digital"):
        df_digital = perpustakaan.tampilkan_buku_digital()
        st.dataframe(df_digital)
    if st.button("Tampilkan Buku Fisik"):
        df_fisik = perpustakaan.tampilkan_buku_fisik()
        st.dataframe(df_fisik)

elif menu == "Update Info Buku":
    judul = st.text_input("Judul Buku yang Ingin Diupdate")
    penulis = st.text_input("Penulis Baru (Kosongkan jika tidak ingin diubah)")
    tahun_terbit = st.number_input("Tahun Terbit Baru (0 jika tidak ingin diubah)", min_value=0, max_value=9999, step=1)
    if st.button("Update"):
        if perpustakaan.update_info_buku(judul, penulis if penulis else None, tahun_terbit if tahun_terbit != 0 else None):
            st.success(f"Informasi buku '{judul}' berhasil diupdate.")
            simpan_data_ke_excel()
        else:
            st.error(f"Buku '{judul}' tidak ditemukan.")
    if st.button("Tampilkan Buku Digital"):
        df_digital = perpustakaan.tampilkan_buku_digital()
        st.dataframe(df_digital)
    if st.button("Tampilkan Buku Fisik"):
        df_fisik = perpustakaan.tampilkan_buku_fisik()
        st.dataframe(df_fisik)

elif menu == "Unduh Data":
    if st.button("Unduh Data Excel"):
        simpan_data_ke_excel()
        with open("data_perpustakaan.xlsx", "rb") as file:
            st.download_button(label="Unduh", data=file, file_name="data_perpustakaan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
