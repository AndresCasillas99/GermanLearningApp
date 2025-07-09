import pandas as pd
import streamlit as st
import re
import random
import spacy
from termcolor import colored

#Large fonts
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 1.3em !important;
    }
    .stRadio > div, .stSelectbox > div, .stTextInput > div, .stButton > button {
        font-size: 1.3em !important;
    }
    .stRadio label, .stSelectbox label {
        font-size: 1.3em !important;
    }
    .stTitle {
        font-size: 2.2em !important;
    }
    </style>
""", unsafe_allow_html=True)

#Title
title = st.markdown("""
<span style='font-size:2.2em; font-weight:bold'>
  <span style='color:black'>German</span>
  <span style='color:red'> Language</span>
  <span style='color:gold'> Practice</span>
  </span>
</span>
""", unsafe_allow_html=True)
st.markdown("""<span style='font-size:1.6em; vertical-align:right; margin-left:15px'>
    <span style='color:black'>by</span>
    <span style='color:black'> Andrés 😎</span>
    <span style='color:black'> 😎 </span>
    😎🇩🇪🇩🇪🇩🇪
  </span>
</span>
""", unsafe_allow_html=True)

#Translation sidebar CSS
st.markdown("""
    <style>
    /* Make all Streamlit text input boxes light grey */
    .stTextInput input, .stTextArea textarea {
        background-color: #f5f5f5 !important;
        border-radius: 8px !important;
        border: 1px solid #ccc !important;
    }
    </style>
""", unsafe_allow_html=True)


if st.session_state.get("start_clicked", False):
    # Pick a random mode
    st.session_state.random_mode = random.choice([
        "Word practice",
        "Sentence practice",
        "Translate words",
        "Translate sentences",
        "Pronoun declination practice",
        "Possessive, reflexive, relative and indefinite pronoun practice"
    ])
    st.session_state.start_clicked = False


#Define modes
modes = [
    "Word practice",
    "Sentence practice",
    "Translate words",
    "Translate sentences",
    "Pronoun declination practice",
    "Possessive, reflexive, relative and indefinite pronoun practice"
]


if "mode" not in st.session_state:
    st.session_state["mode"] = modes[0]

red_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
        font-size: 3.3em;
    }
    </style>
    """, unsafe_allow_html=True)

if st.button("Random mode!"):
    st.session_state["mode"] = random.choice(modes)

#Sidebar menu
mode = st.sidebar.radio("Choose your practice mode (or click the random mode button):", modes, key="mode")

# ...existing code...

#CSS for sidebar styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: lightblue;
        );
        border-radius: 18px;
        padding: 24px 16px 24px 16px;
        margin: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    }
    </style>
""", unsafe_allow_html=True)

# ...existing code...

active_mode = mode

raw_data = """ 
    1. Time	Die Zeit	Die Zeiten
    2. Man Der Mann	Die Männer
    3. Hand	Die Hand	Die Hände
    4. Day	Der Tag	Die Tage
    5. Way	Der Weg	Die Wege
    6. Eye	Das Auge	Die Augen
    7. Thing	Die Sache	Die Sachen
    8. Head	Der Kopf	Die Köpfe
    9. Year	Das Jahr	Die Jahre
    10. Room	Das Zimmer	Die Zimmer
    11. Door	Die Tür	Die Türen
    12. Woman	Die Frau	Die Frauen
    13. Face	Das Gesicht	Die Gesichter
    14. Mother	Die Mutter	Die Mütter
    15. People	Die Leute	-
    16. Night	Die Nacht	Die Nächte
    17. House	Das Haus	Die Häuser
    18. Father	Der Vater	Die Väter
    19. Life	Das Leben	Die Leben
    20. Back	Der Rücken	Die Rücken
    21. Voice	Die Stimme	Die Stimmen
    22. Girl	Das Mädchen	Die Mädchen
    23. Place	Der Ort	Die Orte
    24. Boy	Der Junge	Die Jungen
    25. Car	Das Auto	Die Autos
    26. Side	Die Seite	Die Seiten
    27. Arm	Der Arm	Die Arme
    28. Child	Das Kind	Die Kinder
    29. Word	Das Wort	Die Wörter
    30. Moment	Der Moment	Die Momente
    31. Hair	Das Haar	Die Haare
    32. Foot	Der Fuß	Die Füße
    33. Water	Das Wasser	-
    34. Light	Das Licht	Die Lichter
    35. World	Die Welt	Die Welten
    36. Name	Der Name	Die Namen
    37. Friend	Der Freund	Die Freunde
    38. Window	Das Fenster	Die Fenster
    39. Body	Der Körper	Die Körper
    40. Table	Der Tisch	Die Tische
    41. Morning	Der Morgen	Die Morgen
    42. Bed	Das Bett	Die Betten
    43. Wall	Die Wand	Die Wände
    44. Street	Die Straße	Die Straßen
    45. School	Die Schule	Die Schulen
    46. Air	Die Luft	-
    47. Floor	Der Boden	Die Böden
    48. Hour	Die Stunde	Die Stunden
    49. End	Das Ende	Die Enden
    50. Family	Die Familie	Die Familien
    51. Guy	Der Kerl	Die Kerle
    52. Kind	Das Kind	Die Kinder
    53. Minute	Die Minute	Die Minuten
    54. Story	Die Geschichte	Die Geschichten
    55. God	Der Gott	Die Götter
    56. Week	Die Woche	Die Wochen
    57. Work	Die Arbeit	-
    58. Shoulder	Die Schulter	Die Schultern
    59. Part	Der Teil	Die Teile
    60. Mind	Der Verstand	-
    61. Book	Das Buch	Die Bücher
    62. Finger	Der Finger	Die Finger
    63. Mouth	Der Mund	Die Münder
    64. Kid	Das Kind	Die Kinder
    65. Glass	Das Glas	Die Gläser
    66. Tree	Der Baum	Die Bäume
    67. Sound	Der Klang	Die Klänge
    68. Line	Die Linie	Die Linien
    69. Wife	Die Ehefrau	Die Ehefrauen
    70. Heart	Das Herz	Die Herzen
    71. Money	Das Geld	-
    72. Phone	Das Telefon	Die Telefone
    73. Look	Der Blick	Die Blicke
    74. Leg	Das Bein	Die Beine
    75. Chair	Der Stuhl	Die Stühle
    76. Office	Das Büro	Die Büros
    77. Brother	Der Bruder	Die Brüder
    78. Question	Die Frage	Die Fragen
    79. City	Die Stadt	Die Städte
    80. Month	Der Monat	Die Monate
    81. Baby	Das Baby	Die Babys
    82. Home	Das Zuhause	Die Zuhause
    83. Dog	Der Hund	Die Hunde
    84. Road	Die Straße	Die Straßen
    85. Idea	Die Idee	Die Ideen
    86. Kitchen	Die Küche	Die Küchen
    87. Lot	Das Grundstück	Die Grundstücke
    88. Son	Der Sohn	Die Söhne
    89. Job	Der Job	Die Jobs
    90. Paper	Das Papier	Die Papiere
    91. Sister	Die Schwester	Die Schwestern
    92. Smile	Das Lächeln	Die Lächeln
    93. Point	Der Punkt	Die Punkte
    94. Thought	Der Gedanke	Die Gedanken
    95. Love	Die Liebe	-
    96. Town	Die Stadt	Die Städte
    97. Death	Der Tod	Die Tode
    98. Ground	Der Boden	Die Böden
    99. Others	Die Anderen	-
    100. Fire	Das Feuer	Die Feuer
    101. Step	Der Schritt	Die Schritte
    102. Blood	Das Blut	-
    103. Fact	Die Tatsache	Die Tatsachen
    104. Breath	Der Atem	Die Atemzüge
    105. Lip	Die Lippe	Die Lippen
    106. Sun	Die Sonne	Die Sonnen
    107. Building	Das Gebäude	Die Gebäude
    108. Number	Die Nummer	Die Nummern
    109. Husband	Der Ehemann	Die Ehemänner
    110. Parent	Der Elternteil	Die Elternteile
    111. Corner	Die Ecke	Die Ecken
    112. Problem	Das Problem	Die Probleme
    113. Couple	Das Paar	Die Paare
    114. Daughter	Die Tochter	Die Töchter
    115. Bag	Die Tasche	Die Taschen
    116. Hell	Die Hölle	-
    117. Rest	Die Ruhe	-
    118. Business	Das Geschäft	Die Geschäfte
    119. Sky	Der Himmel	Die Himmel
    120. Box	Die Schachtel	Die Schachteln
    121. Person	Die Person	Die Personen
    122. Reason	Der Grund	Die Gründe
    123. Right	Das Recht	-
    124. Skin	Die Haut	Die Häute
    125. Dad	Der Vater	Die Väter
    126. Case	Der Fall	Die Fälle
    127. Piece	Das Stück	Die Stücke
    128. Doctor	Der Arzt	Die Ärzte
    129. Edge	Der Rand	Die Ränder
    130. Mom	Die Mutter	Die Mütter
    131. Picture	Das Bild	Die Bilder
    132. Sense	Der Sinn	Die Sinne
    133. Ear	Das Ohr	Die Ohren
    134. Second	Die Sekunde	Die Sekunden
    135. Lady	Die Dame	Die Damen
    136. Neck	Der Hals	Die Hälse
    137. Wind	Der Wind	Die Winde
    138. Desk	Der Schreibtisch	Die Schreibtische
    139. Gun	Die Waffe	Die Waffen
    140. Stone	Der Stein	Die Steine
    141. Coffee	Der Kaffee	Die Kaffees
    142. Ship	Das Schiff	Die Schiffe
    143. Earth	Die Erde	-
    144. Food	Das Essen	-
    145. Horse	Das Pferd	Die Pferde
    146. Field	Das Feld	Die Felder
    147. War	Der Krieg	Die Kriege
    148. Afternoon	Der Nachmittag	Die Nachmittage
    149. Sir	Der Herr	Die Herren
    150. Space	Der Raum	Die Räume
    151. Evening	Der Abend	Die Abende
    152. Letter	Der Brief	Die Briefe
    153. Bar	Die Bar	Die Bars
    154. Dream	Der Traum	Die Träume
    155. Apartment	Die Wohnung	Die Wohnungen
    156. Chest	Die Brust	Die Brüste
    157. Game	Das Spiel	Die Spiele
    158. Summer	Der Sommer	Die Sommer
    159. Matter	Die Angelegenheit	Die Angelegenheiten
    160. Silence	Die Stille	-
    161. Top	Die Spitze	Die Spitzen
    162. Rock	Der Felsen	Die Felsen
    163. Power	Die Macht	-
    164. Clothes	Die Kleidung	-
    165. Sign	Das Schild	Die Schilder
    166. Attention	Die Aufmerksamkeit	-
    167. Music	Die Musik	-
    168. State	Der Zustand	Die Zustände
    169. Pocket	Die Tasche	Die Taschen
    170. Dinner	Das Abendessen	Die Abendessen
    171. Hall	Der Saal	Die Säle
    172. Pain	Der Schmerz	Die Schmerzen
    173. Age	Das Alter	-
    174. River	Der Fluss	Die Flüsse
    175. Chance	Die Chance	Die Chancen
    176. Nose	Die Nase	Die Nasen
    177. Shadow	Der Schatten	Die Schatten
    178. Police	Die Polizei	-
    179. Memory	Die Erinnerung	Die Erinnerungen
    180. Color	Die Farbe	Die Farben
    181. Knee	Das Knie	Die Knie
    182. Wood	Das Holz	-
    183. Shirt	Das Hemd	Die Hemden
    184. Party	Die Party	Die Partys
    185. Country	Das Land	Die Länder
    186. Truck	Der Lastwagen	Die Lastwagen
    187. Tooth	Der Zahn	Die Zähne
    188. Bill	Die Rechnung	Die Rechnungen
    189. Scene	Die Szene	Die Szenen
    190. Land	Das Land	Die Länder
    191. Star	Der Stern	Die Sterne
    192. Bird	Der Vogel	Die Vögel
    193. Bedroom	Das Schlafzimmer	Die Schlafzimmer
    194. Uncle	Der Onkel	Die Onkel
    195. Sort	Die Art	-
    196. Group	Die Gruppe	Die Gruppen
    197. Truth	Die Wahrheit	Die Wahrheiten
    198. Trouble	Die Schwierigkeit	-
    199. Crowd	Die Menschenmenge	Die Menschenmengen
    200. Station	Der Bahnhof	Die Bahnhöfe
    201. Tear	Die Träne	Die Tränen
    202. Class	Die Klasse	Die Klassen
    203. Sea	Das Meer	Die Meere
    204. Animal	Das Tier	Die Tiere
    205. Center	Das Zentrum	Die Zentren
    206. Feeling	Das Gefühl	Die Gefühle
    207. Store	Das Geschäft	Die Geschäfte
    208. Mountain	Der Berg	Die Berge
    209. News	Die Nachrichten	-
    210. Shoe	Der Schuh	Die Schuhe
    211. Cat	Die Katze	Die Katzen
    212. Screen	Der Bildschirm	Die Bildschirme
    213. Bottle	Die Flasche	Die Flaschen
    214. Call	Der Anruf	Die Anrufe
    215. Living	Das Wohnzimmer	Die Wohnzimmer
    216. Cheek	Die Wange	Die Wangen
    217. Student	Der Student	Die Studenten
    218. Ball	Der Ball	Die Bälle
    219. Sight	Der Anblick	Die Anblicke
    220. Hill	Der Hügel	Die Hügel
    221. Company	Das Unternehmen	Die Unternehmen
    222. Church	Die Kirche	Die Kirchen
    223. Rain	Der Regen	Die Regen
    224. Suit	Der Anzug	Die Anzüge
    225. One	Die Eins	-
    226. Direction	Die Richtung	Die Richtungen
    227. Will	Der Wille	-
    228. Throat	Der Hals	Die Hälse
    229. Middle	Die Mitte	-
    230. Answer	Die Antwort	Die Antworten
    231. Stuff	Das Zeug	-
    232. Hospital	Das Krankenhaus	Die Krankenhäuser
    233. Camera	Die Kamera	Die Kameras
    234. Dress	Das Kleid	Die Kleider
    235. Card	Die Karte	Die Karten
    236. Yard	Der Hof	Die Höfe
    237. Dark	Die Dunkelheit	-
    238. Shit	Die Scheiße	-
    239. Image	Das Bild	Die Bilder
    240. Machine	Die Maschine	Die Maschinen
    241. Distance	Die Entfernung	Die Entfernungen
    242. Area	Das Gebiet	Die Gebiete
    243. Narrator	Der Erzähler	Die Erzähler
    244. Ice	Das Eis	Die Eis
    245. Snow	Der Schnee	-
    246. Note	Die Notiz	Die Notizen
    247. Mirror	Der Spiegel	Die Spiegel
    248. King	Der König	Die Könige
    249. Fear	Die Angst	-
    250. Officer	Der Beamte	Die Beamten
    251. Hole	Das Loch	Die Löcher
    252. Shot	Der Schuss	Die Schüsse
    253. Guard	Der Wächter	Die Wächter
    254. Conversation	Das Gespräch	Die Gespräche
    255. Boat	Das Boot	Die Boote
    256. System	Das System	Die Systeme
    257. Care	Die Sorge	Die Sorgen
    258. Bit	Das Bit	Die Bits
    259. Movie	Der Film	Die Filme
    260. Bone	Der Knochen	Die Knochen
    261. Page	Die Seite	Die Seiten
    262. Captain	Der Kapitän	Die Kapitäne
    263. Aunt	Die Tante	Die Tanten
    264. Darkness	Die Dunkelheit	-
    265. Control	Die Kontrolle	Die Kontrollen
    266. Drink	Das Getränk	Die Getränke
    267. Hotel	Das Hotel	Die Hotels
    268. Coat	Der Mantel	Die Mäntel
    269. Stair	Die Treppe	Die Treppen
    270. Order	Die Bestellung	Die Bestellungen
    271. Rose	Die Rose	Die Rosen
    272. Miss	Die Miss	-
    273. Hat	Der Hut	Die Hüte
    274. Gold	Das Gold	-
    275. Cigarette	Die Zigarette	Die Zigaretten
    276. Cloud	Die Wolke	Die Wolken
    277. View	Die Aussicht	Die Aussichten
    278. Driver	Der Fahrer	Die Fahrer
    279. Cup	Die Tasse	Die Tassen
    280. Figure	Die Figur	Die Figuren
    281. Expression	Der Ausdruck	Die Ausdrücke
    282. Path	Der Weg	Die Wege
    283. Key	Der Schlüssel	Die Schlüssel
    284. Computer	Der Computer	Die Computer
    285. Flower	Die Blume	Die Blumen
    286. Ring	Der Ring	Die Ringe
    287. Bathroom	Das Badezimmer	Die Badezimmer
    288. Metal	Das Metall	Die Metalle
    289. Moon	Der Mond	Die Monde
    290. Song	Das Lied	Die Lieder
    291. Soldier	Der Soldat	Die Soldaten
    292. Radio	Das Radio	Die Radios
    293. History	Die Geschichte	Die Geschichten
    294. Wave	Die Welle	Die Wellen
    295. Plan	Der Plan	Die Pläne
    296. College	Das College	Die Colleges
    297. Fish	Der Fisch	Die Fische
    298. Garden	Der Garten	Die Gärten
    299. Train	Der Zug	Die Züge
    300. Shop	Das Geschäft	Die Geschäfte
    301. Cop	Der Polizist	Die Polizisten
    302. Art	Die Kunst	-
    303. Beer	Das Bier	Die Biere
    304. North	Der Norden	-
    305. Island	Die Insel	Die Inseln
    306. Bus	Der Bus	Die Busse
    307. Smell	Der Geruch	Die Gerüche
    308. Noise	Das Geräusch	Die Geräusche
    309. Mama	Mama	-
    310. Park	Der Park	Die Parks
    311. South	Der Süden	-
    312. Pair	Das Paar	Die Paare
    313. Lord	Der Herr	Die Herren
    314. Plate	Der Teller	Die Teller
    315. Jacket	Die Jacke	Die Jacken
    316. Help	Die Hilfe	Die Hilfen
    317. Daddy	Der Papa	Die Papas
    318. Grass	Das Gras	Die Gräser
    319. Thanks	Der Dank	Die Danksagungen
    320. Heat	Die Hitze	-
    321. Sleep	Der Schlaf	-
    322. Brain	Das Gehirn	Die Gehirne
    323. Service	Der Service	Die Services
    324. Trip	Die Reise	Die Reisen
    325. Beat	Der Schlag	Die Schläge
    326. Knife	Das Messer	Die Messer
    327. Spot	Der Fleck	Die Flecken
    328. Message	Die Nachricht	Die Nachrichten
    329. Mark	Das Zeichen	Die Zeichen
    330. Teacher	Der Lehrer	Die Lehrer
    331. Gaze	Der Blick	Die Blicke
    332. Village	Das Dorf	Die Dörfer
    333. Winter	Der Winter	Die Winter
    334. Front	Die Front	Die Fronten
    335. Law	Das Gesetz	Die Gesetze
    336. Surface	Die Oberfläche	Die Oberflächen
    337. Bank	Die Bank	Die Banken
    338. Team	Das Team	Die Teams
    339. Maximum	Das Maximum	Die Maxima
    340. Position	Die Position	Die Positionen
    341. Stomach	Der Magen	Die Mägen
    342. Turn	Die Wende	-
    343. West	Der Westen	-
    344. Lunch	Das Mittagessen	Die Mittagessen
    345. Change	Die Veränderung	Die Veränderungen
    346. Creature	Das Lebewesen	Die Lebewesen
    347. Soul	Die Seele	Die Seelen
    348. Leaf	Das Blatt	Die Blätter
    349. Show	Die Show	Die Shows
    350. Gate	Das Tor	Die Tore
    351. Palm	Die Palme	Die Palmen
    352. Plastic	Das Plastik	-
    353. Force	Die Kraft	Die Kräfte
    355. Beach	Der Strand	Die Strände
    356. President	Der Präsident	Die Präsidenten
    357. Shape	Die Form	Die Formen
    358. Smoke	Der Rauch	Die Rauch
    359. Wheel	Das Rad	Die Räder
    360. Silver	Das Silber	-
    361. Roof	Das Dach	Die Dächer
    362. Weight	Das Gewicht	Die Gewichte
    363. Tongue	Die Zunge	Die Zungen
    364. Tea	Der Tee	Die Tees
    365. Track	Die Strecke	Die Strecken
    366. Angle	Der Winkel	Die Winkel
    367. Form	Die Form	Die Formen
    368. Tone	Der Ton	Die Töne
    369. Circle	Der Kreis	Die Kreise
    370. Spring	Der Frühling	Die Frühlinge
    371. Porch	Die Veranda	Die Veranden
    372. Sheet	Das Blatt	Die Blätter
    373. Member	Das Mitglied	Die Mitglieder
    374. Pool	Der Pool	Die Pools
    375. Need	Das Bedürfnis	Die Bedürfnisse
    376. Hope	Die Hoffnung	Die Hoffnungen
    377. Lake	Der See	Die Seen
    378. Breast	Die Brust	Die Brüste
    379. Surprise	Die Überraschung	Die Überraschungen
    380. Interest	Das Interesse	-
    381. Bottom	Der Boden	Die Böden
    382. Spirit	Der Geist	Die Geister
    383. Block	Der Block	Die Blöcke
    384. Language	Die Sprache	Die Sprachen
    385. Bridge	Die Brücke	Die Brücken
    386. Dust	Der Staub	-
    387. Cell	Die Zelle	Die Zellen
    388. Wine	Der Wein	Die Weine
    389. Boot	Der Stiefel	Die Stiefel
    390. Choice	Die Wahl	Die Wahlen
    391. Row	Die Reihe	Die Reihen
    392. Talk	Das Gespräch	Die Gespräche
    393. Plane	Das Flugzeug	Die Flugzeuge
    394. Watch	Die Uhr	Die Uhren
    395. Information	Die Information	Die Informationen
    396. Grandmother	Die Großmutter	-
    397. Wing	Der Flügel	Die Flügel
    398. Bob	Der Bob	Die Bobs
    399. Club	Der Club	Die Clubs
    400. Master	Der Meister	Die Meister
    401. Grace	Die Gnade	Die Gnaden
    402. Forest	Der Wald	Die Wälder
    403. Size	Die Größe	Die Größen
    404. Set	Der Satz	Die Sätze
    405. Marriage	Die Ehe	Die Ehen
    406. Forehead	Die Stirn	Die Stirnen
    407. Storm	Der Sturm	Die Stürme
    408. Doorway	Der Durchgang	Die Durchgänge
    409. Situation	Die Situation	Die Situationen
    410. Counter	Die Theke	Die Theken
    411. Neighbor	Der Nachbar	Die Nachbarn
    412. Photo	Das Foto	Die Fotos
    413. Stage	Die Bühne	Die Bühnen
    414. Meeting	Das Treffen	Die Treffen
    415. Nurse	Die Krankenschwester	Die Krankenschwestern
    416. Security	Die Sicherheit	Die Sicherheiten
    417. Weapon	Die Waffe	Die Waffen
    418. Event	Das Ereignis	Die Ereignisse
    419. Ceiling	Die Decke	Die Decken
    420. Engine	Der Motor	Die Motoren
    421. Gift	Das Geschenk	Die Geschenke
    422. Restaurant	Das Restaurant	Die Restaurants
    423. Board	Das Brett	Die Bretter
    424. Hallway	Der Flur	Die Flure
    425. Army	Die Armee	-
    426. Effort	Der Aufwand	Die Aufwände
    427. East	Der Osten	-
    428. Agent	Der Agent	Die Agenten
    429. Future	Die Zukunft	Die Zukunft
    430. Pant	Die Hose	Die Hosen
    431. Leather	Das Leder	-
    432. Flight	Der Flug	Die Flüge
    433. Sex	Der Sex	-
    434. Court	Das Gericht	Die Gerichte
    435. Course	Der Kurs	Die Kurse
    436. Dirt	Der Schmutz	-
    437. Egg	Das Ei	Die Eier
    438. Chin	Das Kinn	Die Kinne
    439. Stranger	Der Fremde	Die Fremden
    440. Pleasure	Das Vergnügen	Die Vergnügen
    441. Detail	Das Detail	Die Details
    442. Crew	Die Besatzung	Die Besatzungen
    443. Fall	Der Herbst	Die Fälle
    444. Guest	Der Gast	Die Gäste
    445. Experience	Die Erfahrung	Die Erfahrungen
    446. Joke	Der Witz	Die Witze
    447. Sand	Der Sand	-
    448. Fist	Die Faust	Die Fäuste
    449. Action	Die Aktion	Die Aktionen
    450. Walk	Der Spaziergang	Die Spaziergänge
    451. Wedding	Die Hochzeit	Die Hochzeiten
    452. Deal	Das Geschäft	Die Geschäfte
    453. Nature	Die Natur	-
    454. Planet	Der Planet	Die Planeten
    455. Cousin	Der Cousin	Die Cousins
    456. Movement	Die Bewegung	Die Bewegungen
    457. Flesh	Das Fleisch	-
    458. Record	Der Rekord	Die Rekorde
    459. Camp	Das Lager	Die Lager
    460. Newspaper	Die Zeitung	Die Zeitungen
    461. Ray	Der Strahl	Die Strahlen
    462. Human	Der Mensch	Die Menschen
    463. Couch	Die Couch	Die Couches
    464. Motion	Die Bewegung	Die Bewegungen
    465. Grandfather	Der Großvater	Die Großväter
    466. Photograph	Das Foto	Die Fotos
    467. Secret	Das Geheimnis	Die Geheimnisse
    468. Beauty	Die Schönheit	Die Schönheiten
    469. Presence	Die Anwesenheit	-
    470. Bell	Die Glocke	Die Glocken
    471. Folk	Das Volk	-
    472. Button	Der Knopf	Die Knöpfe
    473. List	Die Liste	Die Listen
    474. Level	Das Level	Die Level
    475. Date	Das Datum	Die Daten
    476. Subject	Das Fach	Die Fächer
    477. Difference	Der Unterschied	Die Unterschiede
    478. Pause	Die Pause	Die Pausen
    479. Van	Der Lieferwagen	Die Lieferwagen
    480. Blade	Die Klinge	Die Klingen
    481. Television	Das Fernsehen	Die Fernseher
    482. Cover	Die Abdeckung	Die Abdeckungen
    483. Past	Die Vergangenheit	-
    484. Farm	Die Farm	Die Farmen
    485. Lap	Der Schoß	Die Schoß
    486. Band	Die Band	Die Bands
    487. Lawyer	Der Anwalt	Die Anwälte
    488. Magazine	Das Magazin	Die Magazine
    489. Branch	Der Ast	Die Äste
    490. Frame	Der Rahmen	Die Rahmen
    491. Deck	Das Deck	Die Decks
    492. Effect	Die Wirkung	Die Wirkungen
    493. Dance	Der Tanz	Die Tänze
    494. Vision	Die Vision	Die Visionen
    495. Ghost	Das Geist	Die Geister
    496. Ass	Der Hintern	Die Hintern
    497. Character	Der Charakter	Die Charaktere
    498. Glance	Der Blick	Die Blicke
    499. Goodbye	Der Abschied	-
    500. Parking	Das Parken	-
    501. Breakfast	Das Frühstück	Die Frühstücke
    502. Gesture	Die Geste	Die Gesten
    503. Luck	Das Glück	-
    504. Blanket	Die Decke	Die Decken
    505. Gas	Das Gas	-
    506. Corridor	Der Korridor	Die Korridore
    507. Professor	Der Professor	Die Professoren
    508. Play	Das Stück	Die Stücke
    509. Mistake	Der Fehler	Die Fehler
    510. University	Die Universität	Die Universitäten
    511. Ocean	Der Ozean	Die Ozeane
    512. Century	Das Jahrhundert	Die Jahrhunderte
    513. Honey	Der Honig	-
    514. Pile	Der Stapel	Die Stapel
    515. Bowl	Die Schüssel	Die Schüsseln
    516. Base	Die Basis	Die Basen
    517. Fence	Der Zaun	Die Zäune
    518. Rule	Die Regel	Die Regeln
    519. Laughter	Das Lachen	-
    520. Anger	Der Ärger	-
    521. Sweat	Der Schweiß	-
    522. Accident	Der Unfall	Die Unfälle
    523. Weather	Das Wetter	-
    524. Decision	Die Entscheidung	Die Entscheidungen
    525. Angel	Der Engel	Die Engel
    526. Strength	Die Stärke	Die Stärken
    527. Chicken	Das Huhn	Die Hühner
    528. Study	Das Studium	Die Studien
    529. Tape	Das Band	Die Bänder
    530. Wrist	Das Handgelenk	Die Handgelenke
    531. Stop	Der Halt	Die Halte
    532. Hip	Die Hüfte	Die Hüften
    533. Government	Die Regierung	Die Regierungen
    534. Belly	Der Bauch	Die Bäuche
    535. Queen	Die Königin	Die Königinnen
    536. Report	Der Bericht	Die Berichte
    537. Tail	Der Schwanz	Die Schwänze
    538. Plant	Die Pflanze	Die Pflanzen
    539. Flame	Die Flamme	Die Flammen
    540. Heaven	Der Himmel	Die Himmel
    541. Belt	Der Gürtel	Die Gürtel
    542. Neighborhood	Die Nachbarschaft	Die Nachbarschaften
    543. Energy	Die Energie	-
    544. Green	Das Grün	-
    545. Quarter	Das Viertel	Die Viertel
    546. Enemy	Der Feind	Die Feinde
    547. Move	Der Zug	Die Züge
    548. Entrance	Der Eingang	Die Eingänge
    549. Library	Die Bibliothek	Die Bibliotheken
    550. Writer	Der Schriftsteller	Die Schriftsteller
    551. Peace	Der Frieden	-
    552. Touch	Die Berührung	Die Berührungen
    553. Pot	Der Topf	Die Töpfe
    554. Type	Die Art	-
    555. Cause	Die Ursache	Die Ursachen
    556. Rope	Das Seil	Die Seile
    557. Muscle	Der Muskel	Die Muskeln
    558. Painting	Das Gemälde	Die Gemälde
    559. Curtain	Der Vorhang	Die Vorhänge
    560. Meal	Die Mahlzeit	Die Mahlzeiten
    561. Act	Der Akt	Die Akte
    562. Wolf	Der Wolf	Die Wölfe
    563. Cabin	Die Kabine	Die Kabinen
    564. Charge	Die Gebühr	Die Gebühren
    565. Clock	Die Uhr	Die Uhren
    566. Passenger	Der Passagier	Die Passagiere
    567. Buddy	Der Kumpel	Die Kumpel
    568. Drug	Das Medikament	Die Medikamente
    569. Use	Die Verwendung	Die Verwendungen
    570. Bench	Die Bank	Die Bänke
    571. Traffic	Der Verkehr	-
    572. Relief	Die Erleichterung	-
    573. Cap	Die Mütze	Die Mützen
    574. Pack	Das Pack	Die Packs
    575. Weekend	Das Wochenende	Die Wochenenden
    576. Stand	Der Stand	Die Stände
    577. Elevator	Der Aufzug	Die Aufzüge
    578. Birthday	Der Geburtstag	Die Geburtstage
    579. Lily	Die Lilie	Die Lilien
    580. Iron	Das Eisen	Die Eisen
    581. Meat	Das Fleisch	-
    582. Eyebrow	Die Augenbraue	Die Augenbrauen
    583. Response	Die Antwort	Die Antworten
    584. Speed	Die Geschwindigkeit	Die Geschwindigkeiten
    585. Purpose	Der Zweck	Die Zwecke
    586. Skirt	Der Rock	Die Röcke
    587. Square	Das Quadrat	Die Quadrate
    588. Drive	Die Fahrt	Die Fahrten
    589. Article	Der Artikel	Die Artikel
    590. English	Das Englisch	-
    591. Tower	Der Turm	Die Türme
    592. Battle	Die Schlacht	Die Schlachten
    593. Film	Der Film	Die Filme
    594. Race	Das Rennen	Die Rennen
    595. Shock	Der Schock	Die Schocks
    596. Section	Die Sektion	Die Sektionen
    597. Manner	Die Art	-
    598. Sword	Das Schwert	Die Schwerter
    599. Stick	Der Stock	Die Stöcke
    600. File	Die Datei	Die Dateien
    601. Bread	Das Brot	-
    602. Oil	Das Öl	-
    603. Chain	Die Kette	Die Ketten
    604. Department	Die Abteilung	Die Abteilungen
    605. Project	Das Projekt	Die Projekte
    606. Murder	Der Mord	Die Morde
    607. Bear	Der Bär	Die Bären
    608. Test	Der Test	Die Tests
    609. Visit	Der Besuch	Die Besuche
    610. Milk	Die Milch	-
    611. Boss	Der Chef	Die Chefs
    612. Elbow	Der Ellenbogen	Die Ellenbogen
    613. Desire	Das Verlangen	-
    614. Patient	Der Patient	Die Patienten
    615. Grin	Das Grinsen	-
    616. Lover	Der Liebhaber	Die Liebhaber
    617. Price	Der Preis	Die Preise
    618. Map	Die Karte	Die Karten
    619. Knowledge	Das Wissen	-
    620. Beginning	Der Anfang	Die Anfänge
    621. Cold	Die Kälte	-
    622. Closet	Der Schrank	Die Schränke
    623. Dawn	Die Morgendämmerung	Die Morgendämmerungen
    624. Temple	Der Tempel	Die Tempel
    625. Joy	Die Freude	-
    626. Duty	Die Pflicht	Die Pflichten
    627. Practice	Die Übung	Die Übungen
    628. Heel	Der Absatz	Die Absätze
    629. Valley	Das Tal	Die Täler
    630. Fight	Der Kampf	Die Kämpfe
    631. Wire	Das Kabel	Die Kabel
    632. Jeans	Die Jeans	-
    633. Kiss	Der Kuss	Die Küsse
    634. Jaw	Der Kiefer	Die Kiefer
    635. Run	Der Lauf	Die Läufe
    636. Hold	Das Halten	Die Halten
    637. Relationship	Die Beziehung	Die Beziehungen
    638. Object	Das Objekt	Die Objekte
    639. Attack	Der Angriff	Die Angriffe
    640. Dish	Das Gericht	Die Gerichte
    641. Highway	Die Autobahn	Die Autobahnen
    642. Shade	Der Schatten	Die Schatten
    643. Crime	Das Verbrechen	Die Verbrechen
    644. grey	Das Weiß	-
    645. Partner	Der Partner	Die Partner
    646. Priest	Der Priester	Die Priester
    647. Lawn	Der Rasen	Die Rasen
    648. Laugh	Das Lachen	-
    649. Trunk	Der Stamm	Die Stämme
    650. Cry	Das Weinen	Die Weinen
    651. Program	Das Programm	Die Programme
    652. Ride	Die Fahrt	Die Fahrten
    653. Shelf	Das Regal	Die Regale
    654. Gentleman	Der Herr	Die Herren
    655. Being	Das Wesen	Die Wesen
    656. Steel	Der Stahl	-
    657. Sidewalk	Der Bürgersteig	Die Bürgersteige
    658. Uniform	Die Uniform	Die Uniformen
    659. Pattern	Das Muster	Die Muster
    660. Evidence	Der Beweis	Die Beweise
    661. Player	Der Spieler	Die Spieler
    662. Novel	Der Roman	Die Romane
    663. Pillow	Das Kissen	Die Kissen
    664. Lamp	Die Lampe	Die Lampen
    665. Drawer	Die Schublade	Die Schubladen
    666. Danger	Die Gefahr	Die Gefahren
    667. Detective	Der Detektiv	Die Detektive
    668. Instant	Der Augenblick	Die Augenblicke
    669. Thinking	Das Denken	-
    670. Crack	Der Riss	Die Risse
    671. Prayer	Das Gebet	Die Gebete
    672. Towel	Das Handtuch	Die Handtücher
    673. Glove	Der Handschuh	Die Handschuhe
    674. Bay	Die Bucht	Die Buchten
    675. Audience	Das Publikum	-
    676. Can	Die Dose	Die Dosen
    677. Condition	Der Zustand	Die Zustände
    678. Trail	Der Pfad	Die Pfade
    679. Waist	Die Taille	Die Taillen
    680. Pressure	Der Druck	Die Drücke
    681. Telephone	Das Telefon	Die Telefone
    682. Sink	Das Waschbecken	Die Waschbecken
    683. Return	Die Rückkehr	Die Rückkehr
    684. Breeze	Die Brise	Die Brisen
    685. Taste	Der Geschmack	Die Geschmäcker
    686. Fault	Der Fehler	Die Fehler
    687. Stream	Der Strom	Die Ströme
    688. Result	Das Ergebnis	Die Ergebnisse
    689. Author	Der Autor	Die Autoren
    690. Tip	Der Tipp	Die Tipps
    691. Shower	Die Dusche	Die Duschen
    692. Toe	Die Zehe	Die Zehen
    693. Season	Die Jahreszeit	Die Jahreszeiten
    694. Half	Die Hälfte	Die Hälften
    695. Fool	Der Narr	Die Narren
    696. Tunnel	Der Tunnel	Die Tunnel
    697. Client	Der Kunde	Die Kunden
    698. Garage	Die Garage	Die Garagen
    699. Mission	Die Mission	Die Missionen
    700. Chief	Der Chef	Die Chefs
    701. Bullet	Die Kugel	Die Kugeln
    702. Market	Der Markt	Die Märkte
    703. Loss	Der Verlust	Die Verluste
    704. Series	Die Serie	Die Serien
    705. Pen	Der Stift	Die Stifte
    706. Term	Der Begriff	Die Begriffe
    707. Poem	Das Gedicht	Die Gedichte
    708. Prince	Der Prinz	Die Prinzen
    709. Clay	Der Ton	Die Tone
    710. Lock	Das Schloss	Die Schlösser
    711. Reality	Die Realität	Die Realitäten
    712. Snake	Die Schlange	Die Schlangen 
    713. Apple	Der Apfel	Die Äpfel 
    714. Mask	Die Maske	Die Masken 
    715. Customer	Der Kunde	Die Kunden 
    716. Birth	Die Geburt	Die Geburten 
    717. Break	Die Pause	Die Pausen 
    718. Wonder	Das Wunder	Die Wunder 
    719. Sunlight	Das Sonnenlicht	- 
    720. Tank	Der Panzer	Die Panzer 
    721. Staff	Das Personal	- 
    722. Lie	Die Lüge	Die Lügen 
    723. Faith	Der Glaube	- 
    724. Honor	Die Ehre	- 
    725. Cream	Die Sahne	- 
    726. Sake	Der Grund	- 
    727. Victim	Das Opfer	Die Opfer 
    728. Possibility	Die Möglichkeit	Die Möglichkeiten 
    729. Contact	Der Kontakt	Die Kontakte 
    730. Mood	Die Stimmung	Die Stimmungen 
    731. Thumb	Der Daumen	Die Daumen 
    732. Reading	Das Lesen	- 
    733. Fun	Der Spaß	- 
    734. Candle	Die Kerze	Die Kerzen 
    735. Cave	Die Höhle	Die Höhlen 
    736. Post	Die Post	- 
    737. Prison	Das Gefängnis	Die Gefängnisse 
    738. Emotion	Die Emotion	Die Emotionen 
    739. Leader	Der Führer	Die Führer 
    740. Degree	Der Abschluss	Die Abschlüsse 
    741. Feature	Das Merkmal	Die Merkmale 
    742. Ticket	Die Eintrittskarte	Die Eintrittskarten 
    743. Alien	Das Alien	Die Aliens 
    744. Lesson	Die Lektion	Die Lektionen 
    745. Desert	Die Wüste	Die Wüsten 
    746. Cut	Der Schnitt	Die Schnitte 
    747. Mess	Das Durcheinander	- 
    748. Warning	Die Warnung	Die Warnungen 
    749. Tale	Das Märchen	Die Märchen 
    750. Funeral	Die Beerdigung	Die Beerdigungen 
    751. Cab	Das Taxi	Die Taxis 
    752. Reporter	Der Reporter	Die Reporter 
    753. Present	Das Geschenk	Die Geschenke 
    754. Theater	Das Theater	Die Theater 
    755. Length	Die Länge	- 
    756. Mud	Der Schlamm	- 
    757. Science	Die Wissenschaft	- 
    758. Drop	Der Tropfen	Die Tropfen 
    759. String	Die Schnur	Die Schnüre 
    760. Speech	Die Rede	Die Reden 
    761. Copy	Das Exemplar	Die Exemplare 
    762. Cow	Die Kuh	Die Kühe 
    763. Worker	Der Arbeiter	Die Arbeiter 
    764. Thigh	Der Oberschenkel	Die Oberschenkel 
    765. Lab	Das Labor	Die Labore 
    766. Roll	Die Rolle	Die Rollen 
    767. Fruit	Die Frucht	Die Früchte 
    768. Patch	Das Patch	Die Patches 
    769. Silk	Die Seide	- 
    770. Buck	Der Dollar	Die Dollars 
    771. Brick	Der Ziegel	Die Ziegel 
    772. Rifle	Das Gewehr	Die Gewehre 
    773. Career	Die Karriere	Die Karrieren 
    774. Issue	Die Ausgabe	Die Ausgaben 
    775. Opportunity	Die Gelegenheit	Die Gelegenheiten 
    776. Director	Der Regisseur	Die Regisseure 
    777. Monster	Das Monster	Die Monster 
    778. Vehicle	Das Fahrzeug	Die Fahrzeuge 
    779. Alley	Die Gasse	Die Gassen 
    780. Sleeve	Der Ärmel	Die Ärmel 
    781. Grave	Das Grab	Die Gräber 
    782. Bush	Der Busch	Die Büsche 
    783. Dining	Das Esszimmer	- 
    784. Opening	Die Öffnung	Die Öffnungen 
    785. Twin	Das Zwilling	Die Zwillinge 
    786. Barn	Die Scheune	Die Scheunen 
    787. Pound	Das Pfund	Die Pfunde 
    788. Site	Die Seite	Die Seiten 
    789. Flash	Der Blitz	Die Blitze 
    790. Judge	Der Richter	Die Richter 
    791. Mass	Die Masse	Die Massen 
    792. Process	Der Prozess	Die Prozesse 
    793. Tie	Die Krawatte	Die Krawatten 
    794. Purse	Die Geldbörse	Die Geldbörsen 
    795. Pipe	Die Pfeife	Die Pfeifen 
    796. Dragon	Der Drache	Die Drachen 
    797. Horizon	Der Horizont	Die Horizonte 
    798. Tray	Das Tablett	Die Tabletts 
    799. Envelope	Der Umschlag	Die Umschläge 
    800. Check	Der Scheck	Die Schecks 
    801. Adult	Der Erwachsene	Die Erwachsenen 
    802. Emergency	Der Notfall	Die Notfälle 
    803. Material	Das Material	Die Materialien 
    804. Childhood	Die Kindheit	- 
    805. Habit	Die Gewohnheit	Die Gewohnheiten 
    806. Artist	Der Künstler	Die Künstler 
    807. Address	Die Adresse	Die Adressen 
    808. Scent	Der Duft	Die Düfte 
    809. Universe	Das Universum	Die Universen 
    810. Nod	Das Nicken	- 
    811. Shell	Die Muschel	Die Muscheln 
    812. Community	Die Gemeinschaft	Die Gemeinschaften 
    813. Start	Der Start	Die Starts 
    814. Wound	Die Wunde	Die Wunden 
    815. Mouse	Die Maus	Die Mäuse 
    816. Pilot	Der Pilot	Die Piloten 
    817. Grade	Die Note	Die Noten 
    818. Video	Das Video	Die Videos 
    819. Basket	Der Korb	Die Körbe 
    820. Wagon	Der Waggon	Die Waggons 
    821. Attempt	Der Versuch	Die Versuche 
    822. Sofa	Das Sofa	Die Sofas 
    823. Cake	Der Kuchen	Die Kuchen 
    824. Fellow	Der Kerl	Die Kerle 
    825. Affair	Die Angelegenheit	Die Angelegenheiten 
    826. Shore	Die Küste	Die Küsten 
    827. General	Der General	Die Generäle 
    828. Root	Die Wurzel	Die Wurzeln 
    829. Robe	Der Umhang	Die Umhänge 
    830. Concern	Die Sorge	Die Sorgen 
    831. Press	Die Presse	- 
    832. Rat	Die Ratte	Die Ratten 
    833. Society	Die Gesellschaft	Die Gesellschaften 
    834. Style	Der Stil	Die Stile 
    835. County	Der Bezirk	Die Bezirke 
    836. Command	Der Befehl	Die Befehle 
    837. Visitor	Der Besucher	Die Besucher 
    838. Model	Das Modell	Die Modelle 
    839. Chamber	Die Kammer	Die Kammern 
    840. Beast	Das Tier	Die Tiere 
    841. Bunch	Der Strauß	Die Sträuße 
    842. Background	Der Hintergrund	Die Hintergründe 
    843. Unit	Die Einheit	Die Einheiten 
    844. Furniture	Das Möbel	Die Möbel 
    845. Nail	Der Nagel	Die Nägel 
    846. Scream	Der Schrei	Die Schreie 
    847. Property	Das Eigentum	- 
    848. Equipment	Die Ausrüstung	- 
    849. Driveway	Die Auffahrt	Die Auffahrten 
    850. Grip	Der Griff	Die Griffe 
    851. Tube	Die Röhre	Die Röhren 
    852. Ash	Die Asche	Die Aschen 
    853. Fan	Der Ventilator	Die Ventilatoren 
    854. Opinion	Die Meinung	Die Meinungen 
    855. Data	Die Daten	- 
    856. Connection	Die Verbindung	Die Verbindungen 
    857. Trick	Der Trick	Die Tricks 
    858. Mystery	Das Geheimnis	Die Geheimnisse 
    859. Period	Die Periode	Die Perioden 
    860. Writing	Die Schrift	Die Schriften 
    861. Horror	Der Horror	- 
    862. Candy	Die Süßigkeiten	- 
    863. Bitch	Die Hündin	Die Hündinnen 
    864. Health	Die Gesundheit	- 
    865. Manager	Der Manager	Die Manager 
    866. Safety	Die Sicherheit	- 
    867. Height	Die Höhe	Die Höhen 
    868. Appearance	Das Aussehen	- 
    869. Sigh	Der Seufzer	Die Seufzer 
    870. Mine	Die Mine	Die Minen 
    871. Cloth	Der Stoff	Die Stoffe 
    872. Reaction	Die Reaktion	Die Reaktionen 
    873. Source	Die Quelle	Die Quellen 
    874. Self	Das Selbst	- 
    875. Pistol	Die Pistole	Die Pistolen 
    876. Airport	Der Flughafen	Die Flughäfen 
    877. Hero	Der Held	Die Helden 
    878. Promise	Das Versprechen	Die Versprechen 
    879. Bow	Der Bogen	Die Bögen 
    880. Tent	Das Zelt	Die Zelte 
    881. Booth	Der Stand	Die Stände 
    882. Cash	Das Bargeld	- 
    883. Avenue	Die Allee	Die Alleen 
    884. TShirt	Das T-Shirt	Die T-Shirts 
    885. Carpet	Der Teppich	Die Teppiche 
    886. Basement	Der Keller	Die Keller 
    887. Girlfriend	Die Freundin	Die Freundinnen 
    888. Beard	Der Bart	Die Bärte 
    889. Brow	Die Augenbraue	Die Augenbrauen 
    890. Display	Der Bildschirm	Die Bildschirme 
    891. Signal	Das Signal	Die Signale 
    892. Servant	Der Diener	Die Diener 
    893. Whisper	Das Flüstern	Die Flüster 
    894. Doubt	Der Zweifel	Die Zweifel 
    895. Account	Das Konto	Die Konten 
    896. Magic	Die Magie	- 
    897. Hank	Der Klumpen	Die Klumpen 
    898. Limb	Das Glied	Die Glieder 
    899. Bastard	Der Bastard	Die Bastarde 
    900. Skull	Der Schädel	Die Schädel 
    901. Sentence	Der Satz	Die Sätze 
    902. Collar	Der Kragen	Die Kragen 
    903. Horn	Das Horn	Die Hörner 
    904. Oak	Die Eiche	Die Eichen 
    905. Ankle	Der Knöchel	Die Knöchel 
    906. Doll	Die Puppe	Die Puppen 
    907. Sandwich	Das Sandwich	Die Sandwiches 
    908. Robin	Der Rotkehlchen	Die Rotkehlchen 
    909. Justice	Die Gerechtigkeit	- 
    910. Pride	Der Stolz	- 
    911. Youth	Die Jugend	- 
    912. Secretary	Der Sekretär	Die Sekretäre 
    913. Research	Die Forschung	- 
    914. Sport	Der Sport	Die Sportarten 
    915. Task	Die Aufgabe	Die Aufgaben 
    916. Grant	Das Stipendium	Die Stipendien 
    917. Sheriff	Der Sheriff	Die Sheriffs 
    918. Midnight	Die Mitternacht	- 
    919. Chip	Der Chip	Die Chips 
    920. Theory	Die Theorie	Die Theorien 
    921. Alarm	Der Alarm	Die Alarme 
    922. Collection	Die Sammlung	Die Sammlungen 
    923. Cross	Das Kreuz	Die Kreuze 
    924. Pine	Die Kiefer	Die Kiefern 
    925. Generation	Die Generation	Die Generationen 
    926. Authority	Die Autorität	Die Autoritäten 
    927. Papa	Der Papa	Die Papas 
    928. Journey	Die Reise	Die Reisen 
    929. Pearl	Die Perle	Die Perlen 
    930. Toilet	Die Toilette	Die Toiletten 
    931. Killer	Der Mörder	Die Mörder 
    932. Tool	Das Werkzeug	Die Werkzeuge 
    933. Medicine	Die Medizin	Die Medizinen 
    934. Sugar	Der Zucker	- 
    935. Princess	Die Prinzessin	Die Prinzessinnen 
    936. Argument	Das Argument	Die Argumente 
    937. Cliff	Die Klippe	Die Klippen 
    938. Cart	Der Wagen	Die Wagen 
    939. Crystal	Der Kristall	Die Kristalle 
    940. Bean	Die Bohne	Die Bohnen 
    941. Cage	Der Käfig	Die Käfige 
    942. Chocolate	Die Schokolade	- 
    943. Coast	Die Küste	Die Küsten 
    944. Decade	Das Jahrzehnt	Die Jahrzehnte 
    945. Meaning	Die Bedeutung	Die Bedeutungen 
    946. Gear	Das Getriebe	Die Getriebe 
    947. Suitcase	Der Koffer	Die Koffer 
    948. Operation	Die Operation	Die Operationen 
    949. Breathing	Das Atmen	- 
    950. Role	Die Rolle	Die Rollen 
    951. Version	Die Version	Die Versionen 
    952. Prisoner	Der Gefangene	Die Gefangenen 
    953. Match	Das Spiel	Die Spiele 
    954. Beam	Der Strahl	Die Strahlen 
    955. Castle	Das Schloss	Die Schlösser 
    956. Rush	Der Rausch	Die Räusche 
    957. Lane	Die Fahrspur	Die Fahrspuren 
    958. Clothing	Die Kleidung	- 
    959. Pole	Der Pfahl	Die Pfähle 
    960. Freedom	Die Freiheit	- 
    961. Skill	Die Fähigkeit	Die Fähigkeiten 
    962. Passion	Die Leidenschaft	Die Leidenschaften 
    963. Activity	Die Aktivität	Die Aktivitäten 
    964. Fuck	Der Fick	Die Ficks 
    965. Platform	Die Plattform	Die Plattformen 
    966. Salt	Das Salz	- 
    967. Bike	Das Fahrrad	Die Fahrräder 
    968. Stack	Der Stapel	Die Stapel 
    969. Companion	Der Begleiter	Die Begleiter 
    970. Fate	Das Schicksal	- 
    971. Rage	Die Wut	Die Wut 
    972. Supply	Die Versorgung	Die Versorgungen 
    973. Whale	Der Wal	Die Wale 
    974. Pig	Das Schwein	Die Schweine 
    975. Rabbit	Das Kaninchen	Die Kaninchen 
    976. Aisle	Der Gang	Die Gänge 
    977. Monitor	Der Monitor	Die Monitore 
    978. Helmet	Der Helm	Die Helme 
    979. Respect	Der Respekt	- 
    980. Excitement	Die Aufregung	- 
    981. Lobby	Die Lobby	Die Lobbys 
    982. Boyfriend	Der Freund	Die Freunde 
    983. Fur	Der Pelz	Die Felle 
    984. Range	Die Bandbreite	Die Bandbreiten 
    985. Dick	Der Schwanz	Die Schwänze 
    986. Code	Der Code	Die Codes 
    987. Chapter	Das Kapitel	Die Kapitel 
    988. Reflection	Die Reflexion	Die Reflexionen 
    989. Mail	Die Post	Die Mails 
    990. Fly	Die Fliege	Die Fliegen 
    991. Cabinet	Der Schrank	Die Schränke 
    992. Toy	Das Spielzeug	Die Spielzeuge 
    993. Baseball	Der Baseball	Die Baseballs 
    994. Inside	Das Innere	- 
    995. Pace	Das Tempo	- 
    996. Handle	Der Griff	Die Griffe 
    997. Lead	Das Blei	- 
    998. Amount	Die Menge	Die Mengen 
    999. Nerve	Der Nerv	Die Nerven 
    1000. Terror	Der Terror	- 
    1001. Sweater	Der Pullover	Die Pullover
    1002. Quality	Die Qualität	Die Qualitäten
    1003. Hunter	Der Jäger	Die Jäger
    1004. Paint	Die Farbe	Die Farben
    1005. Buster	Der Zerstörer	Die Zerstörer
    1006. Cotton	Die Baumwolle	- 
    1007. Sergeant	Der Feldwebel	Die Feldwebel
    1008. Credit	Der Kredit	Die Kredite
    1009. Blow	Der Schlag	Die Schläge
    1010. Devil	Der Teufel	Die Teufel
    1011. Threat	Die Bedrohung	Die Bedrohungen
    1012. Success	Der Erfolg	Die Erfolge
    1013. Eve	Der Abend	Die Abende
    1014. Cable	Das Kabel	Die Kabel
    1015. Pan	Die Pfanne	Die Pfannen
    1016. Clerk	Der Angestellte	Die Angestellten
    1017. Title	Der Titel	Die Titel
    1018. Meter	Der Meter	Die Meter
    1019. Shame	Die Schande	- 
    1020. Needle	Die Nadel	Die Nadeln
    1021. Lung	Die Lunge	Die Lungen
    1022. Warrior	Der Krieger	Die Krieger
    1023. Circumstance	Die Umstände	- 
    1024. Studio	Das Studio	Die Studios
    1025. Panic	Die Panik	- 
    1026. Lack	Der Mangel	- 
    1027. Farmer	Der Bauer	Die Bauern
    1028. Accent	Der Akzent	Die Akzente
    1029. Bomb	Die Bombe	Die Bomben
    1030. Panel	Das Panel	Die Panels
    1031. Ability	Die Fähigkeit	Die Fähigkeiten
    1032. Fortune	Das Glück	- 
    1033. Victor	Der Sieger	Die Sieger
    1034. Feather	Die Feder	Die Federn
    1035. Grandma	Die Oma	Die Omas
    1036. Glow	Das Leuchten	Die Leuchten
    1037. Behavior	Das Verhalten	- 
    1038. Passage	Der Durchgang	Die Durchgänge
    1039. Slave	Der Sklave	Die Sklaven
    1040. Lieutenant	Der Leutnant	Die Leutnants
    1041. Barrel	Das Fass	Die Fässer
    1042. Warmth	Die Wärme	- 
    1043. Impression	Der Eindruck	Die Eindrücke
    1044. Mason	Der Maurer	Die Maurer
    1045. Bride	Die Braut	Die Bräute
    1046. Package	Das Paket	Die Pakete
    1047. Fog	Der Nebel	- 
    1048. Walking	Das Gehen	- 
    1049. Balance	Das Gleichgewicht	- 
    1050. Sock	Die Socke	Die Socken
    1051. Robot	Der Roboter	Die Roboter
    1052. Potato	Die Kartoffel	Die Kartoffeln
    1053. Item	Der Gegenstand	Die Gegenstände
    1054. Bath	Das Bad	Die Bäder
    1055. Diamond	Der Diamant	Die Diamanten
    1056. Corpse	Die Leiche	Die Leichen
    1057. Explanation	Die Erklärung	Die Erklärungen
    1058. Structure	Die Struktur	Die Strukturen
    1059. Exit	Der Ausgang	Die Ausgänge
    1060. Pad	Das Kissen	Die Kissen
    1061. Stove	Der Herd	Die Herde
    1062. Blue	Das Blau	- 
    1063. American	Der Amerikaner	Die Amerikaner
    1064. Ruby	Der Rubin	Die Rubine
    1065. Lightning	Das Blitz	Die Blitze
    1066. Pit	Die Grube	Die Gruben
    1067. Colonel	Der Oberst	Die Obersten
    1068. Dock	Der Hafen	Die Häfen
    1069. Creek	Der Bach	Die Bäche
    1070. Advice	Der Rat	Die Ratschläge
    1071. Tourist	Der Tourist	Die Touristen
    1072. Grief	Die Trauer	- 
    1073. Defense	Die Verteidigung	- 
    1074. Bite	Der Biss	Die Bisse
    1075. Museum	Das Museum	Die Museen
    1076. Favor	Der Gefallen	Die Gefallen
    1077. Supper	Das Abendessen	- 
    1078. Comfort	Der Komfort	- 
    1079. Dean	Der Dekan	- 
    1080. Value	Der Wert	Die Werte
    1081. March	Der Marsch	Die Märsche
    1082. Estate	Das Anwesen	Die Anwesen
    1083. Poet	Der Dichter	Die Dichter
    1084. Palace	Der Palast	Die Paläste
    1085. Soup	Die Suppe	Die Suppen
    1086. Nation	Die Nation	Die Nationen
    1087. Jar	Das Glas	Die Gläser
    1088. Standing	Der Stand	- 
    1089. Sack	Der Sack	Die Säcke
    1090. Demon	Der Dämon	Die Dämonen
    1091. Conference	Die Konferenz	Die Konferenzen
    1092. Juice	Der Saft	Die Säfte
    1093. Responsibility	Die Verantwortung	- 
    1094. Brush	Die Bürste	Die Bürsten
    1095. Route	Die Route	Die Routen
    1096. Cheese	Der Käse	Die Käse
    1097. Hood	Die Motorhaube	Die Motorhauben
    1098. Duck	Die Ente	Die Enten
    1099. Saint	Der Heilige	Die Heiligen
    1100. Pass	Der Pass	Die Pässe
    1101. Target	Das Ziel	Die Ziele
    1102. Orange	Die Orange	Die Orangen
    1103. Culture	Die Kultur	Die Kulturen
    1104. Tour	Die Tour	Die Touren
    1105. Commander	Der Kommandant	Die Kommandanten
    1106. Hook	Der Haken	Die Haken
    1107. Mist	Der Nebel	- 
    1108. Training	Das Training	Die Trainings
    1109. Search	Die Suche	Die Suchen
    1110. Coin	Die Münze	Die Münzen
    1111. Miracle	Das Wunder	Die Wunder
    1112. Advantage	Der Vorteil	Die Vorteile
    1113. Exchange	Der Austausch	Die Austausche
    1114. Fiction	Die Fiktion	- 
    1115. Pond	Der Teich	Die Teiche
    1116. Assistant	Der Assistent	Die Assistenten
    1117. Design	Das Design	Die Designs
    1118. Fishing	Das Angeln	- 
    1119. Slope	Der Hang	Die Hänge
    1120. Earl	Der Graf	Die Grafen
    1121. Comment	Der Kommentar	Die Kommentare
    1122. Waiter	Der Kellner	Die Kellner
    1123. Grocery	Der Lebensmittel	Die Lebensmittel
    1124. Ladder	Die Leiter	Die Leitern
    1125. Curve	Die Kurve	Die Kurven
    1126. Volume	Das Volumen	Die Volumina
    1127. Risk	Das Risiko	Die Risiken
    1128. Nightmare	Der Albtraum	Die Albträume
    1129. Existence	Die Existenz	- 
    1130. Trace	Die Spur	Die Spuren
    1131. Disease	Die Krankheit	Die Krankheiten
    1132. Support	Die Unterstützung	- 
    1133. Witness	Der Zeuge	Die Zeugen
    1134. Stock	Der Bestand	Die Bestände
    1135. Device	Das Gerät	Die Geräte
    1136. Landscape	Die Landschaft	Die Landschaften
    1137. Holiday	Der Feiertag	Die Feiertage
    1138. Ace	Das Ass	Die Asse
    1139. Piano	Das Klavier	Die Klaviere
    1140. Gut	Der Darm	- 
    1141. Talent	Das Talent	Die Talente
    1142. Imagination	Die Fantasie	- 
    1143. Black	Das Schwarz	- 
    1144. Reed	Der Rohrkolben	Die Rohrkolben
    1145. Lid	Der Deckel	Die Deckel
    1146. Hint	Der Hinweis	Die Hinweise
    1147. Walker	Der Spaziergänger	Die Spaziergänger
    1148. Chill	Das Schaudern	- 
    1149. Trial	Der Prozess	Die Prozesse
    1150. Interview	Das Interview	Die Interviews
    1151. Approach	Der Ansatz	Die Ansätze
    1152. Scar	Die Narbe	Die Narben
    1153. Fashion	Die Mode	- 
    1154. Channel	Der Kanal	Die Kanäle
    1155. Footstep	Der Fußabdruck	Die Fußabdrücke
    1156. Pickup	Der Pick-up	Die Pick-ups
    1157. Hawk	Der Habicht	Die Habichte
    1158. Trailer	Der Anhänger	Die Anhänger
    1159. Statue	Die Statue	Die Statuen
    1160. Pill	Die Pille	Die Pillen
    1161. Bug	Der Käfer	Die Käfer
    1162. Bucket	Der Eimer	Die Eimer
    1163. Vacation	Der Urlaub	Die Urlaube
    1164. Species	Die Art	Die Arten
    1165. Column	Die Säule	Die Säulen
    1166. Damage	Der Schaden	- 
    1167. Instrument	Das Instrument	Die Instrumente
    1168. Port	Der Hafen	Die Häfen
    1169. Layer	Die Schicht	Die Schichten
    1170. Strip	Der Streifen	Die Streifen
    1171. Garbage	Der Müll	- 
    1172. Rib	Die Rippe	Die Rippen
    1173. Notebook	Das Notizbuch	Die Notizbücher
    1174. Corn	Der Mais	- 
    1175. Offer	Das Angebot	Die Angebote
    1176. Drawing	Die Zeichnung	Die Zeichnungen
    1177. Statement	Die Aussage	Die Aussagen
    1178. Intelligence	Die Intelligenz	- 
    1179. Excuse	Die Entschuldigung	Die Entschuldigungen
    1180. Landing	Die Landung	Die Landungen
    1181. Copyright	Das Urheberrecht	- 
    1182. Rod	Die Stange	Die Stangen
    1183. Fantasy	Die Fantasie	Die Fantasien
    1184. Curiosity	Die Neugierde	- 
    1185. Gown	Das Gewand	Die Gewänder
    1186. Border	Die Grenze	Die Grenzen
    1187. Poetry	Die Poesie	- 
    1188. Firm	Die Firma	Die Firmen
    1189. Rise	Der Anstieg	Die Anstiege
    1190. Handful	Die Handvoll	Die Handvoll
    1191. China	Das Porzellan	- 
    1192. French	Der Franzose	Die Franzosen
    1193. Mean	Der Durchschnitt	Die Durchschnitte
    1194. Deer	Das Reh	Die Rehe
    1195. Print	Der Druck	Die Drucke
    1196. Rail	Die Schiene	Die Schienen
    1197. Rate	Der Tarif	Die Tarife
    1198. Courage	Der Mut	- 
    1199. Arrival	Die Ankunft	Die Ankünfte
    1200. Wish	Der Wunsch	Die Wünsche
    1201. Ridge	Der Bergrücken	Die Bergrücken
    1202. Idiot	Der Idiot	Die Idioten
    1203. Bull	Der Stier	Die Stiere
    1204. Seed	Der Samen	Die Samen
    1205. Progress	Der Fortschritt	- 
    1206. Feel	Das Gefühl	Die Gefühle
    1207. Shorts	Die kurze Hose	Die kurze Hosen
    1208. Citizen	Der Bürger	Die Bürger
    1209. Trash	Der Müll	- 
    1210. Log	Der Baumstamm	Die Baumstämme
    1211. Patience	Die Geduld	- 
    1212. Bat	Die Fledermaus	Die Fledermäuse
    1213. Football	Der Fußball	Die Fußbälle
    1214. Routine	Die Routine	Die Routinen
    1215. Explosion	Die Explosion	Die Explosionen
    1216. Content	Der Inhalt	Die Inhalte
    1217. Scientist	Der Wissenschaftler	Die Wissenschaftler
    1218. Failure	Das Versagen	Die Versagen
    1219. Sin	Die Sünde	Die Sünden
    1220. Butt	Der Hintern	Die Hintern
    1221. Confusion	Die Verwirrung	- 
    1222. Understanding	Das Verständnis	- 
    1223. Trade	Der Handel	Die Handel
    1224. Refrigerator	Der Kühlschrank	Die Kühlschränke
    1225. Mister	Der Herr	Die Herren
    1226. Flashlight	Die Taschenlampe	Die Taschenlampen
    1227. Net	Das Netz	Die Netze
    1228. Sailor	Der Matrose	Die Matrosen
    1229. Attitude	Die Einstellung	Die Einstellungen
    1230. Guilt	Die Schuld	- 
    1231. Crying	Das Weinen	- 
    1232. Sip	Der Schluck	Die Schlucke
    1233. Travel	Das Reisen	Die Reisen
    1234. Cookie	Der Keks	Die Kekse
    1235. Escape	Die Flucht	Die Fluchten
    1236. Instruction	Die Anweisung	Die Anweisungen
    1237. Fabric	Der Stoff	Die Stoffe
    1238. Marble	Der Marmor	Die Marmore
    1239. Glimpse	Der Blick	Die Blicke
    1240. Dusk	Die Dämmerung	- 
    1241. Cottage	Die Hütte	Die Hütten
    1242. Monkey	Der Affe	Die Affen
    1243. Makeup	Das Make-up	- 
    1244. Doc	Der Arzt	Die Ärzte
    1245. Blouse	Die Bluse	Die Blusen
    1246. Rhythm	Der Rhythmus	Die Rhythmen
    1247. Steam	Der Dampf	- 
    1248. Phrase	Die Phrase	Die Phrasen
    1249. Nut	Die Mutter	Die Muttern
    1250. Pencil	Der Bleistift	Die Bleistifte
    1251. Cook	Der Koch	Die Köche
    1252. Flag	Die Flagge	Die Flaggen
    1253. Coach	Der Trainer	Die Trainer
    1254. Swing	Der Schwung	Die Schwünge
    1255. Speaker	Der Lautsprecher	Die Lautsprecher
    1256. Bolt	Der Bolzen	Die Bolzen
    1257. Fat	Das Fett	Die Fette
    1258. Rug	Der Teppich	Die Teppiche
    1259. Knock	Das Klopfen	- 
    1260. Spell	Der Zauber	Die Zauber
    1261. Taxi	Das Taxi	Die Taxis
    1262. Round	Die Runde	Die Runden
    1263. Straw	Der Strohhalm	Die Strohhalme
    1264. Hatch	Die Luke	Die Luken
    1265. Fork	Die Gabel	Die Gabeln
    1266. Evil	Das Böse	- 
    1267. Maid	Die Dienstmädchen	- 
    1268. Relative	Der Verwandte	Die Verwandten
    1269. Witch	Die Hexe	Die Hexen
    1270. Courtyard	Der Innenhof	Die Innenhöfe
    1271. Sensation	Die Sensation	Die Sensationen
    1272. Bubble	Die Blase	Die Blasen
    1273. Reader	Der Leser	Die Leser
    1274. Curl	Die Locke	Die Locken
    1275. Pie	Der Kuchen	Die Kuchen
    1276. Jet	Das Düsenflugzeug	Die Düsenflugzeuge
    1277. Shift	Die Schicht	Die Schichten
    1278. Union	Die Union	Die Unionen
    1279. Teenager	Der Teenager	Die Teenager
    1280. Plain	Die Ebene	Die Ebenen
    1281. Waitress	Die Kellnerin	Die Kellnerinnen
    1282. Reply	Die Antwort	Die Antworten
    1283. Rumor	Das Gerücht	Die Gerüchte
    1284. Gravity	Die Schwerkraft	- 
    1285. Shelter	Das Schutz	Die Schutz 
    1286. Adventure	Das Abenteuer	Die Abenteuer
    1287. Lion	Der Löwe	Die Löwen
    1288. Spine	Die Wirbelsäule	Die Wirbelsäulen
    1289. Confidence	Das Vertrauen	Die Vertrauen
    1290. Depth	Die Tiefe	Die Tiefen
    1291. Reach	Die Reichweite	Die Reichweiten
    1292. Hammer	Der Hammer	Die Hämmer
    1293. Bible	Die Bibel	Die Bibeln
    1294. Contract	Der Vertrag	Die Verträge
    1295. Wallet	Die Brieftasche	Die Brieftaschen
    1296. Jungle	Der Dschungel	Die Dschungel
    1297. Factory	Die Fabrik	Die Fabriken
    1298. Indian	Der Indianer	Die Indianer
    1299. Balcony	Der Balkon	Die Balkone
    1300. Rice	Der Reis	- 
    1301. Knot	Der Knoten	Die Knoten
    1302. Cord	Das Kabel	Die Kabel
    1303. Colleague	Der Kollege	Die Kollegen
    1304. Intention	Die Absicht	Die Absichten
    1305. Stare	Der starren	- 
    1306. Motel	Das Motel	Die Motels
    1307. Attorney	Der Anwalt	Die Anwälte
    1308. Darling	Der Liebling	Die Lieblinge
    1309. Discussion	Die Diskussion	Die Diskussionen
    1310. Atmosphere	Die Atmosphäre	Die Atmosphären
    1311. Performance	Die Aufführung	Die Aufführungen
    1312. Tension	Die Spannung	Die Spannungen
    1313. Text	Der Text	Die Texte
    1314. Strand	Der Strand	Die Strände
    1315. Noon	Der Mittag	- 
    1316. Vein	Die Ader	Die Adern
    1317. Expert	Der Experte	Die Experten
    1318. Gang	Die Bande	Die Banden
    1319. Policeman	Der Polizist	Die Polizisten
    1320. Cancer	Der Krebs	- 
    1321. Fox	Der Fuchs	Die Füchse
    1322. Divorce	Die Scheidung	Die Scheidungen
    1323. Pulse	Der Puls	Die Pulse
    1324. Absence	Die Abwesenheit	- 
    1325. Violence	Die Gewalt	- 
    1326. Humor	Der Humor	- 
    1327. Stool	Der Hocker	Die Hocker
    1328. Gravel	Der Kies	- 
    1329. Treasure	Der Schatz	Die Schätze
    1330. Butter	Die Butter	- 
    1331. Switch	Der Schalter	Die Schalter
    1332. Cigar	Die Zigarre	Die Zigarren
    1333. Canvas	Die Leinwand	Die Leinwände
    1334. Happiness	Das Glück	- 
    1335. Guide	Der Führer	Die Führer
    1336. Pin	Die Stecknadel	Die Stecknadeln
    1337. Actor	Der Schauspieler	Die Schauspieler
    1338. Whole	Das Ganze	- 
    1339. Arrangement	Die Anordnung	Die Anordnungen
    1340. Brown	Das Braun	- 
    1341. Host	Der Gastgeber	Die Gastgeber
    1342. Ribbon	Das Band	Die Bänder
    1343. Scarf	Der Schal	Die Schals
    1344. Scale	Die Skala	Die Skalen
    1345. Proof	Der Beweis	Die Beweise
    1346. Arrow	Der Pfeil	Die Pfeile
    1347. Temperature	Die Temperatur	Die Temperaturen
    1348. Technology	Die Technologie	Die Technologien
    1349. Permission	Die Erlaubnis	Die Erlaubnisse
    1350. Location	Der Standort	Die Standorte
    1351. Claw	Die Klaue	Die Klauen
    1352. Cowboy	Der Cowboy	Die Cowboys
    1353. Agency	Die Agentur	Die Agenturen
    1354. Construction	Der Bau	- 
    1355. Hunting	Die Jagd	- 
    1356. Vegetable	Das Gemüse	Die Gemüse
    1357. Tin	Die Konservendose	Die Konservendosen
    1358. Helicopter	Der Hubschrauber	Die Hubschrauber
    1359. Trap	Die Falle	Die Fallen
    1360. Pat	Der Schlag	- 
    1361. Gap	Die Lücke	Die Lücken
    1362. Pet	Das Haustier	Die Haustiere
    1363. Education	Das Bildung	- 
    1364. Shopping	Die Einkauf	Die Einkäufe
    1365. Shed	Der Schuppen	Die Schuppen
    1366. Agreement	Die Vereinbarung	Die Vereinbarungen
    1367. Soil	Der Boden	- 
    1368. Duke	Der Herzog	Die Herzog
    1369. Shotgun	Das Schrotflinte	Die Schrotflinten
    1370. Notion	Die Idee	Die Ideen
    1371. Rear	Das Heck	- 
    1372. Ceremony	Die Zeremonie	Die Zeremonien
    1373. Spoon	Der Löffel	Die Löffel
    1374. Tub	Die Badewanne	Die Badewannen
    1375. Clue	Der Hinweis	Die Hinweise
    1376. Iris	Die Iris	Die Irisse
    1377. Incident	Der Vorfall	Die Vorfälle
    1378. Crash	Der Zusammenstoß	Die Zusammenstöße
    1379. Journal	Das Journal	Die Journale
    1380. Access	Der Zugriff	- 
    1381. Brass	Das Messing	- 
    1382. Mommy	Die Mama	Die Mamas
    1383. Sidebar	Die Sidebar	Die Sidebars
    1384. Sheep	Das Schaf	Die Schafe
    1385. Engineer	Der Ingenieur	Die Ingenieure
    1386. Hull	Der Rumpf	Die Rümpfe
    1387. Odor	Der Geruch	Die Gerüche
    1388. Appointment	Die Termin	Die Termine
    1389. Invitation	Die Einladung	Die Einladungen
    1390. Rag	Das Lumpen	Die Lumpen
    1391. Good	Das Gute	- 
    1392. Dude	Der Typ	Die Typen
    1393. Treatment	Die Behandlung	Die Behandlungen
    1394. Wisdom	Die Weisheit	- 
    1395. Prize	Der Preis	Die Preise
    1396. Element	Das Element	Die Elemente
    1397. Giant	Der Riese	Die Riesen
    1398. Napkin	Die Serviette	Die Servietten
    1399. Laundry	Die Wäsche	- 
    1400. Option	Die Option	Die Optionen
    1401. Rack	Das Regal	Die Regale
    1402. Request	Die Anfrage	Die Anfragen
    1403. Jail	Das Gefängnis	Die Gefängnisse
    1404. Grandpa	Der Opa	Die Opas
    1405. Ranch	Die Ranch	Die Ranches
    1406. Dot	Der Punkt	Die Punkte
    1407. Script	Das Skript	Die Skripte
    1408. Mall	Das Einkaufszentrum	Die Einkaufszentren
    1409. Ford	Die Furt	Die Furten
    1410. Exercise	Die Übung	Die Übungen
    1411. Widow	Die Witwe	Die Witwen
    1412. Crow	Die Krähe	Die Krähen
    1413. Thread	Der Faden	Die Fäden
    1414. Suicide	Der Selbstmord	Die Selbstmorde
    1415. Notice	Das Hinweis	Die Hinweise
    1416. Sunset	Der Sonnenuntergang	Die Sonnenuntergänge
    1417. Gallery	Die Galerie	Die Galerien
    1418. Vessel	Das Gefäß	Die Gefäße
    1419. Thunder	Der Donner	- 
    1420. Soap	Die Seife	Die Seifen
    1421. Whiskey	Der Whisky	- 
    1422. Female	Die Frau	Die Frauen
    1423. Mayor	Der Bürgermeister	Die Bürgermeister
    1424. Stroke	Der Schlaganfall	Die Schlaganfälle
    1425. Click	Der Klick	Die Klicks
    1426. Reputation	Der Ruf	Die Rufe
    1427. Miller	Der Müller	Die Müller
    1428. Council	Der Rat	Die Räte
    1429. Schedule	Der Zeitplan	Die Zeitpläne
    1430. Cemetery	Der Friedhof	Die Friedhöfe
    1431. Struggle	Der Kampf	Die Kämpfe
    1432. Instinct	Der Instinkt	Die Instinkte
    1433. Calm	Die Ruhe	- 
    1434. Employee	Der Mitarbeiter	Die Mitarbeiter
    1435. Nest	Das Nest	Die Nester
    1436. Limit	Die Grenze	Die Grenzen
    1437. German	Der Deutsche	Die Deutschen
    1438. Monk	Der Mönch	Die Mönche
    1439. Worm	Der Wurm	Die Würmer
    1440. Document	Das Dokument	Die Dokumente
    1441. Sadness	Die Trauer	- 
    1442. Hut	Der Hut	Die Hüte
    1443. Lifetime	Das Leben	Die Leben
    1444. Dancer	Der Tänzer	Die Tänzer
    1445. Insurance	Die Versicherung	Die Versicherungen
    1446. Difficulty	Die Schwierigkeit	Die Schwierigkeiten
    1447. Mattress	Die Matratze	Die Matratzen
    1448. Male	Der Mann	Die Männer
    1449. Clinic	Die Klinik	Die Kliniken
    1450. Ad	Die Anzeige	Die Anzeigen
    1451. Mug	Der Becher	Die Becher
    1452. Kit	Das Set	Die Sets
    1453. Communication	Die Kommunikation	Die Kommunikationen
    1454. Disaster	Die Katastrophe	Die Katastrophen
    1455. Tile	Die Fliese	Die Fliesen
    1456. Receiver	Der Empfänger	Die Empfänger
    1457. Roar	Das Gebrüll	- 
    1458. Troop	Die Truppe	Die Truppen
    1459. Coffin	Der Sarg	Die Särge
    1460. Friendship	Die Freundschaft	Die Freundschaften
    1461. Investigation	Die Untersuchung	Die Untersuchungen
    1462. Sale	Der Verkauf	Die Verkäufe
    1463. Goal	Das Tor	Die Tore
    1464. Ambulance	Der Krankenwagen	Die Krankenwagen
    1465. Moonlight	Das Mondschein	- 
    1466. Ward	Die Station	Die Stationen
    1467. Trousers	Die Hose	Die Hosen
    1468. Wool	Die Wolle	- 
    1469. Mac	Der Regenmantel	Die Regenmäntel
    1470. Minister	Der Minister	Die Minister
    1471. Entry	Der Eintrag	Die Einträge
    1472. Thief	Der Dieb	Die Diebe
    1473. Briefcase	Der Aktenkoffer	Die Aktentaschen
    1474. Pity	Das Mitleid	- 
    1475. Fingertip	Die Fingerspitze	Die Fingerspitzen
    1476. Navy	Die Marine	Die Marinen
    1477. Insect	Das Insekt	Die Insekten
    1478. Velvet	Der Samt	- 
    1479. Bee	Die Biene	Die Bienen
    1480. Cane	Der Stock	Die Stöcke
    1481. Gene	Das Gen	Die Gene
    1482. Salad	Der Salat	Die Salate
    1483. Windshield	Die Windschutzscheibe	Die Windschutzscheiben
    1484. Outfit	Das Outfit	Die Outfits
    1485. Shuttle	Das Shuttle	Die Shuttle
    1486. Shout	Der Schrei	Die Schreie
    1487. Fury	Die Wut	- 
    1488. Challenge	Die Herausforderung	Die Herausforderungen
    1489. Satisfaction	Die Zufriedenheit	- 
    1490. Motor	Der Motor	Die Motoren
    1491. Product	Das Produkt	Die Produkte
    1492. Weed	Das Unkraut	- 
    1493. Stretch	Der Stretch	- 
    1494. Gym	Das Fitnessstudio	Die Fitnessstudios
    1495. Capital	Die Hauptstadt	Die Hauptstädte
    1496. Rim	Der Rand	Die Ränder
    1497. Paw	Die Pfote	Die Pfoten
    1498. Fort	Das Fort	Die Forts
    1499. Cost	Die Kosten	- 
    1500. Poster	Das Poster	Die Poster
    1501. Vampire	Der Vampir	Die Vampire
    1502. Shaft	Der Schaft	Die Schäfte
    1503. Identity	Die Identität	Die Identitäten
    1504. Pavement	Der Gehweg	Die Gehwege
    1505. Asshole	Das Arschloch	Die Arschlöcher
    1506. Strap	Das Band	Die Bänder
    1507. Parlor	Der Salon	Die Salons
    1508. Harbor	Der Hafen	Die Häfen
    1509. Example	Das Beispiel	Die Beispiele
    1510. Web	Das Netz	Die Netze
    1511. Golf	Der Golf	(usually uncountable)
    1512. Crap	Der Mist	(usually uncountable)
    1513. Delight	Die Freude	(usually uncountable)
    1514. Quilt	Die Steppdecke	Die Steppdecken
    1515. Tax	Die Steuer	Die Steuern
    1516. Fold	Die Falte	Die Falten
    1517. Portrait	Das Porträt	Die Porträts
    1518. Tissue	Das Gewebe	Die Gewebe
    1519. Belief	Der Glaube	Die Glauben
    1520. Costume	Das Kostüm	Die Kostüme
    1521. Measure	Das Maß	Die Maße
    1522. Carriage	Die Kutsche	Die Kutschen
    1523. Guitar	Die Gitarre	Die Gitarren
    1524. Knight	Der Ritter	Die Ritter
    1525. Rank	Der Rang	Die Ränge
    1526. Major	Der Major	Die Majore
    1527. Fountain	Der Brunnen	Die Brunnen
    1528. Stall	Der Stall	Die Ställe
    1529. Load	Die Ladung	Die Ladungen
    1530. Spark	Der Funke	Die Funken
    1531. Waste	Der Abfall	(usually uncountable)
    1532. Champagne	Der Champagner	(usually uncountable)
    1533. District	Der Bezirk	Die Bezirke
    1534. Protection	Der Schutz	(usually uncountable)
    1535. Judgment	Das Urteil	Die Urteile
    1536. Sympathy	Das Mitgefühl	(usually uncountable)
    1537. Violet	Das Veilchen	Die Veilchen
    1538. Impact	Der Aufprall	Die Aufprälle
    1539. Disappointment	Die Enttäuschung	Die Enttäuschungen
    1540. Drinking	Das Trinken	(usually uncountable)
    1541. Consciousness	Das Bewusstsein	(usually uncountable)
    1542. Handkerchief	Das Taschentuch	Die Taschentücher
    1543. Dancing	Das Tanzen	(usually uncountable)
    1544. Perfume	Das Parfüm	Die Parfüms
    1545. Network	Das Netzwerk	Die Netzwerke
    1546. Claim	Die Forderung	Die Forderungen
    1547. Nun	Die Nonne	Die Nonnen
    1548. Crown	Die Krone	Die Kronen
    1549. Railing	Das Geländer	Die Geländer
    1550. License	Die Lizenz	Die Lizenzen
    1551. Mercy	Die Gnade	(usually uncountable)
    1552. Balloon	Der Ballon	Die Ballons
    1553. Chaos	Das Chaos	(usually uncountable)
    1554. Fever	Das Fieber	(usually uncountable)
    1555. Locker	Der Schließfach	Die Schließfächer
    1556. Session	Die Sitzung	Die Sitzungen
    1557. Burst	Der Ausbruch	Die Ausbrüche
    1558. Peak	Der Gipfel	Die Gipfel
    1559. Drum	Die Trommel	Die Trommeln
    1560. Focus	Der Fokus	Die Foki
    1561. Frog	Der Frosch	Die Frösche
    1562. Benefit	Der Nutzen	Die Nutzen
    1563. Remark	Die Bemerkung	Die Bemerkungen
    1564. Tide	Die Flut	Die Fluten
    1565. Suspicion	Der Verdacht	Die Verdächte
    1566. Jeep	Der Jeep	Die Jeeps
    1567. Worry	Die Sorge	Die Sorgen
    1568. Literature	Die Literatur	(usually uncountable)
    1569. Archer	Der Bogenschütze	Die Bogenschützen
    1570. Household	Der Haushalt	Die Haushalte
    1571. Powder	Das Pulver	Die Pulver
    1572. Shepherd	Der Hirte	Die Hirten
    1573. Lens	Die Linse	Die Linsen
    1574. Favorite	Der Favorit	Die Favoriten
    1575. Madame	Die Dame	(no plural form)
    1576. Mansion	Die Villa	Die Villen
    1577. Boom	Der Boom	Die Booms
    1578. Lace	Die Spitze	Die Spitzen
    1579. Review	Die Bewertung	Die Bewertungen
    1580. Reception	Der Empfang	Die Empfänge
    1581. Scrap	Der Schrott	(usually uncountable)
    1582. Bead	Die Perle	Die Perlen
    1583. Glare	Das Blenden	(usually uncountable)
    1584. Flow	Der Fluss	Die Flüsse
    1585. Cafe	Das Café	Die Cafés
    1586. Status	Der Status	Die Stati
    1587. Pounding	Das Hämmern	(usually uncountable)
    1588. Rocket	Die Rakete	Die Raketen
    1589. Canyon	Die Schlucht	Die Schluchten
    1590. Sorrow	Die Trauer	(usually uncountable)
    1591. Spider	Die Spinne	Die Spinnen
    1592. Blast	Die Explosion	Die Explosionen
    1593. Personality	Die Persönlichkeit	Die Persönlichkeiten
    1594. Campus	Der Campus	Die Campi
    1595. Curse	Der Fluch	Die Flüche
    1596. Staircase	Das Treppenhaus	Die Treppenhäuser
    1597. Urge	Der Drang	Die Dränge
    1598. Frustration	Die Frustration	(usually uncountable)
    1599. Pump	Die Pumpe	Die Pumpen
    1600. Ease	Die Leichtigkeit	(usually uncountable)
    1601. Count	Der Graf	Die Grafen
    1602. Solution	Die Lösung	Die Lösungen
    1603. Jewelry	Der Schmuck	(usually uncountable)
    1604. Siren	Die Sirene	Die Sirenen
    1605. Hit	Der Hit	Die Hits
    1606. Tradition	Die Tradition	Die Traditionen
    1607. Curb	Der Bordstein	Die Bordsteine
    1608. Variety	Die Vielfalt	Die Vielfalten
    1609. Pirate	Der Pirat	Die Piraten
    1610. Description	Die Beschreibung	Die Beschreibungen
    1611. Dear	Der Liebling	Die Lieblinge
    1612. Anxiety	Die Angst	Die Ängste
    1613. Pitch	Die Tonhöhe	Die Tonhöhen
    1614. Pizza	Die Pizza	Die Pizzen
    1615. Elephant	Der Elefant	Die Elefanten
    1616. Politics	Die Politik	(usually uncountable)
    1617. Tennis	Das Tennis	(usually uncountable)
    1618. Hunger	Der Hunger	(usually uncountable)
    1619. Genius	Das Genie	Die Genies
    1620. Goat	Die Ziege	Die Ziegen
    1621. Victory	Der Sieg	Die Siege
    1622. Combination	Die Kombination	Die Kombinationen
    1623. Affiliation	Die Zugehörigkeit	Die Zugehörigkeiten
    1624. Momma	Die Mama	Die Mamas
    1625. Cape	Das Kap	Die Kaps
    1626. Headlight	Der Scheinwerfer	Die Scheinwerfer
    1627. Governor	Der Gouverneur	Die Gouverneure
    1628. Oxygen	Der Sauerstoff	(usually uncountable)
    1629. Bishop	Der Bischof	Die Bischöfe
    1630. Bundle	Das Bündel	Die Bündel
    1631. Development	Die Entwicklung	Die Entwicklungen
    1632. Fingernail	Der Fingernagel	Die Fingernägel
    1633. Score	Der Punktestand	Die Punktestände
    1634. Mate	Der Kamerad	Die Kameraden
    1635. Rider	Der Reiter	Die Reiter
    1636. Orbit	Die Umlaufbahn	Die Umlaufbahnen
    1637. Vine	Die Rebe	Die Reben
    1638. Suite	Die Suite	Die Suiten
    1639. Bartender	Der Barkeeper	Die Barkeeper
    1640. Coke	Die Cola	(usually uncountable)
    1641. Tune	Die Melodie	Die Melodien
    1642. Glory	Der Ruhm	(usually uncountable)
    1643. Rabbi	Der Rabbi	(plural form is Rabbiner)
    1644. Surgery	Die Operation	Die Operationen
    1645. Cattle	Das Rindvieh	(usually uncountable)
    1646. Ritual	Das Ritual	Die Rituale
    1647. Greeting	Der Gruß	Die Grüße
    1648. Slice	Die Scheibe	Die Scheiben
    1649. Homer	Der Homer	Die Homers
    1650. Fireplace	Der Kamin	Die Kamine
    1651. Jersey	Das Trikot	Die Trikots
    1652. Media	Die Medien	(plural noun)
    1653. Pop	Der Knall	Die Knalle
    1654. Cargo	Die Ladung	Die Ladungen
    1655. Inn	Die Herberge	Die Herbergen
    1656. Deputy	Der Stellvertreter	Die Stellvertreter
    1657. Despair	Die Verzweiflung	(usually uncountable)
    1658. Territory	Das Gebiet	Die Gebiete
    1659. Punch	Der Schlag	Die Schläge
    1660. Jazz	Der Jazz	(usually uncountable)
    1661. Hug	Die Umarmung	Die Umarmungen
    1662. Whistle	Die Pfeife	Die Pfeifen
    1663. Humanity	Die Menschheit	(usually uncountable)
    1664. Craft	Das Handwerk	Die Handwerke
    1665. Daylight	Das Tageslicht	(usually uncountable)
    1666. Worth	Der Wert	Die Werte
    1667. Slip	Die Einlage	Die Einlagen
    1668. Armor	Die Rüstung	Die Rüstungen
    1669. Backpack	Der Rucksack	Die Rucksäcke
    1670. Suggestion	Der Vorschlag	Die Vorschläge
    1671. Den	Die Höhle	Die Höhlen
    1672. Symbol	Das Symbol	Die Symbole
    1673. Colony	Die Kolonie	Die Kolonien
    1674. Conclusion	Der Schluss	Die Schlüsse
    1675. Nostril	Das Nasenloch	Die Nasenlöcher
    1676. Spear	Der Speer	Die Speere
    1677. Impulse	Der Impuls	Die Impulse
    1678. Tomato	Die Tomate	Die Tomaten
    1679. Calf	Das Kalb	Die Kälber
    1680. Autumn	Der Herbst	(usually uncountable)
    1681. Discovery	Die Entdeckung	Die Entdeckungen
    1682. Classroom	Das Klassenzimmer	Die Klassenzimmer
    1683. Delivery	Die Lieferung	Die Lieferungen
    1684. Spray	Das Spray	Die Sprays
    1685. Liquid	Die Flüssigkeit	Die Flüssigkeiten
    1686. Fuel	Der Treibstoff	(usually uncountable)
    1687. Underwear	Die Unterwäsche	(no plural form)
    1688. Dome	Die Kuppel	Die Kuppeln
    1689. Population	Die Bevölkerung	(usually uncountable)
    1690. Affection	Die Zuneigung	(usually uncountable)
    1691. Religion	Die Religion	Die Religionen
    1692. Singer	Der Sänger	Die Sängerinnen
    1693. Attendant	Der Bedienstete	Die Bediensteten
    1694. Illusion	Die Illusion	Die Illusionen
    1695. Link	Der Link	Die Links
    1696. Lounge	Die Lounge	Die Lounges
    1697. Interior	Das Innere	Die Innenräume
    1698. Shrug	Das Achselzucken	(usually uncountable)
    1699. Zone	Die Zone	Die Zonen
    1700. Standard	Der Standard	Die Standards
    1701. Coal	Die Kohle	(usually uncountable)
    1702. Chase	Die Jagd	Die Jagden
    1703. Lump	Der Kloß	Die Klöße
    1704. Charm	Der Charme	Die Charmes
    1705. Legend	Die Legende	Die Legenden
    1706. Consequence	Die Konsequenz	Die Konsequenzen
    1707. Observation	Die Beobachtung	Die Beobachtungen
    1708. Bicycle	Das Fahrrad	Die Fahrräder
    1709. Harm	Der Schaden	(usually uncountable)
    1710. Pay	Der Lohn	Die Löhne
    1711. Prospect	Die Aussicht	Die Aussichten
    1712. Subway	Die U-Bahn	Die U-Bahnen
    1713. Sample	Das Muster	Die Muster
    1714. Cherry	Die Kirsche	Die Kirschen
    1715. Dealer	Der Händler	Die Händler
    1716. Assignment	Die Aufgabe	Die Aufgaben
    1717. Hurry	Die Eile	(usually uncountable)
    1718. Mistress	Die Geliebte	Die Geliebten
    1719. Mound	Der Hügel	Die Hügel
    1720. Nonsense	Der Unsinn	(usually uncountable)
    1721. Committee	Der Ausschuss	Die Ausschüsse
    1722. Echo	Das Echo	Die Echos
    1723. Slack	Der Nachgiebigkeit	(usually uncountable)
    1724. Decker	Die Decker	(plural noun)
    1725. Warehouse	Das Lager	Die Lager
    1726. Bout	Der Kampf	Die Kämpfe
    1727. Toast	Der Toast	Die Toasts
    1728. Facility	Die Einrichtung	Die Einrichtungen
    1729. Basketball	Der Basketball	(usually uncountable)
    1730. Mustache	Der Schnurrbart	Die Schnurrbärte
    1731. Senator	Der Senator	Die Senatoren
    1732. Share	Die Aktie	Die Aktien
    1733. Eyelid	Das Augenlid	Die Augenlider
    1734. Enthusiasm	Die Begeisterung	(usually uncountable)
    1735. Chunk	Das Stück	Die Stücke
    1736. Turtle	Die Schildkröte	Die Schildkröten
    1737. Alcohol	Der Alkohol	(usually uncountable)
    1738. Gum	Der Kaugummi	Die Kaugummis
    1739. Turkey	Der Truthahn	Die Truthähne
    1740. Preacher	Der Prediger	Die Prediger
    1741. Possession	Der Besitz	(usually uncountable)
    1742. Dolly	Die Sackkarre	Die Sackkarren
    1743. Linen	Das Leinen	(usually uncountable)
    1744. Apology	Die Entschuldigung	Die Entschuldigungen
    1745. Lecture	Der Vortrag	Die Vorträge
    1746. Boulder	Der Fels	Die Felsen
    1747. Heap	Der Haufen	Die Haufen
    1748. Photographer	Der Fotograf	Die Fotografen
    1749. Brake	Die Bremse	Die Bremsen
    1750. Demand	Die Nachfrage	Die Nachfragen
    1751. Apron	Die Schürze	Die Schürzen
    1752. Cloak	Der Umhang	Die Umhänge
    1753. Jury	Die Jury	Die Jurys
    1754. Hearing	Die Anhörung	Die Anhörungen
    1755. Gray	Das Grau	(usually uncountable)
    1756. Crate	Die Kiste	Die Kisten
    1757. Method	Die Methode	Die Methoden
    1758. Reference	Die Referenz	Die Referenzen
    1759. Disgust	Der Ekel	(usually uncountable)
    1760. Liquor	Der Schnaps	Die Schnäpse
    1761. Lipstick	Der Lippenstift	Die Lippenstifte
    1762. Core	Der Kern	Die Kerne
    1763. Individual	Das Individuum	Die Individuen
    1764. Container	Der Container	Die Container
    1765. Whore	Die Hure	Die Huren
    1766. Infant	Das Kleinkind	Die Kleinkinder
    1767. Sunglasses	Die Sonnenbrille	Die Sonnenbrillen
    1768. Hose	Die Hose	Die Hosen
    1769. Concert	Das Konzert	Die Konzerte
    1770. Bullshit	Der Unsinn	(usually uncountable)
    1771. Railroad	Die Eisenbahn	Die Eisenbahnen
    1772. Parade	Die Parade	Die Paraden
    1773. Compartment	Das Abteil	Die Abteile
    1774. Resident	Der Bewohner	Die Bewohner
    1775. Oven	Der Ofen	Die Öfen
    1776. Technician	Der Techniker	Die Techniker
    1777. Procedure	Das Verfahren	Die Verfahren
    1778. Fighter	Der Kämpfer	Die Kämpfer
    1779. Grain	Das Korn	Die Körner
    1780. Picnic	Das Picknick	Die Picknicks
    1781. Tribe	Der Stamm	Die Stämme
    1782. Bud	Die Knospe	Die Knospen
    1783. Meadow	Die Wiese	Die Wiesen
    1784. Public	Die Öffentlichkeit	(usually uncountable)
    1785. Poison	Das Gift	Die Gifte
    1786. Buffalo	Der Büffel	Die Büffel
    1787. Region	Die Region	Die Regionen
    1788. Production	Die Produktion	Die Produktionen
    1789. Running	Das Laufen	(usually uncountable)
    1790. Loop	Die Schleife	Die Schleifen
    1791. Sleeping	Das Schlafen	(usually uncountable)
    1792. Soda	Die Limonade	Die Limonaden
    1793. Owl	Die Eule	Die Eulen
    1794. Menu	Das Menü	Die Menüs
    1795. Kick	Der Tritt	Die Tritte
    1796. Ruin	Der Ruin	Die Ruinen
    1797. Ramp	Die Rampe	Die Rampen
    1798. Streak	Die Streif	Die Streifen
    1799. Forearm	Der Unterarm	Die Unterarme
    1800. Bureau	Das Büro	Die Büros
    1801. Knuckle	Das Gelenk	Die Gelenke
    1802. Goose	Die Gans	Die Gänse
    1803. Advance	Der Fortschritt	Die Fortschritte
    1804. Fairy	Die Fee	Die Feen
    1805. Illness	Die Krankheit	Die Krankheiten
    1806. Squad	Das Kommando	Die Kommandos
    1807. Official	Der Beamte	Die Beamten
    1808. Brand	Die Marke	Die Marken
    1809. Organ	Das Organ	Die Organe
    1810. Butterfly	Der Schmetterling	Die Schmetterlinge
    1811. Empire	Das Imperium	Die Reiche
    1812. Profile	Das Profil	Die Profile
    1813. Liberty	Die Freiheit	Die Freiheiten
    1814. Disbelief	Der Unglaube	(usually uncountable)
    1815. Grove	Der Hain	Die Haine
    1816. Shield	Der Schild	Die Schilde
    1817. Saddle	Der Sattel	Die Sättel
    1818. Odds	Die Chancen	(plural noun)
    1819. Cluster	Der Cluster	Die Cluster
    1820. Satellite	Der Satellit	Die Satelliten
    1821. Trigger	Der Auslöser	Die Auslöser
    1822. Puppy	Der Welpe	Die Welpen
    1823. Waiting	Das Warten	(usually uncountable)
    1824. Bulb	Die Glühbirne	Die Glühbirnen
    1825. Dresser	Die Kommode	Die Kommoden
    1826. Patrol	Die Patrouille	Die Patrouillen
    1827. Eagle	Der Adler	Die Adler
    1828. Privacy	Die Privatsphäre	(no plural form)
    1829. Fluid	Die Flüssigkeit	Die Flüssigkeiten
    1830. Herd	Die Herde	(plural noun)
    1831. Headache	Die Kopfschmerzen	(plural noun)
    1832. Amusement	Die Unterhaltung	Die Unterhaltungen
    1833. Wheelchair	Der Rollstuhl	Die Rollstühle
    1834. Policy	Die Politik	(usually uncountable)
    1835. Belle	Die Schönheit	Die Schönheiten
    1836. Tobacco	Der Tabak	(usually uncountable)
    1837. Setting	Die Einstellung	Die Einstellungen
    1838. Tattoo	Das Tattoo	Die Tattoos
    1839. Burden	Die Belastung	Die Belastungen
    1840. Merchant	Der Händler	Die Händler
    1841. Slide	Die Rutsche	Die Rutschen
    1842. Stain	Der Fleck	Die Flecken
    1843. Eating	Das Essen	(usually uncountable)
    1844. Bond	Die Bindung	Die Bindungen
    1845. Swimming	Das Schwimmen	(usually uncountable)
    1846. Foundation	Die Stiftung	Die Stiftungen
    1847. Injury	Die Verletzung	Die Verletzungen
    1848. League	Die Liga	Die Ligen
    1849. Battery	Die Batterie	Die Batterien
    1850. Umbrella	Der Regenschirm	Die Regenschirme
    1851. Emperor	Der Kaiser	Die Kaiser
    1852. Pier	Der Pier	Die Piers
    1853. Tap	Der Wasserhahn	Die Wasserhähne
    1854. Wit	Das Witz	Die Witze
    1855. Cutter	Der Cutter	Die Cutter
    1856. Attic	Der Dachboden	Die Dachböden
    1857. Tiger	Der Tiger	Die Tiger
    1858. Pal	Der Freund	Die Freunde
    1859. Ancestor	Der Vorfahr	Die Vorfahren
    1860. Concentration	Die Konzentration	(usually uncountable)
    1861. Mount	Der Berg	Die Berge
    1862. Expense	Die Kosten	(plural noun)
    1863. Blessing	Der Segen	Die Segen
    1864. Leave	Der Urlaub	(usually uncountable)
    1865. Ledge	Der Vorsprung	Die Vorsprünge
    1866. Torch	Die Fackel	Die Fackeln
    1867. Ink	Die Tinte	(usually uncountable)
    1868. Plot	Die Handlung	Die Handlungen
    1869. Rent	Die Miete	Die Mieten
    1870. Mule	Die Maultier	Die Maultiere
    1871. Arch	Der Bogen	Die Bögen
    1872. Environment	Die Umwelt	Die Umwelten
    1873. Frown	Die Stirnrunzeln	(plural noun)
    1874. Inspector	Der Inspektor	Die Inspektoren
    1875. Midst	Die Mitte	Die Mitte
    1876. Embarrassment	Die Peinlichkeit	Die Peinlichkeiten
    1877. Complaint	Die Beschwerde	Die Beschwerden
    1878. Portion	Die Portion	Die Portionen
    1879. Chuck	Die Wegwerfen	(usually uncountable)
    1880. Clearing	Die Lichtung	Die Lichtungen
    1881. Crisis	Die Krise	Die Krisen
    1882. Necklace	Die Halskette	Die Halsketten
    1883. Lantern	Die Laterne	Die Laternen
    1884. Wealth	Der Reichtum	(usually uncountable)
    1885. Murderer	Der Mörder	Die Mörder
    1886. Civilization	Die Zivilisation	Die Zivilisationen
    1887. Concept	Das Konzept	Die Konzepte
    1888. Lamb	Das Lamm	Die Lämmer
    1889. Stride	Die Schritt	Die Schritte
    1890. Cuff	Das Manschette	Die Manschetten
    1891. Virgin	Die Jungfrau	Die Jungfrauen
    1892. Squirrel	Das Eichhörnchen	Die Eichhörnchen
    1893. Babe	Das Baby	Die Babys
    1894. Starling	Der Star	Die Stare
    1895. Depression	Die Depression	Die Depressionen
    1896. Storage	Die Lagerung	Die Lagerungen
    1897. Altar	Der Altar	Die Altäre
    1898. Tragedy	Die Tragödie	Die Tragödien
    1899. Resource	Die Ressource	Die Ressourcen
    1900. Traveler	Der Reisende	Die Reisenden
    1901. Trust	Das Vertrauen	(usually uncountable)
    1902. Arc	Der Bogen	Die Bögen
    1903. Kingdom	Das Königreich	Die Königreiche
    1904. Jewel	Das Juwel	Die Juwelen
    1905. Musician	Der Musiker	Die Musiker
    1906. Airplane	Das Flugzeug	Die Flugzeuge
    1907. Junk	Der Müll	(usually uncountable)
    1908. Sunshine	Der Sonnenschein	(usually uncountable)
    1909. Lad	Der Junge	Die Jungen
    1910. Elf	Der Elf	Die Elfen
    1911. Protest	Der Protest	Die Proteste
    1912. Hunt	Die Jagd	Die Jagden
    1913. Executive	Der Geschäftsführer	Die Geschäftsführer
    1914. Diary	Das Tagebuch	Die Tagebücher
    1915. Aspect	Der Aspekt	Die Aspekte
    1916. Dial	Das Zifferblatt	Die Zifferblätter
    1917. Slipper	Der Pantoffel	Die Pantoffel
    1918. Actress	Die Schauspielerin	Die Schauspielerinnen
    1919. Shooting	Das Schießen	(usually uncountable)
    1920. Earring	Der Ohrring	Die Ohrringe
    1921. Ant	Die Ameise	Die Ameisen
    1922. Patty	Das Brötchen	Die Brötchen
    1923. Sauce	Die Sauce	Die Saucen
    1924. Missile	Die Rakete	Die Raketen
    1925. Intensity	Die Intensität	(usually uncountable)
    1926. Ditch	Der Graben	Die Gräben
    1927. Daisy	Das Gänseblümchen	Die Gänseblümchen
    1928. Chapel	Die Kapelle	Die Kapellen
    1929. Swamp	Das Sumpf	Die Sümpfe
    1930. Relation	Die Beziehung	Die Beziehungen
    1931. Guess	Die Vermutung	Die Vermutungen
    1932. Crane	Der Kran	Die Kräne
    1933. Encounter	Das Aufeinandertreffen	Die Aufeinandertreffen
    1934. Sequence	Die Abfolge	Die Abfolgen
    1935. Fragment	Das Fragment	Die Fragmente
    1936. Draft	Die Ausarbeitung	Die Ausarbeitungen
    1937. Diner	Das Speiselokal	Die Speiselokale
    1938. Function	Die Funktion	Die Funktionen
    1939. Organization	Die Organisation	Die Organisationen
    1940. Skeleton	Das Skelett	Die Skelette
    1941. Misery	Das Elend	(usually uncountable)
    1942. Herb	Das Kraut	Die Kräuter
    1943. Stump	Der Stumpf	Die Stümpfe
    1944. Stake	Der Einsatz	Die Einsätze
    1945. Puff	Das Puff	Die Puffs
    1946. Creation	Die Schaffung	Die Schaffungen
    1947. Wake	Das Erwachen	Die Erwachen
    1948. Wizard	Der Zauberer	Die Zauberer
    1949. Mat	Das Matte	Die Matten
    1950. Seal	Die Dichtung	Die Dichtungen
    1951. Twilight	Die Dämmerung	(usually uncountable)
    1952. Grunt	Das Grunzen	Die Grunzen
    1953. Punishment	Die Bestrafung	Die Bestrafungen
    1954. Clan	Der Clan	Die Clans
    1955. Copper	Das Kupfer	(usually uncountable)
    1956. Debris	Der Schutt	(no plural form)
    1957. Painter	Der Maler	Die Maler
    1958. Steering	Die Lenkung	Die Lenkungen
    1959. Math	Die Mathematik	(usually uncountable)
    1960. Recognition	Die Anerkennung	(usually uncountable)
    1961. Temper	Der Gemüt	(usually uncountable)
    1962. Regret	Das Bedauern	(usually uncountable)
    1963. Destination	Das Ziel	Die Ziele
    1964. Mill	Die Mühle	Die Mühlen
    1965. Error	Der Fehler	Die Fehler
    1966. Romance	Die Romanze	Die Romanzen
    1967. Topic	Das Thema	Die Themen
    1968. Patio	Die Terrasse	Die Terrassen
    1969. Shovel	Die Schaufel	Die Schaufeln
    1970. Pajamas	Der Schlafanzug	Die Schlafanzüge
    1971. EMail	Die E-Mail	Die E-Mails
    1972. Pigeon	Die Taube	Die Tauben
    1973. Dinosaur	Der Dinosaurier	Die Dinosaurier
    1974. Industry	Die Industrie	Die Industrien
    1975. Operator	Der Operator	Die Operatoren
    1976. Lift	Der Aufzug	Die Aufzüge
    1977. Counselor	Der Berater	Die Berater
    1978. Gathering	Das Treffen	Die Treffen
    1979. Principle	Das Prinzip	Die Prinzipien
    1980. Drama	Das Drama	Die Dramen
    1981. Chick	Das Küken	Die Küken
    1982. Chart	Das Diagramm	Die Diagramme
    1983. Campaign	Die Kampagne	Die Kampagnen
    1984. Laurel	Der Lorbeer	Die Lorbeeren
    1985. Steak	Das Steak	Die Steaks
    1986. Criminal	Der Verbrecher	Die Verbrecher
    1987. Globe	Der Globus	Die Globen
    1988. Bruise	Der Bluterguss	Die Blutergüsse
    1989. Knob	Der Knopf	Die Knöpfe
    1990. Killing	Der Mord	Die Morde
    1991. Sweetheart	Die Liebste	Die Liebsten
    1992. Opera	Die Oper	Die Opern
    1993. Frost	Der Frost	(no plural form)
    1994. Nipple	Die Brustwarze	Die Brustwarzen
    1995. Reverend	Der Pfarrer	Die Pfarrer
    1996. Haze	Der Dunst	(usually uncountable)
    1997. Flood	Die Überschwemmung	Die Überschwemmungen
    1998. Carol	Das Lied	Die Lieder
    1999. Weakness	Die Schwäche	Die Schwächen
    2000. Cooking	Das Kochen	(usually uncountable)
    """

german_vocab = []
for line in raw_data.strip().splitlines():
    line = line.strip()
    if not line:
        continue
    parts = re.split(r'\s{2,}|\t', line)
    if len(parts) == 3:
        m = re.match(r"(\d+)\.\s*(.+)", parts[0])
        if m:
            number = int(m.group(1))
            english = m.group(2).strip()
            german_singular = parts[1].strip()
            german_plural = parts[2].strip()
            german_vocab.append({
                "number": number,
                "english": english,
                "german_singular": german_singular,
                "german_plural": german_plural
            })

if active_mode == 'Word practice':

    df_voc = pd.DataFrame(german_vocab)

    # Initialize session state for tracking and timing
    if "word_idx" not in st.session_state:
        st.session_state.word_idx = None
    if "wp_show_translation" not in st.session_state:
        st.session_state.wp_show_translation = False
    if "wp_known_words" not in st.session_state:
        st.session_state.wp_known_words = set()
    if "wp_unknown_words" not in st.session_state:
        st.session_state.wp_unknown_words = set()

    # Helper to get a new word
    def get_new_word():
        st.session_state.word_idx = df_voc.sample(n=1).index[0]
        st.session_state.wp_show_translation = False
    
    # On first load or after auto-advance, get a new word
    if st.session_state.word_idx is None:
        get_new_word()

    row = df_voc.loc[st.session_state.word_idx]
    german_word = row['german_singular']
    english_word = row['english']
    plural_word = row['german_plural']

    # Extract article and noun
    parts = german_word.split(' ', 1)
    if len(parts) == 2:
        article, noun = parts
    else:
        article, noun = "", german_word

    article_colors = {"der": "blue", "das": "green", "die": "red"}
    color = article_colors.get(article.lower(), "black")
    st.markdown(
    f"<span style='color:{color}; font-size:2em; font-weight:bold'>{article}</span> "
    f"<span style='font-size:2em'>{noun}</span>",
    unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    if not st.session_state.wp_show_translation:
        if st.button("Show translation"):
            st.session_state.wp_show_translation = True
            st.rerun()
    else:
        st.write(f"**English:** {english_word}")
        st.write(f"**Plural:** {plural_word}")
        if st.button("New word!"):
            get_new_word()
            st.rerun()
        with col1:
            if st.button("I knew this word", key="wp_known"):
                st.session_state.wp_feedback = "✅ Marked as known!"
                st.session_state.wp_known_words.add(german_word)
                st.session_state.wp_unknown_words.discard(german_word)
        with col2:
            if st.button("I didn't know this word", key="wp_unknown"):
                st.session_state.wp_feedback = "❌ Marked as unknown."
                st.session_state.wp_unknown_words.add(german_word)
                st.session_state.wp_known_words.discard(german_word)

    # Show stats and lists in sidebar
    st.sidebar.markdown(f"**Known words this session:** {len(st.session_state.wp_known_words)}")
    st.sidebar.markdown(f"**Unknown words this session:** {len(st.session_state.wp_unknown_words)}")

    st.sidebar.markdown("**Known words:**")
    if st.session_state.wp_known_words:
        st.sidebar.write(", ".join(sorted(st.session_state.wp_known_words)))
    else:
        st.sidebar.write("_None yet_")

    st.sidebar.markdown("**Unknown words:**")
    if st.session_state.wp_unknown_words:
        st.sidebar.write(", ".join(sorted(st.session_state.wp_unknown_words)))
    else:
        st.sidebar.write("_None yet_")

elif active_mode == 'Sentence practice':
    df_sentences = pd.read_csv('german-english-sample.tsv', sep='\t', header=None, usecols=[1, 3], names=['german', 'english'])

    # Load German model
    nlp = spacy.load("de_core_news_sm")

    pos_colors = {
        "NOUN": "#00bcd4",    # cyan
        "VERB": "#4caf50",    # green
        "ADJ": "#e040fb",     # magenta
        "ADV": "#9b8410",     # yellow
        "PRON": "#2196f3",    # blue
        "DET": "#9e9e9e",     # grey
        "ADP": "#f44336",     # red
        "AUX": "#4caf50",     # green
        "PROPN": "#00bcd4",   # cyan
        "NUM": "#9b8410",     # yellow
        "CONJ": "#f44336",    # red
        "CCONJ": "#f44336",   # red
        "SCONJ": "#f44336",   # red
        "PART": "#9e9e9e",    # grey
        "INTJ": "#9b8410",    # yellow
        "PUNCT": "#9e9e9e",   # grey
        "SYM": "#9e9e9e",     # grey
        "X": "#9e9e9e"        # grey
    }

    def color_sentence(doc):
        html = ""
        for token in doc:
            color = pos_colors.get(token.pos_, "#9e9e9e")
            html += f"<span style='color:{color}'>{token.text}</span> "
        return html

    # Color legend
    st.sidebar.markdown("""
    **Color legend:**  
    <span style='color:#00bcd4'>NOUN/PROPN</span> (nouns, proper nouns)  
    <span style='color:#4caf50'>VERB/AUX</span> (verbs, auxiliary verbs)  
    <span style='color:#e040fb'>ADJ</span> (adjectives)  
    <span style='color:#ffd600'>ADV/NUM/INTJ</span> (adverbs, numbers, interjections)  
    <span style='color:#2196f3'>PRON</span> (pronouns)  
    <span style='color:#f44336'>ADP/CONJ/CCONJ/SCONJ</span> (prepositions, conjunctions)  
    <span style='color:#9e9e9e'>DET/PART/PUNCT/SYM/X</span> (determiners, particles, punctuation, symbols, other)  
    """, unsafe_allow_html=True)

    # Initialize session state for tracking
    if "sentence_idx" not in st.session_state:
        st.session_state.sentence_idx = None
        st.session_state.show_translation = False
    if "sp_known_sentences" not in st.session_state:
        st.session_state.sp_known_sentences = set()
    if "sp_unknown_sentences" not in st.session_state:
        st.session_state.sp_unknown_sentences = set()
    if "sp_feedback" not in st.session_state:
        st.session_state.sp_feedback = ""

    red_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Show me a sentence!"):
        st.session_state.sentence_idx = df_sentences.sample(n=1).index[0]
        st.session_state.show_translation = False
        st.session_state.sp_feedback = ""

    if st.session_state.sentence_idx is not None:
        row = df_sentences.loc[st.session_state.sentence_idx]
        sentence = row['german']
        doc = nlp(sentence)
        colored_sentence = color_sentence(doc)
        st.markdown(f"**German:**<br><span style='font-size:2em; font-weight:bold'>{colored_sentence}</span>",unsafe_allow_html=True)

        if st.button("Show translation"):
            st.session_state.show_translation = True

        if st.session_state.show_translation:
            st.markdown(f"**English:** {row['english']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("I knew this sentence", key="sp_known"):
                    st.session_state.sp_feedback = "✅ Marked as known!"
                    st.session_state.sp_known_sentences.add(sentence)
                    st.session_state.sp_unknown_sentences.discard(sentence)
            with col2:
                if st.button("I didn't understand this sentence", key="sp_unknown"):
                    st.session_state.sp_feedback = "❌ Marked as unknown."
                    st.session_state.sp_unknown_sentences.add(sentence)
                    st.session_state.sp_known_sentences.discard(sentence)

            if st.session_state.sp_feedback:
                st.markdown(st.session_state.sp_feedback)
                # Automatically show a new sentence after pressing Enter
                st.session_state.sentence_idx = df_sentences.sample(n=1).index[0]
                st.session_state.show_translation = False
                st.session_state.sp_feedback = ""

    # Show stats
    st.sidebar.markdown(f"**Known sentences this session:** {len(st.session_state.sp_known_sentences)}")
    st.sidebar.markdown(f"**Unknown sentences this session:** {len(st.session_state.sp_unknown_sentences)}")

    st.sidebar.markdown("**Known sentences:**")
    if st.session_state.sp_known_sentences:
        st.sidebar.write(", ".join(sorted(st.session_state.sp_known_sentences)))
    else:
        st.sidebar.write("_None yet_")

    st.sidebar.markdown("**Unknown sentences:**")
    if st.session_state.sp_unknown_sentences:
        st.sidebar.write(", ".join(sorted(st.session_state.sp_unknown_sentences)))
    else:
        st.sidebar.write("_None yet_")

elif active_mode == 'Translate words':
    german_vocab = []
    for line in raw_data.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = re.split(r'\s{2,}|\t', line)
        if len(parts) == 3:
            m = re.match(r"(\d+)\.\s*(.+)", parts[0])
            if m:
                number = int(m.group(1))
                english = m.group(2).strip()
                german_singular = parts[1].strip()
                german_plural = parts[2].strip()
                german_vocab.append({
                    "number": number,
                    "english": english,
                    "german_singular": german_singular,
                    "german_plural": german_plural
                })
    df_voc = pd.DataFrame(german_vocab)

    direction = st.radio("Choose translation direction:", ["German → English", "English → German"])

    # Initialize session state for tracking
    if "tw_word_idx" not in st.session_state:
        st.session_state.tw_word_idx = None
        st.session_state.tw_feedback = ""
    if "known_words" not in st.session_state:
        st.session_state.known_words = set()
    if "unknown_words" not in st.session_state:
        st.session_state.unknown_words = set()

    red_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Show me a word!"):
        st.session_state.tw_word_idx = df_voc.sample(n=1).index[0]
        st.session_state.tw_feedback = ""
        st.session_state["tw_input1"] = ""  
        st.session_state["tw_input2"] = ""  

    if st.session_state.tw_word_idx is not None:
        row = df_voc.loc[st.session_state.tw_word_idx]
        german_word = row['german_singular']
        english_word = row['english']

        if direction == "German → English":
            st.markdown(f"**German:**<br><span style='font-size:2em; font-weight:bold'>{german_word}</span>",unsafe_allow_html=True)
            user_input = st.text_input("Write English translation:", key="tw_input1", on_change=lambda: None)
            if user_input:
                if user_input.strip().lower() == english_word.lower() or english_word.lower() in user_input.strip().lower() or user_input.strip().lower() in english_word.lower():
                    st.session_state.tw_feedback = "✅ Correct!"
                    st.session_state.known_words.add(german_word)
                    st.session_state.unknown_words.discard(german_word)
                else:
                    st.session_state.tw_feedback = f"❌ Correct answer: {english_word}"
                    st.session_state.unknown_words.add(german_word)
        else:
            st.markdown(f"**English:**<br><span style='font-size:2em; font-weight:bold'>{english_word}</span>",unsafe_allow_html=True)
            user_input = st.text_input("Write German translation:", key="tw_input2", on_change=lambda: None)
            if user_input:
                if user_input.strip().lower() == german_word.lower() or german_word.lower() in user_input.strip().lower() or user_input.strip().lower() in german_word.lower():
                    st.session_state.tw_feedback = "✅ Correct!"
                    st.session_state.known_words.add(english_word)
                    st.session_state.unknown_words.discard(english_word)
                else:
                    st.session_state.tw_feedback = f"❌ Correct answer: {german_word}"
                    st.session_state.unknown_words.add(english_word)

        if st.session_state.tw_feedback:
            st.markdown(st.session_state.tw_feedback)
            

    # Show stats
    st.sidebar.markdown(f"**Known words this session:** {len(st.session_state.known_words)}")
    st.sidebar.markdown(f"**Unknown words this session:** {len(st.session_state.unknown_words)}")

    st.sidebar.markdown("**Known words:**")
    if st.session_state.known_words:
        st.sidebar.write(", ".join(sorted(st.session_state.known_words)))
    else:
        st.sidebar.write("_None yet_")

    st.sidebar.markdown("**Unknown words:**")
    if st.session_state.unknown_words:
        st.sidebar.write(", ".join(sorted(st.session_state.unknown_words)))
    else:
        st.sidebar.write("_None yet_")
elif active_mode == 'Translate sentences':
    df_sentences = pd.read_csv('german-english-sample.tsv', sep='\t', header=None, usecols=[1, 3], names=['german', 'english'])

    # Initialize session state for tracking
    if "ts_sentence_idx" not in st.session_state:
        st.session_state.ts_sentence_idx = None
        st.session_state.ts_feedback = ""
    if "ts_known_sentences" not in st.session_state:
        st.session_state.ts_known_sentences = set()
    if "ts_unknown_sentences" not in st.session_state:
        st.session_state.ts_unknown_sentences = set()

    direction = st.radio("Choose translation direction:", ["German → English", "English → German"], key="ts_direction")

    red_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Show me a sentence!"):
        st.session_state.ts_sentence_idx = df_sentences.sample(n=1).index[0]
        st.session_state.ts_feedback = ""
        st.session_state["ts_input"] = ""  

    if st.session_state.ts_sentence_idx is not None:
        row = df_sentences.loc[st.session_state.ts_sentence_idx]
        german_sentence = row['german']
        english_sentence = row['english']

        if direction == "German → English":
            st.markdown(f"**German:**<br><span style='font-size:2em; font-weight:bold'>{german_sentence}</span>",unsafe_allow_html=True)
            user_input = st.text_input("Write English translation:", key="ts_input", on_change=lambda: None)
            if user_input:
                if user_input.strip().lower() == english_sentence.strip().lower() or english_sentence.strip().lower() in user_input.strip().lower():
                    st.session_state.ts_feedback = "✅ Correct!"
                    st.session_state.ts_known_sentences.add(german_sentence)
                    st.session_state.ts_unknown_sentences.discard(german_sentence)
                else:
                    st.session_state.ts_feedback = f"❌ Correct answer: {english_sentence}"
                    st.session_state.ts_unknown_sentences.add(german_sentence)
        else:
            st.markdown(f"**English:**<br><span style='font-size:2em; font-weight:bold'>{english_sentence}</span>",unsafe_allow_html=True)
            user_input = st.text_input("Write German translation:", key="ts_input2", on_change=lambda: None)
            if user_input:
                if user_input.strip().lower() == german_sentence.strip().lower() or german_sentence.strip().lower() in user_input.strip().lower():
                    st.session_state.ts_feedback = "✅ Correct!"
                    st.session_state.ts_known_sentences.add(english_sentence)
                    st.session_state.ts_unknown_sentences.discard(english_sentence)
                else:
                    st.session_state.ts_feedback = f"❌ Correct answer: {german_sentence}"
                    st.session_state.ts_unknown_sentences.add(english_sentence)

        if st.session_state.ts_feedback:
            st.markdown(st.session_state.ts_feedback)

    st.sidebar.markdown(f"**Known sentences this session:** {len(st.session_state.ts_known_sentences)}")
    st.sidebar.markdown(f"**Unknown sentences this session:** {len(st.session_state.ts_unknown_sentences)}")

    st.sidebar.markdown("**Known sentences:**")
    if st.session_state.ts_known_sentences:
        st.sidebar.write(", ".join(sorted(st.session_state.ts_known_sentences)))
    else:
        st.sidebar.write("_None yet_")

    st.sidebar.markdown("**Unknown sentences:**")
    if st.session_state.ts_unknown_sentences:
        st.sidebar.write(", ".join(sorted(st.session_state.ts_unknown_sentences)))
    else:
        st.sidebar.write("_None yet_")

elif active_mode == 'Pronoun declination practice':
    german_pronouns = {
        "1st_singular": {
            "nominative": "ich",
            "accusative": "mich",
            "dative": "mir",
            "genitive": "meiner"
        },
        "2nd_singular_informal": {
            "nominative": "du",
            "accusative": "dich",
            "dative": "dir",
            "genitive": "deiner"
        },
        "3rd_singular_masculine": {
            "nominative": "er",
            "accusative": "ihn",
            "dative": "ihm",
            "genitive": "seiner"
        },
        "3rd_singular_feminine": {
            "nominative": "sie",
            "accusative": "sie",
            "dative": "ihr",
            "genitive": "ihrer"
        },
        "3rd_singular_neuter": {
            "nominative": "es",
            "accusative": "es",
            "dative": "ihm",
            "genitive": "seiner"
        },
        "1st_plural": {
            "nominative": "wir",
            "accusative": "uns",
            "dative": "uns",
            "genitive": "unser"
        },
        "2nd_plural_informal": {
            "nominative": "ihr",
            "accusative": "euch",
            "dative": "euch",
            "genitive": "euer"
        },
        "3rd_plural": {
            "nominative": "sie",
            "accusative": "sie",
            "dative": "ihnen",
            "genitive": "ihrer"
        },
        "2nd_singular_formal": {
            "nominative": "Sie",
            "accusative": "Sie",
            "dative": "Ihnen",
            "genitive": "Ihrer"
        },
        "2nd_plural_formal": {
            "nominative": "Sie",
            "accusative": "Sie",
            "dative": "Ihnen",
            "genitive": "Ihrer"
        }
    }

    case_colors = {
        "nominative": "blue",
        "accusative": "red",
        "dative": "green",
        "genitive": "orange"
    }

    # Table header
    header = (
        f"{'Type':<24} "
        f"<span style='color:{case_colors['nominative']};font-weight:bold'>NOM</span>   "
        f"<span style='color:{case_colors['accusative']};font-weight:bold'>ACC</span>   "
        f"<span style='color:{case_colors['dative']};font-weight:bold'>DAT</span>   "
        f"<span style='color:{case_colors['genitive']};font-weight:bold'>GEN</span>"
    )
    st.sidebar.markdown("### German Personal Pronouns by Case")
    st.sidebar.markdown(header, unsafe_allow_html=True)
    st.sidebar.markdown("-" * 80)

    for pron_type, forms in german_pronouns.items():
        row = (
            f"{pron_type:<24} "
            f"<span style='color:{case_colors['nominative']}'>{forms['nominative']}</span>   "
            f"<span style='color:{case_colors['accusative']}'>{forms['accusative']}</span>   "
            f"<span style='color:{case_colors['dative']}'>{forms['dative']}</span>   "
            f"<span style='color:{case_colors['genitive']}'>{forms['genitive']}</span>"
        )
        st.sidebar.markdown(row, unsafe_allow_html=True)

    # Load sentences
    df_sentences = pd.read_csv('german-english-sample.tsv', sep='\t', header=None, usecols=[1, 3], names=['german', 'english'])

    # Session state for tracking
    if "pd_sentence_idx" not in st.session_state:
        st.session_state.pd_sentence_idx = None
        st.session_state.pd_feedback = ""
    if "pd_known_sentences" not in st.session_state:
        st.session_state.pd_known_sentences = set()
    if "pd_unknown_sentences" not in st.session_state:
        st.session_state.pd_unknown_sentences = set()

    pronoun_types = list(german_pronouns.keys())
    cases = ["nominative", "accusative", "dative"]


    red_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Show me a pronoun sentence!"):
        pronoun_type = random.choice(pronoun_types)
        case = random.choice(cases)
        pronoun = german_pronouns[pronoun_type][case]
        st.markdown(
        f"<span style='color:{case_colors[case]}; font-size:1.5em; font-weight:bold'>{pronoun}</span>",
        unsafe_allow_html=True
        )
        matches = df_sentences[df_sentences['german'].str.contains(rf'\b{pronoun}\b', case=False, regex=True)]
        #matches = df_sentences[df_sentences['german'].apply(lambda s: re.search(rf'(^|\s){re.escape(pronoun)}(\s|$)', s, re.IGNORECASE))]
        if not matches.empty:
            st.session_state.pd_row = matches.sample(n=1).iloc[0]
            st.session_state.pd_pronoun = pronoun
            st.session_state.pd_case = case
            st.session_state.pd_type = pronoun_type
            st.session_state.pd_sentence_idx = True
            st.session_state.pd_feedback = ""
            st.session_state["pd_input"] = ""  
        else:
            st.warning("No sentence found with this pronoun. Try again.")

    if st.session_state.get("pd_sentence_idx"):
        row = st.session_state.pd_row
        pronoun = st.session_state.pd_pronoun
        case = st.session_state.pd_case
        pronoun_type = st.session_state.pd_type
        german_sentence = row['german']
        english_sentence = row['english']
        st.markdown(
            f"<div style='font-size:1.3em; font-weight:bold'>Pronoun type: {pronoun_type}, Case: <span style='color:{case_colors[case]}'>{case}</span></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-size:1.5em; font-weight:bold'>German pronoun: <span style='color:{case_colors[case]}'>{pronoun}</span></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-size:2em; font-weight:bold'>{german_sentence}</div>",
            unsafe_allow_html=True
        )


        user_input = st.text_input("Translate to English:", key="pd_input", on_change=lambda: None)
        if user_input:
            if user_input.strip().lower() == english_sentence.strip().lower() or english_sentence.strip().lower() in user_input.strip().lower():
                st.session_state.pd_feedback = "✅ Correct!"
                st.session_state.pd_known_sentences.add(german_sentence)
                st.session_state.pd_unknown_sentences.discard(german_sentence)
            else:
                st.session_state.pd_feedback = f"❌ Correct answer: {english_sentence}"
                st.session_state.pd_unknown_sentences.add(german_sentence)

        if st.session_state.pd_feedback:
            st.markdown(st.session_state.pd_feedback)
    
elif active_mode == 'Possessive, reflexive, relative and indefinite pronoun practice':
    german_pronouns = {
        "possessive": [
            {"pronoun": "mein",  "notes": "my"},
            {"pronoun": "dein",  "notes": "your (informal singular)"},
            {"pronoun": "sein",  "notes": "his / its"},
            {"pronoun": "ihr",   "notes": "her / their"},
            {"pronoun": "unser", "notes": "our"},
            {"pronoun": "euer",  "notes": "your (informal plural)"},
            {"pronoun": "Ihr",   "notes": "your (formal)"}
        ],
        "reflexive": [
            {"pronoun": "mich",  "notes": "myself (accusative)"},
            {"pronoun": "mir",   "notes": "myself (dative)"},
            {"pronoun": "dich",  "notes": "yourself (accusative)"},
            {"pronoun": "dir",   "notes": "yourself (dative)"},
            {"pronoun": "sich",  "notes": "himself, herself, itself, themselves, yourself (formal)"},
            {"pronoun": "uns",   "notes": "ourselves"},
            {"pronoun": "euch",  "notes": "yourselves"}
        ],
        "relative": [
            {"pronoun": "der",    "notes": "masculine nominative singular"},
            {"pronoun": "die",    "notes": "feminine nominative singular & plural"},
            {"pronoun": "das",    "notes": "neuter nominative singular"},
            {"pronoun": "welcher","notes": "which (varies by gender/number)"},
            {"pronoun": "wer",    "notes": "who (used in some relative clauses)"}
        ],
        "indefinite": [
            {"pronoun": "man",       "notes": "one / people (general)"},
            {"pronoun": "jemand",    "notes": "someone"},
            {"pronoun": "niemand",   "notes": "no one / nobody"},
            {"pronoun": "etwas",     "notes": "something"},
            {"pronoun": "nichts",    "notes": "nothing"},
            {"pronoun": "alle",      "notes": "all / everyone"},
            {"pronoun": "einige",    "notes": "some"},
            {"pronoun": "mehrere",   "notes": "several"},
            {"pronoun": "jeder",     "notes": "each / every"},
            {"pronoun": "irgendein", "notes": "any / some"}
        ]
    }

    case_colors = {
        "possessive": "blue",
        "reflexive": "red",
        "relative": "green",
        "indefinite": "orange"
    }

    # Table header
    col_width_type = 16
    col_width_pronoun = 14
    header = (
        f"{'Type':<{col_width_type}}"
        f"<span style='color:{case_colors['possessive']};font-weight:bold'>POSS</span>{' ' * (col_width_pronoun-4)}"
        f"<span style='color:{case_colors['reflexive']};font-weight:bold'>REFLEX</span>{' ' * (col_width_pronoun-6)}"
        f"<span style='color:{case_colors['relative']};font-weight:bold'>REL</span>{' ' * (col_width_pronoun-3)}"
        f"<span style='color:{case_colors['indefinite']};font-weight:bold'>INDEF</span>"
    )
    st.sidebar.markdown("### Types of German Pronouns")
    st.sidebar.markdown(header, unsafe_allow_html=True)
    st.sidebar.markdown("-" * (col_width_type + 4 * col_width_pronoun))

    # Find max number of pronouns in any type
    max_len = max(len(german_pronouns[t]) for t in ["possessive", "reflexive", "relative", "indefinite"])

    for i in range(max_len):
        row = f"{'':<{col_width_type}}"
        for pron_type in ["possessive", "reflexive", "relative", "indefinite"]:
            pron_list = german_pronouns[pron_type]
            if i < len(pron_list):
                pronoun = f"<span style='color:{case_colors[pron_type]}'>{pron_list[i]['pronoun']}</span>"
            else:
                pronoun = ""
            row += f"{pronoun:<{col_width_pronoun}}"
        st.sidebar.markdown(row, unsafe_allow_html=True)

    # Load sentences
    df_sentences = pd.read_csv('german-english-sample.tsv', sep='\t', header=None, usecols=[1, 3], names=['german', 'english'])

    # Session state for tracking
    if "pr_sentence_idx" not in st.session_state:
        st.session_state.pr_sentence_idx = None
        st.session_state.pr_feedback = ""
    if "pr_known_sentences" not in st.session_state:
        st.session_state.pr_known_sentences = set()
    if "pr_unknown_sentences" not in st.session_state:
        st.session_state.pr_unknown_sentences = set()

    pronoun_types = list(german_pronouns.keys())

    red_button = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Show me a sentence with some pronoun!"):
        pronoun_type = random.choice(pronoun_types)
        pronoun_entry = random.choice(german_pronouns[pronoun_type])
        pronoun = pronoun_entry["pronoun"]
        st.markdown(
            f"<span style='color:{case_colors[pronoun_type]}; font-size:1.5em; font-weight:bold'>{pronoun}</span>",
            unsafe_allow_html=True
        )
        matches = df_sentences[df_sentences['german'].str.contains(rf'\b{pronoun}\b', case=False, regex=True)]
        #matches = df_sentences[df_sentences['german'].apply(lambda s: re.search(rf'(^|\s){re.escape(pronoun)}(\s|$)', s, re.IGNORECASE))]
        if not matches.empty:
            st.session_state.pr_row = matches.sample(n=1).iloc[0]
            st.session_state.pr_pronoun = pronoun
            st.session_state.pr_type = pronoun_type
            st.session_state.pr_sentence_idx = True
            st.session_state.pr_feedback = ""
            st.session_state["pr_input"] = ""
        else:
            st.warning("No sentence found with this pronoun. Try again.")

    if st.session_state.get("pr_sentence_idx"):
        row = st.session_state.pr_row
        pronoun = st.session_state.pr_pronoun
        pronoun_type = st.session_state.pr_type
        german_sentence = row['german']
        english_sentence = row['english']
        st.markdown(
        f"<div style='font-size:1.3em; font-weight:bold'>Pronoun type: {pronoun_type.capitalize()}</div>",
        unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-size:1.5em; font-weight:bold'>German pronoun: <span style='color:{case_colors[pronoun_type]}'>{pronoun}</span></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div style='font-size:2em; font-weight:bold'>{german_sentence}</div>",
            unsafe_allow_html=True
        )

        user_input = st.text_input("Translate to English:", key="pr_input", on_change=lambda: None)
        if user_input:
            if user_input.strip().lower() == english_sentence.strip().lower() or english_sentence.strip().lower() in user_input.strip().lower():
                st.session_state.pr_feedback = "✅ Correct!"
                st.session_state.pr_known_sentences.add(german_sentence)
                st.session_state.pr_unknown_sentences.discard(german_sentence)
            else:
                st.session_state.pr_feedback = f"❌ Correct answer: {english_sentence}"
                st.session_state.pr_unknown_sentences.add(german_sentence)
        
        if st.session_state.pr_feedback:
            st.markdown(st.session_state.pr_feedback)

