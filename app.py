import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Machine Parts Analyzer", layout="wide")
st.title("Machine-Parts Comparison Tool")
st.write("Upload two Excel files to instantly spot missing or changed data.")

st.markdown("#### 1. Upload Files")
col1, col2 = st.columns(2)
with col1:
    maindatafile = st.file_uploader("Upload File 1 (Main datafile)", type=["xlsx"])
with col2:
    subdatafile = st.file_uploader("Upload File 2 (Sub datafile)", type=["xlsx"])

if maindatafile and subdatafile:
    main_df = pd.read_excel(maindatafile)
    sub_df = pd.read_excel(subdatafile)

    # indexing from 1
    # indexing from 1
    main_df.index = main_df.index + 1
    sub_df.index = sub_df.index + 1

    st.markdown("#### 2. Configure Columns")
    st.write("Ensure your part numbers and attributes align correctly.")

    # Get column lists
    cols1 = list(main_df.columns)
    cols2 = list(sub_df.columns)

    col_select1 = st.selectbox("Select Part Number column in main datafile 1", cols1)
    col_select2 = st.selectbox("Select Part Number column in sub datafile 2", cols2)

    if st.button("Compare Parts", type="primary"):
        # Ensure part numbers are strings to avoid format matching issues
        main_df[col_select1] = main_df[col_select1].astype(str)
        sub_df[col_select2] = sub_df[col_select2].astype(str)

        # 1. Identify Missing Parts
        missing_in_subdatafile = main_df[
            ~main_df[col_select1].isin(sub_df[col_select2])
        ]
        missing_in_maindatafile = sub_df[
            ~sub_df[col_select2].isin(main_df[col_select1])
        ]

        # 2. Identify Changed Parts (Matching parts but different details)
        # Find common part numbers
        common_parts = pd.merge(
            main_df,
            sub_df,
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

        # ----- calculation for total machine parts matching percentage ------

        # Drop duplicates within each file to get unique rows
        unique_main_df = main_df.drop_duplicates()
        unique_sub_df = sub_df.drop_duplicates()

        # Find overlapping rows and unique rows per file
        # We use an inner merge (intersection) to find matching rows
        matched_rows = pd.merge(unique_main_df, unique_sub_df, how="inner")

        # Calculate Matching Percentage based on Jaccard/Overlap logic: Matches / Total Unique
        # Total unique rows across both files
        union_count = len(pd.concat([unique_main_df, unique_sub_df]).drop_duplicates())
        intersection_count = len(matched_rows)

        match_percentage = (
            (intersection_count / union_count) * 100 if union_count > 0 else 0
        )

        # --- Display Results ---
        st.markdown("#### 📊 Comparison Results")

        tab1, tab2, tab3 = st.tabs(
            [
                f"Missing in sub datafile  ({len(missing_in_subdatafile)})",
                f"New in sub datafile ({len(missing_in_maindatafile)})",
                f"Changed Details ({len(df_changed)})",
            ]
        )

        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header("Main Data File")
                st.dataframe(main_df, height=300)
            with col2:
                st.header("Sub Data File")
                st.dataframe(sub_df, height=300)
            with col3:
                # st.header("Missing: Sub Data File")
                # st.dataframe(missing_in_subdatafile, height=300)
                st.subheader("Matching: Sub Data File")
                st.dataframe(matched_rows, use_container_width=True)

                st.subheader("Missing: Sub Data File")
                st.dataframe(missing_in_subdatafile, use_container_width=True)
            with tab2:
                st.dataframe(missing_in_maindatafile)
        with tab3:
            st.dataframe(df_changed)

        # --- Display matching data percentage ---
        st.subheader("Total Matching Parts Percentage")

        # # Drop duplicates within each file to get unique rows
        # unique_main_df = main_df.drop_duplicates()
        # unique_sub_df = sub_df.drop_duplicates()

        # # Find overlapping rows and unique rows per file
        # # We use an inner merge (intersection) to find matching rows
        # matched_rows = pd.merge(unique_main_df, unique_sub_df, how="inner")

        # # Calculate Matching Percentage based on Jaccard/Overlap logic: Matches / Total Unique
        # # Total unique rows across both files
        # union_count = len(pd.concat([unique_main_df, unique_sub_df]).drop_duplicates())
        # intersection_count = len(matched_rows)

        # match_percentage = (
        #     (intersection_count / union_count) * 100 if union_count > 0 else 0
        # )

        st.divider()
        # st.subheader("Results")
        st.metric("Result: ", f"{match_percentage:.2f}%")
        st.info(
            f"{intersection_count} out of {union_count} unique rows are perfectly matched in both files."
        )

        # # Display the specific overlapping rows
        # if intersection_count > 0:
        #     st.subheader("Matching Rows")
        #     st.dataframe(matched_rows)

        # --- Download Utilities ---
        st.markdown("### Download Reports")

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
