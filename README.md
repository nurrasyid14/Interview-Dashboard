# **Text Mining : AI Interview Evaluation System**
Text Mining's Semester Project Assesment // Class of Text Mining Practicum - Applied Data Science - EEPIS
---
By:

- 33246000007 [Sovia Wahyuningtyas] - Conceptor & Evaluator
- 33246000018 [Muhamad Nur Rasyid]  - System Engineer
---

---
## **Overview**
*AI Interview Evaluation System* adalah Python-based web yang dirancang khusus untuk menentukan keputusan apakah kandidat pekerja layak untuk melanjutkan aplikasi ke tahap interview kedua -- yang artinya "*aim*" dari proyek ini adalah sebatas *mock-up* untuk menentukan kelayakan berdasarkan aspek aspek seperti: *Sentiment*, dan *Relevance* dengan pendekatan NLP melalui 3 blok utama, yakni:

**1. Authorization** 
**2. QnA & Judger**
**3. Evaluator & Reporter**

---
## **Ekspektasi Output**
Kendati *mock-up* ini berfokus pada metode **Text Mining**, namun harapan keluaran utama dari project ini adlaah berupa Dashboard Interaktif yang memuat informasi seperti halnya:
- Skor Sentimen (range -1 s/d 1)
- Skor Relevance (range 0 s/d 1)
- Skor persentase rating kelayakan (range 0 s/d 1)


- `Skor Sentimen = 0` → `Layak = 0.75`
- `Skor Sentimen = -1` → `Layak = 0.5`
P.S Asumsi rata rata skor Jawaban adalah 1 alias sempurna.


Persamaan ini ekuivalen dengan bentuk aljabar:

![formula](https://latex.codecogs.com/svg.image?\bg{transparent}\color{white}\text{Layak}=\frac{\operatorname{avg}(\text{Skor%20Jawaban})+\frac{\text{Skor%20Sentimen}+1}{2}}{2})

---
## **Blok Program**
### **1. Auth**
``` UI
x
```
---
Output dari blok ini berupa dokumen JSON yang berisi metadata user yang akan digunakan sebagai dasar penentu pertanyaan dalam wawancara.
``` json
#ord(initial)yyyymmddhhhmmssxxx.json
{
  "File_ID": "ord(initial.lower())-yyyymmdd-hhmmss-xxx",
  "Nama": "",
  "Tanggal_Lahir": "",
  "Kontak": "",
  "Alamat": "",
  "Keahlian": []
}
```
Misal: Nur Rasyid
``` json
{
  "File_ID": "110-114-20251123-020000-001",
  "Nama": "Nur Rasyid",
  "Tanggal_Lahir": "dd-mm-yyyy",
  "Kontak": "+62 354 000000",
  "Alamat": "EEPIS",
  "Keahlian": ["Data Engineering","Backend Engineering"]
}
```

Kesulitan pertanyaan akan ditentukan pada blok selanjutnya.

### **2. QnA & Judger**
``` UI
x
```
---
Cara kerja blok ini adalah dengan menampilkan 2+16 pertanyaan, yang dimana output akan berupa csv dengan nama {file_id}.csv dengan isi kolom yang akan terus di-append seiring dengan terjawabnya pertanyaan, sehingga akan ada 20 kolom pada pertanyaan terakhir dengan value berupa transkrip pertanyaan di baris pertama, transkrip jawaban di baris kedua, dan skor kelayakan pada baris ketiga (kecuali kolom ID yang di-exclude).

Pertanyaan akan diambil dari bank pertanyaan di app/modules/QnA/questions.py yang akan menyimpan 4 list untuk levels, beginner, intermediate & advanced +1 pertanyaan tentang ekspektasi gaji. dengan len masing masing 2,16,16,16,1.

- 2 Pertanyaan pertama akan menentukan kesulitan melalui pertanyaan pengalaman kerja:

| Lama Kerja (Bulan) | Kategori Kesulitan |
| ------------------ | ------------------ |
| `< 12`             | Mudah              |
| `12 < x < 18`      | Sedang             |
| `> 18`             | Sulit              |

Kolom-kolom dalam csv:
``` SQL
1. ID : int primary key
2. L1 (l = Leveling)
3. L2  
4. Q1
5. Q2
.
.
.
19. Q16
20. Wage_Expectation : int
```

### **3. Evaluator & Reporter**
``` UI
x
```
Blok Penentu Keputusan
### **4. Dashboard Builder -- Interface Block**
``` UI
x
```
Blok Pembuat Antarmuka

---
## **Arsitektur Program**
``` log
├── [app]
│   ├── [data]
│   │   ├── [logs]
│   │   │   └── Err. Report
│   │   ├── [reports]
│   │   │   ├── dev.premium1.csv
│   │   │   └── nurrasyid14_.csv
│   │   ├── [users]
│   │   │   └── dev.premium1.json
│   │   └── README.md
│   ├── [frontend]
│   │   ├── [static]
│   │   │   ├── script.js
│   │   │   └── style.css
│   │   ├── [templates]
│   │   │   ├── dashboard.html
│   │   │   └── login.html
│   │   └── README.md
│   ├── [modules]
│   │   ├── [auth]
│   │   │   ├── __init__.py
│   │   │   ├── auth_manager.py
│   │   │   ├── login.py
│   │   │   ├── metadata_filler.py
│   │   │   └── table_templater.py
│   │   ├── [evaluation]
│   │   │   ├── __init__.py
│   │   │   ├── aggregator.py
│   │   │   ├── analyser.py
│   │   │   └── scorer.py
│   │   ├── [io_manager]
│   │   │   ├── __init__.py
│   │   │   ├── csvio.py
│   │   │   ├── jsonio.py
│   │   │   └── storage_paths.py
│   │   ├── [logging]
│   │   │   └── logger.py
│   │   ├── [QnA]
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py
│   │   │   ├── decisions.py
│   │   │   ├── judger.py
│   │   │   ├── questions.py
│   │   │   └── text_mining.py
│   │   ├── [utils]
│   │   │   ├── __init__.py
│   │   │   ├── idgen.py
│   │   │   ├── pipeline.py
│   │   │   └── validators.py
│   │   ├── __init__.py
│   │   └── frontend_loader.py
│   └── README.md
├── [pages]
│   ├── _1_Login.py
│   ├── _2_Identity.py
│   ├── _3_menu.py
│   ├── _4_Interview.py
│   ├── _5_Result.py
│   └── _6_Dashboard.py
├── [scripts]
│   ├── quick_test.py
│   ├── run.bat
│   ├── run.sh
│   └── test_suite.py
├── .gitignore
├── COMPLETE_GUIDE.md
├── main.py
├── package.json
├── README_SETUP.md
├── README.md
├── REQUIREMENTS_EXPLANATION.md
└── requirements.txt
```
---
## **Lampiran**
1. [GitHub Repository](https://github.com/nurrasyid14/Interview-Dashboard)
2. [Streamlit App](https://sdt007-018-textmining.streamlit.app)