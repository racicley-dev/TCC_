import RecomendArticle

if __name__ == "__main__":
    ra = RecomendArticle('csv_buscas_unificado_ajustado_final.csv')
    articles = ra.print_recommendations_from_strings(0, 5)
    print(articles)