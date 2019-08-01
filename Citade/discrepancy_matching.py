import mysql
import pandas as pd
from botocore.vendored import requests
from Notifications import BankNotification, HouseNotification, CompanyNotification
from Connectors import Fernergo, ArtemisNICE, LexisNexis, Infinity, Aracnis, WebKYC, KYCPortal
from Golden import standarise, render_citadel

def citadel(event, context):
    s3 = boto3.resource('s3')
    # Injest banking data 
    related_parties = pd.read_csv(s3.get('fca-techsprint-citadel-data', 'banking-data/customer_related_parties/customer_related_parties.csv'))
    six_banks = related_parties.groupby('bank_name')

    # Injest, standarised and combine Companies House data
    company_house = pd.read_csv(s3.get('fca-techsprint-citadel-data', 'uk-company-register/psc_register/psc_register.csv'))
    golden_data = Golden.standardise(company_house)

    # For each bank, encrypt then send to main dataset
    for bank in six_banks:
        golden_data = enrich_golden_data(bank, company_house)    
    try:
        res = requests.post(
            "http://bx8ocdir2g.execute-api.eu-west-1.amazonaws.com/prod/encrypt",
            params={},
            headers={"Accept":"","Content-Type":"applications/json"},
            data=customers
        )
        privatised_ubos = res['client']

        # Send privatised bank data to Citadel
        res = requests.post(
            "http://bx8ocdir2g.execute-api.eu-west-1.amazonaws.com/prod/fyn",
            params={},
            headers={"Accept":"","Content-Type":"applications/json"},
            data=privatised_ubos
        )
        
        # Citadel will check for discrepancies between new bank and CH
        golden_data = requests.post(
            "http://bx8ocdir2g.execute-api.eu-west-1.amazonaws.com/prod/banking/new",
            params={},
            headers={"Accept":"","Content-Type":"applications/json"},
            data={'new': privatised_ubos, 'existing': citadel_data}
        )
    except BaseException as e:
        raise(e)
    
    # Alert of Discrepancies
    BankNotification.send(Citadel.send_discrepancies['banks'])
    HouseNotification.send(Citadel.send_discrepancies['house'])
    CompanyNotification.send(Citadel.send_discrepancies['company'])

    # Send Discrepancies to Citadel Dashboard
    Citadel.render_citadel(discrepancies)