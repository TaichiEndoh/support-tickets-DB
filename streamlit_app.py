import datetime
import streamlit as st
import pandas as pd
import altair as alt

# Language selection
language = st.sidebar.selectbox("Select Language / 言語を選択", ["English", "日本語"])

# Initialize session state for gene, usage, and analysis dataframes
if "gene_df" not in st.session_state:
    st.session_state.gene_df = pd.DataFrame(columns=["遺伝子ID", "遺伝子名", "配列", "機能", "登録日"])

if "usage_df" not in st.session_state:
    st.session_state.usage_df = pd.DataFrame(columns=["使用ID", "遺伝子ID", "実験日", "目的", "環境"])

if "analysis_df" not in st.session_state:
    st.session_state.analysis_df = pd.DataFrame(columns=["解析ID", "遺伝子ID", "解析日", "運動パターン", "スコア"])

# Content in English or Japanese based on selection
if language == "English":
    st.title("Zebrafish Gene Database")
    
    # Add a new gene
    st.header("Add a new gene")
    with st.form("add_gene_form"):
        gene_name = st.text_input("Gene Name")
        sequence = st.text_area("Gene Sequence")
        function = st.text_area("Gene Function")
        submitted = st.form_submit_button("Submit")
    
    if submitted:
        gene_id = f"GENE-{len(st.session_state.gene_df) + 1}"
        new_gene = pd.DataFrame(
            {
                "遺伝子ID": [gene_id],
                "遺伝子名": [gene_name],
                "配列": [sequence],
                "機能": [function],
                "登録日": [datetime.date.today().strftime("%Y-%m-%d")]
            }
        )
        st.session_state.gene_df = pd.concat([new_gene, st.session_state.gene_df], ignore_index=True)
        st.success(f"Gene '{gene_name}' added successfully!")

elif language == "日本語":
    #st.title("ゼブラフィッシュ\n遺伝子データベース")  # 改行を追加
    st.markdown("<h1 style='font-size: 40px;'>ゼブラフィッシュ</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 40px;'>遺伝子データベース</h1>", unsafe_allow_html=True)
   
    # 新しい遺伝子を追加
    st.header("新しい遺伝子を追加")
    with st.form("add_gene_form"):
        gene_name = st.text_input("遺伝子名")
        sequence = st.text_area("遺伝子配列")
        function = st.text_area("遺伝子の機能")
        submitted = st.form_submit_button("送信")
    
    if submitted:
        gene_id = f"GENE-{len(st.session_state.gene_df) + 1}"
        new_gene = pd.DataFrame(
            {
                "遺伝子ID": [gene_id],
                "遺伝子名": [gene_name],
                "配列": [sequence],
                "機能": [function],
                "登録日": [datetime.date.today().strftime("%Y-%m-%d")]
            }
        )
        st.session_state.gene_df = pd.concat([new_gene, st.session_state.gene_df], ignore_index=True)
        st.success(f"遺伝子 '{gene_name}' が正常に追加されました！")

# CSVファイルのアップロードによるデータ入力
st.header("CSVファイルから遺伝子データをアップロード" if language == "日本語" else "Upload gene data from CSV file")
uploaded_file = st.file_uploader("CSVファイルを選択" if language == "日本語" else "Select a CSV file", type=["csv"])


if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file)
    st.session_state.gene_df = pd.concat([st.session_state.gene_df, uploaded_df], ignore_index=True)
    st.success("CSVデータが正常にアップロードされました！")

# Display dataframes
st.header("遺伝子情報" if language == "日本語" else "Gene Information")
st.dataframe(st.session_state.gene_df)
