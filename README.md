# 🧬 PepFASTA

🚀 **Live App:** https://your-app-name.streamlit.app

PepFASTA is a scalable Streamlit application for converting proteomics peptide datasets into FASTA format. It supports both single CSV files and batch processing via ZIP upload, making it suitable for real-world laboratory workflows.

---

## 🚀 Overview

PepFASTA transforms wide-format peptide tables (e.g., MaxQuant outputs) into clean, deduplicated FASTA sequences with annotated protein headers.

Designed for downstream applications such as:

* Signal peptide prediction (SignalP, Phobius)
* Sequence alignment (BLAST)
* Functional annotation pipelines

---

## ⚙️ Key Features

### 🔹 Core Functionality

* Convert peptide CSV files into FASTA
* Automatic detection of:

  * Protein ID columns
  * Protein name columns
  * Peptide sequence columns
* Handles **300+ peptide columns**

### 🔹 Data Cleaning

* Removes peptide modifications (e.g., M(ox), Phospho)
* Filters non-IUPAC amino acids
* Converts sequences to uppercase
* Applies minimum peptide length filtering

### 🔹 Deduplication

* Removes duplicate peptides per protein

### 🔹 FASTA Output

```
>ProteinID_indexp Protein Name
```

---

## 📦 Batch Processing

* Upload a `.zip` containing multiple CSV files
* Automatically processes all valid files
* Returns a downloadable ZIP with FASTA outputs

### Example

**Input:**

```
dataset.zip
├── sample1.csv
├── sample2.csv
└── sample3.csv
```

**Output:**

```
output_fasta.zip
├── sample1.fasta
├── sample2.fasta
└── sample3.fasta
```

---

## 📂 Input Format

| Protein_IDs | Protein_names | Peptide_sequence_1 | Peptide_sequence_2 |
| ----------- | ------------- | ------------------ | ------------------ |
| A0A0D9MMY4  | Protein X     | M(ox)KTLLILT       | GAVVTGQGTR         |

✔ Column detection is automatic
✔ No manual configuration required

---

## 📤 Output Format

```fasta
>A0A0D9MMY4_1p Protein X
MKTLLILT

>A0A0D9MMY4_2p Protein X
GAVVTGQGTR
```

---

## 🛠 Installation

```bash
git clone https://github.com/kirankumar88/PepFASTA.git
cd PepFASTA
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deploy Your Own

You can deploy this app for free using Streamlit Community Cloud:

1. Push this repository to GitHub
2. Go to https://streamlit.io/cloud
3. Click **New app**
4. Select your repository (`PepFASTA`)
5. Set entry point as `app.py`
6. Deploy

---

## 📦 Requirements

```
streamlit
pandas
```

---

## 📈 Applications

* Proteomics data preprocessing
* Mass spectrometry workflows
* FASTA generation for SignalP / Phobius
* BLAST sequence analysis
* High-throughput peptide processing

---

## ⚡ Performance

* Vectorized processing using Pandas
* Handles large datasets efficiently
* Supports batch processing workflows

---

## ⚠️ Notes

* Output order may differ from input due to normalization
* Modified peptides are cleaned by default
* Invalid sequences are filtered automatically

---

## 🔮 Future Enhancements

* Progress bar for batch processing
* QC reports and peptide statistics
* Combined FASTA output option
* SignalP / Phobius integration
* Export cleaned CSV

---

## 🤝 Contributing

Contributions and suggestions are welcome.
Please open an issue or submit a pull request.

---

## 📜 License

MIT License

---

## 👨‍🔬 Author

**Kiran Kumar**
Researcher in Biology, AI & ML

---

## ⭐ Support

If you find this tool useful, please consider starring the repository.
