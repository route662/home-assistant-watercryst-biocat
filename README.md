# Home Assistant Integration für Watercryst Biocat

Diese Integration ermöglicht die Einbindung von Watercryst Biocat-Geräten in Home Assistant.

## Funktionsweise der Watercryst Biocat

Der Watercryst Biocat (z.B. KLS3000-C) ist ein innovatives System zur Wasseraufbereitung, das Desinfektion, Mikro-Leckage-Erkennung und automatische Steuerung der Wasserzufuhr integriert. Es sorgt für eine kontinuierliche Überwachung und Anpassung der Wasserqualität und ist besonders für Trinkwasseraufbereitung sowie industrielle Anwendungen geeignet. Das System gewährleistet eine zuverlässige und effiziente Wasserbehandlung, indem es die Wasserzirkulation optimiert und sicherstellt, dass nur sauberes Wasser bereitgestellt wird. Weitere Informationen hierzu siehe Herstellerwebseite.

## Installation

### Über HACS

1. Öffne HACS in deinem Home Assistant.
2. Gehe zu "Integrations".
3. Klicke auf die drei Punkte und wähle "Custom repositories".
4. Füge das Repository `https://github.com/route662/home-assistant-watercryst-biocat` hinzu.
5. Suche nach "Watercryst Biocat" und installiere die Integration.

### Manuelle Installation

1. Lade das Repository als ZIP-Datei herunter und entpacke es.
2. Kopiere den Ordner `watercryst_biocat` nach `custom_components` in deinem Home Assistant Konfigurationsverzeichnis.
3. Starte Home Assistant neu.

## Konfiguration

1. Gehe in Home Assistant zu "Einstellungen" > "Integrationen".
2. Klicke auf "Integration hinzufügen" und suche nach "Watercryst Biocat".
3. Gib deinen API-Schlüssel ein, den du von Watercryst erhalten hast.
4. Folge den Anweisungen auf dem Bildschirm.

## Verwendete Sensoren

- **Wassertemperatur** (`waterTemp`): Zeigt die aktuelle Wassertemperatur in °C an.
- **Wasserdruck** (`pressure`): Zeigt den aktuellen Wasserdruck in bar an.
- **Letztes Wasserzapfvolumen** (`lastWaterTapVolume`): Volumen des zuletzt gezapften Wassers in Litern.
- **Dauer des letzten Wasserzapfens** (`lastWaterTapDuration`): Dauer des letzten Wasserzapfens in Sekunden.
- **Gesamtwasserverbrauch heute** (`totalWaterConsumptionToday`): Gesamtmenge des heute verbrauchten Wassers in Litern.

## Lizenz

Dieses Projekt steht unter der [GPL-3.0-Lizenz](LICENSE).

## Acknowledgments
This integration is based on the work from the [Simon42 Community Forum](https://community.simon42.com/t/curl-in-rest-sensor-wandeln/24438) and the [Watercryst API documentation](https://appapi.watercryst.com/).

### Unterstütze das Projekt

Wenn dir dieses Projekt gefällt und du es unterstützen möchtest, kannst du mir einen Kaffee spendieren:  
[Buy me a coffee](https://buymeacoffee.com/route662)



#### Disclaimer
This project is not affiliated with or endorsed by Watercryst. Use at your own risk.


