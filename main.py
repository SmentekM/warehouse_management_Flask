from flask import Flask, render_template, request
from klasa_manager import *

app = Flask(__name__)


def konto():
    manager.execute('wczytanie_plikow')
    return manager.konto
def magazyn():
    manager.execute('wczytanie_plikow')
    return manager.magazyn
def hist():
    manager.execute('wczytanie_plikow')
    return manager.historia


@app.route('/', methods=['POST', 'GET'])
def index():
    title = "Witaj na stronie głownej Twojej firmy"
    nazwa = str(request.form.get("nazwa"))
    ilosc = float(request.form.get("ilosc",0))
    operacja = str(request.form.get("rodzaj"))
    kwota = float(request.form.get("kwota",0))

    context = {
        "title": title,
        "saldo": konto(),
        "magazyn": magazyn(),
        # "sprzedaż": sprzedaz(konto, produkt_do_przedazy= nazwa,ilosc_do_sprzedazy=ilosc),
        # "konto": saldo( operacja=operacja, kwota=kwota),
        "zapis": manager.execute('zapisz_w_pliku')
    }
    return render_template('strona glowna.html', context=context)

@app.route('/history')
def history():
    title = "Historia operacji"
    context = {
        "title": title,
        "historia": hist()

    }
    return render_template('history.html', context=context)

