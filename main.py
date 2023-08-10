from flask import Flask, render_template, request
from klasa_manager import *

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def index():
    title = "Witaj na stronie głownej Twojej firmy"
    manager.execute('wczytanie_plikow')

    # nazwa = str(request.form.get("nazwa"))
    # ilosc = float(request.form.get("ilosc",0))
    operacja = str(request.form.get("rodzaj"))
    kwota = request.form.get("kwota")
    if operacja and kwota:
        kwota=float(kwota)
        saldo(manager,operacja=operacja,kwota = kwota)
    manager.execute('zapisz_w_pliku')
    # manager.execute('saldo',1000)



    context = {
        "title": title,
        "saldo": manager.konto,
        "magazyn": manager.magazyn,
        # "sprzedaż": sprzedaz(konto, produkt_do_przedazy= nazwa,ilosc_do_sprzedazy=ilosc),
        # "konto": saldo( operacja=operacja, kwota=kwota),

    }
    return render_template('strona glowna.html', context=context)

@app.route('/history')
def history():
    title = "Historia operacji"
    context = {
        "title": title,
         "historia": manager.historia

    }
    return render_template('history.html', context=context)

