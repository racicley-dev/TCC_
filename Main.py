import pandas as pd
from ControllerOpenAI import ControllerOpenAI
from RecomendArticle import RecomendArticle

if __name__ == "__main__":
    readed_article = '''For persons living with chronic conditions, health-related quality of life (HRQoL) symptoms, such as pain, anxiety, depression, and insomnia, often interact and mutually reinforce one another. There is evidence that medical cannabis (MC) may be efficacious in ameliorating such symptoms and improving HRQoL. As many of these HRQoL symptoms may mutually reinforce one another, we conducted an exploratory study to investigate how MC users perceive the efficacy of MC in addressing co-occurring HRQoL symptoms. We conducted a cross-sectional online survey of persons with a state medical marijuana card in Illinois (N = 367) recruited from licensed MC dispensaries across the state. We conducted tests of ANOVA to measure how perceived MC efficacy for each HRQoL symptom varied by total number of treated symptoms reported by participants. Pain was the most frequently reported HRQoL treated by MC, followed by anxiety, insomnia, and depression. A large majority of our sample (75%) reported treating two or more HRQoL symptoms. In general, perceived efficacy of MC in relieving each HRQoL symptom category increased with the number of co-occurring symptoms also treated with MC. Perceived efficacy of MC in relieving pain, anxiety, and depression varied significantly by number of total symptoms experienced. This exploratory study contributes to our understanding of how persons living with chronic conditions perceive the efficacy of MC in treating co-occurring HRQoL symptoms. Our results suggest that co-occurring pain, anxiety, and depression may be particularly amenable to treatment with MC.'''

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

    df = pd.DataFrame(articles)
    df.to_csv("OutSearchArticles.csv")

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