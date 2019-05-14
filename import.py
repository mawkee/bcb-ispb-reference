import csv
import codecs
import json
from collections import OrderedDict
from functools import lru_cache

import requests

url = "https://www.bcb.gov.br/pom/spb/estatistica/port/ParticipantesSTRport.csv"


@lru_cache()
def base_dict():
    ispb = OrderedDict()

    with requests.get(url, stream=True) as csvstream:
        reader = csv.DictReader(
            codecs.iterdecode(csvstream.iter_lines(), "utf-8-sig"),
            skipinitialspace=False,
        )
        for row in reader:
            ispb[row["ISPB"]] = {
                "nome": row["Nome_Reduzido"].strip(),
                "nome_extenso": row["Nome_Extenso"].strip(),
                "compe": (
                    row["Número_Código"] if row["Participa_da_Compe"] == "Sim" else None
                ),
            }
    return ispb


def compe_dict(campo):
    compe = OrderedDict()
    for row in base_dict().values():
        if row["compe"]:
            compe[row["compe"]] = row[campo]
    return compe


def gerar_json(fname, data):
    with codecs.open(fname, "w") as ispb_json:
        json.dump(data, ispb_json, ensure_ascii=False, indent=4, sort_keys=True)


def gerar_json_ispb():
    gerar_json("ispb.json", base_dict())


def gerar_json_compe():
    gerar_json("compe.json", compe_dict("nome"))


def gerar_json_compe_extenso():
    gerar_json("compe.json", compe_dict("nome_extenso"))


def gerar_compe_choices():
    gerar_json("compe_choices.json", list(compe_dict("nome_extenso").items()))


if __name__ == "__main__":
    gerar_json_ispb()
    gerar_json_compe()
    gerar_json_compe_extenso()
    gerar_compe_choices()

