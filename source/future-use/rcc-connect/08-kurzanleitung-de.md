# RCC Connect – Kurzanleitung für Forschende

> **Entwurf für einen künftigen Pilotbetrieb.** RCC Connect ist noch kein
> offiziell freigegebener Download. Die Desktop-Verbindung und die
> Slurm-Entwicklungsumgebung müssen zuvor technisch abgenommen werden.

## Welche Oberfläche soll ich verwenden?

| Aufgabe | Empfohlene Oberfläche |
|---|---|
| R, Statistik, Tabellen und Grafiken | **Positron** auf dem Laptop |
| Python, Skripte, Shell und Debugging | **VS Code** auf dem Laptop |
| Notebooks und geführte Abläufe im Browser | **RCC Workbench** (geplant) |
| Lange oder wiederholte Berechnungen | **Slurm-Batch-Job** |

Die Berechnung läuft auf einem von **Slurm zugewiesenen Rechner**. Ein
Shellhost dient nur der Anmeldung, Dateibearbeitung und Job-Einreichung.
Große Berechnungen und unbeschränkte Verzeichnissuchen (z. B. `rg /projects`)
sollten dort nicht ausgeführt werden.

## Einrichtung des Laptops

Nach Freigabe durch RCC: Laden Sie das Installationspaket ausschließlich aus
einer offiziellen, geprüften RCC-Quelle herunter. Sie benötigen Ihren RCC-
Benutzernamen, einen registrierten SSH-Schlüssel, einen berechtigten Projekt-
zugang und gegebenenfalls die Gerätefreigabe/2FA.

**macOS** (Terminal im entpackten Installationsordner):

```sh
bash ./Install-macOS.command IHR_BENUTZERNAME
~/.local/bin/rcc-open doctor
```

**Windows** (PowerShell):

```powershell
powershell.exe -NoProfile -File .\Install-Windows.ps1 -RccUser IHR_BENUTZERNAME
powershell.exe -NoProfile -File "$HOME\.rcc\bin\rcc-open.ps1" doctor
```

`doctor` prüft lediglich die **lokale SSH-Konfiguration**. Vor der ersten
Verbindung müssen die SSH-Hostschlüssel anhand einer unabhängigen, offiziellen
RCC-Information überprüft werden. Unbekannte Hostschlüssel niemals ungeprüft
bestätigen oder die Prüfung deaktivieren.

## Eine R- oder Python-Sitzung starten

**macOS:**

```sh
~/.local/bin/rcc-open positron MEIN_PROJEKT
~/.local/bin/rcc-open vscode MEIN_PROJEKT
```

Unter Windows verwenden Sie dieselben Argumente mit `rcc-open.ps1`. Der
Launcher beantragt eine Slurm-Entwicklungssitzung und zeigt eine Job-ID
(z. B. `12345`) sowie ein SSH-Ziel (`rcc-dev-12345`). Öffnen Sie in der
gewählten Entwicklungsumgebung **Remote SSH** und anschließend den Ordner
`/projects/MEIN_PROJEKT`. Bei Positron muss die SSH-Anmeldung ohne interaktive
Nachfragen funktionieren; auch der Hostschlüssel des zugeteilten Workers
muss vorher verifiziert sein.

## Verbindung verloren?

**Keine zweite Sitzung auf Verdacht starten.** Prüfen Sie zunächst vorhandene
Slurm-Jobs und verbinden Sie sich mit der bestehenden Job-ID erneut:

```sh
~/.local/bin/rcc-open list
~/.local/bin/rcc-open attach positron MEIN_PROJEKT 12345
```

Zum Abschluss Ressourcen freigeben:

```sh
~/.local/bin/rcc-open stop 12345
```

Projektdateien gehören nach `/projects/MEIN_PROJEKT`. Temporäre Daten können
innerhalb eines Jobs nach `$TMPDIR`; sie können nach Jobende verloren gehen.
Weitere Hilfe: [Fehlerbehebung](06-troubleshooting.md) (Englisch; Übersetzung
für die Veröffentlichung vorgesehen).
## Sichere Wiederverbindung (v2.2)

Beim Wiederverbinden prüft RCC Connect, dass das Slurm-Job-Arbeitsverzeichnis exakt zum ausgewählten Projekt (`/projects/PROJEKT`) gehört. Bei fehlender Bestätigung: **keinen zweiten Job starten**, sondern zunächst `rcc-open list` prüfen.
