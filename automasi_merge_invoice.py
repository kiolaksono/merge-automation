# -*- coding: utf-8 -*-
"""
Skrip Otomatisasi Merge PDF Invoice
Output nama file mengikuti nama file invoice asli + "_merged"
"""

import os
import sys

try:
    from pypdf import PdfMerger
except ImportError:
    print("Error: Library 'pypdf' belum terinstal.")
    input("\nTekan Enter untuk keluar...")
    sys.exit(1)

def tentukan_urutan_file(filename):
    fn = filename.lower()
    if 'inv' in fn:
        return (0, fn)
    elif fn.startswith('outputtaxinvoice'):
        return (1, fn)
    elif fn.startswith('approval'):
        return (2, fn)
    else:
        return (3, fn)  # BAST acak/random ke sini

def merge_invoice_folders(main_directory):
    output_directory = os.path.join(main_directory, "HASIL_MERGE_TOTAL")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    print("=" * 60)
    print(" MEMULAI PROSES PENGGABUNGAN INVOICE OTOMATIS ")
    print("=" * 60)
    
    folders = [f for f in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, f))]
    success_count = 0
    
    for folder_name in folders:
        if folder_name == "HASIL_MERGE_TOTAL":
            continue
            
        folder_path = os.path.join(main_directory, folder_name)
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            continue
            
        print(f"\n[ Memproses Folder: {folder_name} ]")
        
        # Cari file invoice di dalam folder ini untuk dijadikan nama output
        nama_invoice_asli = None
        for file_pdf in pdf_files:
            if 'inv' in file_pdf.lower():
                nama_invoice_asli = os.path.splitext(file_pdf)[0] # Mengambil nama tanpa .pdf
                break
        
        # Tentukan nama file hasil akhir
        if nama_invoice_asli:
            output_filename = f"{nama_invoice_asli}_merged.pdf"
        else:
            # Jika file invoice tidak ditemukan, gunakan nama folder sebagai cadangan
            output_filename = f"{folder_name}_merged.pdf"
            print("  (!) Peringatan: File invoice tidak ditemukan di folder ini.")
            
        # Urutkan file berdasarkan aturan
        pdf_files.sort(key=tentukan_urutan_file)
        
        merger = PdfMerger()
        try:
            for idx, pdf in enumerate(pdf_files, 1):
                print(f"   {idx}. {pdf}")
                full_pdf_path = os.path.join(folder_path, pdf)
                merger.append(full_pdf_path)
            
            output_file_path = os.path.join(output_directory, output_filename)
            
            with open(output_file_path, "wb") as fout:
                merger.write(fout)
            merger.close()
            
            print(f"-> V SUKSES: Disimpan sebagai '{output_filename}'")
            success_count += 1
            
        except Exception as e:
            print(f"-> X GAGAL: Gagal memproses folder ini. Error: {e}")
            if 'merger' in locals():
                merger.close()

    print("\n" + "=" * 60)
    print(f" PROSES SELESAI! Berhasil menggabungkan {success_count} folder tagihan.")
    print(" Silakan cek folder 'HASIL_MERGE_TOTAL'.")
    print("=" * 60)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
    merge_invoice_folders(current_dir)
    input("\nTekan Enter untuk menutup jendela ini...")