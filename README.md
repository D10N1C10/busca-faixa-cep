# busca-cep

## Scenario
To collect data from a website and then write the results to a file.
- Use the http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm URL;
- Get data from at least two UFs. The more, the better;
- Collect all records for each UF;
- Each record must contain at least 3 fields: "localidade", "faixa de cep" and a generated "id". Do not let duplicate records in your output file;
- The output format must be JSONL

## Prerequisites
- Python 3.x
- Geckodriver
- Firefox
- Some python libraries

## Installing

**Install the following Python libraries:**
- request2 
- pandas
- lxml
- beautfulsoup4
- selenium

With: 
``` 
pip install -r requirements.txt
```
**Geckodriver:**

[Instructions in the official repository.](https://github.com/mozilla/geckodriver/releases)

## Running the code
```
python buscacep.py
```
