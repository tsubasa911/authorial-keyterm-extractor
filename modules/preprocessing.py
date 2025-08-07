# modules/preprocessing.py

import spacy
import streamlit as st

@st.cache_resource
def load_spacy_model():
    """
    spacyモデルをロードする関数。
    """
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except Exception as e:
        st.error(f"SpaCyモデル 'en_core_web_sm' のロード中にエラーが発生しました: {e}")
        st.stop()

# アプリの起動時にモデルをロード
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