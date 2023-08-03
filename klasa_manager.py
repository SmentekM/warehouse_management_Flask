import os
import json

class Manager:
    def __init__(self, *args, **kwargs):
        self.funkcje = {}
        self.konto = []
        self.historia = []

        self.magazyn = {}

    def assing(self, nazwa):
        def decorate(cb):
            self.funkcje[nazwa] = cb
        return decorate

    def execute(self, nazwa):
        if nazwa not in self.funkcje:
            print(f'Funkcja {nazwa} nie jest zdefiniowana')
        else:
            self.funkcje[nazwa](self)

manager = Manager()

@manager.assing('wczytanie_plikow')
def wczytanie_plikow(manager):
    if not os.path.exists('saldo.txt'):
        manager.konto = 0
    else:
        with open('saldo.txt', 'r') as f:
            for ele in f:
                manager.konto = float(ele)

    if not os.path.exists('saldo.txt'):
        manager.historia = []
    else:
        with open('przeglad.txt', 'r') as f:
            for ele in f:
                x = ele[:-1]
                manager.historia.append(x)

    if not os.path.exists('magazyn.txt'):
        manager.magazyn = {}
    else:
        with open('magazyn.txt', 'r') as f:
            for ele in f:
                manager.magazyn = json.loads(ele.replace("'", '"'))

@manager.assing('zapisz_w_pliku')
def zapisz_w_pliku(manager):
    with open('saldo.txt', 'w') as f:
        f.write(str(manager.konto))
    with open('magazyn.txt', 'w') as f:
        f.write(str(manager.magazyn))
    with open('przeglad.txt', 'w') as f:
        for ele in manager.historia:
            f.write(ele + '\n')

@manager.assing('saldo')
def saldo(manager,operacja,kwota):
    print('Wybrales saldo')
    # operacja = str.lower(input('Podaj rodzaj operacji w -wpłata, p - platość:  '))
    # kwota = float(input('Podaj kwotę: '))
    if operacja == 'w':
        manager.konto += kwota
        zadanie = f"Dokonano {operacja} na kwotę {kwota}"
        manager.historia.append(zadanie)

    elif operacja == 'p' and manager.konto >= kwota:
        manager.konto -= kwota
        zadanie = f"Dokonano {operacja} na kwotę {kwota}"
        manager.historia.append(zadanie)

    elif operacja == 'p' and manager.konto < kwota:
        print('Niemasz srodków na koncie')
    else:
        print('Podałes zły rodzaj operacji!!')


@manager.assing('sprzedaz')
def sprzedaz(manager):
    print('Wybrałeś sprzedaż produktu.')
    produkt_do_przedazy = str(input(' Podaj produkt do sprzedaży: '))
    ilosc_do_sprzedazy = float(input('Podaj ilość produktów do spredaży: '))
    if produkt_do_przedazy not in manager.magazyn:
        print('Produktu nie ma w magazynie. Nie może zostac sprzedany.')
    if produkt_do_przedazy in manager.magazyn:
        dane_produktu = manager.magazyn.get(produkt_do_przedazy)
        ilosc_produktu = dane_produktu['ilosc']
        if ilosc_produktu > ilosc_do_sprzedazy:
            cena_sprzedazy = dane_produktu['cena']
            manager.konto += ilosc_do_sprzedazy * cena_sprzedazy
            ilosc_produktu -= ilosc_do_sprzedazy
            sprzedaz_produktu = {produkt_do_przedazy: {
                'cena zakupu': cena_sprzedazy,
                'ilosc': ilosc_do_sprzedazy,
            }}
            manager.magazyn[produkt_do_przedazy] = {'cena': cena_sprzedazy, 'ilosc': ilosc_produktu}

            zadanie = f"Sprzedano {produkt_do_przedazy}: ilośc: {ilosc_do_sprzedazy} cena: {cena_sprzedazy}"
            manager.historia.append(zadanie)

        elif ilosc_produktu == ilosc_do_sprzedazy:
            cena_sprzedazy = dane_produktu['cena']
            manager.konto += ilosc_do_sprzedazy * cena_sprzedazy
            ilosc_produktu -= ilosc_do_sprzedazy
            sprzedaz_produktu = {produkt_do_przedazy: {
                'cena zakupu': cena_sprzedazy,
                'ilosc': ilosc_do_sprzedazy,
            }}
            del manager.magazyn[produkt_do_przedazy]

            zadanie = f"Sprzedano {produkt_do_przedazy}: ilośc: {ilosc_do_sprzedazy} cena: {cena_sprzedazy}"
            manager.historia.append(zadanie)

        else:
            print(f'Na stanie magazynu nie ma wystarczającej ilości produktu.\n'
                  f' W magazynie jest {ilosc_produktu}')

@manager.assing('zakup')
def zakup(manager):
    print('Wybrałeś zakup produktu.')
    produkt = str(input('Podaj nazwę produktu: '))
    cena_zakupu = float(input('Podaj cenę produktu: '))
    ilosc = float(input('Podaj ilosc produktów: '))
    zakupiona_ilosc = ilosc
    if cena_zakupu <= 0:
        print('Podano niewłaściwą cenę zakupu!')
    elif cena_zakupu * ilosc <= manager.konto:
        if produkt in manager.magazyn:
            manager.konto -= cena_zakupu * ilosc
            zakup_produktu = {produkt: {
                'cena zakupu': cena_zakupu,
                'ilosc': ilosc,
            }}
            ilosc += ilosc
            manager.magazyn[produkt] = {'cena': cena_zakupu, 'ilosc': ilosc}

            zadanie = f"zakupiono {produkt}: cena: {cena_zakupu} ilość: {zakupiona_ilosc}"
            manager.historia.append(zadanie)

        else:
            zakup_produktu = {produkt: {
                'cena zakupu': cena_zakupu,
                'ilosc': ilosc,
            }}
            manager.magazyn[produkt] = {'cena': cena_zakupu, 'ilosc': ilosc}
            manager.konto -= cena_zakupu * ilosc

            zadanie = f"zakupiono {produkt}: cena: {cena_zakupu} ilość: {zakupiona_ilosc} "

            manager.historia.append(zadanie)

    else:
        print('Nie masz wystarczających środków na koncie na zakup produktu.')

@manager.assing('konto')
def konto(manager):
    print('Wybrales sprawdzenie stanu konta firmowego.')
    print(f'Stan konta firmowego wynosi: [{manager.konto}]')

@manager.assing('lista')
def lista(manager):
    print('Wybrales sprawdzenie stanu magazynu')
    for k, v in manager.magazyn.items():
        print(f'{k} - {v}')

@manager.assing('magazyn')
def magazyn(manager):
    print('Wybrałeś magazyn.\n'
          'Lista produktów znajdująca sie w magazynie:')
    for k in manager.magazyn.keys():
        print(f'{k}')
    wybrany_produkt = str(input('Podaj nazwę wybranego produktu: '))
    if wybrany_produkt not in manager.magazyn:
        print('Wybranego produktu nie ma w magazynie')
    else:
        print(f'Stan dla wybranego produktu: {wybrany_produkt} - {manager.magazyn[wybrany_produkt]}')

@manager.assing('przeglad')
def przeglad(manager):
    print('Wybrales przeglad histori wykonanych akcji.')
    od = input('Podaj poczatek zakresu: ')
    do = input('Podaj koniec zakresu: ')
    liczba_akcji = len(manager.historia)
    if od:
        od = int(od)
    else:
        od = 0
    if do:
        do = int(do)
    else:
        do = liczba_akcji
    if od < 0 or od > liczba_akcji or do < 0 or do > liczba_akcji:
        print(f'Podałeś zły zakres. Liczba wszytskich akcji wynosi: {liczba_akcji}')
    else:
        print(f'Twoj zakres to od {od} do {do}')
        print(manager.historia[od: do])