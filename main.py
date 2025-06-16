import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Inisialisasi database
conn = sqlite3.connect('peminjaman.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS peminjaman (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    judul_buku TEXT,
    tanggal_pinjam TEXT,
    tanggal_kembali TEXT
)
""")
conn.commit()

# Fungsi simpan data
def simpan_data():
    nama = entry_nama.get()
    judul = entry_judul.get()
    tgl_pinjam = entry_pinjam.get()
    tgl_kembali = entry_kembali.get()
    if nama and judul and tgl_pinjam and tgl_kembali:
        cursor.execute("INSERT INTO peminjaman (nama, judul_buku, tanggal_pinjam, tanggal_kembali) VALUES (?, ?, ?, ?)",
                       (nama, judul, tgl_pinjam, tgl_kembali))
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        entry_nama.delete(0, tk.END)
        entry_judul.delete(0, tk.END)
        entry_pinjam.delete(0, tk.END)
        entry_kembali.delete(0, tk.END)
    else:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")

# Fungsi lihat data
def lihat_data():
    window_data = tk.Toplevel()
    window_data.title("Data Peminjaman")

    tree = ttk.Treeview(window_data, columns=("ID", "Nama", "Judul", "Pinjam", "Kembali"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nama", text="Nama")
    tree.heading("Judul", text="Judul Buku")
    tree.heading("Pinjam", text="Tanggal Pinjam")
    tree.heading("Kembali", text="Tanggal Kembali")

    cursor.execute("SELECT * FROM peminjaman")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    tree.pack(padx=10, pady=10)

# Fungsi hapus data
def hapus_data():
    id_data = entry_id_hapus.get()
    if id_data:
        cursor.execute("DELETE FROM peminjaman WHERE id=?", (id_data,))
        conn.commit()
        messagebox.showinfo("Sukses", f"Data dengan ID {id_data} berhasil dihapus")
        entry_id_hapus.delete(0, tk.END)
    else:
        messagebox.showwarning("Peringatan", "Masukkan ID yang ingin dihapus")

# GUI setup
root = tk.Tk()
root.title("Aplikasi Peminjaman Buku")

tk.Label(root, text="Nama").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(root)
entry_nama.grid(row=0, column=1)

tk.Label(root, text="Judul Buku").grid(row=1, column=0, sticky="w")
entry_judul = tk.Entry(root)
entry_judul.grid(row=1, column=1)

tk.Label(root, text="Tanggal Pinjam").grid(row=2, column=0, sticky="w")
entry_pinjam = tk.Entry(root)
entry_pinjam.grid(row=2, column=1)

tk.Label(root, text="Tanggal Kembali").grid(row=3, column=0, sticky="w")
entry_kembali = tk.Entry(root)
entry_kembali.grid(row=3, column=1)

tk.Button(root, text="Simpan", command=simpan_data).grid(row=4, column=0, pady=10)
tk.Button(root, text="Lihat Data", command=lihat_data).grid(row=4, column=1)
tk.Label(root, text="ID untuk Hapus:").grid(row=5, column=0, sticky="w")
entry_id_hapus = tk.Entry(root)
entry_id_hapus.grid(row=5, column=1)
tk.Button(root, text="Hapus", command=hapus_data).grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
