# app/modules/auth/table_templater.py

def empty_metadata_template():
    """
    Provide an empty template before the user fills the form.
    """
    return {
        "File_ID": "",
        "Nama": "",
        "Tanggal_Lahir": "",
        "Kontak": "",
        "Alamat": "",
        "Keahlian": [],
        "Username": ""
    }
