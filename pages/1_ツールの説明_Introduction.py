import streamlit as st
from modules.sidebar_lang import set_language

lang_code, lang_dict = set_language()

st.title(lang_dict[lang_code]["title_intro"])
st.caption(lang_dict[lang_code]["caption_intro"])

# Hero（概要）
if lang_code == "ja":
    st.info(
        "このツールは **英語の学術テキスト** から *キーターム* を抽出し、"
        " **リスト / バブルチャート / ワードクラウド** で可視化します。"
        " 初めてでも、下の「クイックスタート」で最短ルートを確認できます。"
    )
else:
    st.info(
        "This tool extracts *key terms* from **English academic texts** and "
        "visualizes them as **List / Bubble Chart / Word Cloud**. "
        "Check 'Quick Start' below for the fastest way to get started."
    )

st.divider()

# 主な機能
st.subheader("✨ " + ("Main Features" if lang_code == "en" else "主な機能"))
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("### 📥 " + ("Input" if lang_code == "en" else "入力"))
    st.markdown(
        "- `.txt` upload or paste\n- English text only\n- Click **Start Analysis**"
        if lang_code == "en" else
        "- `.txt` アップロード or 直接入力\n- 英語テキスト専用\n- **分析開始** ボタンで実行"
    )

with col2:
    st.markdown("### 🧠 " + ("Analysis" if lang_code == "en" else "分析"))
    st.markdown(
        "- spaCy preprocessing (lemmatization/POS)\n- Remove stopwords/numbers/symbols\n- TF-IDF with reference corpus"
        if lang_code == "en" else
        "- spaCy 前処理（lemmatize / POS）\n- ストップワード/数字/記号の除去\n- 比較コーパス × **TF-IDF** で特徴語抽出"
    )

with col3:
    st.markdown("### 📊 " + ("Visualization & Export" if lang_code == "en" else "可視化・出力"))
    st.markdown(
        "- **List** (sort/filter)\n- **Bubble Chart** (TF-IDF × Freq × Length)\n- **Word Cloud** / save PNG"
        if lang_code == "en" else
        "- **リスト**（並替/品詞フィルタ）\n- **バブル**（TF-IDF×頻度×語長）\n- **ワードクラウド** / PNG保存"
    )

st.divider()

# クイックスタート
st.subheader("🚀 " + ("Quick Start" if lang_code == "en" else "クイックスタート"))
if lang_code == "ja":
    st.markdown(
        "1. 左の **「2_分析ツール」** ページへ移動\n"
        "2. テキストを入力 or `.txt` をアップロード\n"
        "3. **分析開始** をクリック\n"
        "4. タブで **リスト / バブル / クラウド** を確認\n"
        "5. 必要なら **PNG保存** ボタンでダウンロード\n"
    )
else:
    st.markdown(
        "1. Go to **'2_Analysis Tool'** page from the sidebar\n"
        "2. Enter text or upload `.txt`\n"
        "3. Click **Start Analysis**\n"
        "4. View results in **List / Bubble / Cloud** tabs\n"
        "5. Save PNG if needed\n"
    )


# ───────────────── 結果の読み方（まとめ）
with st.expander("📝 " + ("How to read the results (metrics)" if lang_code == "en" else "結果の読み方（指標の意味）"), expanded=False):
    if lang_code == "ja":
        st.markdown(
            "**TF-IDF**: その語が *文書に特有* である度合い（高いほど特有）。\n\n"
            "- **リスト**: 上ほど重要（選んだ並替基準）。**頻度**＝出現回数、**品詞**はspaCy。\n"
            "- **バブル**: 右（TF-IDF↑）× 上（頻度↑）が“特有かつ多用”。サイズ＝語の文字数、色＝品詞。\n"
            "- **ワードクラウド**: 大きい語ほどTF-IDFが高い。**配置や色は装飾**（意味なし）。\n"
            "\n詳細は各ページ末尾の“この結果の読み方”も参照してください。"
        )
    else:
        st.markdown(
            "**TF-IDF**: Degree to which a term is *specific to the document* (higher = more specific).\n\n"
            "- **List**: Higher rows are more important (by the selected sort key). **Frequency** = occurrences; **POS** from spaCy.\n"
            "- **Bubble**: Right (TF-IDF↑) × Up (Frequency↑) means “specific and frequently used.” Size = term length (chars), color = POS.\n"
            "- **Word Cloud**: Larger words have higher TF-IDF. **Layout/colors are decorative** (no meaning).\n"
            "\nFor details, also see “How to read these results” at the bottom of each page."
        )


st.divider()

# ───────────────── 比較コーパス一覧（折りたたみ）
st.subheader("📚 " + ("Reference Corpus (corpus/)" if lang_code == "en" else "比較コーパス（corpus/）"))
with st.expander("See the breakdown of doc1–doc10" if lang_code == "en" else "doc1〜doc10 の内訳を見る"):

    st.markdown(
        "- **doc1**: BERT — https://arxiv.org/abs/1810.04805\n"
        "- **doc2**: Transformer — https://arxiv.org/abs/1706.03762\n"
        "- **doc3**: GPT — https://www.semanticscholar.org/paper/GPT-(OpenAI)-2018\n"
        "- **doc4**: ResNet — https://arxiv.org/abs/1512.03385\n"
        "- **doc5**: RoBERTa — https://arxiv.org/abs/1907.11692\n"
        "- **doc6**: GPT‑3 — https://arxiv.org/abs/2005.14165\n"
        "- **doc7**: XAI — https://arxiv.org/abs/2006.11371\n"
        "- **doc8**: AI Planning & NLP — https://dl.acm.org/\n"
        "- **doc9**: T5 — https://arxiv.org/abs/1910.10683\n"
        "- **doc10**: Automatic Summarization — https://arxiv.org/abs/1704.04289"
    )

st.divider()

# ───────────────── 環境と使い方（2カラム）
left, right = st.columns(2)
with left:
    st.subheader("🧩 " + ("Development Environment" if lang_code == "en" else "開発環境"))
    st.code(
        "- Python 3.x\n"
        "- Streamlit\n"
        "- spaCy（en_core_web_sm）\n"
        "- NLTK / scikit-learn\n"
        "- matplotlib / plotly（kaleido）\n"
        "- wordcloud",
        language="markdown",
    )
with right:
    st.subheader("🔧 " + ("Setup" if lang_code == "en" else "セットアップ"))
    st.markdown(
        "```bash\n"
        "pip install -r requirements.txt\n"
        "python -m spacy download en_core_web_sm\n"
        "streamlit run app.py\n"
        "```"
    )


st.caption("© Tsubasa Sato / Contact: s1290116@u-aizu.ac.jp")
