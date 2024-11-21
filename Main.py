from RecomendArticle import RecomendArticle

if __name__ == "__main__":
    ra = RecomendArticle('csv_buscas_unificado_ajustado_final.csv')
    article_source, articles, index_near, index_futher = ra.print_recommendations_from_strings(0, 5)
    
    print('Artigo Fonte')
    print(article_source)

    print('\nArtigos Recomendados')
    print(articles)

    print('\nIndices Próximos')
    print(index_near)

    print('\nIndices Afastados')
    print(index_futher)