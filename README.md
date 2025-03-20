# Home Assistant Integration for Watercryst Biocat

[English](#english) | [Deutsch](#deutsch)

---

## English

### Overview
This integration allows you to integrate Watercryst Biocat devices into Home Assistant.

### Features
- Retrieve real-time data such as water temperature, pressure, and consumption.
- Support for sensors and binary sensors.
- Easy configuration via the Home Assistant user interface.

### How It Works
The Watercryst Biocat integration communicates with the Watercryst Biocat system via its API. The integration retrieves data from the Biocat system, such as:
- **Water temperature**: The current temperature of the water in the system.
- **Water pressure**: The pressure in the water system.
- **Water consumption**: Statistics about water usage, including the volume and duration of the last water tap and the total water consumption for the day.

The integration uses the Modbus protocol to communicate with the Biocat system, ensuring reliable and efficient data retrieval. All retrieved data is exposed as sensors in Home Assistant, allowing you to monitor and automate based on water system metrics.

### How the Watercryst Biocat Works
The Watercryst Biocat system is a water treatment device designed to prevent limescale buildup in water systems. It works by using a catalytic process to modify the structure of calcium and magnesium ions in the water, preventing them from forming hard limescale deposits. The system operates without the need for chemicals or electricity, making it environmentally friendly and maintenance-free. The integration allows you to monitor the system's performance and water quality metrics directly in Home Assistant.

### Installation

#### Via HACS
1. Open HACS in your Home Assistant.
2. Go to **Integrations**.
3. Click the three dots in the top-right corner and select **Custom repositories**.
4. Add the repository URL: `https://github.com/route662/home-assistant-watercryst-biocat`.
5. Search for **Watercryst Biocat** and install the integration.
6. Restart Home Assistant.

#### Manual Installation
1. Download the repository as a ZIP file and extract it.
2. Copy the `watercryst_biocat` folder to the `custom_components` directory in your Home Assistant configuration folder.
3. Restart Home Assistant.

### Configuration
1. Go to **Settings > Integrations** in Home Assistant.
2. Click **Add Integration** and search for **Watercryst Biocat**.
3. Enter your API key provided by Watercryst.
4. Follow the on-screen instructions.

### Supported Sensors
- **Water Temperature** (`waterTemp`): Displays the current water temperature in °C.
- **Water Pressure** (`pressure`): Displays the current water pressure in bar.
- **Last Water Tap Volume** (`lastWaterTapVolume`): Volume of the last water tap in liters.
- **Last Water Tap Duration** (`lastWaterTapDuration`): Duration of the last water tap in seconds.
- **Total Water Consumption Today** (`totalWaterConsumptionToday`): Total water consumption today in liters.

### Logo
The logo used in this project is the property of Watercryst and is used here for informational purposes only. For more details, visit the [Watercryst website](https://www.watercryst.com).

### Acknowledgments
Special thanks to **Ralf Winter** for his contributions and inspiration for this integration.

### License
This project is licensed under the [GPL-3.0 License](LICENSE).

### Support the Project
If you find this project helpful and would like to support it, consider buying me a coffee:  
[Buy me a coffee](https://buymeacoffee.com/route662)

---

## Deutsch

### Übersicht
Diese Integration ermöglicht die Einbindung von Watercryst Biocat-Geräten in Home Assistant.

### Funktionen
- Echtzeitdaten wie Wassertemperatur, Druck und Verbrauch abrufen.
- Unterstützung für Sensoren und binäre Sensoren.
- Einfache Konfiguration über die Benutzeroberfläche von Home Assistant.

### Funktionsweise
Die Watercryst Biocat-Integration kommuniziert über die API des Watercryst Biocat-Systems. Die Integration ruft Daten vom Biocat-System ab, darunter:
- **Wassertemperatur**: Die aktuelle Temperatur des Wassers im System.
- **Wasserdruck**: Der Druck im Wassersystem.
- **Wasserverbrauch**: Statistiken über den Wasserverbrauch, einschließlich des Volumens und der Dauer des letzten Wasserzapfens sowie des gesamten Wasserverbrauchs für den Tag.

Die Integration verwendet das Modbus-Protokoll, um mit dem Biocat-System zu kommunizieren. Dies gewährleistet eine zuverlässige und effiziente Datenübertragung. Alle abgerufenen Daten werden als Sensoren in Home Assistant bereitgestellt, sodass du dein Wassersystem überwachen und Automatisierungen basierend auf den Wasserwerten erstellen kannst.

### Funktionsweise der Watercryst Biocat
Das Watercryst Biocat-System ist ein Wasseraufbereitungsgerät, das entwickelt wurde, um Kalkablagerungen in Wassersystemen zu verhindern. Es arbeitet mit einem katalytischen Prozess, der die Struktur von Kalzium- und Magnesiumionen im Wasser verändert, sodass diese keine harten Kalkablagerungen bilden können. Das System kommt ohne Chemikalien oder Strom aus, was es umweltfreundlich und wartungsfrei macht. Die Integration ermöglicht es dir, die Leistung des Systems und die Wasserqualitätsmetriken direkt in Home Assistant zu überwachen.

### Installation

#### Über HACS
1. Öffne HACS in deinem Home Assistant.
2. Gehe zu **Integrationen**.
3. Klicke oben rechts auf die drei Punkte und wähle **Benutzerdefinierte Repositories**.
4. Füge die Repository-URL `https://github.com/route662/home-assistant-watercryst-biocat` hinzu.
5. Suche nach **Watercryst Biocat** und installiere die Integration.
6. Starte Home Assistant neu.

#### Manuelle Installation
1. Lade das Repository als ZIP-Datei herunter und entpacke es.
2. Kopiere den Ordner `watercryst_biocat` in das Verzeichnis `custom_components` deiner Home Assistant-Konfiguration.
3. Starte Home Assistant neu.

### Konfiguration
1. Gehe in Home Assistant zu **Einstellungen > Integrationen**.
2. Klicke auf **Integration hinzufügen** und suche nach **Watercryst Biocat**.
3. Gib deinen API-Schlüssel ein, den du von Watercryst erhalten hast.
4. Folge den Anweisungen auf dem Bildschirm.

### Unterstützte Sensoren
- **Wassertemperatur** (`waterTemp`): Zeigt die aktuelle Wassertemperatur in °C an.
- **Wasserdruck** (`pressure`): Zeigt den aktuellen Wasserdruck in bar an.
- **Letztes Wasserzapfvolumen** (`lastWaterTapVolume`): Volumen des zuletzt gezapften Wassers in Litern.
- **Dauer des letzten Wasserzapfens** (`lastWaterTapDuration`): Dauer des letzten Wasserzapfens in Sekunden.
- **Gesamtwasserverbrauch heute** (`totalWaterConsumptionToday`): Gesamtmenge des heute verbrauchten Wassers in Litern.

### Logo
Das in diesem Projekt verwendete Logo ist Eigentum von Watercryst und wird hier nur zu Informationszwecken verwendet. Weitere Informationen findest du auf der [Watercryst-Webseite](https://www.watercryst.com).

### Danksagungen
Besonderer Dank gilt **Ralf Winter** für seine Beiträge und Inspiration zu dieser Integration.

### Lizenz
Dieses Projekt steht unter der [GPL-3.0-Lizenz](LICENSE).

### Unterstütze das Projekt
Wenn dir dieses Projekt gefällt und du es unterstützen möchtest, kannst du mir einen Kaffee spendieren:  
[Buy me a coffee](https://buymeacoffee.com/route662)


