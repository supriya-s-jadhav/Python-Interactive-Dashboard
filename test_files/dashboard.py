# import libraries

import pandas as pd
import streamlit as st
import difflib


st.set_page_config(page_title="Machine Parts Analyzer", layout="wide")
# Load the dataset
main_datafile = pd.read_excel(
    "/Users/supriyasampatjadhav/Documents/GitRepositories/Python-Interactive-Dashboard/data/Master_File.xlsx"
)
sub_datafile = pd.read_excel(
    "/Users/supriyasampatjadhav/Documents/GitRepositories/Python-Interactive-Dashboard/data/Data_File.xlsx"
)

# indexing from 1
main_datafile.index = main_datafile.index + 1
sub_datafile.index = sub_datafile.index + 1

# create two columns
col1, col2 = st.columns(2)

# Display data in columns
with col1:
    st.header("Main Data File")
    st.dataframe(main_datafile, height=300)

with col2:
    st.header("Sub Data File")
    st.dataframe(sub_datafile, height=300)
