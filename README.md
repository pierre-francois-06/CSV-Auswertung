# CSV-Auswertung

Dieses Programm wertet eine CSV-Datei mit Messwerten aus.

Berechnet werden:
- Erwartungswert
- Standardabweichung
- Schiefe
- Exzess

Zusätzlich wird ein Histogramm als PNG-Datei gespeichert.

## Was wird benötigt?

- Python 3
- `matplotlib` für das Histogramm

Falls `matplotlib` noch nicht installiert ist, kann es mit diesem Befehl installiert werden:

```powershell
python -m pip install matplotlib
```

## Ordnerstruktur

Die CSV-Dateien sollen im Ordner `Daten` liegen.

Beispiel:

```text
CSV-Auswertung/
|-- auswertung.py
|-- README.md
|-- Daten/
|   |-- Daten.csv
|   |-- TestDaten.csv
|   |-- Histogramme/
```

## Format der CSV-Datei

Die CSV-Datei soll sehr einfach aufgebaut sein:
- eine Zahl pro Zeile
- keine Überschrift
- Dezimaltrennzeichen darf `,` oder `.` sein

Beispiel:

```text
8,10
8,92
9,03
9,08
```

## Programm starten

Öffne ein Terminal im Ordner `CSV-Auswertung`.

Dann starte das Programm mit:

```powershell
python auswertung.py
```

Danach fragt das Programm nach dem Namen der CSV-Datei im Ordner `Daten`.

Beispiel:

```text
Gib den Namen der CSV-Datei im Ordner 'Daten' ein: TestDaten.csv
```

Du kannst den Dateinamen auch direkt beim Start angeben:

```powershell
python auswertung.py TestDaten.csv
```

## Was macht das Programm?

Das Programm:
- sucht die Datei zuerst im Ordner `Daten`
- liest alle Zahlen aus der CSV-Datei ein
- berechnet die Kennzahlen
- zeigt die Ergebnisse in der Konsole an
- speichert das Histogramm als PNG-Datei

## Wo wird das Histogramm gespeichert?

Das Histogramm wird im Ordner `Histogramme` gespeichert, der automatisch im Ordner `Daten` angelegt wird.

Beispiel:

```text
Daten/Histogramme/TestDaten_Histogramm.png
```

## Wenn ein Fehler mit matplotlib erscheint

Dann verwendet dein Editor oder dein Terminal wahrscheinlich ein anderes Python als das, in dem `matplotlib` installiert wurde.

Wenn das Programm diese Meldung zeigt, kopiere einfach den dort ausgegebenen Befehl und führe ihn genau so aus.

Beispiel:

```powershell
"C:\Pfad\zu\python.exe" -m pip install matplotlib
```

## Kurzbeispiel

```powershell
python auswertung.py Daten.csv
```

Danach werden:
- die Kennzahlen in der Konsole angezeigt
- das Histogramm als PNG gespeichert
