# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 20:18:42 2015

@author: Alex
"""

import requests
import csv
import json
import pickle
import pandas as pd
#import time
from bs4 import BeautifulSoup

#number of critics to download from BFI database
num_critics = 1206 

#loads in a dictionary of title replacements to allow for searching movie titles in OMDBAPI
replace = {"The Winter's Bone":"Winter's Bone",
           "81/2":"8 1/2",
           "Closely Observed Trains":"Closely Watched Trains",
           "The Bicycle Thieves":"Bicycle Thieves",
           "Minamata: The Victims and their World" : "Minamata",
           "Red Peony Gambler: Oryu's Return":"Hibotan bakuto: oryu sanjo",
           "Summer In Narita":"Nihon Kaiho sensen: Sanrizuka no natsu",
           "Tatooed Life":"Tattooed Life",
           "Shadows of Our Forgotten Ancestors":"Shadows of Forgotten Ancestors",
           "The Werckmeister Harmonies":"Werckmeister Harmonies",
           "La Maman et la putain":"The Mother and the Whore",
           "A One and a Two":"Yi yi",
           "Ugetsu Monogatari":"Ugetsu",
           "Did Wolff von Amerongen Commit Bankruptcy Offenses?":"Wolff Von Amerongen: Did He Commit Bancruptcy Offences?",
           "Enfant Secret, L'":"L'Enfant Secret",
           "Aguirre, Wrath of God":"Aguirre, the Wrath of God",
           "Sansho Dayu":"Sansho the Bailiff",
           "Yeelen":"Brightness",
           "The Godfather: Part I":"The Godfather",
           "The Bohemian Life":"La Vie de Boheme",
           "Even the Dwarves Started Small":"Even Dwarfs Started Small",
           "olvidados, Los":"Los olvidados",
           "Les Diaboliques":"Diaboliques",
           "The Wedding Suit":"Lebassi Baraye Arossi",
           "The Story of the Late Chrysanthemums":"Zangiku monogatari",
           "And There Was Light":"And Then There Was Light",
           "Birth of the Nation":"Die Geburt der Nation",
           "Scenes from a City Life (Dushi Fengguang)":"Dushi Fengguang",
           "Straits of Love and Hate (Aien Kyo)":"Straits of Love and Hate",
           "Jules et Jim":"Jules and Jim",
           "Blood of the Beasts":"Le sang des betes",
           "Opera Jawa":"Requiem from Java",
           "Terminator II: Judgement Day":"Terminator 2: Judgment Day",
           "Les enfants du paradis":"Children of Paradise",
           "The Most Important Thing: Love":"That Most Important Thing: Love",
           "Three Colours: Red":"Three Colors: Red",
           "McCabe and Mrs Miller":"McCabe & Mrs. Miller",
           "Spring, Summer, Fall, Winter and Spring\xe2\x80\xa6":"Spring, Summer, Fall, Winter... and Spring",
           "The Taste of Cherry":"Taste of Cherry",
           "A Time to Live and a Time To Die":"A Time to Live, a Time to Die",
           "Where is My Friend's House?":"Where is the Friend's Home?",
           "Walden: Diaries, Notes and Sketches":"Walden",
           "Man of the Story":"Kathapurushan",
           "Macunaima/Jungle Freaks":"Macunaima",
           "The Choses de la Vie, Les/Little Things in Life":"The Things of Life",
           "Three Colours: Blue":"Three Colors: Blue",
           "Masque of Red Death":"The Masque of the Red Death",
           "One-Armed Boxer II":"Master of the Flying Guillotine",
           "The Phantom of the Paradise":"Phantom of the Paradise",
           "The Saga of Anatahan":"Ana-ta-han",
           "Bed and Sofa":"Tretya meshchanskaya",
           "A Tale of Tales":"Tale of Tales",
           "Noi Vivi":"We the Living",
           "Our Nazi":"Notre nazi",
           "Notre Music":"Notre musique",
           "Le Feu follet":"The Fire Within",
           "Om Dar-ba-Dar":"Om Dar-B-Dar",
           "The Lord of the Rings: Fellowship of the Ring, The (Theatrical version)":"The Lord of the Rings: The Fellowship of the Ring",
           "The House of Trubnaia Square":"Dom na Trubnoy",
           "La sortie des usines Lumi\xc3\xa8re":"Employees Leaving the Lumiere Factory",
           "The Night of the Living Dead":"Night of the Living Dead",
           "Parents' Heart":"Fu mu xin",
           "My Neighbour Totoro":"My Neighbor Totoro",
           "Europa 51":"Europe '51",
           "Soldier's Prayer, A (Human Condition Trilogy Part 3":"The Human Condition III: A Soldier's Prayer",
           "Dekalog":"The Decalogue",
           "The Seasons of the Year":"Four Seasons",
           "Cold Nights":"Han ye",
           "T G Psychic Rally in Heaven":"T.G.: Psychic Rally in Heaven",
           "Journey on the Hour Hand":"Akrebin yolculugu",
           "Les Vacances de M. Hulot":"Mr. Hulot's Holiday",
           "The Battle of Chile":"La batalla de Chile: La lucha de un pueblo sin armas - Primera parte: La insurrecion de la burguesia",
           "The Green Ray":"Summer",
           "The Rise to Power of Louis XIV":"The Rise of Louis XIV",
           "Visions of Meditation":"Visions in Meditation #1",
           "Age d'Or, L'":"L'Age d'Or",
           "Shirley Thompson vs The Aliens":"Shirley Thompson vs The Aliens",
           "segno di Venere, Il":"Il segno di Venere",
           "Is Not a Film, This":"This Is Not a Film",
           "A Chronicle of a Disappearance":"Chronicle of a Disappearance",
           "Rome Rather Than You":"Roma wa la n'touma",
           "Saint Tukaram":"Sant Tukaram",
           "Assomoir, L'":"Drink",
           "The Tiger of Eschnapur/The Indian Tomb":"Tiger of Bengal",
           "The Draughtman's Contract":"The Draughtsman's Contract",
           "A Severe Young Man":"Strogiy yunosha",
           "Firemans Ball":"The Firemen's Ball",
           "Winnipeg, My":"My Winnipeg",
           "The Holly Girl":"The Holy Girl",
           "loge de l'amour/In Praise of Love":"In Praise of Love",
           "Lousiana Story":"Louisiana Story",
           "Viva l'Amour":"Vive L'Amour",
           "Rapsodia satanica":"Satan's Rhapsody",
           "William Shakespeare's Romeo+Juliet":"Romeo + Juliet",
           "Rabo\xc4\x8dij poselok":"Rabochiy posyolok",
           "Three Years Without God":"Tatlong taong walang Diyos",
           "The Truth About Bebe Donde":"The Truth of Our Marriage",
           "accuse, J'":"J'accuse!",
           "The Melomaniac":"The Music Lover",
           "Days of the Eclipse":"Days of Eclipse",
           "London 66'-67'- Pink Floyd":"Pink Floyd London '66-'67",
           "Nothing but the Hours":"Nothing But Time",
           "A Grin Without a Cat":"Grin Without a Cat",
           "I Know Where I\'m Going!":"I Know Where I'm Going!",
           "Uzak/Distant":"Distant",
           "Historias Extraordinarias":"Extraordinary Stories",
           "The Water Carrier has Died":"Al-saqqa mat",
           "Cries and Whispers":"Cries & Whispers",
           "Enfance nue, L'":"Naked Childhood",
           "Nelly et Monsieur Arnaud":"Nelly & Monsieur Arnaud",
           "Woman of the Dunes":"Woman in the Dunes",
           "I was Nineteen":"Ich war neunzehn",
           "Les demoiselles de Rochefort":"The Young Girls of Rochefort",
           "Slow Summer":"Langsamer Sommer",
           "A Corner in the Wheat":"A Corner in Wheat",
           "Videograms of a Revolution":"Videogramme einer Revolution",
           "Manila by Night":"City After Dark",
           "Hours for Jerome I & II":"Hours for Jerome",
           "Prenom: Carmen":"First Name: Carmen",
           "Aleksandr Nevski":"Alexander Nevsky",
           "Made in Germany and USA":"Made in Germany und USA",
           "A Blonde in Love":"The Loves of a Blonde",
           "Cycling Chronicles: Landscape the Boy Saw":"Cycling Chronicles: Landscapes the Boy Saw",
           "La nuit du carrefour":"Night at the Crossroads",
           "Spiritual Voices":"Dukhovnye golosa. Iz dnevnikov voyny. Povestvovanie v pyati chastyakh",
           "Pirates of the Caribbean III: At World's End":"Pirates of the Caribbean: At World's End",
           "Dodeskaden":"Dodes'ka-den",
           "Les Acrobatic Sisters Dainef, The/six soeurs Dainef":"Acrobatic Sisters Dainef",
           "Pasazerka":"Passenger",
           "Images of the World and the Inscription of the War":"Bilder der Welt und Inschrift des Krieges",
           "aveugle de Jerusalem, L'":"The Blind Man of Jerusalem",
           "The Big Swallow":"A Photographic Contortion",
           "Obscure Object of Desire, That":"That Obscure Object of Desire",
           "Fire in Castile (Tactil Vision of the Wasteland of Fear)":"Fire in Castilla (Tactilvision from the Moor of the Fright)",
           "Hawks and Sparrows":"The Hawks and the Sparrows",
           "Yawar Mallku":"Blood of the Condor",
           "Without Anesthesia":"Rough Treatment",
           "Boon bin yen":"Ah Ying",
           "In a Year of 13 Moons":"In a Year with 13 Moons",
           "La Signora di Tutti":"Everybody's Woman",
           "Goodbye, Dragon Inn":"Good Bye, Dragon Inn",
           "The Sound of the Mountain":"Sound of the Mountain",
           "Iodo":"Io Island",
           "Amour existe, L'":" L'Amour existe",
           "Eros Plus Massacre":"Eros + Massacre",
           "Daratt":"Dry Season",
           "Beauty No 2":"Beauty #2",
           "Monty Python's Life of Brian":"Life of Brian",
           "The Battle of Chile: Part 2":"La batalla de Chile: La lucha de un pueblo sin armas - Segunda parte: El golpe de estado",
           "Bande \xc3\xa0 part":"Band of Outsiders",
           "The Treasure of Sierra Madre":"The Treasure of the Sierra Madre",
           "Three Songs About Lenin":"Tri pesni o Lenine",
           "Oedipux Rex":"Oedipus Rex",
           "The Thousand Eyes of Dr Mabuse":"The 1,000 Eyes of Dr. Mabuse",
           "The Three Crowns of the Sailor":"Three Crowns of the Sailor",
           "Super Dyke Meets Madam X":"Superdyke Meets Madame X",
           "Othon":"Eyes Do Not Want to Close at All Times, or, Perhaps One Day Rome Will Allow Herself to Choose in Her Turn",
           "Advise and Consent":"Advise & Consent",
           "Tales of the Taira Clan":"Taira Clan Saga",
           "Le Testament Du Dr. Cordelier":"Experiment in Evil",
           "Fertile Memory":"Al Dhakira al Khasba",
           "Chant d'amour, Un":"A Song of Love",
           "Lift to the Scaffold":"Elevator to the Gallows",
           "visite au Louvre, Une":"Une visite au Louvre",
           "The German Sisters":"Marianne and Juliane",
           "Falbalas/Paris Frills":"Paris Frills",
           "Dead or Alive 2: Birds":"Dead or Alive 2: Tobosha",
           "Hotel des Ameriques":"Hotel America",
           "Red Viburnum":"The Red Snowball Tree",
           "Grido, Il":"Il Grido",
           "The Death of Maria Malibran":"Der Tod der Maria Malibran",
           "The Colour of Paradise":"The Color of Paradise",
           "Goodbye Lenin!":"Good Bye Lenin!",
           "Beshkempir":"The Adopted Son",
           "Land of Fathers":"Zemlya ottsov",
           "Trasferimento di modulazione":"Transfer of Modulation",
           "La verifica incerta":"Verifica incerta - Disperse Exclamatory Phase",
           "La ville des pirates":"City of Pirates",
           "The Way Things Go":"Der Lauf der Dinge",
           "79 Springtimes":"79 primaveras",
           "Entuziazm: Simfoniya Donbassa":"Enthusiasm",
           "femme est une femme, Une":"A Woman Is a Woman",
           "Cronaca familiare":"Family Portrait",
           "The Age of Cosimo de Medici":"The Age of the Medici",
           "Echo of the Jackboot":"Triumph Over Violence",
           "Aura, El":"The Aura",
           "Milagro de P. Tinto, El":"The Miracle of P. Tinto",
           "Artists under the Big Top: Perplexed":"The Artist in the Circus Dome: Clueless",
           "How to be Loved":"Jak byc kochana",
           "The Great Rock and Roll Swindle":"The Great Rock 'n' Roll Swindle",
           "Palomita Blanca":"Little White Dove",
           "Reassemblange":"Reassemblage: From the Firelight to the Screen",
           "Rubios, Los":"The Blonds",
           "La dr\xc3\xb4lesse":"The Hussy",
           "All of my Life":"All My Life",
           "The Ghost and Mrs Muir":"The Ghost and Mrs. Muir",
           "Femme Douce, Une":"A Gentle Woman",
           "The Left-Handed Woman":"Die linkshandige Frau",
           "Night of the Bride":"The Nun's Night",
           "The Lady With The Little Dog":"The Lady with the Dog",
           "Seopyeonje":"Sopyonje",
           "Arguments and a Story or Reason, Debate and a Tale":"Reason, Debate and a Story",
           "The Union of the Great Cause":"S.V.D. - Soyuz velikogo dela",
           "The Mad Fox":"Love, Thy Name Be Sorrow",
           "La naissance de l\xe2\x80\x99amour":"The Birth of Love",
           "His Wife is a Hen":"Yego zhena kuritsa",
           "Chunhyangdyun":"Chunhyang",
           "Of Freaks and Men":"Pro urodov i lyudey",
           "Man's Favourite Sport?":"Man's Favorite Sport?",
           "The Pale Rider":"Pale Rider",
           "Les statues meurent aussi\xe2\x80\xa6":"Statues also Die",
           "Black Rose is an Emblem of Sorrow, Red Rose is an Emblem of Love":"Chyornaya roza - emblema pechali, krasnaya roza - emblema lyubvi",
           "Smell of Camphor, Fragrance of Jasmine":"Booye kafoor, atre yas",
           "Rich and Strange":"East of Shanghai",
           "Drunken Master II":"The Legend of Drunken Master",
           "Death of the Land of Encantos":"Death in the Land of Encantos",
           "Lancelot Du Lac":"Lancelot of the Lake",
           "The 3 Rooms of Melancholia":"Melancholian 3 huonetta",
           "Amor Natural, O":"O Amor Natural",
           "A Loss Is To Be Expected":"Loss Is to Be Expected",
           "El grito del sur. Casas Viejas":"El grito del sur. Casas Viejas",
           "Berlin, Symphony of a City":"Berlin: Symphony of a Great City",
           "Sanrizuka: Heta Village":"Sanrizuka: Heta buraku",
           "Ivan the Terrible II":"Ivan the Terrible, Part II",
           "La Mujer del Puerto":"The Woman of the Port",
           "humanit\xc3\xa9, L'":"Humanité",
           "Gori, gori, moya zvezda":"Shine, Shine, My Star",
           "Dragon Gate Inn":"Dragon Inn",
           "Martha, Macy, May, Marlene":"Martha Marcy May Marlene",
           "Nine and a Half Weeks":"Nine 1/2 Weeks",
           "Nanami: Inferno of First Love":"Nanami: The Inferno of First Love",
           "Take Care of Your Scarf, Tatjana":"Take Care of Your Scarf, Tatiana",
           "Unfinished Piece for the Player Piano":"An Unfinished Piece for Mechanical Piano",
           "Le Quatro Volte":"Le Quattro Volte",
           "I'm Alright Jack":"I'm All Right Jack",
           "Shop on the Main Street":"The Shop on Main Street",
           "Workers Leaving the Factory Gate":"Employees Leaving the Lumiere Factory",
           "Little Otik":"Greedy Guts",
           "The Inmortal Story":"The Immortal Story",
           "The Assasination of Jesse James by the Coward Robert Ford":"",
           "A Japanese Village":"The Assassination of Jesse James by the Coward Robert Ford",
           "Recorda\xc3\xa7\xc3\xb5es da Casa Amarela":"Recollections of the Yellow House",
           "Les Rendez-vous du diable":"The Devil's Blast",
           "Moderato catabile":"Seven Days... Seven Nights",
           "Trait\xc3\xa9 de bave et d'\xc3\xa9ternit\xc3\xa9":"Venom and Eternity",
           "Scattered Clouds a.k.a. Two In The Shadow":"Two in the Shadow",
           "Boat Leaving the Port":"Barque sortant du port",
           "Nicht l\xc3\xb6schbares Feuer":"The Inextinguishable Fire",
           "Who's Afraid of Virginia Wolf?":"Who's Afraid of Virginia Woolf?",
           "West Indies, ou les n\xc3\xa8gres marrons de la libert\xc3\xa9":"West Indies",
           "Dreams of Hind and Camilia":"Ahlam Hind we Kamilia",
           "Princess Yang Kwei Fei":"Yokihi",
           "The Man on the Roof":"Man on the Roof",
           "A Heart in Winter":"Un Coeur en Hiver",
           "A Simple Even":"A Simple Event",
           "Banditi a Orgosolo":"Bandits of Orgosolo", 
           "Rio 40 Graus":"Rio 100 Degrees F.",
           "Cien ni\xc3\xb1os esperando un tren":"One Hundred Children Waiting for a Train",
           "Etre et avoir":"To Be and to Have",
           "Animals Are Beautiful People":"Beautiful People",
           "The Argentinian Lesson":"Argentynska lekcja",
           "Mein Liebster Feind":"My Best Fiend",
           "Sex Pistols -The Filth and The Fury":"The Filth and the Fury",
           "Siddheshwari":"Siddeshwari",
           "ruption volcanique \xc3\xa0 la Martinique":"The Terrible Eruption of Mount Pelee and Destruction of St. Pierre, Martinique",
           "Freeze, Die Come Alive":"Freeze Die Come to Life",
           "Bidone, Il":"Il Bidone",
           "Vendredi Soir":"Friday Night",
           "Edouard et Caroline":"Edward and Caroline",
           "Jingi no hakaba":"Graveyard of Honor",
           "Turks Fruit":"Turkish Delight",
           "A Real Young Lady":"A Real Young Girl",
           "The Emperor of the Mughals":"Mughal-E-Azam",
           "Funeral Fest, Burial Lunch":"Sedmina - Pozdravi Marijo",
           "The Gay Divorce":"The Gay Divorcee",
           "Bahia of All The Saints":"Bahia de Todos os Santos",
           "Star Wars":"Star Wars: Episode IV - A New Hope",
           "Rome Open City" : "Rome, Open City",
           "Blow Up": "Blow-Up",
           "Diaboliques":"Diabolique",
           "Anthem":"The Anthem",
           "Dushi Fengguang":"Dushi fengguang",
           "Fountainhead":"The Fountainhead",
           "Diary":"Yoman",
           "The Empire Strikes Back":"Star Wars: Episode V - The Empire Strikes Back",
           "Nausicaa of the Valley of the Wind":"Nausicaa of the Valley of the Wind",
           "Le mepris":"Contempt",
           "Madame de...":"The Earrings of Madame de...",
           "Histoire(s) du cinema":"Histoire(s) du cinema: Seul le cinema",
           "La Belle et la Bete":"Beauty and the Beast",
           "Amour fou, L'":"L'Amour fou",
           "3.10 to Yuma":"3:10 to Yuma",
           "Muhammad Ali: The Greatest":"The Greatest",
           "Hapax Legomena":"Hapax Legomena I: Nostalgia",
           "Gion Festival":"Gion matsuri",
           "I Am (Jestem)":"I Am", 
           "The Inmigrant":"The Immigrant",
           "The Night of Counting the Years":"The Mummy",
           "Capitaine Fracasse, Le":"Captain Fracasse",
           "Nuit et jour":"Night and Day",
           "Gamlet":"Kozintsevs Hamlet",
           "Hamlet":"Oliviers Hamlet",
           "Episode 3 – ‘Enjoy Poverty’":"Episode 3: 'Enjoy Poverty'",
           "Tilai":"The Law"}     
                    
#downloads each voter's webpage
def download_directors():   
    header = ["fName","lName","country","poll","selectionName","selectionYear","selectionDirector"]
    with open('test.csv', 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(header)    
        
    
    for n in range(1,num_critics):
        print 'http://explore.bfi.org.uk/sightandsoundpolls/2012/voter/%d' %n    
        r=requests.get('http://explore.bfi.org.uk/sightandsoundpolls/2012/voter/%d' %n)
        soup = BeautifulSoup(r.content)
        for info in soup.findAll("div", {"class": "sas-voter-details-header"}):
            name = info.h1.contents
            details = info.div.contents       
            name = name[0].split(' ')        
            firstname = name[0]
            lastname = name[-1]
            try:            
                country = details[2].strip()      
            except:
                country = "ERROR"
                
            critics = "critics"
            directors = "directors"        
            try:            
                if critics in details[4]: 
                    poll = "critics"
                elif directors in details[4]:
                    poll = "directors"
                else:
                    poll = "None"
            except:
                poll = "ERROR"
        for info in soup.findAll("div", {"class": "sas-voter-details-votes"}):
            for entry in info.findAll("tr"):
                row = [firstname,lastname,country,poll]            
                for d in entry.findAll("td"):
                    row.append(d.get_text())
                with open('test.csv', 'ab') as fp:
                    a = csv.writer(fp, delimiter=',')
                    a.writerow([s.encode('utf8') if type(s) is unicode else s for s in row])   

#Removes final word from back and moves to front
#Example "Winter's Bone, The" -> "The Winter's Bone"
#Assumes a space at start of removed final word 
def move_to_front(title, removal_string):
    if title.endswith(removal_string):
        removal_length = -1* len(removal_string)
        #print title        
        #print removal_string
        #print removal_length        
        title = title[:removal_length]
        #print title        
        removal_string = removal_string.lstrip(", ")        
        title = removal_string + " " + title
        #print title
        #print "DONE"                
        return title
    else:
        return title

#audits and corrects titles with issues
def audit(title, replace):      
    title = move_to_front(title, ", The")
    title = move_to_front(title, ", An")
    title = move_to_front(title, ", A")
    title = move_to_front(title, ", La")
    title = move_to_front(title, ", Les")
    title = move_to_front(title, ", Le")
    title = move_to_front(title, ", El")
    title = move_to_front(title, ", Un")
    if title in replace:
        title = replace[title]
    return title
        
#makes a simple list from a csv column
def listify_column(fname, col):
    listified = []
    with open(fname,'r') as f:
        reader=csv.reader(f)
        for row in reader:
            title = audit(row[col], replace)
            if title not in listified:
                listified.append(title)
            else:
                continue
        return listified

#Creates movie dictionary with relevant data for each movie
def create_movie_dictionary(info):
    temp_lib={}    
    try:    
        temp_lib["runtime"]=int(info["Runtime"].rstrip(" min"))   
    except:
        temp_lib["runtime"]="UNKNOWN"
        #print info["Title"], "Runtime error!"
    try:        
        temp_lib["rating"]=info["Rated"]
    except:
        temp_lib["rating"]="UNKNOWN"
        #print info["Title"], "Rating error!"
    try:
        temp_lib["genre"]=info["Genre"].split(", ")
    except:
        temp_lib["genre"]="UNKNOWN"
        #print info["Title"], "Genre error!"
    try:
        temp_lib["language"] = info["Language"].split(", ")
    except:
        temp_lib["language"]="UNKNOWN"
        #print info["Title"], "Language error!"
    try:
        temp_lib["country"] = info["Country"].split(", ")
    except:
        temp_lib["country"]="UNKNOWN"
        #print info["Title"], "Country error!"    
    return temp_lib

def download_movie_info(movie_list):
    movie_lib={}
    error=[]    
    for title in movie_list:    
        #print 'http://www.omdbapi.com/?t=%s&y=&plot=short&r=json' %title        
        exceptions = ["Nihongdeng xia de shaobing","Gruningers Fall","Godzilla","Melancolia","Peggy and Fred in Hell","Downfall Reworked for YouTube","Long Film for Ambient Light","The Sky Socialist","NYC Street Scenes and Noises","Fox News Outtakes 4-399/400 NYC Street Scenes and Noises","Fela Kuti","Bresson's entire oeuvre","Review 36th Year No.5","My Hand Outstretched to the Winged Distance and Sightless Measure","Heimat","Oliviers Hamlet","Kozintsevs Hamlet", "Hapax Legomena","From the Notebook ofâ€¦","Histoire(s) du cinema","Living on the Edge","81/2","Z","Nuit et jour","The Inmigrant","I Am (Jestem)","M","Amour fou, L'","Muhammad Ali: The Greatest","3.10 to Yuma","Gion Festival","La Belle et la Bete","Tilai","Capitaine Fracasse, Le","The Night of Counting the Years"]        
        if title in exceptions:
            continue
        else:
                    
            try:         
                r = requests.get('http://www.omdbapi.com/?t=%s&y=&plot=short&r=json' %title)
                info = r.json()
                try: #adds a library for every movie                    
                    temp_lib=create_movie_dictionary(info)
                    movie_lib[title]=temp_lib
                except: #in case of error appends title to an error list 
                    error.append(title)
                    print "Search Error! ", title
            except:
                error.append(title)
                print "Search Error! ", title
    #secion devoted to downloading data that requires special handling
    try:
        movie_lib["M"]=download_exceptions('http://www.omdbapi.com/?i=tt0022100&plot=short&r=json')
    except:
        print "M - ERROR"        
        error.append("M")
    try:
        movie_lib["L'Amour fou"]=download_exceptions("http://www.omdbapi.com/?t=L'Amour+fou&y=1969&plot=short&r=json")
    except:
        print "L'Amour fou - ERROR"        
        error.append("L'Amour fou")        
    try:
        movie_lib["The Greatest"]=download_exceptions("http://www.omdbapi.com/?i=tt0076111&plot=short&r=json")
    except:
        print "The Greatest - ERROR"        
        error.append("The Greatest")
    try:
        movie_lib["3:10 to Yuma"]=download_exceptions("http://www.omdbapi.com/?i=tt0050086&plot=short&r=json")
    except:
        print "3:10 to Yuma - ERROR"        
        error.append("3:10 to Yuma")
    try:
        movie_lib["Gion matsuri"]=download_exceptions("http://www.omdbapi.com/?i=tt0024060&plot=short&r=json")
    except:
        print "Gion matsuri - ERROR"        
        error.append("Gion matsuri")
    try:
        movie_lib["Beauty and the Beast"]=download_exceptions("http://www.omdbapi.com/?i=tt0038348&plot=short&r=json")
    except:
        print "Beauty and the Beast - ERROR"        
        error.append("Beauty and the Beast") 
    try:
        movie_lib["The Law"]=download_exceptions("http://www.omdbapi.com/?i=tt0100784&plot=short&r=json")
    except:
        print "The Law - ERROR"        
        error.append("The Law") 
    try:
        movie_lib["Captain Fracasse"]=download_exceptions("http://www.omdbapi.com/?i=tt0034575&plot=short&r=json")
    except:
        print "Captain Fracasse - ERROR"        
        error.append("Captain Fracasse")
    try:
        movie_lib["The Mummy"]=download_exceptions("http://www.omdbapi.com/?i=tt0064703&plot=short&r=json")
    except:
        print "The Mummy - ERROR"        
        error.append("The Mummy") 
    try:
        movie_lib["I Am"]=download_exceptions("http://www.omdbapi.com/?i=tt0478175&plot=short&r=json")
    except:
        print "I Am - ERROR"
        error.append("I Am") 
    try:
        movie_lib["The Immigrant"]=download_exceptions("http://www.omdbapi.com/?i=tt0008133&plot=short&r=json")
    except:
        print "The Immigrant - ERROR"        
        error.append("The Immigrant")
    try:
        movie_lib["Night and Day"]=download_exceptions("http://www.omdbapi.com/?i=tt0102566&plot=short&r=json")
    except:
        print "Night and Day - ERROR"        
        error.append("Night and Day")
    try:
        movie_lib["Z"]=download_exceptions("http://www.omdbapi.com/?i=tt0065234&plot=short&r=json")
    except:
        print "Z - ERROR"        
        error.append("Z")
    try:
        movie_lib["81/2"]=download_exceptions("http://www.omdbapi.com/?i=tt0056801&plot=short&r=json")
    except:
        print "81/2 - ERROR"        
        error.append("81/2")
    try:
        movie_lib["Living on the Edge"]=download_exceptions("http://www.omdbapi.com/?i=tt0403230&plot=short&r=json")
    except:
        print "Living on the Edge - ERROR"        
        error.append("Living on the Edge")
    try:
        movie_lib["Kozintsevs Hamlet"]=download_exceptions("http://www.omdbapi.com/?i=tt0058126&plot=short&r=json")
    except:
        print "Kozintsevs Hamlet - ERROR"        
        error.append("Kozintsevs Hamlet")
    try:
        movie_lib["Oliviers Hamlet"]=download_exceptions("http://www.omdbapi.com/?i=tt0058126&plot=short&r=json")
    except:
        print "Oliviers Hamlet - ERROR"        
        error.append("Oliviers Hamlet")
    try:
        movie_lib["Heimat"]=download_exceptions("http://www.omdbapi.com/?i=tt0087400&plot=short&r=json")
    except:
        print "Heimat - ERROR"        
        error.append("Heimat")
    try:
        movie_lib["Melancolia"]=download_exceptions("http://www.omdbapi.com/?i=tt1269566&plot=short&r=json")
    except:
        print "Melancolia - ERROR"        
        error.append("Melancolia")
    try:
        movie_lib["Godzilla"]=download_exceptions("http://www.omdbapi.com/?i=tt0047034&plot=short&r=json")
    except:
        print "Godzilla - ERROR"        
        error.append("Godzilla")
    try:
        movie_lib["Gruningers Fall"]=download_exceptions("http://www.omdbapi.com/?i=tt0132198&plot=short&r=json")
    except:
        print "Gruningers Fall - ERROR"        
        error.append("Gruningers Fall")
    
    
    return error, movie_lib

def download_exceptions(request):
    r = requests.get(request)
    info = r.json()
    temp_lib=create_movie_dictionary(info)
    return temp_lib    

def concatenate_list(list_name):
    #concatenates list if greater than 1 and less than number
    #returns string "Multiple" if greater than number
    #returns only item in list as string if equal to 1
    output = ",".join(list_name)
    return output

def create_data(critic_file, title_col, movie_file, replace): 
#critic_file is data downloaded from BFI, movie file is data downloaded with OMDBAPI, title_col is the column in critic_file that movie titles are kept, replace is replacement dictionary 
    exceptions = ["Nihongdeng xia de shaobing","Peggy and Fred in Hell","Downfall Reworked for YouTube","Long Film for Ambient Light","The Sky Socialist","NYC Street Scenes and Noises","Fox News Outtakes 4-399/400 NYC Street Scenes and Noises","Fela Kuti","Bresson's entire oeuvre","Review 36th Year No.5","My Hand Outstretched to the Winged Distance and Sightless Measure"]            
    header = ["fName","lName","country","poll","selectionName","selectionYear","selectionDirector","newName", "rating", "runtime", "genre", "language", "country"]    
    with open('flat_output.csv', 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerow(header)        
    with open(critic_file,'r') as f:
        firstrow = True        
        reader=csv.reader(f)
        for row in reader:
            if firstrow is False:            
                title = row[title_col]
                new_title = audit(title, replace)            
                if new_title in exceptions:
                    continue
                else:
                    row.append(new_title)            
                    with open(movie_file, 'r') as m:
                        data=json.load(m)                      
                        try:                    
                            genre = data[new_title]["genre"]
                        except:
                            genre = "ERROR"
                            print new_title, "GENRE ERROR"
                        try:                        
                            rating = data[new_title]["rating"]
                        except:
                            rating = "ERROR"
                            print new_title, "RATING ERROR"
                        try:                        
                            runtime = data[new_title]["runtime"]
                        except:
                            runtime = "ERROR" 
                            print new_title, "RUNTIME ERROR"
                        try:                        
                            language = data[new_title]["language"]
                        except:
                            language = "ERROR"                        
                            print new_title, "LANGUAGE ERROR"
                        try:                        
                            country = data[new_title]["country"]
                        except:
                            country = "ERROR"
                            print new_title, "COUNTRY ERROR"
                    genre = concatenate_list(genre)
                    language = concatenate_list(language)
                    country = concatenate_list(country)                
                    row.extend((rating, runtime, genre, language, country))         
                    with open('flat_output.csv', 'ab') as ap:
                        b = csv.writer(ap, delimiter=',')        
                        b.writerow(row) 
            else:
                firstrow = False
    
        
def create_dummies(data):
    movies=pd.read_csv(data)     
    pd.concat([movies, movies['genre'].str.get_dummies(sep=','),movies['language'].str.get_dummies(sep=','),movies['country.1'].str.get_dummies(sep=',')], axis=1).to_csv('dummies.csv')    
    
        
def main():
    #download_directors()
    movies = listify_column('test.csv',4)
    #downloads movie info and places it into a json file and an error file    
    error, movie_lib = download_movie_info(movies)
    with open('moviedata.json', 'w') as outfile:
        json.dump(movie_lib, outfile)
    with open('unfound.txt', 'wb') as f:
        pickle.dump(error, f)
    #creates a final csv file that combines the moviedata and the critic data from BFI
    create_data("test.csv", 4, "moviedata.json", replace)
    create_dummies('flat_output.csv') 
    #error, movie_lib = test()
    #print error
    #print movie_lib
    
main()


            