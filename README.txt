著者スタイル・キーターム抽出ツール (Authorial Style Key-Term Extractor)
=========================================================

概要
----
本ツールは、理系学生や研究者向けに、自身の執筆した英語論文やレポートを分析し、
一般的な学術的文章と比較して語彙の使用における執筆の癖や特徴（キーターム）を抽出・可視化するものです。

特に、論文執筆に不慣れな学生が、自身の語彙選択を客観的に評価・改善できることを目的としています。

主な機能
--------
1. テキスト入力
   - .txtファイルアップロード、またはテキストエリアで直接入力
   - 英語テキスト専用
   - 「分析開始」ボタンで明示的に分析を実行

2. 語彙抽出・分析
   - spaCyによる前処理（小文字化、品詞タグ付け、Lemmatization）
   - ストップワード、数字、記号の除去
   - TF-IDFスコア計算による特徴語彙の抽出
   - ユーザー文書は、事前に用意された「学術比較コーパス」と比較される（準備中）

3. 可視化
   - リスト表示（TF-IDFスコア順／頻度順、品詞フィルター対応）
   - バブルチャート（TF-IDFスコア × 頻度、品詞別色、語長バブルサイズ）
   - ワードクラウド（TF-IDFスコアに基づくサイズ反映）

4. 出力機能
   - バブルチャート、ワードクラウドのPNGエクスポートボタン付き
   - 今後、語彙リストCSV出力にも対応予定

開発環境
--------
- Python 3.x
- Streamlit
- spaCy（en_core_web_sm）
- NLTK
- scikit-learn
- matplotlib
- plotly（+ kaleido）
- wordcloud

フォルダ構成（予定）
---------------------
authorial-keyterm-extractor/
│
├── app.py                          # Streamlit アプリ本体
├── corpus/                         # 学術比較コーパス（.txt文書が格納される）
│   ├── doc1.txt
│   └── ...
├── data/                           # 追加データ（将来使用）
│   └── reference_corpus.txt
├── modules/                        # モジュール群
│   ├── preprocessing.py            # 前処理機能
│   ├── tfidf.py                    # TF-IDF 計算処理（コーパス対応）
│   ├── visualization.py           # 可視化・画像出力
│   └── corpus_loader.py           # 比較コーパス読み込み（新規追加予定）
├── outputs/                        # ダウンロード画像の保存先
│   └── wordcloud.png / bubble_chart.png
├── assets/                         # UIスタイルなど（任意）
│   └── style.css
└── README.txt                      # このファイル


比較コーパス対応表
------------------
以下は、分析時に参照される比較用学術コーパス（corpus フォルダ）の内容一覧です。

corpus/doc1.txt  
- 論文: Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"  
- URL: https://arxiv.org/abs/1810.04805  
- 区分: Abstract + Introduction  
- 理由: BERTの概要説明で自然言語処理の文体・語彙傾向が示されている。現代NLP文書の比較に最適。

corpus/doc2.txt  
- 論文: Vaswani et al., "Attention Is All You Need"  
- URL: https://arxiv.org/abs/1706.03762  
- 区分: Introduction〜Model Architecture  
- 理由: Transformerの提案論文。学術的な導入説明や技術構成に特有の語彙が豊富で参考に適す。

corpus/doc3.txt  
- 論文: Radford et al., "Improving Language Understanding by Generative Pre-Training"（GPT）  
- URL: https://www.semanticscholar.org/paper/GPT-(OpenAI)-2018  
- 区分: 導入＋手法概要  
- 理由: 自然言語処理における生成型モデルの代表的論文。専門用語や論理展開のスタイル分析に有効。

corpus/doc4.txt  
- 論文: He et al., "Deep Residual Learning for Image Recognition"（ResNet）  
- URL: https://arxiv.org/abs/1512.03385  
- 区分: Introduction + Residual Block Explanation  
- 理由: 画像認識分野の重要論文。NLP以外の学術語彙・スタイルとの比較に役立つ。

corpus/doc5.txt  
- 論文: Liu et al., "RoBERTa: A Robustly Optimized BERT Pretraining Approach"  
- URL: https://arxiv.org/abs/1907.11692  
- 区分: 導入＋訓練改善点の要約  
- 理由: BERTの改良提案。語彙の再利用や手法改善に特化した記述が多く、著者スタイル比較に好適。

corpus/doc6.txt  
- 論文: Brown et al., "GPT‑3: Language Models are Few‑Shot Learners"  
- URL: https://arxiv.org/abs/2005.14165  
- 区分: 導入部（few‑shot学習の背景とモデル紹介）  
- 理由: 巨大モデルによる学習法が語彙・説得表現などに影響するスタイル比較に適当。

corpus/doc7.txt  
- 論文: Das & Rad, "Opportunities and Challenges in Explainable Artificial Intelligence (XAI): A Survey"  
- URL: https://arxiv.org/abs/2006.11371  
- 区分: 導入部（XAIの背景と課題）  
- 理由: 倫理や解釈性という文章テーマが異なる文脈語彙として多様性に寄与。

corpus/doc8.txt  
- 論文: Jin & Zhuo, "Integrating AI Planning with Natural Language Processing: A Combination of Explicit and Tacit Knowledge"  
- URL: https://dl.acm.org/doi/10.1145/...  
- 区分: 導入部（AI計画とNLPの融合）  
- 理由: 新興テーマである「計画NLP」の語彙と構文を含み、比較に有用。

corpus/doc9.txt  
- 論文: Raffel et al., "T5: Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer"  
- URL: https://arxiv.org/abs/1910.10683  
- 区分: 導入部（T5フレームワークの統一的言語処理アプローチ）  
- 理由: text‑to‑text形式の統一モデルであり、多様なタスク語彙を含む学術語彙として優れる。

corpus/doc10.txt  
- 論文: Nenkova & McKeown, "Automatic Summarization: Past, Present and Future"  
- URL: https://arxiv.org/abs/1704.04289  
- 区分: 導入部（自動要約の概要と課題）  
- 理由: NLPの要約分野を体系的に扱う文献で、文脈語彙と構成スキルの比較に適切。


使い方
-------
1. Python環境の準備
   - 仮想環境を作成（推奨）
   - 必要ライブラリをインストール：
     pip install -r requirements.txt
   - spaCyの英語モデルをダウンロード：
     python -m spacy download en_core_web_sm
2. `corpus/` フォルダ内に学術文書（.txt）を格納
3. Streamlitアプリを起動:  
4. テキストを入力／アップロード → 「分析開始」をクリック
5. 「リスト／バブル／クラウド」タブで結果を閲覧
6. 必要に応じて画像をダウンロード

今後の拡張予定
--------------
- 学術比較コーパスの分野選択（社会科学、生命科学など）
- 語彙リストのCSVエクスポート機能
- 他ファイル形式（PDF, DOCXなど）の読み込み対応
- 類義語クラスタリング、意味的類似度による分析
- 参考論文や他人の文章とのスタイル比較機能

連絡先
-------
（プロジェクト担当者の氏名やメールアドレス等をここに記載）
