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

# Vad har jag lärt mig?

## Bottle.py

Behöver inte gå in djupt här eftersom det påminner mycket om web.py men detta var mitt första projekt i bottle så helt klart har man lärt sig saker. 

### CORS med OPTIONS

Det är ju självklart nu men tog mig ett tag att förstå, eftersom Angulars gränssnitt körs under en helt annan domän än JSON gränssnittet så måste man ju tillåta den domänen att göra anrop. Annars hade det varit en enorm säkerhetsrisk. 

Angular gör OPTIONS anrop när den ser att domänen inte matchar, den letar då efter vissa HTTP headers som ska tala om främst vilka domäner som är tillåtna, vilka andra headers och vilka metoder. 

Dessa speciella headers fick jag stoppa in i varje route-funktion, hade varit kul att kunna göra det globalt men jag vet inte hur än.

### Less is more

Todo.Database är så minimal som möjligt. 

### Debug

Bottle verkar ännu mer minimal än web.py i hur den knyter upp stdout för svar till klienter. I web.py skickas ju t.ex. print-data direkt till konsollen där man startat servern. I bottle så försvinner datan om den inte skickas till stderr istället. 

### JSONEncoder

Detta förstod jag redan men bra att nämna möjligheten att returnera vilket JSON-kompatibelt objekt som helst med DateEncoder klassen som ärver från JSONEncoder. 

Hjälpte när jag hade problem i Angular med datumformatet. 

## ConfigParser

Dagarna då jag använde json-filer för konfiguration är över. 

## Angular.js

Lärde mig otroligt mycket eftersom jag aldrig arbetat med något liknande. Det har tagit mig väldigt lång tid också eftersom jag stapplat mig fram utan att ha en djup förståelse för Javascript OOP som jag tror hade hjälpt. 

Ska inte nämna självklara saker som routes och controllers eftersom man lär sig det i Angulars phonecat tutorial. 

### CORS

Här fick jag aktivera CORS med $httpProvider i config(). 

    $httpProvider.defaults.useXDomain = true;

Se js/todo.js för mer info. 

### Arv

$httpProvider är som en mall för $http, så man kan ange standardvärden där som ärvs ner till $http senare i koden. 

T.ex. hur jag anger ett standardvärde i app.config() med $httpProvider och sedan drar nytta av det i en controller när jag använder $http-tjänsten. 

Ursäkta svengelskan...

### Filter

Har skapat filter när jag gick igenom Angular Phonecat tutorial men det var kul att få ett skarpt fall i js/todo.js också. 

Filtret cutOffString i js/todo.js var också ett bra exempel på injektion av beroenden i filter och standardargument för Javascript-funktioner. 
