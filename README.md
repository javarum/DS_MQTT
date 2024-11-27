1. **Machine Registration and Identification**

Maschinen identifizieren sich beim Start mit einem eindeutigen Namen oder einer Id (z. B. factory/machines/register).
   
2. **Publishing Sensor Data**

Maschinen veröffentlichen regelmäßig Sensordaten (z. B. Vibration, Temperatur, Fehlercodes)
   
3. **Timestamp for each message**

Jede Nachricht enthält einen Zeitstempel und eventuell die gemessenen Werte.
   
4. **Machine Shutdown**

Wenn eine kritische Warnung erkannt wird, sendet das zentrale System einen Shutdown-Befehl