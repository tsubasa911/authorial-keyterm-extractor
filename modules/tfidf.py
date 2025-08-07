from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer

# def compute_tfidf(documents: List[List[str]], top_n: int = 10) -> List[Dict[str, Any]]:
#     """
#     文書ごとにTF-IDFスコアを計算し、上位top_nの語を抽出する。
    
#     Parameters:
#     - documents: 単語リストのリスト（例：[["this", "is", "doc1"], ["this", "is", "doc2"]]）
#     - top_n: 各文書で抽出する上位キーターム数

#     Returns:
#     - 各文書ごとのキータームとスコア（リスト）
#     """
#     # 文字列に結合（例: ["word1", "word2"] → "word1 word2"）
#     texts = [" ".join(tokens) for tokens in documents]

#     # TF-IDFベクトライザ
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(texts)
#     feature_names = vectorizer.get_feature_names_out()

#     results = []

#     # 各文書ごとに処理
#     for doc_index in range(tfidf_matrix.shape[0]):
#         tfidf_scores = tfidf_matrix[doc_index].tocoo()
#         word_scores = {
#             feature_names[i]: score for i, score in zip(tfidf_scores.col, tfidf_scores.data)
#         }

#         # 上位top_nの語を抽出（スコア順）
#         sorted_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
#         result = [{"term": term, "score": round(score, 4)} for term, score in sorted_keywords]
#         results.append(result)

#     return results

from sklearn.feature_extraction.text import TfidfVectorizer

def compute_tfidf_with_reference(user_doc_tokens, reference_docs, top_n=30):
    """
    reference_docs: List of List[str]  （比較用コーパス）
    user_doc_tokens: List[str]         （ユーザー入力文書）

    TF-IDFスコアを全体で計算し、ユーザー文書の特徴語上位 top_n を返す。
    """
    all_docs = reference_docs + [user_doc_tokens]  # 最後がユーザー文書

    # 各文書をスペース区切りにして TF-IDF ベクトル化
    texts = [" ".join(doc) for doc in all_docs]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    # ユーザー文書のTF-IDFスコア（最後の行）
    user_tfidf_vector = tfidf_matrix[-1].toarray().flatten()
    terms = vectorizer.get_feature_names_out()

    # 上位N語をTF-IDFスコア順にソートして抽出
    top_terms = sorted(
        zip(terms, user_tfidf_vector),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return [{"term": term, "score": score} for term, score in top_terms]
