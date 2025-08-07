import spacy
import streamlit as st
import subprocess
import sys

# @st.cache_resource デコレータを使用してモデルのダウンロードとロードをキャッシュ
@st.cache_resource
def load_spacy_model():
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        st.info("spaCyモデル 'en_core_web_sm' が見つかりませんでした。インストールを試みます...")
        
        # モデルをダウンロード
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            st.success("モデルのインストールが完了しました。")
        except subprocess.CalledProcessError as e:
            st.error(f"モデルのインストール中にエラーが発生しました: {e}")
            st.stop()
        
        # ダウンロード後に再度ロード
        nlp = spacy.load("en_core_web_sm")
        return nlp

# アプリケーション全体でモデルをロード
nlp = load_spacy_model()

def preprocess_text(text):
    """
    英語テキストを前処理し、特徴語彙の抽出に適した形で返す。
    """
    text = text.lower()
    doc = nlp(text)

    processed_tokens = []

    for token in doc:
        # 基本的なノイズ除去条件
        if (
            not token.is_punct
            and not token.is_space
            and not token.like_num
            and token.is_alpha
        ):
            # ストップワードの除去（ただし動詞は除外しない）
            if token.is_stop and token.pos_ != "VERB":
                continue

            processed_tokens.append({
                "lemma": token.lemma_,
                "pos": token.pos_,
                "text": token.text
            })

    return processed_tokens
