import streamlit as st
from modules.preprocessing import preprocess_text
from modules.visualization import generate_bubble_chart, generate_wordcloud
from collections import Counter
import pandas as pd
from modules.visualization import export_matplotlib_figure_to_png, export_plotly_figure_to_png

@st.cache_data
def get_reference_corpus():
    from modules.corpus_loader import load_and_preprocess_corpus
    return load_and_preprocess_corpus("corpus")

st.title("著者スタイル・キーターム抽出ツール")

# --- 1. テキスト入力 ---
uploaded_file = st.file_uploader("分析したい英語テキスト（.txt）をアップロード", type=["txt"])
text_input = ""

if uploaded_file is not None:
    text_input = uploaded_file.read().decode("utf-8")
else:
    text_input = st.text_area("またはここに英語テキストを入力してください（英語のみ）", height=200)

# --- 2. 分析ボタン ---
analyze = st.button("分析を開始")

# --- 3. 分析処理（ボタンが押されたら実行、結果をセッションに保存） ---
if analyze and text_input.strip():
    tokens = preprocess_text(text_input)

    # （新：比較コーパスを使う）
    reference_corpus = get_reference_corpus()  # キャッシュされた学術文書リスト
    user_doc_tokens = [token["lemma"] for token in tokens]

    from modules.tfidf import compute_tfidf_with_reference
    tfidf_results = compute_tfidf_with_reference(user_doc_tokens, reference_corpus, top_n=30)

    lemma_pos_map = {token["lemma"]: token["pos"] for token in tokens}
    lemma_freq = Counter([token["lemma"] for token in tokens])

    tfidf_data = []
    for item in tfidf_results:
        lemma = item["term"]
        tfidf_data.append({
            "単語": lemma,
            "TF-IDFスコア": item["score"],
            "頻度": lemma_freq.get(lemma, 0),
            "品詞": lemma_pos_map.get(lemma, "N/A")
        })

    df = pd.DataFrame(tfidf_data)

    # セッションに保存
    st.session_state["tokens"] = tokens
    st.session_state["df"] = df

# --- 4. 分析結果がある場合にタブ表示 ---
if "df" in st.session_state:
    df = st.session_state["df"]

    tab1, tab2, tab3 = st.tabs(["📋 リスト表示", "🔵 バブルチャート", "☁️ ワードクラウド"])

    # 📋 リスト表示タブ
    with tab1:
        st.subheader("語彙リスト（フィルター・並び替え可能）")

        # 並び替えとフィルター（リスト表示に限定）
        sort_by = st.selectbox("並び替え基準を選択:", ["TF-IDFスコア", "頻度"])
        pos_options = df["品詞"].unique().tolist()
        selected_pos = st.multiselect("品詞フィルター:", pos_options, default=pos_options)

        filtered_df = df[df["品詞"].isin(selected_pos)]
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=False).reset_index(drop=True)

        st.dataframe(filtered_df)

    # 🔵 バブルチャートタブ
    with tab2:
        st.subheader("特徴語バブルチャート")
        fig = generate_bubble_chart(df)  # 全データを使用（フィルター非適用）
        st.plotly_chart(fig, use_container_width=True)

        #pngダウンロードボタン
        png_bytes = export_plotly_figure_to_png(fig)
        st.download_button(
            label="📥 バブルチャートをPNGで保存",
            data=png_bytes,
            file_name="bubble_chart.png",
            mime="image/png"
        )

    # ☁️ ワードクラウドタブ
    with tab3:
        st.subheader("ワードクラウド")
        fig = generate_wordcloud(df)
        st.pyplot(fig)

        #pngダウンロードボタン
        wc_png = export_matplotlib_figure_to_png(fig)
        st.download_button(
            label="📥 ワードクラウドをPNGで保存",
            data=wc_png,
            file_name="wordcloud.png",
            mime="image/png"
        )

    # 補足説明
    with st.expander("TF-IDFスコアとは？"):
        st.markdown("""
        **TF-IDFスコア**は、その単語が文書内で頻出かつ、他の文書ではあまり出現しない「特徴的な単語」であることを示します。  
        スコアが高いほど、**その文書に特有な語彙**と判断されます。
        """)

else:
    st.info("テキストを入力後、『分析を開始』ボタンを押してください。")