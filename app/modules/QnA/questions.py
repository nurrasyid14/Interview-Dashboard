# Question Bank for Hire-ON! Interview System
# Contains 240 questions (5 positions x 3 levels x 16 questions) + leveling + wage

from typing import Dict, List

# Job positions with wage ranges
JOB_POSITIONS = {
    "Chef": {"min_wage": 4500000, "max_wage": 12000000, "standard": 6000000},
    "OB": {"min_wage": 3000000, "max_wage": 5000000, "standard": 3500000},
    "Business Advisor": {"min_wage": 8000000, "max_wage": 25000000, "standard": 12000000},
    "Accountant": {"min_wage": 5000000, "max_wage": 15000000, "standard": 8000000},
    "General Manager": {"min_wage": 15000000, "max_wage": 50000000, "standard": 25000000},
}

# Leveling questions (same for all positions)
LEVELING_QUESTIONS = [
    "Berapa lama Anda telah bekerja dalam bidang Anda? (dalam bulan)",
    "Ceritakan secara singkat pengalaman kerja paling signifikan Anda."
]

# Wage expectation question
WAGE_QUESTION = "Berapa ekspektasi gaji Anda per bulan? (dalam Rupiah)"

# ================================================================
# CHEF QUESTIONS
# ================================================================
CHEF_BEGINNER = [
    "Apa motivasi Anda untuk menjadi seorang chef?",
    "Bagaimana Anda menjaga kebersihan area kerja di dapur?",
    "Ceritakan pengalaman Anda dalam menyiapkan bahan makanan dasar.",
    "Bagaimana Anda mengikuti instruksi resep dengan tepat?",
    "Apa yang Anda ketahui tentang keamanan pangan?",
    "Bagaimana Anda menangani peralatan dapur dengan aman?",
    "Ceritakan pengalaman Anda bekerja dalam tim dapur.",
    "Bagaimana Anda memprioritaskan tugas saat jam sibuk?",
    "Apa tantangan terbesar Anda saat belajar memasak?",
    "Bagaimana Anda menerima kritik dari senior chef?",
    "Apa teknik memasak dasar yang Anda kuasai?",
    "Bagaimana Anda memastikan kualitas bahan makanan?",
    "Ceritakan pengalaman Anda dengan mise en place.",
    "Bagaimana Anda menangani pesanan yang menumpuk?",
    "Apa yang membuat Anda tertarik dengan dunia kuliner?",
    "Bagaimana Anda menjaga konsistensi rasa masakan?"
]

CHEF_INTERMEDIATE = [
    "Bagaimana Anda mengelola inventory bahan makanan?",
    "Ceritakan pengalaman Anda menciptakan menu baru.",
    "Bagaimana Anda menangani komplain pelanggan tentang makanan?",
    "Apa strategi Anda dalam mengontrol food cost?",
    "Bagaimana Anda melatih junior chef baru?",
    "Ceritakan situasi ketika Anda harus berimprovisasi dengan bahan terbatas.",
    "Bagaimana Anda memastikan standar HACCP dipatuhi?",
    "Apa pendekatan Anda dalam menu engineering?",
    "Bagaimana Anda menangani tekanan saat rush hour?",
    "Ceritakan pengalaman Anda dengan catering skala besar.",
    "Bagaimana Anda mengadaptasi resep untuk dietary restrictions?",
    "Apa kontribusi terbaik Anda di kitchen sebelumnya?",
    "Bagaimana Anda menjaga motivasi tim dapur?",
    "Ceritakan pengalaman Anda dengan seasonal menu.",
    "Bagaimana Anda mengevaluasi performa bawahan?",
    "Apa filosofi memasak Anda?"
]

CHEF_ADVANCED = [
    "Bagaimana Anda mengembangkan konsep kuliner untuk restoran?",
    "Ceritakan pengalaman memimpin tim dapur besar.",
    "Bagaimana Anda menangani krisis di kitchen?",
    "Apa strategi Anda untuk mendapatkan bintang Michelin?",
    "Bagaimana Anda membangun supplier relationship?",
    "Ceritakan pengalaman Anda dengan restaurant opening.",
    "Bagaimana Anda mengintegrasikan sustainability di dapur?",
    "Apa pendekatan Anda dalam R&D kuliner?",
    "Bagaimana Anda mengelola multi-outlet kitchen operation?",
    "Ceritakan pengalaman Anda dengan media dan public relations.",
    "Bagaimana Anda menjaga brand consistency across outlets?",
    "Apa strategi talent development Anda untuk tim?",
    "Bagaimana Anda menangani food trend dan inovasi?",
    "Ceritakan pengalaman kolaborasi dengan celebrity chef.",
    "Bagaimana Anda membangun kitchen culture yang positif?",
    "Apa legacy kuliner yang ingin Anda tinggalkan?"
]

# ================================================================
# OB (OFFICE BOY) QUESTIONS
# ================================================================
OB_BEGINNER = [
    "Apa motivasi Anda untuk posisi ini?",
    "Bagaimana Anda menjaga kebersihan area kerja?",
    "Ceritakan pengalaman Anda dalam pekerjaan serupa.",
    "Bagaimana Anda mengatur waktu untuk menyelesaikan tugas?",
    "Apa yang Anda ketahui tentang standar kebersihan kantor?",
    "Bagaimana Anda menangani permintaan mendadak dari staff?",
    "Ceritakan pengalaman Anda bekerja dengan banyak orang.",
    "Bagaimana Anda memprioritaskan tugas harian?",
    "Apa tantangan terbesar dalam pekerjaan kebersihan?",
    "Bagaimana Anda menerima instruksi dari atasan?",
    "Apa peralatan kebersihan yang Anda kuasai?",
    "Bagaimana Anda memastikan area selalu rapi?",
    "Ceritakan cara Anda menyiapkan ruang meeting.",
    "Bagaimana Anda menangani tugas yang banyak sekaligus?",
    "Apa yang membuat Anda cocok untuk posisi ini?",
    "Bagaimana Anda menjaga stamina selama bekerja?"
]

OB_INTERMEDIATE = [
    "Bagaimana Anda mengelola jadwal pembersihan rutin?",
    "Ceritakan pengalaman Anda mengkoordinasi dengan vendor.",
    "Bagaimana Anda menangani keluhan dari penghuni kantor?",
    "Apa strategi Anda dalam menghemat supplies?",
    "Bagaimana Anda melatih staff baru?",
    "Ceritakan situasi ketika Anda harus handle emergency.",
    "Bagaimana Anda memastikan standar hygiene terjaga?",
    "Apa pendekatan Anda dalam facility maintenance?",
    "Bagaimana Anda menangani event preparation?",
    "Ceritakan pengalaman Anda dengan office relocation.",
    "Bagaimana Anda mengadaptasi dengan protokol kesehatan?",
    "Apa kontribusi terbaik Anda di kantor sebelumnya?",
    "Bagaimana Anda menjaga hubungan baik dengan semua staff?",
    "Ceritakan pengalaman Anda dengan pest control.",
    "Bagaimana Anda mengevaluasi hasil kerja sendiri?",
    "Apa inisiatif yang pernah Anda usulkan?"
]

OB_ADVANCED = [
    "Bagaimana Anda mengembangkan SOP untuk tim housekeeping?",
    "Ceritakan pengalaman memimpin tim facility management.",
    "Bagaimana Anda menangani building emergency?",
    "Apa strategi Anda untuk green office initiative?",
    "Bagaimana Anda membangun vendor partnership?",
    "Ceritakan pengalaman Anda dengan building renovation.",
    "Bagaimana Anda mengintegrasikan smart building system?",
    "Apa pendekatan Anda dalam budget management?",
    "Bagaimana Anda mengelola multi-floor operation?",
    "Ceritakan pengalaman Anda dengan audit compliance.",
    "Bagaimana Anda menjaga service standard across shifts?",
    "Apa strategi training program untuk tim?",
    "Bagaimana Anda menangani workplace safety?",
    "Ceritakan pengalaman implementasi new technology.",
    "Bagaimana Anda membangun service culture?",
    "Apa improvement terbesar yang pernah Anda lakukan?"
]

# ================================================================
# BUSINESS ADVISOR QUESTIONS
# ================================================================
BA_BEGINNER = [
    "Apa motivasi Anda menjadi business advisor?",
    "Bagaimana Anda menganalisis data bisnis sederhana?",
    "Ceritakan pengalaman Anda dengan market research.",
    "Bagaimana Anda menyusun presentasi bisnis?",
    "Apa yang Anda ketahui tentang business model canvas?",
    "Bagaimana Anda menangani deadline project?",
    "Ceritakan pengalaman Anda dalam team collaboration.",
    "Bagaimana Anda memprioritaskan multiple tasks?",
    "Apa tantangan terbesar dalam analytical work?",
    "Bagaimana Anda menerima feedback dari senior?",
    "Apa tools analisis yang Anda kuasai?",
    "Bagaimana Anda memastikan akurasi data?",
    "Ceritakan pengalaman Anda dengan client interaction.",
    "Bagaimana Anda menangani informasi yang kompleks?",
    "Apa yang membuat Anda tertarik di consulting?",
    "Bagaimana Anda menjaga profesionalisme?"
]

BA_INTERMEDIATE = [
    "Bagaimana Anda mengelola client relationship?",
    "Ceritakan pengalaman Anda memimpin project kecil.",
    "Bagaimana Anda menangani client yang demanding?",
    "Apa strategi Anda dalam competitive analysis?",
    "Bagaimana Anda mentoring junior analyst?",
    "Ceritakan situasi ketika rekomendasi Anda ditolak.",
    "Bagaimana Anda memastikan deliverable berkualitas?",
    "Apa pendekatan Anda dalam stakeholder management?",
    "Bagaimana Anda menangani scope creep?",
    "Ceritakan pengalaman Anda dengan industry specialization.",
    "Bagaimana Anda mengadaptasi approach untuk different clients?",
    "Apa kontribusi terbaik Anda dalam project?",
    "Bagaimana Anda menjaga team productivity?",
    "Ceritakan pengalaman Anda dengan change management.",
    "Bagaimana Anda mengevaluasi project success?",
    "Apa framework consulting favorit Anda?"
]

BA_ADVANCED = [
    "Bagaimana Anda mengembangkan practice area baru?",
    "Ceritakan pengalaman memimpin engagement besar.",
    "Bagaimana Anda menangani crisis dalam project?",
    "Apa strategi Anda untuk business development?",
    "Bagaimana Anda membangun thought leadership?",
    "Ceritakan pengalaman Anda dengan C-suite presentation.",
    "Bagaimana Anda mengintegrasikan digital transformation?",
    "Apa pendekatan Anda dalam pricing strategy?",
    "Bagaimana Anda mengelola partner relationship?",
    "Ceritakan pengalaman Anda dengan M&A advisory.",
    "Bagaimana Anda menjaga firm reputation?",
    "Apa strategi talent acquisition untuk firm?",
    "Bagaimana Anda menangani ethical dilemma?",
    "Ceritakan pengalaman turnaround project.",
    "Bagaimana Anda membangun consulting methodology?",
    "Apa legacy yang ingin Anda tinggalkan di industry?"
]

# ================================================================
# ACCOUNTANT QUESTIONS
# ================================================================
ACC_BEGINNER = [
    "Apa motivasi Anda menjadi akuntan?",
    "Bagaimana Anda memastikan akurasi pembukuan?",
    "Ceritakan pengalaman Anda dengan software akuntansi.",
    "Bagaimana Anda mengorganisir dokumen keuangan?",
    "Apa yang Anda ketahui tentang standar akuntansi?",
    "Bagaimana Anda menangani deadline laporan?",
    "Ceritakan pengalaman Anda dengan reconciliation.",
    "Bagaimana Anda memprioritaskan tugas akuntansi?",
    "Apa tantangan terbesar dalam bookkeeping?",
    "Bagaimana Anda menerima koreksi dari supervisor?",
    "Apa jenis laporan keuangan yang Anda kuasai?",
    "Bagaimana Anda memastikan compliance pajak dasar?",
    "Ceritakan pengalaman Anda dengan data entry.",
    "Bagaimana Anda menangani discrepancy?",
    "Apa yang membuat Anda tertarik di bidang keuangan?",
    "Bagaimana Anda menjaga ketelitian dalam bekerja?"
]

ACC_INTERMEDIATE = [
    "Bagaimana Anda mengelola closing bulanan?",
    "Ceritakan pengalaman Anda dengan financial analysis.",
    "Bagaimana Anda menangani audit external?",
    "Apa strategi Anda dalam tax planning?",
    "Bagaimana Anda melatih junior accountant?",
    "Ceritakan situasi ketika menemukan irregularity.",
    "Bagaimana Anda memastikan internal control efektif?",
    "Apa pendekatan Anda dalam budgeting?",
    "Bagaimana Anda menangani multi-entity reporting?",
    "Ceritakan pengalaman Anda dengan ERP implementation.",
    "Bagaimana Anda mengadaptasi dengan new accounting standards?",
    "Apa kontribusi terbaik Anda di finance team?",
    "Bagaimana Anda menjaga relationship dengan auditor?",
    "Ceritakan pengalaman Anda dengan cost analysis.",
    "Bagaimana Anda mengevaluasi financial performance?",
    "Apa improvement process yang pernah Anda implementasi?"
]

ACC_ADVANCED = [
    "Bagaimana Anda mengembangkan finance strategy?",
    "Ceritakan pengalaman memimpin finance transformation.",
    "Bagaimana Anda menangani financial crisis?",
    "Apa strategi Anda untuk investor relations?",
    "Bagaimana Anda membangun finance team culture?",
    "Ceritakan pengalaman Anda dengan IPO preparation.",
    "Bagaimana Anda mengintegrasikan finance dengan operations?",
    "Apa pendekatan Anda dalam treasury management?",
    "Bagaimana Anda mengelola multi-country compliance?",
    "Ceritakan pengalaman Anda dengan board reporting.",
    "Bagaimana Anda menjaga governance standard?",
    "Apa strategi succession planning di finance?",
    "Bagaimana Anda menangani regulatory changes?",
    "Ceritakan pengalaman digital finance implementation.",
    "Bagaimana Anda membangun finance excellence?",
    "Apa financial legacy yang ingin Anda tinggalkan?"
]

# ================================================================
# GENERAL MANAGER QUESTIONS
# ================================================================
GM_BEGINNER = [
    "Apa motivasi Anda dalam management?",
    "Bagaimana Anda mengkoordinasi tim kecil?",
    "Ceritakan pengalaman leadership pertama Anda.",
    "Bagaimana Anda menyusun work plan?",
    "Apa yang Anda ketahui tentang people management?",
    "Bagaimana Anda menangani konflik antar staff?",
    "Ceritakan pengalaman Anda dengan project coordination.",
    "Bagaimana Anda memprioritaskan team tasks?",
    "Apa tantangan terbesar dalam memimpin?",
    "Bagaimana Anda menerima masukan dari tim?",
    "Apa gaya leadership yang Anda terapkan?",
    "Bagaimana Anda memastikan target tercapai?",
    "Ceritakan pengalaman Anda memotivasi orang lain.",
    "Bagaimana Anda menangani underperforming staff?",
    "Apa yang membuat Anda tertarik di management?",
    "Bagaimana Anda menjaga work-life balance tim?"
]

GM_INTERMEDIATE = [
    "Bagaimana Anda mengelola departmental budget?",
    "Ceritakan pengalaman Anda dengan organizational change.",
    "Bagaimana Anda menangani cross-functional conflict?",
    "Apa strategi Anda dalam talent development?",
    "Bagaimana Anda melatih emerging leaders?",
    "Ceritakan situasi ketika harus membuat keputusan sulit.",
    "Bagaimana Anda memastikan operational excellence?",
    "Apa pendekatan Anda dalam performance management?",
    "Bagaimana Anda menangani stakeholder management?",
    "Ceritakan pengalaman Anda dengan business expansion.",
    "Bagaimana Anda mengadaptasi dengan market changes?",
    "Apa kontribusi terbaik Anda sebagai leader?",
    "Bagaimana Anda menjaga team engagement?",
    "Ceritakan pengalaman Anda dengan process improvement.",
    "Bagaimana Anda mengevaluasi team performance?",
    "Apa philosophy management Anda?"
]

GM_ADVANCED = [
    "Bagaimana Anda mengembangkan corporate strategy?",
    "Ceritakan pengalaman memimpin business turnaround.",
    "Bagaimana Anda menangani organizational crisis?",
    "Apa strategi Anda untuk market leadership?",
    "Bagaimana Anda membangun executive team?",
    "Ceritakan pengalaman Anda dengan merger integration.",
    "Bagaimana Anda mengintegrasikan digital transformation?",
    "Apa pendekatan Anda dalam board governance?",
    "Bagaimana Anda mengelola multi-business unit?",
    "Ceritakan pengalaman Anda dengan international expansion.",
    "Bagaimana Anda menjaga corporate culture?",
    "Apa strategi succession planning Anda?",
    "Bagaimana Anda menangani public relations crisis?",
    "Ceritakan pengalaman innovation initiative.",
    "Bagaimana Anda membangun sustainable business?",
    "Apa legacy yang ingin Anda tinggalkan di organization?"
]

# ================================================================
# COMPILED QUESTION BANK
# ================================================================
QUESTION_BANK: Dict[str, Dict[str, List[str]]] = {
    "Chef": {
        "beginner": CHEF_BEGINNER,
        "intermediate": CHEF_INTERMEDIATE,
        "advanced": CHEF_ADVANCED
    },
    "OB": {
        "beginner": OB_BEGINNER,
        "intermediate": OB_INTERMEDIATE,
        "advanced": OB_ADVANCED
    },
    "Business Advisor": {
        "beginner": BA_BEGINNER,
        "intermediate": BA_INTERMEDIATE,
        "advanced": BA_ADVANCED
    },
    "Accountant": {
        "beginner": ACC_BEGINNER,
        "intermediate": ACC_INTERMEDIATE,
        "advanced": ACC_ADVANCED
    },
    "General Manager": {
        "beginner": GM_BEGINNER,
        "intermediate": GM_INTERMEDIATE,
        "advanced": GM_ADVANCED
    }
}


def get_questions_for_position(position: str, level: str) -> List[str]:
    """Get 16 questions for a specific position and level."""
    if position not in QUESTION_BANK:
        raise ValueError(f"Unknown position: {position}")
    if level not in QUESTION_BANK[position]:
        raise ValueError(f"Unknown level: {level}")
    return QUESTION_BANK[position][level]


def get_leveling_questions() -> List[str]:
    """Get the 2 leveling questions."""
    return LEVELING_QUESTIONS


def get_wage_question() -> str:
    """Get the wage expectation question."""
    return WAGE_QUESTION


def get_all_questions(position: str, level: str) -> List[str]:
    """Get all 19 questions (2 leveling + 16 position + 1 wage)."""
    questions = LEVELING_QUESTIONS.copy()
    questions.extend(get_questions_for_position(position, level))
    questions.append(WAGE_QUESTION)
    return questions


def get_job_positions() -> Dict:
    """Get all job positions with wage info."""
    return JOB_POSITIONS


def determine_level(months: int) -> str:
    """Determine difficulty level based on experience months."""
    if months < 12:
        return "beginner"
    elif months < 18:
        return "intermediate"
    return "advanced"


__all__ = [
    "get_questions_for_position",
    "get_leveling_questions",
    "get_wage_question",
    "get_all_questions",
    "get_job_positions",
    "determine_level",
    ]
