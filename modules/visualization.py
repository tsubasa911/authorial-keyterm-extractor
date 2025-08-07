import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

def generate_bubble_chart(df: pd.DataFrame):
    """
    TF-IDFスコア、頻度、文字数、品詞に基づくバブルチャートを生成。
    dfには以下の列が必要: ['単語', 'TF-IDFスコア', '頻度', '品詞']
    """
    df = df.copy()
    df["文字数"] = df["単語"].apply(len)

    fig = px.scatter(
        df,
        x="TF-IDFスコア",
        y="頻度",
        size="文字数",
        color="品詞",
        hover_name="単語",
        size_max=40,
        title="バブルチャート：特徴語の可視化",
    )
    return fig


# modules/visualization.py に追加

def generate_wordcloud(df):
    """
    TF-IDFスコアに基づくワードクラウド画像を返す。
    df: '単語' と 'TF-IDFスコア' を含む DataFrame
    """
    tfidf_dict = dict(zip(df["単語"], df["TF-IDFスコア"]))

    # ワードクラウド生成
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="Dark2"
    ).generate_from_frequencies(tfidf_dict)

    # matplotlibのFigureを返す
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig

def export_matplotlib_figure_to_png(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return buf

def export_plotly_figure_to_png(fig):
    buf = BytesIO()
    fig.write_image(buf, format="png", engine="kaleido")
    buf.seek(0)
    return buf
