from pathlib import Path
import importlib
import math
import sys


def lade_daten(dateipfad):
    """Liest die CSV-Datei ein und wandelt Dezimalkommas in floats um."""
    werte = []

    with open(dateipfad, "r", encoding="utf-8-sig") as datei:
        for zeilennummer, zeile in enumerate(datei, start=1):
            text = zeile.strip()

            # Leere Zeilen werden übersprungen.
            if not text:
                continue

            # Deutsches Dezimalkomma wird für Python in einen Punkt umgewandelt.
            text = text.replace(",", ".")

            try:
                wert = float(text)
            except ValueError as fehler:
                raise ValueError(
                    f"Ungültiger Wert in Zeile {zeilennummer}: {zeile!r}"
                ) from fehler

            werte.append(wert)

    if not werte:
        raise ValueError("Die Datei enthält keine verwertbaren Zahlen.")

    return werte


def berechne_kennzahlen(werte):
    """Berechnet die Kennzahlen der empirischen Verteilung."""
    n = len(werte)

    # Erwartungswert der empirischen Verteilung
    mittelwert = sum(werte) / n

    # Zentrale Momente werden für Standardabweichung, Schiefe und Exzess benötigt.
    abweichungen = [wert - mittelwert for wert in werte]
    m2 = sum(abweichung ** 2 for abweichung in abweichungen) / n
    m3 = sum(abweichung ** 3 for abweichung in abweichungen) / n
    m4 = sum(abweichung ** 4 for abweichung in abweichungen) / n

    standardabweichung = math.sqrt(m2)

    # Falls alle Werte gleich sind, wären Schiefe und Exzess nicht sinnvoll definiert.
    if standardabweichung == 0:
        schiefe = 0.0
        exzess = -3.0
    else:
        schiefe = m3 / (standardabweichung ** 3)
        exzess = m4 / (standardabweichung ** 4) - 3

    return {
        "anzahl": n,
        "mittelwert": mittelwert,
        "standardabweichung": standardabweichung,
        "schiefe": schiefe,
        "exzess": exzess,
        "minimum": min(werte),
        "maximum": max(werte),
    }


def erstelle_histogramm(werte, mittelwert, standardabweichung, ausgabedatei):
    """Erstellt ein Histogramm und speichert es als PNG-Datei."""
    try:
        matplotlib = importlib.import_module("matplotlib")
        matplotlib.use("Agg")
        plt = importlib.import_module("matplotlib.pyplot")
    except ImportError as fehler:
        python_pfad = sys.executable
        raise ImportError(
            "Für das Histogramm wird matplotlib benötigt.\n"
            f"Verwendetes Python: {python_pfad}\n"
            f"Installiere es genau dafür mit:\n\"{python_pfad}\" -m pip install matplotlib"
        ) from fehler

    minimum = min(werte)
    maximum = max(werte)
    ausgabedatei = Path(ausgabedatei).resolve()
    ausgabedatei.parent.mkdir(parents=True, exist_ok=True)

    # Wahl der Klassenzahl: ungefähr Wurzel aus n.
    anzahl_klassen = max(6, round(math.sqrt(len(werte))))

    # Das Histogramm verwendet damit äquidistante Klassen.
    figur, achse = plt.subplots(figsize=(10, 6))
    achse.hist(
        werte,
        bins=anzahl_klassen,
        edgecolor="black",
        color="skyblue",
    )

    # Erwartungswert als senkrechte Linie
    achse.axvline(
        mittelwert,
        color="red",
        linewidth=2,
        label=f"Erwartungswert = {mittelwert:.3f}",
    )

    # Bereich von mu - sigma bis mu + sigma als zusätzliche Orientierung
    achse.axvspan(
        mittelwert - standardabweichung,
        mittelwert + standardabweichung,
        color="orange",
        alpha=0.25,
        label="Bereich: Mittelwert ± Standardabweichung",
    )

    achse.set_title("Histogramm der empirischen Verteilung")
    achse.set_xlabel("Temperatur")
    achse.set_ylabel("Häufigkeit")

    # Falls alle Werte identisch sind, braucht die x-Achse trotzdem einen kleinen Bereich.
    if minimum == maximum:
        achse.set_xlim(minimum - 0.5, maximum + 0.5)
    else:
        achse.set_xlim(minimum, maximum)

    achse.grid(axis="y", alpha=0.3)
    achse.legend()
    figur.tight_layout()
    figur.savefig(str(ausgabedatei), format="png", dpi=150)
    plt.close(figur)

    if not ausgabedatei.exists():
        raise OSError(f"Die PNG-Datei wurde nicht gespeichert: {ausgabedatei}")


def waehle_datei(aktueller_ordner):
    """Bestimmt die gewünschte CSV-Datei."""
    # Optional kann der Dateiname direkt beim Start übergeben werden.
    if len(sys.argv) > 1:
        dateiname = sys.argv[1].strip()
    else:
        dateiname = input("Gib den Namen der CSV-Datei im Ordner 'Daten' ein: ").strip()

    if not dateiname:
        raise ValueError("Es wurde kein Dateiname eingegeben.")

    dateipfad = Path(dateiname)

    # Relative Pfade werden auf den Ordner des Skripts bezogen.
    if not dateipfad.is_absolute():
        moegliche_pfade = [
            aktueller_ordner / "Daten" / dateipfad,
            aktueller_ordner / dateipfad,
        ]

        for pfad in moegliche_pfade:
            if pfad.exists():
                return pfad

        dateipfad = aktueller_ordner / dateipfad

    return dateipfad


def bestimme_ausgabedatei(dateipfad):
    """Erstellt einen passenden Dateinamen für das Histogramm."""
    histogramm_ordner = dateipfad.parent / "Histogramme"
    histogramm_ordner.mkdir(exist_ok=True)
    return histogramm_ordner / f"{dateipfad.stem}_Histogramm.png"


def main():
    aktueller_ordner = Path(__file__).resolve().parent

    try:
        dateipfad = waehle_datei(aktueller_ordner)
    except ValueError as fehler:
        print(fehler)
        return

    ausgabedatei = bestimme_ausgabedatei(dateipfad)

    if not dateipfad.exists():
        print(f"Die Datei wurde nicht gefunden: {dateipfad}")
        return

    try:
        werte = lade_daten(dateipfad)
        kennzahlen = berechne_kennzahlen(werte)
    except Exception as fehler:
        print(f"Fehler beim Einlesen oder Berechnen: {fehler}")
        return

    print("Auswertung der empirischen Verteilung")
    print("------------------------------------")
    print(f"Datei:                   {dateipfad.name}")
    print(f"Anzahl der Werte:        {kennzahlen['anzahl']}")
    print(f"Minimum:                 {kennzahlen['minimum']:.3f}")
    print(f"Maximum:                 {kennzahlen['maximum']:.3f}")
    print(f"Erwartungswert:          {kennzahlen['mittelwert']:.6f}")
    print(f"Standardabweichung:      {kennzahlen['standardabweichung']:.6f}")
    print(f"Schiefe:                 {kennzahlen['schiefe']:.6f}")
    print(f"Exzess:                  {kennzahlen['exzess']:.6f}")

    try:
        erstelle_histogramm(
            werte,
            kennzahlen["mittelwert"],
            kennzahlen["standardabweichung"],
            ausgabedatei,
        )
        print(f"Histogramm gespeichert:  {ausgabedatei}")
    except ImportError as fehler:
        print()
        print(fehler)
    except Exception as fehler:
        print()
        print(f"Fehler beim Erstellen des Histogramms: {fehler}")


if __name__ == "__main__":
    main()
