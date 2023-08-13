from flask import Flask, render_template, request,url_for, redirect
from klasa_manager import *

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def index():
    title = "Witaj na stronie głownej Twojej firmy"
    manager.execute('wczytanie_plikow')

    nazwa = str(request.form.get("nazwa"))
    ilosc_do_sprzedazy = request.form.get("ilosc")
    operacja = str(request.form.get("rodzaj"))
    kwota = request.form.get("kwota")
    nazwa_produktu = request.form.get('nazwa_zakupu')
    ilosc_do_zakupu = request.form.get('ilosc_zakupiona')
    cena = request.form.get('cena')
    if operacja and kwota:
        kwota=float(kwota)
        saldo(manager, operacja=operacja, kwota=kwota)

    if nazwa and ilosc_do_sprzedazy:
        ilosc_do_sprzedazy = float(ilosc_do_sprzedazy)
        sprzedaz(manager,produkt_do_przedazy=nazwa, ilosc_do_sprzedazy=ilosc_do_sprzedazy)
    if nazwa_produktu and ilosc_do_zakupu and cena:
        ilosc_do_zakupu = float(ilosc_do_zakupu)
        cena = float(cena)
        zakup(manager, produkt=nazwa_produktu, cena_zakupu=cena, ilosc=ilosc_do_zakupu)
    manager.execute('zapisz_w_pliku')

    context = {
        "title": title,
        "saldo": manager.konto,
        "magazyn": manager.magazyn,
      
    }
    return render_template('strona glowna.html', context=context)

@app.route('/history',methods=['POST', 'GET'])
def history():
    if request.method == "POST":
        start = request.form.get("start")
        koniec = request.form.get("koniec")
        return redirect(url_for("zakres_histori",start=start, koniec=koniec))
    else:

        title = "Historia operacji"
        context = {
            "title": title,
             "historia": manager.historia
        }
        return render_template('history.html', context=context)
@app.route('/history/<start>/<koniec>')
def zakres_histori(start, koniec):
    title = "Historia operacj w wybranym zakresie"


    context = {
        "title": title,
        "historia": przeglad(manager, od=start, do=koniec)}
#
#
    return render_template('history_zakres.html', context=context)


