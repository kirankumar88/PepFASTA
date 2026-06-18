import streamlit as st
import pandas as pd
import re
import zipfile
import io

st.set_page_config(page_title="CSV → Peptide_FASTA_Generator", layout="wide")

st.title("🧬 CSV → Peptide_FASTA_Generator")

st.subheader("📄 Example Input Format")

sample_data = pd.DataFrame({
    "Protein_IDs": ["A0A0D9MMY4", "B8N5Q9"],
    "Protein_names": [
        "Tetratricopeptide repeat domain protein",
        "Cytochrome c oxidase subunit 2"
    ],
    "Peptide_sequence_1": ["M(ox)KTLLILT", "LLAGGTTK"],
    "Peptide_sequence_2": ["GAVVTGQGTR", "PEPTIDESEQ"],
    "Peptide_sequence_3": ["", "ACDEFGHIK"]
})

csv_sample = sample_data.to_csv(index=False)

st.download_button(
    label="📥 Download Sample CSV",
    data=csv_sample,
    file_name="sample_peptide_input.csv",
    mime="text/csv"
)

st.dataframe(sample_data)
st.write("Upload a CSV or ZIP file (MaxQuant-style) to generate FASTA.")

# =========================
# CORE PROCESS FUNCTION
# =========================
def process_dataframe(df, remove_mods, remove_duplicates, min_length):

    # Auto-detect columns
    protein_col = [c for c in df.columns if "protein" in c.lower() and "id" in c.lower()][0]
    protein_name_col = [c for c in df.columns if "protein" in c.lower() and "name" in c.lower()][0]
    peptide_cols = [c for c in df.columns if "peptide" in c.lower()]

    # Melt
    df_long = df.melt(
        id_vars=[protein_col, protein_name_col],
        value_vars=peptide_cols,
        value_name="Peptide"
    )

    # Clean
    df_long = df_long.dropna(subset=["Peptide"])
    df_long["Peptide"] = df_long["Peptide"].astype(str).str.strip()
    df_long = df_long[df_long["Peptide"] != ""]

    if remove_mods:
        df_long["Peptide"] = df_long["Peptide"].str.replace(r'\(.*?\)', '', regex=True)

    df_long["Peptide"] = df_long["Peptide"].str.replace(r'[^A-Za-z]', '', regex=True).str.upper()
    df_long = df_long[df_long["Peptide"].str.len() >= min_length]

    valid_aa = set("ACDEFGHIKLMNPQRSTVWY")
    df_long = df_long[df_long["Peptide"].apply(lambda x: set(x).issubset(valid_aa))]

    if remove_duplicates:
        df_long = df_long.drop_duplicates(subset=[protein_col, "Peptide"])

    df_long["pep_index"] = df_long.groupby(protein_col).cumcount() + 1

    df_long[protein_name_col] = (
        df_long[protein_name_col]
        .astype(str)
        .str.replace(r'[>\n]', ' ', regex=True)
        .str.strip()
        .str[:100]
    )

    df_long["header"] = (
        ">" +
        df_long[protein_col] + "_" +
        df_long["pep_index"].astype(str) + "p " +
        df_long[protein_name_col]
    )

    fasta_output = "\n".join(df_long["header"] + "\n" + df_long["Peptide"]) + "\n"

    return fasta_output, df_long


# =========================
# MODE SELECTOR
# =========================
mode = st.radio("Select Mode", ["Single CSV", "Batch (ZIP)"])

# =========================
# SETTINGS
# =========================
st.subheader("⚙️ Settings")

remove_mods = st.checkbox("Remove modifications (e.g., M(ox))", value=True)
remove_duplicates = st.checkbox("Remove duplicate peptides", value=True)
min_length = st.number_input("Minimum peptide length", value=7)

# =========================
# SINGLE FILE MODE
# =========================
if mode == "Single CSV":

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.subheader("📊 Data Preview")
        st.dataframe(df.head())

        if st.button("🚀 Generate FASTA"):

            with st.spinner("Processing..."):
                fasta_output, df_long = process_dataframe(
                    df, remove_mods, remove_duplicates, min_length
                )

            st.success("✅ FASTA generated!")

            st.download_button(
                "📥 Download FASTA",
                fasta_output,
                file_name="output.fasta",
                mime="text/plain"
            )

            st.subheader("📈 Summary")
            col1, col2 = st.columns(2)
            col1.metric("Total Peptides", len(df_long))
            col2.metric("Total Proteins", df_long.iloc[:,0].nunique())


# =========================
# BATCH MODE (ZIP)
# =========================
if mode == "Batch (ZIP)":

    zip_file = st.file_uploader("Upload ZIP file containing CSVs", type=["zip"])

    if zip_file:

        if st.button("🚀 Process ZIP"):

            with st.spinner("Processing batch..."):

                input_zip = zipfile.ZipFile(zip_file)
                output_buffer = io.BytesIO()

                processed = 0
                skipped = 0

                with zipfile.ZipFile(output_buffer, "w") as output_zip:

                    for file_name in input_zip.namelist():

                        if not file_name.endswith(".csv"):
                            continue

                        try:
                            with input_zip.open(file_name) as f:
                                df = pd.read_csv(f)

                            fasta_output, _ = process_dataframe(
                                df, remove_mods, remove_duplicates, min_length
                            )

                            out_name = file_name.replace(".csv", ".fasta")
                            output_zip.writestr(out_name, fasta_output)

                            processed += 1

                        except:
                            skipped += 1
                            continue

            st.success(f"✅ Batch complete! Processed: {processed}, Skipped: {skipped}")

            st.download_button(
                "📥 Download FASTA ZIP",
                data=output_buffer.getvalue(),
                file_name="output_fasta.zip",
                mime="application/zip"
            )