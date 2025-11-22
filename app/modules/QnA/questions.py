# app/modules/QnA/questions.py
"""
Question bank for the QnA module.

Structure:
- 2 leveling questions
- 16 beginner questions
- 16 intermediate questions
- 16 advanced questions
- 1 wage expectation question
"""

from typing import Dict, List


leveling_questions: List[str] = [
    "Berapa lama Anda telah bekerja dalam bidang Anda? (bulan)",
    "Ceritakan secara singkat pengalaman kerja paling signifikan Anda."
]

beginner_questions: List[str] = [
    "Apa motivasi Anda dalam bekerja?",
    "Bagaimana Anda mengatasi tugas yang sulit?",
    "Berikan contoh ketika Anda belajar keterampilan baru.",
    "Bagaimana Anda mengatur waktu dalam aktivitas harian?",
    "Apa arti komitmen bagi Anda?",
    "Bagaimana Anda menjaga konsistensi kerja?",
    "Ceritakan pengalaman Anda bekerja dalam tim.",
    "Apa tantangan terbesar Anda dalam pekerjaan sebelumnya?",
    "Bagaimana Anda menerima instruksi baru?",
    "Apa yang membuat Anda tetap termotivasi?",
    "Bagaimana Anda menangani situasi tekanan ringan?",
    "Apa kualitas pribadi terbaik Anda?",
    "Bagaimana Anda memastikan kehadiran tepat waktu?",
    "Apa tanggapan Anda terhadap perubahan mendadak?",
    "Bagaimana Anda menjaga komunikasi yang baik dengan rekan kerja?",
    "Apa tujuan jangka pendek Anda dalam karir?"
]

intermediate_questions: List[str] = [
    "Berikan contoh situasi ketika Anda harus mengambil keputusan penting.",
    "Bagaimana Anda menangani konflik dalam tim?",
    "Ceritakan bagaimana Anda menyelesaikan masalah yang kompleks.",
    "Bagaimana Anda memastikan kualitas hasil kerja?",
    "Apa kontribusi terbaik Anda di tempat kerja terakhir?",
    "Bagaimana Anda mengatur prioritas kerja?",
    "Bagaimana Anda menghadapi tekanan deadline?",
    "Apa pendekatan Anda dalam menjalankan instruksi kerja?",
    "Ceritakan situasi ketika Anda harus menunjukkan keandalan tinggi.",
    "Bagaimana Anda meningkatkan efisiensi kerja?",
    "Bagaimana Anda memastikan komunikasi tetap efektif dalam tim?",
    "Ceritakan pengalaman Anda menghadapi perubahan besar.",
    "Apa strategi Anda dalam mempelajari hal baru?",
    "Bagaimana Anda menjaga integritas saat bekerja?",
    "Bagaimana Anda mengelola beberapa tugas sekaligus?",
    "Apa langkah Anda dalam mengoreksi kesalahan pribadi?"
]

advanced_questions: List[str] = [
    "Ceritakan pengalaman memimpin proyek atau tim.",
    "Bagaimana Anda mengambil keputusan strategis dalam tekanan?",
    "Berikan contoh masalah yang Anda selesaikan dengan pendekatan analitis.",
    "Bagaimana Anda memastikan anggota tim tetap termotivasi?",
    "Ceritakan situasi ketika Anda harus menunjukkan integritas yang kuat.",
    "Bagaimana Anda membangun sistem kerja yang efisien?",
    "Bagaimana Anda mengatasi beban kerja berat?",
    "Ceritakan pengalaman ketika Anda harus bertindak sangat cepat.",
    "Bagaimana Anda mengevaluasi performa diri sendiri?",
    "Apa strategi Anda menghadapi perselisihan antar divisi?",
    "Bagaimana Anda menangani resiko operasional?",
    "Ceritakan pengalaman menyelesaikan konflik staf.",
    "Bagaimana Anda memastikan keberlanjutan kerja tim?",
    "Apa pendekatan Anda dalam mengembangkan talenta junior?",
    "Ceritakan momen ketika Anda harus mengambil keputusan yang tidak populer.",
    "Bagaimana Anda menjaga standar profesionalisme dalam situasi sulit?"
]

wage_question: str = "Berapa ekspektasi gaji Anda? (angka)"



def load_questions() -> Dict[str, List[str]]:
    return {
        "leveling": leveling_questions,
        "beginner": beginner_questions,
        "intermediate": intermediate_questions,
        "advanced": advanced_questions,
        "wage": [wage_question]
    }
