# modules/preprocessing.py

import spacy
import streamlit as st
import subprocess
import sys

@st.cache_resource
def load_spacy_model():
    """
    spacyモデルをロードし、存在しない場合は自動でダウンロードする関数。
    この関数は一度だけ実行され、結果がキャッシュされます。
    """
    try:
        # モデルのロードを試みる
        nlp = spacy.load("en_core_web_sm")
        st.success("SpaCyモデル 'en_core_web_sm' が正常にロードされました。")
        return nlp
    except OSError:
        # モデルが見つからない場合、ダウンロード処理を実行
        st.info("SpaCyモデル 'en_core_web_sm' が見つかりません。インストールを試みます...")
        
        try:
            # subprocess を使ってモデルのダウンロードコマンドを実行
            # `-m`オプションでspacyモジュールとして実行
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            st.success("モデルのインストールが完了しました。再ロードします...")
        except subprocess.CalledProcessError as e:
            st.error(f"モデルのインストール中にエラーが発生しました: {e}")
            st.stop()
        
        # ダウンロード後に再度モデルをロード
        try:
            nlp = spacy.load("en_core_web_sm")
            return nlp
        except Exception as e:
            st.error(f"モデルの再ロード中に予期せぬエラーが発生しました: {e}")
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