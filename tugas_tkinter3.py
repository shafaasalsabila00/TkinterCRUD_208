import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk

def koneksi():
    return sqlite3.connect("nilai_siswa.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()

def insert_siswa(nama, biologi, fisika, inggris, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    con.commit()
    con.close()

# 2. Menambahkan update dan delete data ke SQLite
# 3. Buat Fungsi untuk update dan delete
def update_siswa(id, nama, biologi, fisika, inggris, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    """, (nama, biologi, fisika, inggris, prediksi, id))
    con.commit()
    con.close()

def delete_siswa(id):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM nilai_siswa WHERE id = ?", (id,))
    con.commit()
    con.close()

def read_siswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT * FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

# 1. Menambahkan kondisi nilai yang berbeda untuk setiap pilihan prodi yang diinginkan
# 5. Jika nilai Biologi paling tinggi, maka hasil prediksi = Kedokteran
# 6. Jika nilai Fisika paling tinggi, maka hasil prediksi = Teknik
# 7. Jika nilai Inggris paling tinggi, maka hasil prediksi = Bahasa
def prediksi_fakultas(bio, fis, eng):
    # Kondisi nilai yang berbeda: Tambahkan threshold minimum untuk setiap prodi
    # Jika nilai Biologi paling tinggi dan >= 70, maka Kedokteran
    if bio >= 70 and bio > fis and bio > eng:
        return "Kedokteran"
    # Jika nilai Fisika paling tinggi dan >= 70, maka Teknik
    elif fis >= 70 and fis > bio and fis > eng:
        return "Teknik"
    # Jika nilai Inggris paling tinggi dan >= 70, maka Bahasa
    elif eng >= 70 and eng > bio and eng > fis:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

create_table()

class AppNilai(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Siswa")
        self.geometry("900x500")
        self.configure(bg="#f0f2f5")
        self.selected_id = None  # Untuk menyimpan ID yang dipilih untuk update

        main = tk.Frame(self, bg="#f0f2f5")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        frame_form = tk.LabelFrame(main, text="Input Nilai Siswa", padx=10, pady=10)
        frame_form.pack(side="left", fill="y", padx=10)

        tk.Label(frame_form, text="Nama Siswa:").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frame_form, width=25)
        self.ent_nama.grid(row=1, column=0, pady=5)

        tk.Label(frame_form, text="Nilai (0 - 100):").grid(row=2, column=0, sticky="w", pady=(10,0))

        frm_nilai = tk.Frame(frame_form)
        frm_nilai.grid(row=3, column=0, pady=5)

        tk.Label(frm_nilai, text="Biologi").grid(row=0, column=0)
        self.ent_bio = tk.Entry(frm_nilai, width=7)
        self.ent_bio.grid(row=1, column=0, padx=4)

        tk.Label(frm_nilai, text="Fisika").grid(row=0, column=1)
        self.ent_fis = tk.Entry(frm_nilai, width=7)
        self.ent_fis.grid(row=1, column=1, padx=4)

        tk.Label(frm_nilai, text="Inggris").grid(row=0, column=2)
        self.ent_ing = tk.Entry(frm_nilai, width=7)
        self.ent_ing.grid(row=1, column=2, padx=4)

        btns = tk.Frame(frame_form)
        btns.grid(row=4, column=0, pady=15)

        # 8. Terdapat button tkinter untuk submit nilai
        tk.Button(btns, text="Submit", width=10, command=self.insert_data).pack(side="left", padx=5)
        tk.Button(btns, text="Clear", width=10, command=self.clear_inputs).pack(side="left", padx=5)

        frame_table = tk.LabelFrame(main, text="Data Tersimpan")
        frame_table.pack(side="right", fill="both", expand=True)

        cols = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings")

        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # 4. Buat 2 Tombol button baru
        btn_frame = tk.Frame(frame_table)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Update", command=self.load_for_update).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_data).pack(side="left", padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_data()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_id = item['values'][0]

    def load_for_update(self):
        if self.selected_id is None:
            msg.showerror("Error", "Pilih data dari tabel terlebih dahulu!")
            return
        # Ambil data dari database berdasarkan ID
        con = koneksi()
        cur = con.cursor()
        cur.execute("SELECT * FROM nilai_siswa WHERE id = ?", (self.selected_id,))
        row = cur.fetchone()
        con.close()
        if row:
            self.ent_nama.delete(0, tk.END)
            self.ent_nama.insert(0, row[1])
            self.ent_bio.delete(0, tk.END)
            self.ent_bio.insert(0, row[2])
            self.ent_fis.delete(0, tk.END)
            self.ent_fis.insert(0, row[3])
            self.ent_ing.delete(0, tk.END)
            self.ent_ing.insert(0, row[4])

    def delete_data(self):
        if self.selected_id is None:
            msg.showerror("Error", "Pilih data dari tabel terlebih dahulu!")
            return
        if msg.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?"):
            delete_siswa(self.selected_id)
            msg.showinfo("Sukses", "Data berhasil dihapus.")
            self.load_data()
            self.clear_inputs()
            self.selected_id = None

    def clear_inputs(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_bio.delete(0, tk.END)
        self.ent_fis.delete(0, tk.END)
        self.ent_ing.delete(0, tk.END)
        self.selected_id = None

    def validate(self):
        try:
            nama = self.ent_nama.get().strip()
            b = int(self.ent_bio.get().strip())
            f = int(self.ent_fis.get().strip())
            i = int(self.ent_ing.get().strip())

            if not nama or not (0 <= b <= 100) or not (0 <= f <= 100) or not (0 <= i <= 100):
                raise ValueError()

            return nama, b, f, i

        except:
            msg.showerror("Error", "Isi data dengan benar! Nilai harus 0-100.")
            return None

    def insert_data(self):
        data = self.validate()
        if not data:
            return
        
        nama, bio, fis, ing = data
        pred = prediksi_fakultas(bio, fis, ing)

        if self.selected_id:
            # Update data
            update_siswa(self.selected_id, nama, bio, fis, ing, pred)
            msg.showinfo("Sukses", "Data berhasil diupdate.")
        else:
            # Insert data baru
            insert_siswa(nama, bio, fis, ing, pred)
            msg.showinfo("Sukses", "Data berhasil disimpan.")
        
        self.load_data()
        self.clear_inputs()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = read_siswa()
        for r in rows:
            self.tree.insert("", tk.END, values=r)

if __name__ == "__main__":
    AppNilai().mainloop()