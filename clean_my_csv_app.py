#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:08:24 2025

@author: mac
"""

import streamlit as st
import pandas as pd
import os

# Set cleaned data directory
import tempfile

# Use a temporary directory for saving cleaned files
cleaned_data_dir = tempfile.mkdtemp()


st.title("🔬 Hep A IgM CSV Cleaner")
st.write("Upload your raw CSV file, and this tool will clean and export it.")

# File uploader
uploaded_file = st.file_uploader("📂 Drag and drop your Hep A IgM CSV file", type="csv")

if uploaded_file:
    # Read CSV
    # Read CSV with encoding handling
    df = pd.read_csv(uploaded_file, skiprows=28, delimiter="|", engine="python", on_bad_lines="skip", encoding="utf-8", encoding_errors="ignore")


    # Remove first row
    df = df.iloc[1:].reset_index(drop=True)

    # Define columns to keep
    columns_to_keep = ['Episode Number', 'Collection Date', 'Registration Date', 'Episode Region',
                       'Hospital', 'Age', 'Sex', 'HAM Specimen Type Description', 'HAM  Authorised Date',
                       'HAM - V0204 - Hep A IgM Result', 'HAM - V0206 - Hep A IgM Value@']

    # Keep only relevant columns
    df = df[columns_to_keep]

    # Convert dates
    df['Registration Date'] = pd.to_datetime(df['Registration Date'], errors='coerce', dayfirst=True)
    df['HAM  Authorised Date'] = pd.to_datetime(df['HAM  Authorised Date'], errors='coerce', dayfirst=True)

    # Calculate TAT (Turnaround Time in Days)
    df["TAT"] = (df["HAM  Authorised Date"] - df["Registration Date"]).dt.days

    # Generate cleaned filename
    original_filename = uploaded_file.name
    cleaned_filename = "cleaned_" + original_filename
    cleaned_filepath = os.path.join(cleaned_data_dir, cleaned_filename)

    # Save cleaned CSV
    df.to_csv(cleaned_filepath, index=False)

    # Show cleaned dataframe
    st.success(f"✅ File cleaned and saved as `{cleaned_filename}`!")
    st.dataframe(df.head())

    # Download button
    st.download_button(label="⬇️ Download Cleaned CSV", data=df.to_csv(index=False), file_name=cleaned_filename, mime="text/csv")
