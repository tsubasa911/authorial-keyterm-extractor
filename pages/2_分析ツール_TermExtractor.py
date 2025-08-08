import streamlit as st
import pandas as pd
from collections import Counter
from modules.preprocessing import preprocess_text
from modules.visualization import (
    generate_bubble_chart,
    generate_wordcloud,
    export_matplotlib_figure_to_png,
    export_plotly_figure_to_png,
)
from modules.sidebar_lang import set_language

lang_code, lang_dict = set_language()

st.title("📊 " + lang_dict[lang_code]["title_intro"])
st.caption(lang_dict[lang_code]["caption_intro"] + (" — Analysis Page" if lang_code == "en" else " — 分析ページ"))

@st.cache_data
def get_reference_corpus():
    from modules.corpus_loader import load_and_preprocess_corpus
    return load_and_preprocess_corpus("corpus")

# ===== 入力カード =====
st.divider()
st.subheader("📥 " + ("Input" if lang_code == "en" else "入力"))
with st.container(border=True):
    input_method = st.radio(
        lang_dict[lang_code]["input_method"],
        [lang_dict[lang_code]["input_direct"], lang_dict[lang_code]["input_file"]],
        horizontal=True,
    )

    user_text = ""
    if input_method == lang_dict[lang_code]["input_file"]:
        uploaded = st.file_uploader(lang_dict[lang_code]["upload_text"], type=["txt"])
        if uploaded is not None:
            user_text = uploaded.read().decode("utf-8", errors="ignore")
            st.success((f"File loaded: {len(user_text)} chars") if lang_code == "en" else f"ファイル読込完了：{len(user_text)} chars")
    else:
        user_text = st.text_area(lang_dict[lang_code]["enter_text"], height=180)

    col_btn1, col_btn2 = st.columns([1,1])
    with col_btn1:
        analyze = st.button(lang_dict[lang_code]["start_analysis"], type="primary", use_container_width=True)
    with col_btn2:
        if st.button(lang_dict[lang_code]["clear_input"], use_container_width=True):
            st.session_state.pop("df", None)
            st.session_state.pop("tokens", None)
            st.session_state.pop("list_limit", None)
            st.rerun()

# ===== 分析処理 =====
if analyze and user_text.strip():
    with st.spinner("Processing..." if lang_code == "en" else "分析中…（前処理 → 比較コーパス読込 → TF-IDF計算）"):
        try:
            tokens = preprocess_text(user_text)
            reference_corpus = get_reference_corpus()
            user_doc_tokens = [t["lemma"] for t in tokens]

            from modules.tfidf import compute_tfidf_with_reference
            tfidf_results = compute_tfidf_with_reference(user_doc_tokens, reference_corpus, top_n=200)

            lemma_pos_map = {t["lemma"]: t["pos"] for t in tokens}
            lemma_freq = Counter(user_doc_tokens)

            pos_col = "品詞" if lang_code == "ja" else "POS"
            tfidf_data = []
            for item in tfidf_results:
                lemma = item["term"]
                tfidf_data.append({
                    "単語" if lang_code == "ja" else "Term": lemma,
                    lang_dict[lang_code]["tfidf_score"]: item["score"],
                    lang_dict[lang_code]["frequency"]: lemma_freq.get(lemma, 0),
                    pos_col: lemma_pos_map.get(lemma, "N/A"),
                })

            df = pd.DataFrame(tfidf_data)

            st.session_state["tokens"] = tokens
            st.session_state["df"] = df
            st.session_state["list_limit"] = 30
            st.success("Analysis complete." if lang_code == "en" else "分析が完了しました。下の結果タブを確認してください。")
        except Exception as e:
            st.error(f"Error: {e}")

# ===== 結果表示 =====
if "df" in st.session_state:
    df = st.session_state["df"]
    tokens = st.session_state.get("tokens", [])

    st.subheader(lang_dict[lang_code]["summary"])
    with st.container(border=True):
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("Tokens" if lang_code=="en" else "総トークン数（有効）", f"{len(tokens):,}")
        with colB:
            st.metric("Unique Lemmas" if lang_code=="en" else "ユニーク語彙（lemma）", f"{len(set([t['lemma'] for t in tokens])):,}")
        with colC:
            st.metric("Key Terms" if lang_code=="en" else "抽出キーターム（上限）", f"{len(df):,}")

    st.divider()
    st.subheader(lang_dict[lang_code]["display_settings"])
    with st.container(border=True):
        pos_col = "品詞" if lang_code == "ja" else "POS"
        pos_options = df[pos_col].unique().tolist()
        selected_pos = st.multiselect(lang_dict[lang_code]["pos_filter"], pos_options, default=pos_options)
        apply_filter_to_plots = st.checkbox(lang_dict[lang_code]["apply_filter"], value=False)

    filtered_df = df[df[pos_col].isin(selected_pos)].reset_index(drop=True)

    tab1, tab2, tab3 = st.tabs([lang_dict[lang_code]["list_tab"], lang_dict[lang_code]["bubble_tab"], lang_dict[lang_code]["wordcloud_tab"]])

    with tab1:
        sort_by = st.selectbox(lang_dict[lang_code]["sort_by"], [lang_dict[lang_code]["tfidf_score"], lang_dict[lang_code]["frequency"]], index=0)
        filtered_df_sorted = filtered_df.sort_values(by=sort_by, ascending=False).reset_index(drop=True)

        list_limit = st.session_state.get("list_limit", 30)
        display_df = filtered_df_sorted.head(list_limit).copy()
        display_df.index = range(1, len(display_df) + 1)
        st.dataframe(display_df, use_container_width=True)

        if len(filtered_df_sorted) > list_limit:
            if st.button(lang_dict[lang_code]["show_more"]):
                st.session_state["list_limit"] = min(list_limit + 10, len(filtered_df_sorted))
                st.rerun()

    with tab2:
        st.subheader(lang_dict[lang_code]["bubble_chart_title"])
        plot_df = filtered_df if apply_filter_to_plots else df
        fig = generate_bubble_chart(plot_df)
        st.plotly_chart(fig, use_container_width=True)
        png_bytes = export_plotly_figure_to_png(fig)
        st.download_button(lang_dict[lang_code]["bubble_save"], data=png_bytes, file_name="bubble_chart.png", mime="image/png", use_container_width=True)

    with tab3:
        st.subheader(lang_dict[lang_code]["wordcloud_title"])
        plot_df_wc = filtered_df if apply_filter_to_plots else df
        fig_wc = generate_wordcloud(plot_df_wc)
        st.pyplot(fig_wc, use_container_width=True)
        wc_png = export_matplotlib_figure_to_png(fig_wc)
        st.download_button(lang_dict[lang_code]["wordcloud_save"], data=wc_png, file_name="wordcloud.png", mime="image/png", use_container_width=True)

else:
    st.info(lang_dict[lang_code]["info_message"])
