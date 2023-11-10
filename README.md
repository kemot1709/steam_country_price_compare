# Steam Country Price Compare
Compare Steam prices of many games between two countries

# Usage
```
python3 price_comparison.py country_from country_to [exchange_rate]
```

Country from and country to have to be in `ISO 3166-1 alpha-2` (probably) code.

```
python3 price_comparison.py UK TR
```

Exchange rate overwrites data read from ECB. It can be used eg. for countries not supported by ECB:
```
python3 price_comparison.py UK KZ 570.27
```

# Supported currencies
Support only currencies that are listed by [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

* AUD: Australian Dollar
* BGN: Bulgarian Lev
* BRL: Brazilian Real
* CAD: Canadian Dollar
* CHF: Swiss Franc
* CNY: Chinese Renminbi Yuan
* CZK: Czech Koruna
* DKK: Danish Krone
* EUR: Euro
* GBP: British Pound
* HKD: Hong Kong Dollar
* HUF: Hungarian Forint
* IDR: Indonesian Rupiah
* ILS: Israeli New Sheqel
* INR: Indian Rupee
* ISK: Icelandic Króna
* JPY: Japanese Yen
* KRW: South Korean Won
* MXN: Mexican Peso
* MYR: Malaysian Ringgit
* NOK: Norwegian Krone
* NZD: New Zealand Dollar
* PHP: Philippine Peso
* PLN: Polish Złoty
* RON: Romanian Leu
* SEK: Swedish Krona
* SGD: Singapore Dollar
* THB: Thai Baht
* TRY: Turkish Lira
* USD: United States Dollar
* ZAR: South African Rand
