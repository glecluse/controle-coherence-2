import streamlit as st
import pandas as pd
import openai



col1, col2, col3, col4 = st.columns(4)
with col2:
    st.image("logo.png", width=400)

st.markdown("""# Application de contrôle comptable avec intelligence artificielle

Bienvenue dans notre application de contrôle comptable utilisant l'intelligence artificielle, développée spécifiquement pour automatiser et améliorer l'analyse de vos documents comptables.

## Objectif de l'application
En tant qu'expert-comptable, nous comprenons l'importance d'une vérification rapide et précise des données financières. C'est pourquoi cette application a été conçue pour intégrer les technologies d'IA, facilitant ainsi le contrôle de vos balances comptables et de vos recommandations financières.

### Fonctionnalités principales
- **Analyse des balances comptables** : L'application compare vos données avec des recommandations spécifiques pour détecter les incohérences.
- **Contrôle intelligent** : Grâce à l'intelligence artificielle, vous pouvez interroger directement vos documents comptables et obtenir des suggestions d'optimisation ou des alertes en cas de non-conformité.
- **Automatisation** : Gagnez du temps en automatisant le contrôle de vos données financières, vous permettant ainsi de vous concentrer sur l'essentiel : conseiller vos clients.

### Pourquoi intégrer l'IA ?
L'intelligence artificielle permet d'améliorer la précision et la rapidité des contrôles, tout en réduisant les risques d'erreurs humaines. Avec cette application, vous bénéficiez d'une technologie de pointe pour garantir une gestion comptable conforme et optimisée.

---

**Notre objectif** : vous fournir un outil performant, simple d'utilisation, et aligné avec vos besoins en tant que professionnel de la comptabilité.

L'application a été développée par Geoffrey. N'hésitez pas à le solliciter pour toute demande de modification : geoffrey@lpde.com
""")
