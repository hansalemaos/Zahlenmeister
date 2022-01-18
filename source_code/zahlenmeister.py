import regex
from num2words import num2words
import os
from winregistry import WinRegistry
from random import randrange
from maximize_console import maximize_console
from menudownload import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from einfuehrung import einfuehrung
from farbprinter.farbprinter import Farbprinter
drucker = Farbprinter()


def richtig(leerzeichen=5):
    global userpunkte
    global gesamtpunkte
    gesamtpunkte = gesamtpunkte + 1
    userpunkte = userpunkte + 1
    print(drucker.f.black.brightgreen.bold(f'\nDeine Antwort ist richtig! \nErreichte Punkte:\t\t') +   drucker.f.black.brightgreen.negative(
        f'  {userpunkte}  ') + drucker.f.black.brightgreen.bold(f'\nMaximale Punktanzahl:\t\t') + drucker.f.black.brightgreen.negative(
        f'  {gesamtpunkte}  ') + drucker.f.black.brightgreen.bold(f'\n'))
    print('\n' * leerzeichen)


def falsch(richtigeantwort, leerzeichen=5):
    global userpunkte
    global gesamtpunkte
    gesamtpunkte = gesamtpunkte + 1
    print(drucker.f.black.brightred.bold(f'\nDeine Antwort ist falsch! Die richtige Antwort ist: {richtigeantwort}\nErreichte Punkte:\t\t') +   drucker.f.black.brightred.negative(
        f'  {userpunkte}  ') + drucker.f.black.brightred.bold(f'\nMaximale Punktanzahl:\t\t') + drucker.f.black.brightred.negative(
        f'  {gesamtpunkte}  ') + drucker.f.black.brightred.bold(f'\n'))
    print('\n' * leerzeichen)


def get_number_from_user(satzdrucken, farbe='brightyellow'):
    anfang = ''
    while not isinstance(anfang, int):
        try:
            anfang = input(drucker.f.black[farbe].italic(satzdrucken))
            anfang = int(anfang)
        except:
            print(drucker.f.black.brightred.italic('\nEingabe konnte nicht verstanden werden!\n'))
    return anfang


def get_vlc_exe_path():
    def datei_auswaehlen_mit_tkinter():
        Tk().withdraw()
        videodatei = askopenfilename(filetypes=[("VLC PLAYER EXE", "vlc.exe")])
        ausgabeordner = regex.sub(r"/[^/]+\.\w+$", "", videodatei)
        print(videodatei, ausgabeordner)
        return videodatei, ausgabeordner
    TEST_REG_PATH = r"HKCR\VLC.3g2\shell\AddToPlaylistVLC"
    with WinRegistry() as client:
        test_entry = client.read_entry(TEST_REG_PATH, "Icon")
        try:
            vlcexe = regex.findall('"[^"]+vlc.exe"', test_entry.value)[0].strip('"')
            print(drucker.f.black.brightgreen.italic(f"vlc.exe Found! {vlcexe}"))
        except Exception as Fehler:
            print(drucker.f.black.brightred.italic(f"vlc.exe not found!"))
            print(drucker.f.black.brightyellow.italic(f"Please select VLC.EXE"))
            vlcexe, _ = datei_auswaehlen_mit_tkinter()
            print(Fehler)
    return vlcexe


if __name__ == '__main__':
    maximize_console()
    einfuehrung(name='Zahlenmeister')
    auswahl = auswahlmenu_erstellen(
        optionen=['Buchstaben -> Zahlen (neunundzwanzig -> 29)', 'Zahlen -> Buchstaben (29 -> neunundzwanzig)',
                  'Audio -> Zahlen (VLC Player muss installiert sein: www.videolan.org'],
        uberschrift='Was möchtest du trainieren?', color='brightblue', unterdemtext='\nDeine Eingabe\n')

    einfuehrung('Zahlenmeister')
    anfang = get_number_from_user(satzdrucken='\nBei welcher Zahl soll ich anfangen?\n', farbe='brightyellow')
    ende = get_number_from_user(satzdrucken='\nBei welcher Zahl soll ich aufhören?\n', farbe='brightcyan')
    anzahlaufgaben = get_number_from_user(satzdrucken='\nWie viele Aufgaben sollen erstellt werden?\n', farbe='brightgreen')
    if auswahl == '3':
        wieoftwiederholen = get_number_from_user(satzdrucken='\nWie oft soll das Audio wiederholt werden?\n', farbe='brightmagenta')

    gesamtpunkte = 0
    userpunkte = 0
    vlcpath=''
    if auswahl == '3':
        vlcpath = get_vlc_exe_path()
    for x in range(anzahlaufgaben):
        gesuchtezahl = randrange(anfang, ende)
        gesuchtezahlalswort = num2words(gesuchtezahl, lang='de')
        if auswahl == '1':
            usereingabe = input(drucker.f.black.brightmagenta.negative('\nWelche Zahl ist das: ') + drucker.f.black.brightmagenta.bold(f'   {gesuchtezahlalswort}   ') + drucker.f.black.brightmagenta.negative('?\n') )
            try:
                usereingabe = usereingabe.strip()
                usereingabe = int(usereingabe)
                if usereingabe == gesuchtezahl:
                    richtig()
                elif usereingabe != gesuchtezahl:
                    falsch(richtigeantwort=gesuchtezahl)
            except:
                falsch(richtigeantwort=gesuchtezahl)
        if auswahl == '2':
            usereingabe = input(drucker.f.black.brightmagenta.negative('\nSchreibe die Zahl als Wort/Wörter: ') + drucker.f.black.brightmagenta.bold(f'    {gesuchtezahl}    ') + drucker.f.black.brightmagenta.negative('\n Achte auf die Groß-/Kleinschreibung!\n') )
            if usereingabe.strip() == gesuchtezahlalswort:
                richtig()
            if usereingabe.strip() != gesuchtezahlalswort:
                falsch(richtigeantwort=gesuchtezahlalswort)
        if auswahl == '3':
            mp3datei = r'zahlen_temp_audioxxxxxx.mp3'
            kommando_google_stimme = f'gtts-cli "{gesuchtezahlalswort}" --lang de --output {mp3datei}'
            os.system(kommando_google_stimme)
            kommando_abspielen_mit_vlc = fr'"{vlcpath}" --input-repeat={wieoftwiederholen} -Idummy --play-and-exit {mp3datei}'
            os.system(kommando_abspielen_mit_vlc)
            usereingabe = input(drucker.f.black.brightmagenta.negative('\nSchreibe die Zahl entweder als Zahl (29) oder als Wort/Wörter (neunundzwanzig) Achte auf die Groß-/Kleinschreibung!\n') )
            if str(usereingabe).strip() == str(gesuchtezahl) or usereingabe == gesuchtezahlalswort:
                richtig()
                continue
            falsch(richtigeantwort=f'{gesuchtezahl} / {gesuchtezahlalswort}')

    fertig = input(drucker.f.black.brightmagenta.normal(f'\nDu hast insgesamt ') + drucker.f.brightmagenta.black.normal( (f'  {userpunkte}  ')  +  drucker.f.black.brightmagenta.normal(' von ') + drucker.f.brightmagenta.black.normal(f'   {gesamtpunkte}   ') + drucker.f.black.brightmagenta.normal(' erreicht\n')))


