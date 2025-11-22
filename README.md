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
Cara kerja blok ini adalah dengan menampilkan 2+16 pertanyaan, yang dimana output akan berupa csv dengan nama {file_id}.csv dengan isi kolom yang akan terus di-append seiring dengan terjawabnya pertanyaan, sehingga akan ada 19 kolom pada pertanyaan terakhir dengan value berupa transkrip pertanyaan di baris pertama, transkrip jawaban di baris kedua, dan skor kelayakan pada baris ketiga (kecuali kolom ID yang di-exclude).

Pertanyaan akan diambil dari bank pertanyaan di app/modules/QnA/questions.py yang akan menyimpan 4 list untuk levels, beginner, intermediate & advanced. dengan len masing masing 2,16,16,16.

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
app/
├── data/                          # Stored JSON/CSV/parquet outputs for all users, logs, and analysis artifacts
│
├── modules/
│   ├── auth/
│   │   ├── login.py               # Handles user authentication, sessions, tokens
│   │   ├── metadata_filler.py     # Processes form inputs, validates metadata (name, age, job, username)
│   │   └── table_templater.py     # Generates JSON templates for user profile based on metadata
│   │
│   ├── QnA/
│   │   ├── questions.py           # Question bank for 18-item questionnaire (text + metadata)
│   │   ├── text_mining.py         # NLP engine: preprocessing, LDA topics, sentiment/semantic models
│   │   └── decision.py            # Computes acceptance decisions based on clarity/semantic/relevance scores
│   │
│   ├── evaluation/
│   │   ├── scorer.py              # Converts questionnaire answers into numerical scores (0–1)
│   │   ├── analyser.py            # Text mining: clarity scoring, semantic similarity, relevance, frequent words
│   │   └── aggregator.py          # Merges metadata + scores + text mining into final dashboard CSV
│   │
│   ├── utils/
│   │   ├── idgen.py               # Generates user IDs: ord(initial)<timestamp><counter>
│   │   ├── validators.py          # Username rules, age ≥ 18 check, field validation schemas (e.g., Pydantic)
│   │   └── pipeline.py            # Provides PipelineBlock base class + orchestrates multi-stage execution
│   │
│   ├── io_manager/
│   │   ├── jsonio.py              # Saves/loads metadata & questionnaire JSON files
│   │   ├── csvio.py               # Writes/reads scoring, analysis, and dashboard CSV files
│   │   └── storage_paths.py       # Standardizes file paths for all components (auth, QnA, analysis)
│   │
│   ├── logging/
│   │   └── logger.py              # Central logging utility: pipeline logs, user logs, error tracking
│   │
│   └── __init__.py                # Marks modules folder as a Python package
│
└── README.md                      # High-level documentation for backend structure and workflow
```
---