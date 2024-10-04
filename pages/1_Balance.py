# import des librairies
import streamlit as st
import pandas as pd
import numpy as np



def verifier_coherence(balance_df):

    def reserves_legales(balance_df):
        # Filtrer les comptes commençant par 1013 (capital versé) et 1061 (réserve légale)
        comptes_capital = balance_df[balance_df['compte'].astype(str).str.startswith('1013')]
        comptes_reserve = balance_df[balance_df['compte'].astype(str).str.startswith('1061')]

        # Vérification de la présence de comptes 1013 et 1061
        if not comptes_capital.empty and not comptes_reserve.empty:
            # Calculer la somme du capital versé et de la réserve légale
            capital_verse = comptes_capital['crédit'].sum()
            reserve_legale = comptes_reserve['crédit'].sum()

            # Comparer si la réserve légale dépasse 10% du capital versé
            if reserve_legale > (0.10 * capital_verse):
                st.write("Vérifier le montant de la réserve légale")
                st.write(f"Montant du capital versé : {capital_verse}, Montant de la réserve légale : {reserve_legale}")
                st.markdown("[Référence législative](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006229005)")
                st.write("---")
                       

    def perte_exercice(balance_df):
        # Vérifier si le compte 129000 existe avant d'accéder à sa valeur
        if 129000 in balance_df['compte'].values:
            perte = balance_df.loc[balance_df['compte'] == 129000, 'crédit'].values[0]
            if not np.isnan(perte):
                st.write("Le compte RESULTAT DE L'EXERCICE (PERTE) ne peut pas être créditeur")
                st.write(f"Montant au crédit du compte 129000 : {perte}")
                st.write("---")

    def gain_exercice(balance_df):
        # Vérifier si le compte 120000 existe avant d'accéder à sa valeur
        if 120000 in balance_df['compte'].values:
            gain = balance_df.loc[balance_df['compte'] == 120000, 'débit'].values[0]
            if not np.isnan(gain):
                st.write("Le compte RESULTAT DE L'EXERCICE (GAIN) ne peut pas être débiteur")
                st.write(f"Montant au crédit du compte 120000 : {gain}")
                st.write("---")

    def dotations(balance_df):
        # Vérifier la présence de comptes commençant par "21"
        comptes_21 = balance_df[balance_df['compte'].astype(str).str.startswith('21')]
    
        if not comptes_21.empty:
            # Si des comptes "21" sont présents, vérifier la présence de comptes commençant par "681"
            comptes_681 = balance_df[balance_df['compte'].astype(str).str.startswith('681')]
            
            if comptes_681.empty:
                # Si des comptes "681" ne sont pas présents
                st.write("Des comptes commençant par 21 sont présents, mais aucun compte commençant par 681.")
                st.write("---")

    def check_reserves_balance(balance_df):
        """
        Vérifier si (101 + 110 - 118 + 1068 + 120 - 129999) < 50% du solde du compte 101
        Les capitaux propres représentent moins de 50% du capital social
        """
                
        # Filtrer pour les comptes pertinents et calculer les sommes
        total_debit = balance_df.loc[balance_df['compte'].str.startswith(('101', '106', '120', '129000')), 'débit'].sum(min_count=1)
        total_credit_129999 = balance_df.loc[balance_df['compte'] == '129999', 'crédit'].sum(min_count=1)
        
        # Calculer la somme requise
        result_sum = total_debit - total_credit_129999

        # Obtenir le crédit des comptes commençant par 101
        total_credit_101 = balance_df.loc[balance_df['compte'].str.startswith('101'), 'crédit'].sum(min_count=1)
        
        # Comparer avec 50 % du crédit du compte 101
        if result_sum >= 0.5 * total_credit_101:
            st.write( "Attention, les capitaux propres représentent moins de 50 % du capital social")
            st.markdown("[Référence législative](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047292156)")
            st.write("---")

    def check_credit_n1_and_mouvements_debit(balance_df):
        '''
        Non affectation ou non extourne du résultat
        Le résultat de l'exercice précédent figure toujours dans la balance
        '''
        # Filtrer les comptes commençant par 120
        compte_120 = balance_df.loc[balance_df['compte'].str.startswith('120')]
        
        # Vérifier la présence d'un montant dans 'crédit_n-1'
        if not compte_120['crédit_n-1'].isna().all():
            # Vérifier la présence d'un montant dans 'mouvements_débit'
            if compte_120['mouvements_débit'].isna().all():
                st.write("Le résultat de l'exercice ne semble pas avoir été affecté")
                st.write("---")

    def check_provision_conges_payes(balance_df):
        """
        Cette fonction vérifie si un compte commençant par 6411 avec un montant dans la colonne 'débit' est présent,
        et si un compte commençant par 64112 avec un montant dans la colonne 'débit' existe également.
        Si ce n'est pas le cas, elle renvoie un message indiquant que la provision pour congés payés n'a pas été constatée.
        """
        
        # Filtrer pour les comptes commençant par 6411 avec un montant dans la colonne 'débit'
        compte_6411 = balance_df.loc[balance_df['compte'].str.startswith('6411') & balance_df['débit'].notna()]
        
        # Filtrer pour les comptes commençant par 64112 avec un montant dans la colonne 'débit'
        compte_6412 = balance_df.loc[balance_df['compte'].str.startswith('6412') & balance_df['débit'].notna()]
        
        # Vérifier si le compte 6411 est présent sans correspondance avec 64112
        if not compte_6411.empty and compte_6412.empty:
            st.write("La provision pour congés payés ne semble pas avoir été constatée.")
            st.markdown("[Comment calculer la provision pour congés payés](https://www.compta-facile.com/comptabilisation-de-la-provision-pour-conges-payes/)")
            st.write("---")

    def subventions_investissement(balance_df):
        '''
        Contrôle de la présence de la quote part de subbention virée au résultat

        '''

        # Vérification de la présence d'un compte commençant par 131 avec un montant au débit
        account_131_exists = balance_df[(balance_df['compte'].str.startswith('131')) & (balance_df['crédit'].notna())]

        # Vérification de la présence d'un compte commençant par 777 avec un montant au crédit
        account_777_exists = balance_df[(balance_df['compte'].str.startswith('777')) & (balance_df['crédit'].notna())]

        # Logique pour déterminer le message de sortie
        if not account_131_exists.empty and account_777_exists.empty:
            message = "Il existe une subvention d'investissement et il n'y a pas la présence de la quote-part de subvention virée au compte de résultat inscrite au compte 777."
        
            st.write(message)
            st.write("---")

    def check_provisions_balance(balance_df):
        """
        Cette fonction vérifie la présence de comptes commençant par 15 avec un montant dans la colonne 'crédit'.
        Si aucun compte n'est trouvé, elle renvoie un message d'alerte concernant l'absence de provisions.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer pour les comptes commençant par 15 avec un montant dans la colonne 'crédit'
        comptes_15_credit = balance_df.loc[balance_df['compte'].str.startswith('15') & balance_df['crédit'].notna()]
        
        # Vérifier si des comptes 15 avec des montants au crédit sont présents
        if comptes_15_credit.empty:
            st.write( """\n Il n'y a pas de provisions inscrites au bilan. Assurez-vous auprès du client qu'il n'y a pas de :\n
        - Provisions pour risques,\n
        - Provisions pour pensions et obligations similaires,\n 
        - Provisions pour restructurations,\n 
        - Provisions pour impôt,\n 
        - Provisions pour renouvellement des immobilisations,\n 
        - Provisions pour charges à répartir sur plusieurs exercices.""")
            st.write("---")

    def check_emprunts_et_interets(balance_df):
        """
        Cette fonction vérifie si un compte commençant par 164 est présent dans la colonne 'crédit'.
        Si oui, elle vérifie également la présence des comptes commençant par 6616 avec un montant dans la colonne 'débit'.
        Si aucun compte commençant par 6616 n'est trouvé, elle affiche un message d'avertissement concernant les intérêts non comptabilisés.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer pour les comptes commençant par 164 avec un montant dans la colonne 'crédit'
        comptes_164_credit = balance_df.loc[balance_df['compte'].str.startswith('164') & balance_df['crédit'].notna()]
        
        # Si le compte 164 est trouvé, vérifier la présence des comptes commençant par 6616 avec un montant au débit
        if not comptes_164_credit.empty:
            comptes_6616_debit = balance_df.loc[balance_df['compte'].str.startswith('6616') & balance_df['débit'].notna()]
            
            # Si aucun compte commençant par 6616 n'est trouvé avec un montant au débit, afficher un avertissement
            if comptes_6616_debit.empty:
                st.write("Attention, l'entreprise a des emprunts et les intérêts ne sont pas comptabilisés.")
                st.write("---")

    def check_amortissements_incorporels(balance_df):
        """
        Cette fonction vérifie si un compte commençant par 20 avec un montant au crédit est présent.
        Si oui, elle vérifie également la présence d'un compte commençant par 6811.
        Si le compte 6811 n'est pas trouvé, elle renvoie un message d'avertissement concernant l'absence de dotation aux amortissements incorporels.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer pour les comptes commençant par 20 avec un montant au crédit
        comptes_20_credit = balance_df.loc[balance_df['compte'].str.startswith('20') & balance_df['débit'].notna()]
        
        # Si le compte 20 est trouvé, vérifier la présence du compte commençant par 6811
        if not comptes_20_credit.empty:
            compte_68111 = balance_df.loc[balance_df['compte'].str.startswith('68111') & balance_df['débit'].notna()]
            
            # Si le compte 6811 n'est pas trouvé, afficher un avertissement
            if compte_68111.empty:
                st.write("Il y a des amortissements incorporels. Aucune dotation aux amortissements incorporels n'a été constatée.")
                st.write("---")

    def variation_stock(balance_df):
        """
        Cette fonction vérifie si la variation de stock a été comptabilisée pour les comptes commençant par '37'.
        Si le montant du 'débit_n-1' est égal au montant du 'débit', un message est généré.
        """
        
        # Assurer que les colonnes 'débit_n-1' et 'débit' sont bien au format numérique
        balance_df['débit_n-1'] = pd.to_numeric(balance_df['débit_n-1'], errors='coerce')
        balance_df['débit'] = pd.to_numeric(balance_df['débit'], errors='coerce')

        # Filtrer les comptes commençant par '37'
        accounts_37 = balance_df[balance_df['compte'].str.startswith('37')]

        # Parcours des lignes et vérification
        messages = []
        for index, row in accounts_37.iterrows():
            # Comparer avec une tolérance pour éviter les petits écarts numériques
            if pd.notna(row['débit_n-1']) and pd.notna(row['débit']) and (row['débit_n-1'] == row['débit']):
                message = "Il semble que la variation de stock n'ait pas été comptabilisée pour le compte {}.".format(row['compte'])
                messages.append(message)
        
        # Afficher les messages à la fin
        if messages:
            for message in messages:
                st.write(message)
            st.write("---")

    def fournisseur_debiteur(balance_df):
        # Vérification des comptes commençant par 401 qui ont une valeur dans la colonne 'débit'
        accounts_401_debit = balance_df[(balance_df['compte'].str.startswith('401')) & (balance_df['débit'].notna())]

        # Si des comptes sont trouvés, afficher le message
        if not accounts_401_debit.empty:
            st.write("Un compte fournisseur est débiteur.")
            st.write("---")

    def check_mouvements_comptes_attente(balance_df):
        """
        Cette fonction vérifie la présence de mouvements dans les comptes commençant par 47,
        soit dans la colonne 'mouvements_débit' ou 'mouvements_crédit'.
        Si des mouvements sont présents, un message est affiché.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer les comptes commençant par '47'
        comptes_47 = balance_df[balance_df['compte'].str.startswith('47')]
        
        # Vérifier s'il y a des mouvements dans 'mouvements_débit' ou 'mouvements_crédit'
        comptes_47_mouvements = comptes_47[(comptes_47['mouvements_débit'].notna()) | (comptes_47['mouvements_crédit'].notna())]
        
        # Si des mouvements sont trouvés, afficher un message
        if not comptes_47_mouvements.empty:
            st.write("Il y a des mouvements dans les comptes d'attente (47..).")
            st.write("---")

    def check_compte_4456_4457(balance_df):
        """
        Cette fonction vérifie qu'il n'y a pas de compte commençant par 44566 ou 44571
        dans les colonnes 'débit' ou 'crédit'.
        Si un tel compte est trouvé, un message d'avertissement est affiché.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer pour les comptes commençant par 4456 ou 4457 dans les colonnes 'débit' ou 'crédit'
        comptes_4456_4457 = balance_df[(balance_df['compte'].str.startswith('4456') | balance_df['compte'].str.startswith('4457')) &
                                        ((balance_df['débit'].notna()) | (balance_df['crédit'].notna()))]
        
        # Vérifier si des comptes sont trouvés
        if not comptes_4456_4457.empty:
            st.write("Attention : des comptes de TVA hors TVA à payer 44551 ne sont pas soldés")
            st.write("---")

    def check_comptes_45_debit(balance_df):
        """
        Cette fonction vérifie qu'il n'y a pas de montant dans la colonne 'débit' pour les comptes commençant par 45.
        Si un montant est trouvé, un message d'avertissement est affiché.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer pour les comptes commençant par 45 avec un montant dans la colonne 'débit'
        comptes_45_debit = balance_df[balance_df['compte'].str.startswith('45') & balance_df['débit'].notna()]
        
        # Vérifier si des comptes sont trouvés
        if not comptes_45_debit.empty:
            st.write("Un ou plusieurs comptes courants d'associés sont débiteurs.")
            st.write("---")

    def check_comptes_486_debit(balance_df):
        """
        Cette fonction vérifie la présence d'un montant dans la colonne 'débit' pour les comptes commençant par 486.
        Si un montant est trouvé, un message est affiché.
        """
        
        # Convertir les comptes en chaînes de caractères au cas où
        balance_df['compte'] = balance_df['compte'].astype(str)
        
        # Filtrer pour les comptes commençant par 486 avec un montant dans la colonne 'débit'
        comptes_486_debit = balance_df[balance_df['compte'].str.startswith('486') & balance_df['débit'].notna()]
        
        # Vérifier si des comptes sont trouvés
        if comptes_486_debit.empty:
            st.write("Il n'y a pas de charges constatées d'avance enregistrées en comptabilité")
            st.write("---")
        

      
        
        
        
         
              
        
            
        
        
        

    # Appel des fonctions internes pour vérifier la cohérence
    reserves_legales(balance_df)
    perte_exercice(balance_df)
    gain_exercice(balance_df)
    dotations(balance_df)
    check_reserves_balance(balance_df)
    check_credit_n1_and_mouvements_debit(balance_df)
    check_provision_conges_payes(balance_df)
    subventions_investissement(balance_df)
    check_provisions_balance(balance_df)
    check_emprunts_et_interets(balance_df)
    check_amortissements_incorporels(balance_df)
    variation_stock(balance_df)
    fournisseur_debiteur(balance_df)
    check_mouvements_comptes_attente(balance_df)
    check_compte_4456_4457(balance_df)
    check_comptes_45_debit(balance_df)
    check_comptes_486_debit(balance_df)


# Interface Streamlit

col1, col2, col3, col4 = st.columns(4)
with col2:
    st.image("logo.png", width=400)

st.title("Contrôle de la cohérence de la balance après opérations d'inventaire")
uploaded_file = st.file_uploader("Téléchargez la balance au format XLSX", type="xlsx")

st.markdown("""La balance au format `.xlsx` doit être extraite de **Odoo** en sélectionnant **"Tout déplier"** dans les options."""
)

if uploaded_file is not None:
    balance_df = pd.read_excel(uploaded_file)
    balance_df.columns=['compte','libelle','débit_n-1', 'crédit_n-1','mouvements_débit','mouvements_crédit','débit',"crédit"]
    balance_df = balance_df.dropna(subset=['compte'])
    balance_df['compte'] = balance_df['compte'].astype(int)
    balance_df['débit'] = pd.to_numeric(balance_df['débit'], errors='coerce')
    balance_df['crédit'] = pd.to_numeric(balance_df['crédit'], errors='coerce')
    balance_df['compte'] = balance_df['compte'].astype(str)
    balance_df.replace(0, np.nan, inplace=True)

    # Vérification de la cohérence
    verifier_coherence(balance_df)

else:
    st.write("Merci de charger la balance...")
