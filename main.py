import polars as pl
import streamlit as st


def main():
    st.header("Doctoralia")

    df = upload_data()
    if df is None:
        st.write("No data uploaded")
        return

    df_raw = df.with_columns(pl.col("FECHA").str.strptime(pl.Date, "%d/%m/%Y")).sort("FECHA")

    df = df_raw.group_by("NUM PACIENTE").agg(
        pl.col("FECHA").min().alias("FECHA_INICIO"),
        pl.col("ESTADO").filter(pl.col("ESTADO") == "Realizada y pagada").count().alias("REALIZADAS"),
        pl.col("ESTADO").filter(pl.col("ESTADO") == "Pendiente").count().alias("PENDIENTES"),
        pl.col("ASUNTO").first(),
        pl.col("AGENDA").first().map_elements(agenda_to_name, return_dtype=pl.String),
        pl.col("CANAL").first(),
    )

    st.subheader("Visitas")
    st.write(df)

    #st.subheader("Raw data")
    #st.write(df_raw)


def agenda_to_name(agenda: str):
    tokens = agenda.split(" ")
    if tokens[0] == "Online":
        return tokens[1]
    return tokens[0]


def upload_data():
    files = st.file_uploader("Upload your data", accept_multiple_files=True, type="csv")
    if not files:
        return None

    df = read_csv(files[0])

    for file in files[1:]:
        df.extend(read_csv(file))

    return df


def read_csv(file):
    return pl.read_csv(file, separator=";", truncate_ragged_lines=True)


if __name__ == "__main__":
    main()
