import streamlit as st
from PyPDF2 import PdfReader
import re

def extract_issuer_name(text):
    patterns = {
        "pattern 1" : r"Issuer\s*(?:Name)?\s*:\s*(.*)",
        "pattern 2" : r"(?m)^Issuer\s*$\n^(.*)",
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            issuer_name = match.group(1)
            break
        else:
            issuer_name = "Not located"

    return issuer_name

def extract_cusip(text):
    pattern = pattern = r"\bCUSIP\b.*?\b([A-Za-z0-9]{9})\b"

    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        cusip = match.group(1)
    else:
        cusip = "Not located"

    return cusip

def extract_cusip_isin(text):
    pattern = r"CUSIP\s*/\s*ISIN\s*:\s*(\w+)\s*/\s*(\w+)"
    match = re.search(pattern,text,flags=re.IGNORECASE)
    if match:
        cusip = match.group(1)
        isin = match.group(2)
    else:
        cusip = "not located"
        isin = "not located"

    return cusip, isin

def extract_ccy(text):

    ccy_map = {
        "$" : "USD",
        "USD":"USD",
        "U.S. Dollars" : "USD",
        "Not located" : "Not located",
    }

    patterns = {
        "pattern 1": r"currency\s*:\s*(.*)",
        "pattern 2": r"(?m)currency\s*\n^(.*)",
        "pattern 3": r"(\$)",
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            ccy = match.group(1)
            break
        else:
            ccy = "Not located"

    return ccy_map[ccy.strip()]

def extract_note_ccy(text):
    patterns = {
        "pattern 3": r"Issue Date of the notes:\s*(\w+\$?)(\d{1,3}(?:,\d{3})*(?:\.\d+)?)",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            note_ccy = match.group(1)
            break
        else:
            note_ccy = "Not located"

    return note_ccy

def extract_trade_date(text):

    patterns = {
        "pattern 1": r"Trade date\s*:\s*(.*)",
        "pattern 2": r"(?m)Trade date\s*\n^(.*)",
        "pattern 3": r"\bTrade\b\s+\w+:(?:\*)?\s*(.*)"
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            trade_date = match.group(1)
            break
        else:
            trade_date = "Not located"

    return trade_date

def extract_valuation_date(text):

    patterns = {
        "pattern 1": r"Valuation date\s*:\s*(.*)",
        "pattern 2": r"(?m)Valuation date\s*\n^(.*)",
        "pattern 3": r"\bValuation\b\s+\w+:(?:\*)?\s*(.*)"
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            valuation_date = match.group(1)
            break
        else:
            valuation_date = "Not located"

    return valuation_date

def extract_issue_date(text):

    patterns = {
        "pattern 1": r"Issue date\s*:\s*(.*)",
        "pattern 2": r"(?m)Issue date\s*\n*^(.*)",
        "pattern 3": r"\bIssue\b\s+\w+:\s*(.*)",
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            issue_date = match.group(1)
            break
        else:
            issue_date = "Not located"

    #Check if the issue_date contains other text that we want to ignore
    pattern = r"\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b"
    match = re.search(pattern,issue_date)

    if match:
        issue_date = match.group(1)

    return issue_date

def extract_barrier(text):

    patterns = {
        "pattern 1": r"barrier\s*:\s*(.*)",
        "pattern 2": r"\bbarrier\b\s+\w+:\s*(.*)",
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            barrier = match.group(1)
            break
        else:
            barrier = "Not located"

    pattern = r'(\d{1,2}.?\d{1,2}?%)'
    match = re.search(pattern, barrier, flags=re.IGNORECASE)

    if match:
        barrier = match.group(1)

    return barrier

def extract_trigger_level(text):

    patterns = {
        "pattern 1": r"Trigger Level\s*:\s*(.*)",
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            trigger_level = match.group(1)
            break
        else:
            trigger_level = "Not located"

    return trigger_level

def extract_interest_commence_date(text):
    patterns = {
        "pattern 1": r"Interest commencement date:(.*)"
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            interest_commence_date = match.group(1)
            break
        else:
            interest_commence_date = "Not located"

    return interest_commence_date

def extract_coupon(text):

    patterns = {
        "pattern 1": r"coupon\s*:\s*(?:\w*\s*\n*)*(\d{1,2}.?\d{1,2}?%)",
        "pattern 2": r"\bCoupon\b\s*:\w+\s*(\d{1,2}.?\d{1,2}?%)",
        "pattern 3": r"\bCoupon\b\s*(\w+\s*):\s*\w+\s*(\d{1,2}.?\d{1,2}?%)",
        "pattern 4": r"\bFixed coupon[a-z]\b\s*(?:\n.*)+\n(.*)%/s*/n*$",
        "pattern 5": r"(\w{1,2}.?\w{1,2,3,4}?%)",
        "pattern 6": r"Interest Rate:(.*)"
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            coupon = match.group(1)
            print(pattern_name)
            break
        else:
            coupon = "Not located"

    return coupon


def extract_maturity_date(text):

    patterns = {
        "pattern 1": r"Maturity date\s*:\s*(.*)",
        "pattern 2": r"(?m)Maturity date\s*\n^(.*)",
        "pattern 3": r"\bMaturity\b\s+\w+:(?:\*)?\s*(.*)"
    }

    for patter_name, pattern in patterns.items():
        match = re.search(pattern, text,flags=re.IGNORECASE)
        if match:
            maturity_date = match.group(1)
            break
        else:
            maturity_date = "Not located"

    #Check if the issue_date contains other text that we want to ignore
    pattern = r"\b(\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})\b"
    match = re.search(pattern,maturity_date)

    if match:
        maturity_date = match.group(1)

    return maturity_date
def extract_denomination(text):
    pattern_1 = r"denominations?\s*:?\s*(?:USD\s+)?\$?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)"
    pattern_2 = r"denominations?\s*:\s*(.*)"

    match1 = re.search(pattern_1,text,flags=re.IGNORECASE)
    match2 = re.search(pattern_2,text,flags=re.IGNORECASE)

    if match1:
        denomination = match1.group(1)
    elif match2:
        denomination = match2.group(1)
        # check if a value needs to be extracted
        pattern = r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)"
        match = re.search(pattern,denomination)
        if match:
            denomination = match.group(1)
    else:
        denomination = "not located"

    return denomination

def extract_principal(text):

    patterns = {
        "pattern 1": r"Issue Date of the note\s*s:\s*(\w+\$?(\d{1,3}(?:,\d{3})*(?:\.\d+)?))",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            principal = match.group(1)
            break
        else:
            principal = "Not located"

    return principal
def extract_note_type(text):

    patterns = {
        "pattern 1": r"Type of notes\s*:?(.*)",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            note_type = match.group(1)
            break
        else:
            note_type = "Not located"

    return note_type

def extract_clearing_system(text):

    patterns = {
        "pattern 1": r"Clearing System\s*:?(.*)",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            clearing_system = match.group(1)
            break
        else:
            clearing_system = "Not located"

    return clearing_system

def extract_day_count(text):

    patterns = {
        "pattern 1": r"Day Count Fraction\s*:?(.*)",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            day_count_fraction = match.group(1)
            break
        else:
            day_count_fraction = "Not located"

    return day_count_fraction

def extract_stablising_manager(text):

    patterns = {
        "pattern 1": r"Stabilisation Manager\s*:?(.*)",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            stabilisation_manager = match.group(1)
            break
        else:
            stabilisation_manager = "Not located"

    return stabilisation_manager
def extract_calculation_agent(text):

    patterns = {
        "pattern 1": r"Calculation Agent\s*:?(.*)",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            calc_agent = match.group(1)
            break
        else:
            calc_agent = "Not located"

    return calc_agent

def extract_issue_price(text):

    patterns = {
        "pattern 1": r"Issue Price\s*:?\s*(\d+\.\d+)\s*%",
    }

    for pattern_name, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            issue_price = match.group(1)+"%"
            break
        else:
            issue_price = "Not located"

    return issue_price

def extract_isin(text):
    pattern = pattern = r"ISIN\s*:?\s*([A-Za-z0-9]{9,12})"
    match = re.search(pattern, text,flags=re.IGNORECASE)
    if match:
        isin = match.group(1)
    else:
        isin = "Not located"

    return isin

def extract_common_code(text):
    pattern = pattern = r"Common Code\s*:?(.*)"
    match = re.search(pattern, text,flags=re.IGNORECASE)
    if match:
        common_code = match.group(1)
    else:
        common_code = "Not located"

    return common_code

def extract_listing_venue(text):
    pattern = pattern = r"Listed\s*:?(.*)"
    match = re.search(pattern, text,flags=re.IGNORECASE)
    if match:
        listing_venue = match.group(1)
    else:
        listing_venue = "Not located"

    return listing_venue

def extract_call_option(text):
    pattern = r"Call Option.*?:\s*(.*?)\n"
    match = re.search(pattern, text,flags=re.DOTALL)
    if match:
        call_option = match.group(1)
    else:
        call_option = "Not located"

    return call_option

def extract_put_option(text):
    pattern = r"Put option.*?:\s*(.*?)\n"
    match = re.search(pattern, text,flags=re.DOTALL)
    if match:
        put_option = match.group(1)
    else:
        put_option = "Not located"

    return put_option

def extract_text_from_pdf(text,st):

    issuer_name = extract_issuer_name(text)
    st.write("Issuer: ",issuer_name)

    isin = extract_isin(text)
    st.write("ISIN: ",isin)
    common_code = extract_common_code(text)
    st.write("Common Code: ", common_code)
    denomination = extract_denomination(text)
    st.write("Denomination: ",denomination)
    principal = extract_principal(text)
    st.write("Principal: ", principal)
    note_type = extract_note_type(text)
    st.write("Note Type: ", note_type)
    issue_price = extract_issue_price(text)
    st.write("Issue Price: ", issue_price)
    note_ccy = extract_note_ccy(text)
    st.write("Currency: ",note_ccy)
    coupon = extract_coupon(text)
    st.write("Coupon: ", coupon)
    trade_date = extract_trade_date(text)
    st.write("Trade Date: ",trade_date)
    issue_date = extract_issue_date(text)
    st.write("Issue Date: ",issue_date)
    maturity_date = extract_maturity_date(text)
    st.write("Maturity Date: ",maturity_date)
    call_option = extract_call_option(text)
    st.write("Call Option: ", call_option)
    put_option = extract_put_option(text)
    st.write("Put Option: ", put_option)
    interest_commence_date = extract_maturity_date(text)
    st.write("Interest Commence: ", interest_commence_date)
    day_count_fraction = extract_day_count(text)
    st.write("Day Count Fraction: ", day_count_fraction)
    calc_agent = extract_calculation_agent(text)
    st.write("Calculation Agent: ", calc_agent)
    stablising_manager = extract_stablising_manager(text)
    st.write("Stablising Manager: ", stablising_manager)
    listing_venue = extract_listing_venue(text)
    st.write("Listing Venue: ", listing_venue)
    clearing_system = extract_clearing_system(text)
    st.write("Clearing System:", clearing_system)

    return text

def main():
    st.set_page_config(page_title="Extract Data from Term Sheet")
    st.image("https://i.ibb.co/FKSBzFh/Marketnode-Logo.png", width=400)
    st.header("Extract data from Term Sheet")

    # upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        result_df = []
        print(text)
        extracted_text = extract_text_from_pdf(text,st)



if __name__ == '__main__':
    main()
