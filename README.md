## Anonimiseringstool voor afbeeldingen

Deze tool is gebaseerd op de open source software
[Anonymizer van understand.AI](https://github.com/understand-ai/anonymizer).

## Wat doet de anonimiseringstool?
De tool herkent gezichten en nummerborden/kentekenplaten, en maakt een kopie van de afbeelding waarin de gedetecteerde gezichten en kentekens geblurred worden.

## Examples

![License Plate Example Raw](examples/coco02.jpg?raw=true "Title")
![License Plate Anonymized](examples/coco02_anonymized.jpg?raw=true "Title")

![Face Example Raw](examples/coco01.jpg?raw=true "Title")
![Face Example Anonymized](examples/coco01_anonymized.jpg?raw=true "Title")


## Installatievereisten
- Minstens 10 GB vrije schijfruimte + installatie van Docker Desktop
- Een GPU van Nvidia (niet vereist, maar sterk aangeraden voor ~50x snellere uitvoering)

**Heb ik een Nvidia GPU?**

Controleer als volgt: 
ctrl+alt+del &rightarrow; taakbeheer &rightarrow; (evt) meer details &rightarrow; prestaties/performance &rightarrow; 
kijk links bij GPU of er een NVIDIA model staat.

De anonimiseringssoftware gebruikt een Neuraal Netwerk (kunstmatige intelligentie) dat vele malen sneller is bij gebruik van een Nvidia GPU.

## Technische opbouw
De kern van deze software zijn twee neurale netwerken: De een is getraind om gezichten te herkennen, de andere om kentekenplaten/nummberborden te detecteren.
De neurale netwerken zijn geïmplementeerd met behulp van de Machine Learning library [Tensorflow](https://www.tensorflow.org/). 
De anonimiseringstool is geschreven in programmeertaal [Python](https://www.python.org/) en wordt in een virtual environment van het softwarepakket [Docker](https://www.docker.com/products/docker-desktop/) aangeboden. 

### Wat is Docker?
Docker is software waarmee je afgeschermde omgevingen (genaamd containers) kunt opzetten binnen je computer, compleet met eigen besturingssysteem.
Het eerste voordeel is dat onafhankelijk wat voor fratsen je uithaalt binnen zo'n container, alles daarbuiten onveranderd blijft en vice versa.
Je kunt dus ook geen conflicten kan krijgen met reeds geïnstalleerde programma's of instellingen buiten die omgeving.
Het tweede voordeel is dat alle gebruikers van dezelfde container gegarandeerd precies dezelfde software, instellingen, tools, versies, etc. hebben.
Hierdoor werkt iedereen in een identieke omgeving, die door de ontwikkelaar/beheerder van de container vastgelegd is.
Het derde voordeel is dat er een groot aantal losse componenten geïnstalleerd moeten worden om de anonimiseringstool werkend te krijgen,
en dat dat allemaal automatisch gebeurt tijdens het aanmaken van de Docker container.

## Installatie
1. Update je de drivers van de NVIDIA grafische kaart naar de nieuwste versie, minimaal versie 527.41.
Huidige versie controleren? Zoek in Windows naar Nvidia Control Panel, open de app. Als de versie-informatie niet direct zichtbaar is, kan je helemaal linksonder op System Information klikken; het eerste veld bij 'details' is de driver versie.
Links staat de naam van de grafische kaart, die je https://www.nvidia.com/download/index.aspx moet invoeren om de bijbehorende drivers te downloaden. Sluit het Nvidia Control Panel voor je de installatie start.
2. Installeer [Docker Desktop](https://www.docker.com/products/docker-desktop) met administrator-rechten (rechtermuisklik op Docker Desktop, "run as administrator")
   </br>1.a. Het zou kunnen dat je een onderdeel van windows genaamd WSL(2) moet downloaden of updaten om Docker te kunnen gebruiken. 
   Volg de download instructies op de website van Docker hiervoor.
3. Start Docker met administrator-rechten (rechtermuisklik op Docker Desktop, "run as administrator")
4. Scroll naar boven in deze pagina en klik rechts bovenaan op de groene <>Code knop, en Download als .zip bestand.
5. Pak het zip-bestand uit op een locatie op je computer waar je de software wilt installeren.
6. Start een Command Prompt door op de Windows start knop te drukken en te zoeken naar 'cmd'.
   *Rechter-muisklik op het command prompt, en kies om het command prompt uit te voeren met administrator-rechten.*
7. Ga in de command prompt naar de locatie waar de inhoud van het zipbestand staat. 
   Dit doe je door het commando 'cd LOCATIE' in te voeren.
Stel dat je het zipbestand in je downloads map hebt uitgepakt ("hier uitpakken"), dan is er een map aangemaakt genaamd Anonymizer-master met daarin een aantal bestanden. In dat geval typ je bijvoorbeeld:
```
cd C:\Users\GEBRUIKERSNAAM\Downloads\Anonymizer-master\
   ``` 

en druk op enter om het commando uit te voeren. 

*Tip: Je kan de locatie knippen en plakken. Soms werkt het plakken binnen het command prompt niet zoals gebruikelijk met ctrl+v maar d.m.v. een rechtermuisklik.*

8. Controleer dat je in de juiste locatie zit door het commando 'dir' in te voeren. 
   Als het goed is retourneert het command prompt dezelfde lijst van bestanden en mappen als bovenaan deze pagina, waaronder een bestand genaamd Dockerfile.

9. De 1-na laatste stap is het downloaden van de gewichten van de neurale netwerken.
Maak hiervoor eerst een map "weights" aan in de installatiemap waar je de zipfile hebt uitgepakt. 
In deze "weights" map, moet je de volgende twee bestanden zetten:
Gezichten: https://drive.google.com/file/d/1CwChAYxJo3mON6rcvXsl82FMSKj82vxF


nummerborden / kentekens: 
    https://drive.google.com/file/d/1Fls9FYlQdRlLAtw-GVS_ie1oQUYmci9g

Download deze 2 .pb bestanden van zo'n 180MB per stuk, en sla de twee op in de map genaamd "weights", dus 
als we het vorige voorbeeld volgen in de volgende map:
```
C:\Users\GEBRUIKERSNAAM\Downloads\Anonymizer-master\weights\
   ``` 
Mochten de twee .pb bestanden niet meer beschikbaar zijn op Google Drive, stuur dan een berichtje naar de beheerder.

10. De laatste stap: voer het volgende commando in; **Let op: Met deze stap wordt een paar GB (~7.5 GB) aan software gedownload en geïnstalleerd, dit zal een tijd duren.**   
```
docker build -t anon .
   ```

Er vliegt nu een hoop tekst door beeld in de command prompt. Zodra onderstaand bericht onderaan de tekst staat is de installatie geslaagd.
```
=> => naming to docker.io/library/anon
```

Indien de onderste regels een error weergeven, vraag om ondersteuning aan de beheerder en stuur de foutmelding en alle bijbehorende tekst mee.

11. Het laatste commando is:

```
docker compose build
   ```
Dit commando hoort in enkele seconden klaar te zijn en als onderste regel weer te geven:
```
=> => naming to docker.io/library/anonymizer-master-anon
```

Als alle bovenstaande stappen zonder foutmeldingen doorlopen zijn, is de tool nu gereed voor gebruik.

## Gebruik
1. De instellingen van de anonimiseringstool staan opgeslagen in een bestand genaamd "**.env**". Dit bestand staat net als de Dockerfile in het uitgepakte zipbestand en kan je openen met Kladblok/Notepad. Let op: Windows heeft soms de neiging om dit bestand te verbergen. Zie je het bestand niet en wil je het zichtbaar maken? In Windows Explorer staat bovenaan onder Beeld de optie om verborgen bestanden te tonen.
 Pas de instellingen aan naar wens en sla het bestand op. De meeste instellingen kunnen bij normaal gebruik ongewijzigd blijven, alleen de instellingen voor de input- en output folder zijn essentieel om goed in te stellen.
 *Let op: De naam van het .env bestand mag niet gewijzigd worden.*
2. Start Docker Desktop met administrator-rechten (rechter muisklik op het icoontje, "Als administrator uitvoeren")
3. Start een Command Prompt door op de Windows start knop te drukken en te zoeken naar 'cmd'.
   Rechter-muisklik op het command prompt, en kies om het command prompt uit te voeren met administrator-rechten.

4. Ga in de command prompt naar de locatie waar alle code voor de anonimiseringstool staat. 
   Dit doe je door het commando 'cd LOCATIE' in te voeren in de command prompt.
Stel dat je de code in je downloads map hebt uitgepakt onder de naam Anonymizer, dan typ je bijvoorbeeld:
```
cd C:\Users\GEBRUIKERSNAAM\Downloads\Anonymizer\
   ````
 en druk op enter om het commando uit te voeren.
</br> *Tip: Je kan de locatie knippen en plakken. Plakken werkt binnen het command prompt niet zoals gebruikelijk met ctrl+v maar d.m.v. een rechtermuisklik.*
5. Controleer dat je in de juiste locatie zit door het commando 'dir' in te voeren. 
   Als het goed is retourneert het command prompt dezelfde lijst van bestanden en mappen als bovenaan deze pagina, waaronder een bestand genaamd Dockerfile
6. Voer het volgende commando in; hiermee start je het anonimiseringsproces.   
```
docker compose run anon
   ````
7. Er verschijnt in de command prompt wat tekst waaronder een kopie van de gebruikte anonymizer-instellingen, en na 10 tot 30 seconden komt een voortgangsbalk in beeld. De output folder zal nu langzaam vollopen met geanonimiseerde afbeeldingen. Het proces is voltooid wanneer de volgende tekst getoond wordt: 
```
Successfully anonymized [] images.
```
8. Om de software na gebruik netjes af te sluiten, voer je het volgende commando in:
```
docker compose down
   ````
waarna je het command prompt kan wegklikken en Docker kan afsluiten.



## Software updaten
Indien het in de toekomst nodig is om aanpassingen aan de software te maken, zal dat gebeuren via de laatste twee stappen van het reguliere installatieproces zoals hierboven beschreven.
Zodra de beheerder van de software de gewenste aanpassingen aan de code heeft uitgevoerd, is die update binnen te halen met de volgende drie commando's in het command prompt:
1. Open het command prompt en navigeer naar de installatie-locatie, bijv:
```
cd C:\Users\GEBRUIKERSNAAM\Downloads\Anonymizer\
   ```

2. Het volgende commando download de nieuwste versie:
```
docker build -t anon .
   ```

3. Met dit laatste commando wordt de oude versie van de software vervangen door de nieuwere:
```
docker compose build
   ```

## Kwaliteit
Deze software probeert gezichten en kentekens te herkennen. Dit gaat echter niet altijd goed. Er zijn twee soorten fouten die gemaakt kunnen worden.

1. De meest impactvolle potentiële fout is dat een gezicht of kenteken niet geanonimiseerd wordt.
De verwachting is dat met standaard instellingen, ongeveer 80-90% van alle gezichten/hoofden geblurred wordt.
Voor kentekenplaten is de verwachting dat met gebruik van standaardinstellingen ongeveer 80-90% van alle identificeerbare kentekens geblurred worden.
Vooral kentekens die niet in het midden van de voor- of achterkant van het voertuig geplaatst zijn, worden niet altijd herkend.
Denk bijv. aan kentekenplaten geplaatst achter de voorwielen van een vrachtwagen.
Een andere belangrijke caveat is dat de anonimiseringstool getrained is op beelden die vanaf ooghoogte/dashcam-hoogte geschoten zijn.
Bij beelden met een hiervan sterk afwijkend perspectief zal de kwaliteit mogelijk suboptimaal zijn. 

2. Een minder impactvolle potentiële fout is een deel van de foto geblurred wordt die geen gezicht of kentekenplaat bevat.
Dit gebeurt normaalgesproken weinig (~1x per 10 foto's) bij standaardinstellingen, maar vooral de module voor kentekenplaten wil nog wel eens andere rechthoekige bebording als kentekenplaat aanzien en blurren.
Het is natuurlijk onwenselijk als er vaak onnodig grote delen van het beeldmateriaal onherkenbaar gemaakt wordt waar geen privacygevoelige gegevens op staan.

## Archief
Hieronder staat de originele documentatie van de anonimizer zoals die oorspronkelijk van het internet gehaald is.

## Installation

To install the anonymizer just clone this repository, create a new python3.6 environment and install the dependencies.  
The sequence of commands to do all this is

```bash
python -m venv ~/.virtualenvs/anonymizer
source ~/.virtualenvs/anonymizer/bin/activate

git clone https://github.com/understand-ai/anonymizer
cd anonymizer

pip install --upgrade pip
pip install -r requirements.txt
```

To make sure everything is working as intended run the test suite with the following command

```bash
pytest
```

Running the test cases can take several minutes and is dependent on your GPU (or CPU) and internet speed.  
Some test cases download model weights and some perform inference to make sure everything works as intended.


## Usage

In case you want to run the model on CPU, make sure that you install `tensorflow` instead of `tensorflow-gpu` listed
in the `requirements.txt`.

Since the weights will be downloaded automatically all that is needed to anonymize images is to run

```bash
PYTHONPATH=$PYTHONPATH:. python anonymizer/bin/anonymize.py --input /path/to/input_folder --image-output /path/to/output_folder --weights /path/to/store/weights
```

from the top folder of this repository. This will save both anonymized images and detection results as json-files to
the output folder.

### Advanced Usage

In case you do not want to save the detections to json, add the parameter `no-write-detections`.
Example:

```bash
PYTHONPATH=$PYTHONPATH:. python anonymizer/bin/anonymize.py --input /path/to/input_folder --image-output /path/to/output_folder --weights /path/to/store/weights --no-write-detections
```

Detection threshold for faces and license plates can be passed as additional parameters.
Both are floats in [0.001, 1.0]. Example:

```bash
PYTHONPATH=$PYTHONPATH:. python anonymizer/bin/anonymize.py --input /path/to/input_folder --image-output /path/to/output_folder --weights /path/to/store/weights --face-threshold=0.1 --plate-threshold=0.9
```

By default only `*.jpg` and `*.png` files are anonymized. To for instance only anonymize jpgs and tiffs, 
the parameter `image-extensions` can be used. Example:

```bash
PYTHONPATH=$PYTHONPATH:. python anonymizer/bin/anonymize.py --input /path/to/input_folder --image-output /path/to/output_folder --weights /path/to/store/weights --image-extensions=jpg,tiff
```

The parameters for the blurring can be changed as well. For this the parameter `obfuscation-kernel` is used.
It consists of three values: The size of the gaussian kernel used for blurring, it's standard deviation and the size
of another kernel that is used to make the transition between blurred and non-blurred regions smoother.
Example usage:

```bash
PYTHONPATH=$PYTHONPATH:. python anonymizer/bin/anonymize.py --input /path/to/input_folder --image-output /path/to/output_folder --weights /path/to/store/weights --obfuscation-kernel="65,3,19"
```

## Attributions

An image for one of the test cases was taken from the COCO dataset.  
The pictures in this README are under an [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode) license.
You can find the pictures [here](http://farm4.staticflickr.com/3081/2289618559_2daf30a365_z.jpg) and [here](http://farm8.staticflickr.com/7062/6802736606_ed325d0452_z.jpg).
