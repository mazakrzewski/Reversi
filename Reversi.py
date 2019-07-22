#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# program zawiera gre Rewersi
# wielkosc planszy zmienia sie zmieniajac waroosc liczbyw w plansza(x)
#
#
#


import random  # losowanie ruchu przeciwnika

import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Plansza(Gtk.Window):
    """klasa zawierajaca gre."""

    def mozliwe_ruchy(self):
        """Funkcja oblicza mozliwe ruchy dla aktualnego gracza."""
        self.mozliwe = []
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                if self.tablica[i][j] == 0:
                    for m in [-1, 0, 1]:
                        for n in [-1, 0, 1]:
                            if m != 0 or n != 0:
                                przesuniecie_poziome = m
                                przesuniecie_pionowe = n
                                if self.tablica[i + przesuniecie_poziome][j + przesuniecie_pionowe] != self.znak:
                                    while self.tablica[i + przesuniecie_poziome][j + przesuniecie_pionowe] != 0:
                                        if self.tablica[i + przesuniecie_poziome][
                                                    j + przesuniecie_pionowe] == self.znak:
                                            self.mozliwe.append((i, j))
                                        przesuniecie_poziome += m
                                        przesuniecie_pionowe += n

    def nowa_gra(self, btn):
        """resetuje gre."""
        self.tablica = [[0 for col in range(self.rozmiar + 1)] for row in range(self.rozmiar + 1)]
        self.znak = 1
        self.tablica[self.rozmiar / 2 - 1][self.rozmiar / 2 - 1] = 1
        self.tablica[self.rozmiar / 2][self.rozmiar / 2] = 1
        self.tablica[self.rozmiar / 2][self.rozmiar / 2 - 1] = 2
        self.tablica[self.rozmiar / 2 - 1][self.rozmiar / 2] = 2
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                self.buttons[i][j].get_child().set_markup("{}".format(self.znaki_tab[self.tablica[i][j]]))
                if self.tablica[i][j] == 0:
                    self.buttons[i][j].set_sensitive(True)
                else:
                    self.buttons[i][j].set_sensitive(False)

        self.mozliwe_ruchy()

    def __init__(self, arg1):
        """Inicjuje powstanie planszy. """
        self.window = Gtk.Window()
        self.window.set_title("saper")
        self.window.set_default_size(200, 200)
        self.window.connect("delete-event", lambda x, y: Gtk.main_quit())

        # okresla wielkosc planszy
        if arg1 % 2 == 1:
            self.rozmiar += 1
        self.rozmiar = arg1
        self.tablica = []
        self.znaki_tab = dict([(0, '<span foreground="black"><b>0</b></span>'),
                               (1, '<span foreground="red"><b>1</b></span>'),
                               (2, '<span foreground="blue"><b>2</b></span>')])
        self.znak = 1
        self.punkty_gracz = 2
        self.punkty_komputer = 2

        # ukladam przyciski na siatce
        if self.rozmiar % 2 == 1:
            self.rozmiar += 1
        grid = Gtk.Grid()
        self.buttons = []
        for i in range(self.rozmiar):
            self.buttons.append([])
            for j in range(self.rozmiar):
                b = Gtk.Button.new_with_label(" ")
                self.buttons[i].append(b)
                grid.attach(b, i, j, 1, 1)
                b.connect("clicked", self.kliknieto, i, j)

                # dodaje przycisk nawa gra
        self.wynik_gracza = Gtk.Button(label="Red: {}".format(self.punkty_gracz))
        self.wynik_gracza.get_child().set_markup('<span foreground="red">Red: {}</span>'.format(self.punkty_gracz))
        self.buttons.append(self.wynik_gracza)
        grid.attach(self.wynik_gracza, self.rozmiar + 1, 0, 1, 1)
        self.wynik_gracza.set_sensitive(False)
        self.wynik_przeciwnika = Gtk.Button(label="Blue: {}".format(self.punkty_komputer))
        self.wynik_przeciwnika.get_child().set_markup(
            '<span foreground="blue">Blue: {}</span>'.format(self.punkty_komputer))
        self.wynik_przeciwnika.set_sensitive(False)
        self.buttons.append(self.wynik_przeciwnika)
        grid.attach(self.wynik_przeciwnika, self.rozmiar + 1, 1, 1, 1)

        # dodaje przycisk nawa gra
        b = Gtk.Button(label="Nowa gra")
        self.buttons.append(b)
        grid.attach(b, 0, self.rozmiar + 1, self.rozmiar, 1)
        b.connect("clicked", self.nowa_gra)
        self.window.add(grid)
        # kolumny maja miec identyczna szerokosc, wiersze identyczna wysokosc
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        self.nowa_gra("clicked")

        self.window.show_all()

    def zmien_znak(self):
        """Zmiana aktualnego znaku (gracza)."""
        self.znak = 1 if self.znak == 2 else 2

    def nowa_gra_wiadomocs(self, btn):
        """Tworzy nowa gre i zamyka okno wyniku."""
        self.nowa_gra("clicked")
        self.wiadomosc.destroy()

    def wiad(self, ):
        """Otwiera okno z informacjo o wyniku gry."""
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                self.buttons[i][j].set_sensitive(False)

        self.wiadomosc = Gtk.Window()
        self.wiadomosc.set_title("tutul")
        self.wiadomosc.set_default_size(400, 100)
        b = Gtk.Button("Nowa gra")
        b.connect("clicked", self.nowa_gra_wiadomocs)
        self.wiadomosc.add(b)
        self.wiadomosc.show_all()

    def ruch(self, wspolrzedne):
        """Wykonuje ruch gracza."""
        # Przysisk to kontener ktory zawiera tylko jednego potomka: labelke.
        # Na labelce moge wywolac metode set_markup
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    przes_poziome = i
                    przes_pionowe = j
                    while self.tablica[wspolrzedne[0] + przes_poziome][wspolrzedne[1] + przes_pionowe] != 0:
                        if self.tablica[wspolrzedne[0] + przes_poziome][wspolrzedne[1] + przes_pionowe] == self.znak:
                            while przes_poziome != 0 or przes_pionowe != 0:
                                self.tablica[wspolrzedne[0] + przes_poziome][wspolrzedne[1] + przes_pionowe] = self.znak
                                self.buttons[wspolrzedne[0] + przes_poziome][
                                    wspolrzedne[1] + przes_pionowe].get_child().set_markup(
                                    self.znaki_tab[self.znak])
                                self.buttons[wspolrzedne[0] + przes_poziome][
                                    wspolrzedne[1] + przes_pionowe].set_sensitive(False)
                                przes_poziome -= i
                                przes_pionowe -= j
                            break
                        przes_poziome += i
                        przes_pionowe += j

        self.tablica[wspolrzedne[0]][wspolrzedne[1]] = self.znak
        self.buttons[wspolrzedne[0]][wspolrzedne[1]].get_child().set_markup(self.znaki_tab[self.znak])
        self.buttons[wspolrzedne[0]][wspolrzedne[1]].set_sensitive(False)

    def policz_punkty(self):
        """Aktualizuje wynk graczy."""
        self.punkty_gracz = 0
        self.punkty_komputer = 0
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                if self.tablica[i][j] == 1:
                    self.punkty_gracz += 1
                elif self.tablica[i][j] == 2:
                    self.punkty_komputer += 1
        self.wynik_gracza.get_child().set_markup('<span foreground="red">Red: {}</span>'.format(self.punkty_gracz))
        self.wynik_przeciwnika.get_child().set_markup(
            '<span foreground="blue">Blue: {}</span>'.format(self.punkty_komputer))

    def wiad(self):
        """Otwiera okno z informacjo o wyniku gry."""
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                self.buttons[i][j].set_sensitive(False)

        self.wiadomosc = Gtk.Window()
        if self.punkty_gracz > self.punkty_komputer:
            self.wiadomosc.set_title("Wygrana {}:{}".format(self.punkty_gracz, self.punkty_komputer))
        else:
            self.wiadomosc.set_title("Przegrana {}:{}".format(self.punkty_gracz, self.punkty_komputer))
        self.wiadomosc.set_default_size(400, 100)
        b = Gtk.Button("Nowa gra")
        b.connect("clicked", self.nowa_gra_wiadomocs)
        self.wiadomosc.add(b)

        self.wiadomosc.show_all()

    def kliknieto(self, btn, x, y):
        """obsluguje klikniecie w plansze."""
        if (x, y) in self.mozliwe:
            self.ruch((x, y))
            self.zmien_znak()
            self.mozliwe_ruchy()
            self.policz_punkty()
            if self.mozliwe == []:
                self.wiad()
            self.ruch(random.choice(self.mozliwe))
            self.zmien_znak()
            self.mozliwe_ruchy()
            self.policz_punkty()
            if self.mozliwe == []:
                self.wiad()


if __name__ == "__main__":
    a = Plansza(6)
    Gtk.main()
