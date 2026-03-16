# LexiScan - Systemövergripande Ordbok

En GTK4/Adwaita-app som ger dig ordbok-uppslagning direkt i alla applikationer genom att markera text.

## Funktioner

- **Urklippsövervakning** - Markera text i valfri app för automatisk ordbok-uppslagning
- **Svenska-Engelska ordbok** - Stöd för översättning i båda riktningar
- **Definitioner** - Visar ordets betydelse, ordklass och exempel
- **Uttal** - Fonetisk transkription (IPA) med ljuduppspelning
- **Bildstöd** - ARASAAC-piktogram för visuellt stöd
- **Kortkommandon** - Ctrl+Shift+D för att aktivera/avaktivera
- **Modernt gränssnitt** - GTK4 med Adwaita-design

## Skärmbilder

Appen visar en popup med:
- Ordets uttal och fonetik
- Definitioner med exempel
- Svenska-engelska översättningar
- ARASAAC-piktogram (bildstöd)

## Installation

### Systemkrav

- Python 3.9+
- GTK4 och libadwaita
- X11 (för urklippsövervakning)
- xclip eller xsel

### Ubuntu/Debian

```bash
# Installera systemberoenden
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 \
    gir1.2-gdkpixbuf-2.0 xclip

# Klona repot
git clone https://github.com/yeager/LexiScan.git
cd LexiScan

# Installera Python-beroenden
pip install -r requirements.txt

# Installera appen
pip install -e .
```

### Fedora

```bash
sudo dnf install python3-gobject gtk4 libadwaita python3-cairo xclip
git clone https://github.com/yeager/LexiScan.git
cd LexiScan
pip install -r requirements.txt
pip install -e .
```

### Arch Linux

```bash
sudo pacman -S python-gobject gtk4 libadwaita python-cairo xclip
git clone https://github.com/yeager/LexiScan.git
cd LexiScan
pip install -r requirements.txt
pip install -e .
```

## Användning

### Starta appen

```bash
lexiscan
# eller
python -m lexiscan
```

### Kortkommandon

| Kortkommando | Funktion |
|---|---|
| `Ctrl+Shift+D` | Aktivera/avaktivera overlay |
| `Ctrl+Shift+L` | Tvinga uppslagning av markerad text |
| `Ctrl+Q` | Avsluta |
| `Escape` | Stäng popup |

### Användning

1. Starta LexiScan
2. Markera text i valfri applikation
3. En popup visas med definition, uttal, översättning och bildstöd
4. Klicka på högtalarikonen för att höra uttalet
5. Använd sökfältet för manuell sökning

## Skrivbordsintegration

Kopiera desktop-filen för att LexiScan ska synas i programmenyn:

```bash
cp data/com.github.lexiscan.desktop ~/.local/share/applications/
```

För autostart:

```bash
cp data/com.github.lexiscan.desktop ~/.config/autostart/
```

## API-tjänster

LexiScan använder följande fria API:er:

- **Free Dictionary API** - Engelska och svenska definitioner
- **Folkets Lexikon** (KTH) - Svenska-engelska översättningar
- **MyMemory Translation** - Fallback-översättning
- **ARASAAC** - Piktogram/bildstöd

Inget API-nyckel krävs.

## Utveckling

```bash
git clone https://github.com/yeager/LexiScan.git
cd LexiScan
pip install -e .
python -m lexiscan
```

### Översättningar

Redigera `.po`-filer i `po/`-mappen. Generera ny `.pot`-fil:

```bash
xgettext --language=Python --keyword=_ -o po/lexiscan.pot \
    lexiscan/*.py lexiscan/**/*.py
```

## Licens

GPL-3.0 - Se [LICENSE](LICENSE)

## Tack till

- [ARASAAC](https://arasaac.org/) - Piktogram under Creative Commons BY-NC-SA
- [Free Dictionary API](https://dictionaryapi.dev/)
- [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/) - KTH
