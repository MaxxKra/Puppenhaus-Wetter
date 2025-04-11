
# 🧸🌤️ Puppenhaus Wetter – Custom Weather Entity für Home Assistant

Willkommen zur offiziellen Integration **"Puppenhaus Wetter"**, einer voll simulierten `weather`-Entität für dein Home Assistant Dashboard – perfekt für Miniaturwelten, Smarthome-Demoboards oder kreative Projekte wie das **Smarthome Puppenhaus**! 🏡✨

![Puppenhaus Wetter in Aktion](https://github.com/MaxxKra/Puppenhaus-Wetter/raw/main/images/dashboard_example.png)

---

## 🔧 Features

✅ Echte `weather.`-Entität für Home Assistant  
✅ Kompatibel mit Wetterkarten und Forecast-Kacheln  
✅ Nutzt simulierte Sensorwerte (z. B. Potis, Schalter, Input-Number etc.)  
✅ Automatische Umschaltung auf `clear-night` bei Nacht  
✅ Feels-like Temperatur  
✅ Forecast mit drei Zeitpunkten  
✅ Kompatibel mit HA 2024+  
✅ Keine externe API notwendig – läuft lokal & offline!

---

## 📦 Installation

> 📥 Via HACS (manuell)

1. HACS → Integrationen → Repositories → Benutzerdefiniertes Repo hinzufügen  
2. URL: `https://github.com/MaxxKra/Puppenhaus-Wetter`  
3. Typ: `Integration`  
4. Installieren, dann HA neustarten

---

## 🛠️ Manuelle Installation

1. Repository klonen oder ZIP herunterladen  
2. Inhalt in deinen Ordner `custom_components/puppenhaus_weather/` kopieren  
3. In deiner `configuration.yaml` hinzufügen:

```yaml
weather:
  - platform: puppenhaus_weather
```

4. Home Assistant neustarten

---

## 🧪 Beispiel-Dashboard

Du kannst die Entität direkt in einer `weather-forecast` Karte verwenden:

```yaml
type: weather-forecast
entity: weather.puppenhaus_wetter
```

![Lovelace Vorschau](https://github.com/MaxxKra/Puppenhaus-Wetter/raw/main/images/weather_card.png)

---

## 📸 Sensorquellen

Diese Integration nutzt u. a. folgende (simulierte) Sensoren:

| Sensor                              | Typ           |
|-------------------------------------|----------------|
| `sensor.umwelttableau_aussentemperatur` | Temperatur   |
| `sensor.umwelttableau_wolkendichte`     | Bewölkung    |
| `sensor.umwelttableau_windgeschwindigkeit` | Wind      |
| `binary_sensor.umwelttableau_regen`     | Regen an/aus |
| `binary_sensor.umwelttableau_gewitter`  | Gewitter     |
| `sensor.umwelttableau_sonnenstand`      | Sonnenstand  |

---

## ❤️ Für wen ist das?

Diese Integration richtet sich an:

- Entwickler:innen von Smart-Home-Demoboards  
- Home Assistant Bastler mit Sinn für Show & Spaß  
- Menschen mit Miniaturhäusern, die echt Wetter brauchen 😄

---

## 🧑‍💻 Code & Mitwirken

Pull Requests & Issues willkommen!  
👉 [GitHub Repository ansehen](https://github.com/MaxxKra/Puppenhaus-Wetter)

---

## 🧡 Unterstützt durch:  
[Smart Home Bastler – YouTube & Tools](https://smarthomebastler.de)

---

**Viel Spaß beim Basteln!**
