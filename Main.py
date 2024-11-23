from RecomendArticle import RecomendArticle
from ControllerOpenAI import ControllerOpenAI

if __name__ == "__main__":
    readed_article = '''Perceived Efficacy of Medical Cannabis in the Treatment of Co-Occurring Health-Related Quality of Life Symptoms,"For persons living with chronic conditions, health-related quality of life (HRQoL) symptoms, such as pain, anxiety, depression, and insomnia, often interact and mutually reinforce one another. There is evidence that medical cannabis (MC) may be efficacious in ameliorating such symptoms and improving HRQoL. As many of these HRQoL symptoms may mutually reinforce one another, we conducted an exploratory study to investigate how MC users perceive the efficacy of MC in addressing co-occurring HRQoL symptoms. We conducted a cross-sectional online survey of persons with a state medical marijuana card in Illinois ('''

    ra = RecomendArticle('csv_buscas_unificado_ajustado_final.csv',  readed_article)
    article_source, articles, index_near, index_futher = ra.print_recommendations_from_strings(6)
    
    print('Artigo Fonte')
    print(article_source)

    print('\nArtigos Recomendados')
    print(articles)

    print('\nIndices Próximos')
    print(index_near)

    print('\nIndices Afastados')
    print(index_futher)

    # Geração do gráfico
    controller = ControllerOpenAI()
    embeddings = [controller.get_embedding(article['abstract']) for article in articles]
    components = controller.pca_components_from_embeddings(embeddings)

    # Gera o gráfico com base nos embeddings
    labels = [f"Priority {article['article_priority']}" for article in articles]
    strings = [article['abstract'] for article in articles]
    chart = controller.chart_from_components(components, labels=labels, strings=strings)

    # Exibe o gráfico
    chart.show()