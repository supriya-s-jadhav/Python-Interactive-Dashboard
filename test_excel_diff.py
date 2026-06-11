import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel Part Number Comparator", layout="wide")
st.title("⚙️ Part Number Comparison Tool")
st.write("Upload two Excel files to instantly spot missing or changed data.")

st.markdown("### 1. Upload Files")
col1, col2 = st.columns(2)
with col1:
    maindatafile = st.file_uploader("Upload File 1 (Main datafile)", type=["xlsx"])
with col2:
    subdatafile = st.file_uploader("Upload File 2 (Sub datafile)", type=["xlsx"])

if maindatafile and subdatafile:
    df1 = pd.read_excel(maindatafile)
    df2 = pd.read_excel(subdatafile)

    st.markdown("### 2. Configure Columns")
    st.write("Ensure your part numbers and attributes align correctly.")

    # Get column lists
    cols1 = list(df1.columns)
    cols2 = list(df2.columns)

    col_select1 = st.selectbox("Select Part Number column in File 1", cols1)
    col_select2 = st.selectbox("Select Part Number column in File 2", cols2)

    if st.button("Compare Parts", type="primary"):
        # Ensure part numbers are strings to avoid format matching issues
        df1[col_select1] = df1[col_select1].astype(str)
        df2[col_select2] = df2[col_select2].astype(str)

        # 1. Identify Missing Parts
        missing_in_subdatafile = df1[~df1[col_select1].isin(df2[col_select2])]
        missing_in_maindatafile = df2[~df2[col_select2].isin(df1[col_select1])]

        # 2. Identify Changed Parts (Matching parts but different details)
        # Find common part numbers
        common_parts = pd.merge(
            df1,
            df2,
            left_on=col_select1,
            right_on=col_select2,
            suffixes=("_f1", "_f2"),
            how="inner",
        )

        changed_rows = []
        for index, row in common_parts.iterrows():
            # Check for any column differences across the matching rows
            for col in cols1:
                if col in cols2 and col != col_select1:
                    val1 = row[f"{col}_f1"]
                    val2 = row[f"{col}_f2"]
                    # Ignore NaN/None matches
                    if pd.isna(val1) and pd.isna(val2):
                        continue
                    if val1 != val2:
                        changed_rows.append(
                            {
                                "Part Number": row[col_select1],
                                "Column": col,
                                "File 1 Value": val1,
                                "File 2 Value": val2,
                            }
                        )

        df_changed = pd.DataFrame(changed_rows)

        # --- Display Results ---
        st.markdown("### 📊 Comparison Results")

        tab1, tab2, tab3 = st.tabs(
            [
                f"Missing in sub datafile  ({len(missing_in_subdatafile)})",
                f"New in sub datafile ({len(missing_in_maindatafile)})",
                f"Changed Details ({len(df_changed)})",
            ]
        )

        with tab1:
            st.dataframe(missing_in_subdatafile)
        with tab2:
            st.dataframe(missing_in_maindatafile)
        with tab3:
            st.dataframe(df_changed)

        # --- Download Utilities ---
        st.markdown("### 📥 Download Reports")

        def to_excel(df_list):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                for name, df in df_list:
                    df.to_excel(writer, index=False, sheet_name=name)
            return output.getvalue()

        excel_data = [
            ("Missing_in_subdatafile", missing_in_subdatafile),
            ("New_in_subdatafile", missing_in_maindatafile),
            ("Changed_Details", df_changed),
        ]

        st.download_button(
            label="💾 Download All Reports as Excel",
            data=to_excel(excel_data),
            file_name="Part_Comparison_Results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
