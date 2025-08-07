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
        # モデルがロードできない場合はエラーメッセージを表示
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
    # ... (既存の処理ロジック)

    return processed_tokens