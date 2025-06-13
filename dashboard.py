import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

st.set_page_config(layout="wide")  # Grand écran

# Chargement des données
df = pd.read_csv("cleaned_data.csv")

# Création des tranches de prix si besoin
if 'tranche_prix' not in df.columns:
    df['tranche_prix'] = pd.cut(df['Price'], bins=[0,40,80,120,200,300], labels=['<40', '40-80', '80-120', '120-200', '200+'])

# Tabs/Slides
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Vue globale", "Top/Flop Produits", "Prix & Satisfaction", "Avis & Sentiment", "Nuages de mots"])

with tab1:
    st.header("Vue d'ensemble rapide")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Répartition des avis par tranche de prix")
        fig, ax = plt.subplots()
        sns.countplot(x='tranche_prix', data=df, ax=ax, palette='pastel')
        ax.set_xlabel("Tranche de prix (€)")
        ax.set_ylabel("Nombre d’avis")
        st.pyplot(fig)
    with col2:
        st.subheader("Répartition des notes")
        fig2, ax2 = plt.subplots()
        sns.countplot(x='Rating', data=df, ax=ax2, palette='Blues')
        ax2.set_xlabel("Note")
        ax2.set_ylabel("Nombre d’avis")
        st.pyplot(fig2)


with tab2:
    st.header("Top/Flop Produits")
    # Grouper par nom de catégorie produit ("Class Name")
    summary = df.groupby('Class Name').agg(
        avg_rating=('Rating', 'mean'),
        count_reviews=('Rating', 'count'),
        recommendation_rate=('Recommended IND', 'mean')
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 catégories de produits les plus vendues")
        top_vendus = summary.sort_values('count_reviews', ascending=False).head(5)
        st.bar_chart(top_vendus.set_index('Class Name')['count_reviews'])

    with col2:
        st.subheader("Top 5 catégories de produits les mieux notées (min 20 avis)")
        top_notes = summary[summary['count_reviews']>=20].sort_values('avg_rating', ascending=False).head(5)
        st.bar_chart(top_notes.set_index('Class Name')['avg_rating'])

    st.markdown("#### Bottom 5 catégories de produits les moins vendues")
    bottom_vendus = summary.sort_values('count_reviews', ascending=True).head(5)
    st.bar_chart(bottom_vendus.set_index('Class Name')['count_reviews'])

    st.markdown("#### Bottom 5 catégories de produits les moins bien notées (min 20 avis)")
    bottom_notes = summary[summary['count_reviews']>=20].sort_values('avg_rating', ascending=True).head(5)
    st.bar_chart(bottom_notes.set_index('Class Name')['avg_rating'])


with tab3:
    st.header("Prix & Satisfaction")
    fig, ax = plt.subplots()
    sns.boxplot(x='tranche_prix', y='Rating', data=df, ax=ax, palette='viridis')
    ax.set_xlabel("Tranche de prix (€)")
    ax.set_ylabel("Note")
    st.pyplot(fig)

    st.markdown("##### Analyse par catégorie de produit")
    top_cat = df['Class Name'].value_counts().head(5).index
    data_topcat = df[df['Class Name'].isin(top_cat)]
    fig2, ax2 = plt.subplots(figsize=(8,4))
    sns.boxplot(x='Class Name', y='Rating', data=data_topcat, ax=ax2, palette='Set2')
    ax2.set_xlabel("Catégorie")
    ax2.set_ylabel("Note")
    st.pyplot(fig2)


with tab4:
    st.header("Analyse des avis & du sentiment")
    if 'sentiment_label' in df.columns:
        sentiment_counts = df['sentiment_label'].value_counts(normalize=True) * 100
        st.subheader("Répartition des sentiments (%)")
        st.bar_chart(sentiment_counts)
        st.markdown("**Exemple :** " + ', '.join([f"{k}: {v:.1f}%" for k, v in sentiment_counts.items()]))
    if 'sentiment_score' in df.columns:
        st.subheader("Distribution du score de sentiment")
        fig, ax = plt.subplots()
        sns.histplot(df['sentiment_score'].dropna(), bins=30, kde=True, color="green", ax=ax)
        st.pyplot(fig)

with tab5:
    st.header("Nuage de mots des avis clients")
    text_all = ' '.join(df['Review Text'].dropna().astype(str).str.lower())
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=400).generate(text_all)
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt.gcf())
