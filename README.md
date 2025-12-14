Tämän projektin aihe perustuu uuteen ARC Raiders pelin "ARC" robottivihollisiin, jotka tuhoutuessa pudottavat erilaisia materiaaleja. Tässä sovelluksessa käyttäjät pystyvät jakamaan erityyppiset ARC:it ja niiden mahdolliset pudotettavat materiaalit.
Jos et tiedä pelistä mitään voit aina keksiä omia asioita käyttäessä sovellusta.

# Kuinka käyttää sovellusta
Tein itse sovelluksen Windows-käyttöjärjestelmällä, joten en ole varma toimiiko sovellus muilla järjestelmillä, mutta Windowsilla sovellus ainakin toimii seuraavasti:

Lataamalla koko kansio "sw"

Avaamalla kansion sisällä oleva "app.py" (Huom. sovellus tulee avata kansion sw sisällä)

Kopioimalla sivun "osoite" mihin tahansa selaimeen

Tämän jälkeen sovelluksen pitäisi toimia

Jos haluat resetoida sovelluksen, poista kansiosta sw "database.db" ja tyhjennä selaimesta evästeet.

# Sovelluksen toiminnot:
Käyttäjä voi luoda tunnuksen ja salasanan

Käyttäjä voi lisätä/muokata/poistaa omia tietokohteita vihollisista (vihollisten nimet, mahdolliset palkinnot ja mistä vihollisen voi löytää).

Kaikkien käyttäjien lisäämät viholliset ovat nähtävissä kaikille (myös niille, joilla ei ole käytössä käyttäjää).

Käyttäjä (toimii myös ilman käyttäjää) voi käyttää hakukonetta ja etsiä vihollisen nimen, materiaalin tai materiaalien määrän mukaan käyttäjien tekemiä tietokohteita (oikeastaan voisi hakea mitä tahansa kunhan haun sisältö löytyy vihollisen nimestä tai mahdollisista palkinnoista)

Käyttäjät voivat jättää kommentteja toisten (tai omiin) vihollisten tietokohteisiin, jossa voivat antaa uutta tietoa alkuperäiseen tietokohteeseen (esim. x vihollinen pudotti minulla 3 y materiaalia, voitko päivittää tietokohdetta?).

Käyttäjäsivu jokaiselle käyttäjälle, mikä listaa kyseisen käyttäjän lisäämät tietokohteet sekä luku lisättyjen tietokohteiden ja kommenttien määrästä.

Käyttäjä pystyy valitsemaan jokaiselle viholliselle luokittelun, joka kertoo mistä vihollisen voi löytää (Esim. "Indoors" tai "Outdoors")

# Inspiraatiot ja lähteet
Sovellusta pääosin kehitettiin samoin tavoin kuin Antti Laaksosen videosarjassa

Lisäksi tietysti myös kurssimateriaalista on hyödynnetty joitakin kohtia, ja CurreChattia on hyödynnetty luomaan databasen muodostaminen Windows-ympäristössä ja korjaamaan joitakin bugeja
