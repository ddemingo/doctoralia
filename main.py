import polars as pl
import streamlit as st


def main():
    st.header("Doctoralia")

    upload_data()


def upload_data():
    files = st.file_uploader("Upload your data", accept_multiple_files=True, type=["csv"])
    for file in files:
        df = pl.read_csv(file, separator=";", truncate_ragged_lines=True)
        st.write(df)


if __name__ == "__main__":
    main()
