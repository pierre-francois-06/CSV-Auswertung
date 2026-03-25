from pathlib import Path
import math


# Name der CSV-Datei im aktuellen Ordner
DATEINAME = "Daten (Set IV, A6) [CSV].csv"

# Name der Ausgabedatei für das Histogramm
HISTOGRAMM_DATEI = "histogramm.png"


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
        import matplotlib.pyplot as plt
    except ImportError as fehler:
        raise ImportError(
            "Für das Histogramm wird matplotlib benötigt. "
            "Installiere es mit: pip install matplotlib"
        ) from fehler

    minimum = min(werte)
    maximum = max(werte)

    # Einfache Wahl der Klassenzahl: ungefähr Wurzel aus n.
    anzahl_klassen = max(6, round(math.sqrt(len(werte))))

    # Das Histogramm verwendet damit äquidistante Klassen.
    plt.figure(figsize=(10, 6))
    plt.hist(
        werte,
        bins=anzahl_klassen,
        edgecolor="black",
        color="skyblue",
    )

    # Erwartungswert als senkrechte Linie
    plt.axvline(
        mittelwert,
        color="red",
        linewidth=2,
        label=f"Erwartungswert = {mittelwert:.3f}",
    )

    # Bereich von mu - sigma bis mu + sigma als zusätzliche Orientierung
    plt.axvspan(
        mittelwert - standardabweichung,
        mittelwert + standardabweichung,
        color="orange",
        alpha=0.25,
        label="Bereich: Mittelwert ± Standardabweichung",
    )

    plt.title("Histogramm der empirischen Verteilung")
    plt.xlabel("Temperatur")
    plt.ylabel("Häufigkeit")
    plt.xlim(minimum, maximum)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(ausgabedatei, dpi=150)
    plt.close()


def main():
    aktueller_ordner = Path(__file__).resolve().parent
    dateipfad = aktueller_ordner / DATEINAME
    ausgabedatei = aktueller_ordner / HISTOGRAMM_DATEI

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
