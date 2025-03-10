# IN2110

For å gjøre oppgavene i IN2110 trenger dere pakker som ikke finnes som standard på IFI sine Linux-maskiner. For å gjøre ting enklere har vi laget et ferdig utviklingsmiljø, i form av et såkalt _virtual environment_ som gir deg riktig versjon av python med de nødvendige pakkene tilgjengelig.

## Oppsett

Utviklingsmiljøet finnes ferdig installert på IFI sine maskiner, men kan også installeres på egen maskin.

### IFI sine maskiner (anbefalt)

Den enkleste måten å kjøre utviklingsmiljøet er å enten bruke en av IFI sine terminaler, eller logge inn på IFI sin login
server via ssh:

```
$ ssh <ditt-uio-brukernavn>@login.ifi.uio.no
```

Herfra kan du starte utviklingsmiljøet ved å kjøre:

```
[bruker@host ~]$ ~nikolhm/in2110-shared/in2110-shell
(in2110-env) [bruker@host ~]$ 
```

For å gå ut av miljøet kan du f.eks. gi kommandoen exit:
```
(in2110-env) [bruker@host ~]$ exit
[bruker@host ~]$ 
```

### Egen maskin

Vi bruker Python 3.6 i dette kurset og antar at dette allerede er tilgjengelig dersom du vil installere utviklingsmiljøet på egen maskin. For å installere miljøet, klon først dette git-repoet, cd til mappen in2110-shared, og kjør følgende kommando:

```
$ ./init-2110-env
```

Dette vil sette opp det virtuelle miljøet og installere de nødvendige pakkene (dette tar noen minutter). For å starte mijøet, kjør:

```
$ ./in2110-shell
```
eller på Windows bruk:


### Installering på Windows

Etter vår erfaring kan det være vanskelig å sette opp miljøet på Windows, men vi vet at følgende fungerer. Hvis du allerede har Python 3.6 på maskinen din, kan du prøve å kjøre

```
> .\init-2110-env.bat
```

Hvis alt fungerer, kan du da kjøre miljøet ved å skrive:

```
> .\in2110-shell.bat
```

Hvis ikke, anbefaler vi følgende. 
(1) Slett alle tidligere versjoner av Python, og last ned Python 3.6.8 fra Pythons hjemmeside https://www.python.org/downloads/ . Slett mappa "in2110-env" hvis du prøvde å kjøre init-2110-env.bat men det ikke fungerte. Kommandoen `python` må altså referere til Python 3.6.8 for at skriptet skal funke.
(2) Når du har lastet ned Python, kan du prøve å kjøre skriptet init-in2110-env.bat igjen.
(3) Underveis kan det hende at du får en feilmelding der du blir bedt om å laste ned Microsoft C++ Build Tools fra https://visualstudio.microsoft.com/visual-cpp-build-tools/. Hvis det skjer, gå inn på siden og last ned installasjonsprogrammet. Åpne programmet og kryss av på C++ build tools. På høyresiden kan du hake av flere bokser. Det virket for oss etter at vi haket av de fem øverste og de to nederste boksene. Merk at installasjonen krever omtrent 7.5 gigabyte ledig plass. 
(4) Når dette er på plass kan du prøve å kjøre skriptet en gang til. Nå skal det fungere!


## Bruk

Når du har startet utviklingsmiljøet kan du starte Python på vanlig måte:

```
$ python
```

Dette vil starte riktig versjon av Python med de nødvendige pakkene installert.

## Problemer

Om du har noen problemer med utviklingsmiljøet kan du spørre oss i forumet (dvs. [issues på semester-repoet](https://github.uio.no/IN2110/v21)). Det er viktig at du legger med full utskrift fra
terminal sånn at vi kan identifisere problemet.
