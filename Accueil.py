import streamlit as st
import pandas as pd



col1, col2, col3, col4 = st.columns(4)
with col2:
    st.image("logo.png", width=400)

st.markdown("""# Application de Contrôle de Cohérence Comptable

## Description

Cette application, développée avec **Streamlit** et du code **Python**, permet d'effectuer un contrôle de cohérence sur divers documents comptables, tels que la **balance**, le **compte de résultat** et le **bilan**. Elle utilise des algorithmes spécifiques pour analyser les données et identifier les incohérences potentielles dans les écritures comptables.

## Fonctionnalités principales

- **Import de fichiers comptables :** L'application permet de charger des fichiers Excel contenant des documents comptables (balance, compte de résultat, bilan).
- **Analyse des comptes :** Le système effectue une vérification automatique des comptes selon des règles prédéfinies pour s'assurer de la cohérence des soldes et des écritures comptables.
- **Contrôle des anomalies :** Le programme détecte et signale automatiquement les incohérences telles que les écarts de soldes, les erreurs dans les écritures ou les mouvements inhabituels.
- **Génération de rapports :** À la fin de l'analyse, un rapport récapitulatif est généré, indiquant les anomalies détectées et fournissant des suggestions pour les corriger.
- **Interface intuitive :** Grâce à l'utilisation de Streamlit, l'interface est simple et interactive, permettant une navigation aisée à travers les différentes étapes du contrôle comptable.

## Documents pris en charge

- **Balance comptable**
- **Compte de résultat / prochainement**
- **Bilan / prochainement**

## Technologies utilisées

- **Python** : Pour le traitement des données et la vérification des règles de cohérence.
- **Pandas** : Pour manipuler les fichiers Excel et effectuer les analyses de données.
- **Openpyxl** : Pour la gestion des fichiers Excel.
- **Streamlit** : Pour créer une interface utilisateur simple et interactive.

## Utilisation

1. **Importer les fichiers comptables** en les chargeant via l'interface.
2. **Lancer l'analyse** : Le système analysera automatiquement les données et vérifiera les incohérences.
3. **Examiner les résultats** : Le rapport généré vous indiquera les points à corriger ou à vérifier.
4. **Télécharger le rapport** : Un fichier contenant les détails de l'analyse est disponible en téléchargement à la fin de l'opération.

## Conclusion

Cette application simplifie le processus de vérification comptable en automatisant les contrôles de cohérence, ce qui permet de gagner du temps tout en assurant la précision des documents financiers.

""")
