# modules/sidebar_lang.py
import streamlit as st

def set_language():
    """サイドバーで言語切替を行い、lang_codeと辞書を返す"""
    if "lang" not in st.session_state:
        st.session_state.lang = "ja"

    lang_code = st.sidebar.selectbox(
        "Language / 言語",
        options=["ja", "en"],
        index=0 if st.session_state.lang == "ja" else 1,
        format_func=lambda x: "日本語" if x == "ja" else "English"
    )

    st.session_state.lang = lang_code

    lang_dict = {
        "ja": {
            # 共通
            "title_intro": "著者スタイル・キーターム抽出ツール",
            "caption_intro": "Authorial Style Key-Term Extractor",
            "upload_text": "分析したい英語テキスト（.txt）をアップロード",
            "enter_text": "ここに英語テキストを入力してください",
            "start_analysis": "分析を開始",
            "clear_input": "入力をクリア",
            "list_tab": "📋 リスト表示",
            "bubble_tab": "🔵 バブルチャート",
            "wordcloud_tab": "☁️ ワードクラウド",
            "info_message": "テキストを入力して『分析を開始』をクリックすると、ここに結果が表示されます。",
            # 入力
            "input_method": "入力方法を選択してください",
            "input_direct": "テキストを直接入力",
            "input_file": "テキストファイル（.txt）をアップロード",
            # サマリー
            "summary": "📈 分析サマリー",
            "display_settings": "⚙️ 表示設定",
            "pos_filter": "品詞フィルター",
            "apply_filter": "フィルター内容をバブル/ワードクラウドにも適用する",
            "sort_by": "並び替え基準",
            "tfidf_score": "TF-IDFスコア",
            "frequency": "頻度",
            "show_more": "さらに表示 (+10)",
            # バブル
            "bubble_chart_title": "特徴語バブルチャート",
            "bubble_save": "📥 バブルチャートをPNGで保存",
            # ワードクラウド
            "wordcloud_title": "ワードクラウド",
            "wordcloud_save": "📥 ワードクラウドをPNGで保存"
        },
        "en": {
            # Common
            "title_intro": "Authorial Style Key-Term Extractor",
            "caption_intro": "Authorial Style Key-Term Extractor",
            "upload_text": "Upload English text (.txt) for analysis",
            "enter_text": "Enter English text here",
            "start_analysis": "Start Analysis",
            "clear_input": "Clear Input",
            "list_tab": "📋 List View",
            "bubble_tab": "🔵 Bubble Chart",
            "wordcloud_tab": "☁️ Word Cloud",
            "info_message": "Enter text and click 'Start Analysis' to see results here.",
            # Input
            "input_method": "Select input method",
            "input_direct": "Direct text input",
            "input_file": "Upload text file (.txt)",
            # Summary
            "summary": "📈 Analysis Summary",
            "display_settings": "⚙️ Display Settings",
            "pos_filter": "POS Filter",
            "apply_filter": "Apply filter to Bubble/Word Cloud",
            "sort_by": "Sort by",
            "tfidf_score": "TF-IDF Score",
            "frequency": "Frequency",
            "show_more": "Show More (+10)",
            # Bubble
            "bubble_chart_title": "Key Term Bubble Chart",
            "bubble_save": "📥 Save Bubble Chart as PNG",
            # Word Cloud
            "wordcloud_title": "Word Cloud",
            "wordcloud_save": "📥 Save Word Cloud as PNG"
        }
    }

    return lang_code, lang_dict
