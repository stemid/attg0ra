# Att Göra

Hello, this is a Swedish project I made for learning more about Angular.js and Bottle.py. It's a Todo list manager but I will not use english anymore. 

Detta är alltså ett läroprojekt jag gjorde för att lära mig mer om Angular.js och Bottle.py, som båda var väldigt nya koncept för mig när jag började. 

Det långsiktiga målet var att kunna slutföra en större applikation jag arbetar på som också ska använda sig av Angular, jag kunde inte fortsätta på den eftersom jag saknade förståelse för vad jag gjorde. 

Att göra betyder att det är en lista av saker att göra, kallas en Todo Lista på engelska. 

Den är gjord i två delar, först ett JSON gränssnitt mot en databas, och sedan ett gränssnitt i HTML och Javascript. 

# Installation

## JSON Server

Eftersom applikationen är gjord i två delar så måste man även installera den på det viset, först kan man antingen starta JSON gränssnittet med den inbyggda webbservern så här. 

    python attg0ra.py

Redigera filen attg0ra.cfg för att avgöra var den ska lyssna, det är ingen arbetshäst men den duger för en personlig lista. 

### WSGI

Att göra: Skriv om hur man driftar servern med Nginx/Apache och WSGI. 

## Webbgränssnitt 

Webbgränssnittet kräver bara en webbläsare som kan läsa HTML egentligen, problemet är att filerna i katalogen public/ måste kunna läsa filerna i katalogen static/assets/js/. Därför kan man använda en simpel nginx konfiguration. 

    server {
      listen 8000;
      server_name localhost;
      location / {
        root attg0ra/public;
        index index.html;
      }
      location /static {
        alias attg0ra/static;
      }
    }

Redigera sedan filen attg0ra.cfg och se till att ui_host stämmer överens med värdnamnet där ni använder webbgränssnittet. En begäran mot JSON gränssnittet måste komma från den adressen för att fungera. 

## Databas

Att göra: Skriv mer om databasen. Det ligger ett databasschema i katalogen tools/. 
