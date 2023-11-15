import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv ('offres_moto.csv')

# Création de l'histogramme
df['Année'].plot(kind='hist', bins=20, edgecolor='black')
plt.title('Distribution des années de production')
plt.xlabel('Année')
plt.ylabel('Fréquence')
plt.show()