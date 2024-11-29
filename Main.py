import pandas as pd
from ControllerOpenAI import ControllerOpenAI
from RecomendArticle import RecomendArticle

if __name__ == "__main__":
    #Cannabis
    #readed_article = '''For persons living with chronic conditions, health-related quality of life (HRQoL) symptoms, such as pain, anxiety, depression, and insomnia, often interact and mutually reinforce one another. There is evidence that medical cannabis (MC) may be efficacious in ameliorating such symptoms and improving HRQoL. As many of these HRQoL symptoms may mutually reinforce one another, we conducted an exploratory study to investigate how MC users perceive the efficacy of MC in addressing co-occurring HRQoL symptoms. We conducted a cross-sectional online survey of persons with a state medical marijuana card in Illinois (N = 367) recruited from licensed MC dispensaries across the state. We conducted tests of ANOVA to measure how perceived MC efficacy for each HRQoL symptom varied by total number of treated symptoms reported by participants. Pain was the most frequently reported HRQoL treated by MC, followed by anxiety, insomnia, and depression. A large majority of our sample (75%) reported treating two or more HRQoL symptoms. In general, perceived efficacy of MC in relieving each HRQoL symptom category increased with the number of co-occurring symptoms also treated with MC. Perceived efficacy of MC in relieving pain, anxiety, and depression varied significantly by number of total symptoms experienced. This exploratory study contributes to our understanding of how persons living with chronic conditions perceive the efficacy of MC in treating co-occurring HRQoL symptoms. Our results suggest that co-occurring pain, anxiety, and depression may be particularly amenable to treatment with MC.'''

    #HIV
    readed_article = '''Pre-exposure prophylaxis (PrEP) persistence is suboptimal in the United States. In the Deep South, a region with high rates of new HIV diagnosis, patterns of PrEP discontinuation remain unexplored. We evaluated data from a clinic-based PrEP program in Jackson, Mississippi and included patients initiating PrEP between August 2018 and April 2021. We considered patients to have a gap in PrEP coverage if they had at least 30 days without an active PrEP prescription; those who restarted PrEP after 30 days were classified as 'stopped and restarted' and those who never obtained a new PrEP prescription were classified as 'stopped and did not restart'. Patients without a gap in coverage were considered 'continuously on PrEP'. We estimated median time to first PrEP discontinuation and examined factors associated with time to first PrEP discontinuation. Of 171 patients who received an initial 90-day PrEP prescription; 75% were assigned male at birth and 74% identified as Black. The median time to first discontinuation was 90 days (95% CI 90-114). Twenty-two percent were continuously on PrEP, 28% stopped and restarted (median time off PrEP = 102 days), and 50% stopped and did not restart. Associations with early PrEP stoppage were notable for patients assigned sex female vs male (adjusted hazard ratio [aHR] = 1.6, 95% CI 1.0-2.5) and those living over 25 miles from clinic vs. 0-10 miles (aHR 1.89, 95% CI 1.2-3.0). Most patients never refilled an initial PrEP prescription though many patients re-started PrEP. Interventions to improve persistence and facilitate re-starts are needed.'''


    ra = RecomendArticle('csv_buscas_unificado_ajustado_final.csv',  readed_article)
    article_source, articles, index_near, index_futher, embeddings = ra.print_recommendations_from_strings(6)
    
    print('Artigo Fonte')
    print(article_source)

    print('\nArtigos Recomendados')
    print(articles)

    #print('\nIndices Próximos')
    #print(index_near)

    #print('\nIndices Afastados')
    #print(index_futher)

    print("Embbedings")
    print(embeddings)

    #df = pd.DataFrame(articles)
    #df.to_csv("OutSearchArticles2.csv")

    # Geração do gráfico
    controller = ControllerOpenAI()
    #embeddings = [controller.get_embedding(article['abstract']) for article in articles]
    components = controller.pca_components_from_embeddings(embeddings)

    # Gera o gráfico com base nos embeddings
    labels = [f"Priority {article['article_priority']}" for article in articles]
    strings = [article['abstract'] for article in articles]
    chart = controller.chart_from_components(components, labels=labels, strings=strings)

    # Exibe o gráfico
    chart.show()