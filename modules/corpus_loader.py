import os
from modules.preprocessing import preprocess_text

def load_and_preprocess_corpus(corpus_dir="corpus"):
    """
    corpus_dir内のすべての.txtファイルを読み込み、前処理（lemmatizationなど）を実施。
    各文書を「lemmaのリスト」として返す。

    Returns:
        List[List[str]]: 例 [['cnn', 'image', 'classification'], ['deep', 'learning', 'model', ...], ...]
    """
    corpus_docs = []

    for filename in os.listdir(corpus_dir):
        if filename.endswith(".txt"):
            path = os.path.join(corpus_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                tokens = preprocess_text(text)
                lemmas = [token["lemma"] for token in tokens]
                corpus_docs.append(lemmas)

    return corpus_docs
