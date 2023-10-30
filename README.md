# Financial Metrics Comparison App
Fetches and sorts the requested financial metrics of public companies.

# How to Run
* Clone or download the repo and extract it.
* Populate "config.cfg" with Redis database info and FinancialModelingPrep API key
* Run "app.py"

# How to Use
* input "1" to rank stocks by metric
* input stock symbols, like "MSFT" for Microsoft, press "Enter" after each symbol
* input "0" to end the stock list
* input a valid financial metric, listed valid inputs:

    - "price"
    - "ratio quick-ratio"
    - "ratio debt-to-equity"
    - "ratio price-to-earnings"
    - "ratio price-to-book"
    - "ratio return-on-equity"
    - "ratio net-profit-margin"

* input "2" to view the trending stock
* input "3" to exit
