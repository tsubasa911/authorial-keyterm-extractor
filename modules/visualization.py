# modules/visualization.py
from io import BytesIO

def _resolve_cols(df):
    """
    言語に依存しないよう、使用カラム名を解決する。
    優先順は日本語→英語。存在しない場合は KeyError を投げる。
    """
    def pick(*candidates):
        for c in candidates:
            if c in df.columns:
                return c
        raise KeyError(f"Expected one of {candidates} in DataFrame columns: {list(df.columns)}")

    term_col   = pick("単語", "Term")
    tfidf_col  = pick("TF-IDFスコア", "TF-IDF Score")
    freq_col   = pick("頻度", "Frequency")
    pos_col    = pick("品詞", "POS")
    return term_col, tfidf_col, freq_col, pos_col


def generate_bubble_chart(df):
    """
    バブル: x=TF-IDF, y=Frequency, size=文字数, color=POS
    言語（日本語/英語）どちらのカラムでも動作する。
    """
    import plotly.express as px

    term_col, tfidf_col, freq_col, pos_col = _resolve_cols(df)

    tmp = df.copy()
    # 長さは内部専用カラムとして追加（列名を固定しない）
    tmp["_len_chars"] = tmp[term_col].astype(str).str.len()

    fig = px.scatter(
        tmp,
        x=tfidf_col,
        y=freq_col,
        size="_len_chars",
        color=pos_col,
        hover_name=term_col,
        size_max=48,
    )
    # 軽いレイアウト調整（UIは変えない：軸や凡例の存在・構成はそのまま）
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig


def generate_wordcloud(df):
    """
    Word Cloud: 重みは TF-IDF を使用。言語非依存カラム対応。
    """
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    term_col, tfidf_col, _, _ = _resolve_cols(df)

    # NaN/空文字を除外しつつ dict を作成
    freqs = {}
    for _, row in df.iterrows():
        term = str(row[term_col]).strip()
        if not term:
            continue
        try:
            score = float(row[tfidf_col])
        except Exception:
            continue
        # score<=0 は無視（必要なら）
        if score > 0:
            freqs[term] = score

    wc = WordCloud(width=1200, height=600, background_color="white")
    wc.generate_from_frequencies(freqs)

    fig = plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    return fig


def export_matplotlib_figure_to_png(fig):
    """
    matplotlib Figure -> PNG bytes
    """
    import matplotlib.pyplot as plt
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def export_plotly_figure_to_png(fig):
    """
    plotly Figure -> PNG bytes（kaleido使用）
    """
    # to_image は kaleido が必要。requirements に kaleido を含めておくこと。
    png_bytes = fig.to_image(format="png", scale=2)
    return png_bytes
