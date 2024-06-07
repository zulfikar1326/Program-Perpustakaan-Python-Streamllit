import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


class Buku:
    def __init__(self, judul, penulis, tahun_terbit):
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.status = "tersedia"

    def info_buku(self):
        return f"Judul: {self.judul}, Penulis: {self.penulis}, Tahun Terbit: {self.tahun_terbit}, Status: {self.status}"

class BukuDigital(Buku):
    def __init__(self, judul, penulis, tahun_terbit, ukuran_file, format_file):
        super().__init__(judul, penulis, tahun_terbit)
        self.ukuran_file = ukuran_file
        self.format_file = format_file

    def info_buku(self):
        info = super().info_buku()
        return f"{info}, Ukuran File: {self.ukuran_file}MB, Format: {self.format_file}"

class BukuFisik(Buku):
    def __init__(self, judul, penulis, tahun_terbit, jumlah_halaman, berat):
        super().__init__(judul, penulis, tahun_terbit)
        self.jumlah_halaman = jumlah_halaman
        self.berat = berat

    def info_buku(self):
        info = super().info_buku()
        return f"{info}, Jumlah Halaman: {self.jumlah_halaman}, Berat: {self.berat} gram"

class Perpustakaan:
    def __init__(self):
        self.daftar_buku = []

    def tambah_buku(self, buku):
        self.daftar_buku.append(buku)

    def cari_buku(self, judul):
        for buku in self.daftar_buku:
            if buku.judul.lower() == judul.lower():
                return buku
        return None

    def tampilkan_semua_buku(self):
        data = []
        for buku in self.daftar_buku:
            if isinstance(buku, BukuDigital):
                data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, buku.ukuran_file, buku.format_file, '', ''])
            elif isinstance(buku, BukuFisik):
                data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, '', '', buku.jumlah_halaman, buku.berat])
            else:
                data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, '', '', '', ''])
        return pd.DataFrame(data, columns=['Judul', 'Penulis', 'Tahun Terbit', 'Status', 'Ukuran File (MB)', 'Format File', 'Jumlah Halaman', 'Berat (gram)'])

    def pinjam_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "tersedia":
            buku.status = "dipinjam"
            return True
        return False

    def kembalikan_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "dipinjam":
            buku.status = "tersedia"
            return True
        return False

    def hapus_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku:
            self.daftar_buku.remove(buku)
            return True
        return False

    def update_info_buku(self, judul, penulis=None, tahun_terbit=None):
        buku = self.cari_buku(judul)
        if buku:
            if penulis:
                buku.penulis = penulis
            if tahun_terbit:
                buku.tahun_terbit = tahun_terbit
            return True
        return False

    def tampilkan_buku_dipinjam(self):
        data = []
        for buku in self.daftar_buku:
            if buku.status == "dipinjam":
                if isinstance(buku, BukuDigital):
                    data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, buku.ukuran_file, buku.format_file, '', ''])
                elif isinstance(buku, BukuFisik):
                    data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, '', '', buku.jumlah_halaman, buku.berat])
                else:
                    data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, '', '', '', ''])
        return pd.DataFrame(data, columns=['Judul', 'Penulis', 'Tahun Terbit', 'Status', 'Ukuran File (MB)', 'Format File', 'Jumlah Halaman', 'Berat (gram)'])

    def tampilkan_buku_digital(self):
        data = []
        for buku in self.daftar_buku:
            if isinstance(buku, BukuDigital):
                data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, buku.ukuran_file, buku.format_file])
        return pd.DataFrame(data, columns=['Judul', 'Penulis', 'Tahun Terbit', 'Status', 'Ukuran File (MB)', 'Format File'])

    def tampilkan_buku_fisik(self):
        data = []
        for buku in self.daftar_buku:
            if isinstance(buku, BukuFisik):
                data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status, buku.jumlah_halaman, buku.berat])
        return pd.DataFrame(data, columns=['Judul', 'Penulis', 'Tahun Terbit', 'Status', 'Jumlah Halaman', 'Berat (gram)'])
