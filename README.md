# 著者スタイル・キーターム抽出ツール  
**Authorial Style Key-Term Extractor**

## 📌 プロジェクト概要
本ツールは、理系学生や研究者向けに、自身の執筆した論文やレポートの語彙使用を分析し、一般的な学術的文章スタイルと比較して**執筆の癖や特徴的な語彙（キーターム）**を抽出・可視化します。  
これにより、論文の語彙選択を客観的に評価し、改善に役立てることを目的としています。

---

## 🎯 主な機能

### 1. テキスト入力
- **.txtファイルのアップロード** または **直接入力** に対応
- 英語テキスト専用
- Streamlit の `st.file_uploader` / `st.text_area` を活用

### 2. 語彙抽出・分析
- **比較コーパス**  
  学術論文やニュース記事などの論理的文章を事前に用意し、比較対象として使用
- **TF-IDF計算**  
  入力テキストと比較コーパスを比較し、TF-IDFスコアを算出  
  高スコアな語＝入力テキストに特有で重要な語
- **ノイズ除去**  
  NLTK等のストップワードリストで機能語を除外
- **品詞タグ付け**  
  spaCyによるlemmatization・POS解析を実施

### 3. 結果表示・可視化
- **📋 リスト表示**  
  単語、TF-IDFスコア、頻度、品詞を表形式で表示  
  品詞フィルタ機能あり
- **🔵 バブルチャート**（デフォルト）  
  - X軸: TF-IDFスコア  
  - Y軸: 頻度  
  - バブルサイズ: 単語の文字数  
  - バブル色: 品詞
- **☁️ ワードクラウド**  
  - 単語の大きさ: TF-IDFスコア反映  
  - 視覚的に特徴語を把握可能

---

## ⚙️ 開発環境
- Python 3.x
- [Streamlit](https://streamlit.io/)
- [spaCy](https://spacy.io/)（`en_core_web_sm`）
- [NLTK](https://www.nltk.org/)
- [scikit-learn](https://scikit-learn.org/)
- [matplotlib](https://matplotlib.org/) / [plotly](https://plotly.com/python/)（`kaleido`）
- [wordcloud](https://amueller.github.io/word_cloud/)

---

## 🚀 セットアップ方法
```bash
# リポジトリをクローン
git clone https://github.com/yourusername/authorial-keyterm-extractor.git
cd authorial-keyterm-extractor

# 必要ライブラリのインストール
pip install -r requirements.txt

# spaCy英語モデルのダウンロード
python -m spacy download en_core_web_sm

# アプリ起動
streamlit run app.py
```

---

## 📚 使用方法
1. サイドバーから言語を選択（日本語 / 英語）
2. **「2_分析ツール」** ページを開く
3. テキストを入力 or `.txt` ファイルをアップロード
4. **分析開始** ボタンをクリック
5. 結果タブ（リスト / バブル / ワードクラウド）で分析結果を確認
6. 必要に応じてPNG形式で保存

---

## 📝 解釈のポイント
- **TF-IDFスコア**：高いほど入力文書に特有の語
- **リスト**：上位ほど重要（選択したソート基準に基づく）
- **バブルチャート**：右上にある語は「特有かつ多用」
- **ワードクラウド**：大きい語ほど特有性が高い（色や位置は意味なし）

---

## 💡 開発上の留意点
- Streamlit のキャッシュ機能（`@st.cache_data`）でコーパスの読み込みを高速化
- コーパスは事前に前処理（lemmatization・POS付与）を済ませて保存
- デモとして、学生のレポートと学術論文を比較する事例を用意  
  例：「この単語はTF-IDFが高く形容詞なので、修飾語にスタイルの特徴が出ています」

---