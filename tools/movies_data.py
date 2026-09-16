# -*- coding: utf-8 -*-
"""
Master movie list for MovieFlix.

Each entry: (title, genre, description, rating, year, wiki_page)

`wiki_page` is only used by tools/build_dataset.py to download the official
poster image. It never reaches the running application.
"""

MOVIES = [
    ("Inception", "Sci-Fi, Thriller, Action",
     "A skilled thief who steals secrets from inside dreams is offered a chance at redemption if he can plant an idea in a target's subconscious mind.",
     8.8, 2010, "Inception"),

    ("Interstellar", "Sci-Fi, Drama, Adventure",
     "A team of explorers travels through a wormhole near Saturn in a desperate attempt to find a new home for a dying humanity.",
     8.7, 2014, "Interstellar (film)"),

    ("The Matrix", "Sci-Fi, Action",
     "A computer hacker learns that his reality is a simulation built by machines and joins a rebellion to free the human race.",
     8.7, 1999, "The Matrix"),

    ("The Dark Knight", "Action, Crime, Drama",
     "Batman faces the Joker, an anarchic criminal mastermind who pushes Gotham City and its protector to their moral breaking point.",
     9.0, 2008, "The Dark Knight"),

    ("The Avengers", "Action, Adventure, Sci-Fi",
     "Earth's mightiest heroes are recruited into a single team to stop an alien invasion led by the trickster god Loki.",
     8.0, 2012, "The Avengers (2012 film)"),

    ("Iron Man", "Action, Sci-Fi, Adventure",
     "A billionaire weapons inventor builds a powered armour suit to escape captivity and becomes a technological superhero.",
     7.9, 2008, "Iron Man (2008 film)"),

    ("Spider-Man", "Action, Adventure, Sci-Fi",
     "A shy high school student gains spider-like powers after a bite and learns that great power brings great responsibility.",
     7.4, 2002, "Spider-Man (2002 film)"),

    ("Titanic", "Romance, Drama",
     "A poor artist and a wealthy young woman fall in love aboard the doomed maiden voyage of the RMS Titanic.",
     7.9, 1997, "Titanic (1997 film)"),

    ("The Notebook", "Romance, Drama",
     "A poor young man and a rich girl fall deeply in love one summer, and their story is retold years later to an ageing woman.",
     7.8, 2004, "The Notebook"),

    ("Harry Potter and the Philosopher's Stone", "Fantasy, Adventure, Family",
     "An orphaned boy discovers he is a wizard and begins his first year at Hogwarts School of Witchcraft and Wizardry.",
     7.6, 2001, "Harry Potter and the Philosopher's Stone (film)"),

    ("Jurassic World", "Adventure, Sci-Fi, Action",
     "A fully functioning dinosaur theme park collapses into chaos when a genetically engineered hybrid predator escapes its enclosure.",
     6.9, 2015, "Jurassic World"),

    ("Pirates of the Caribbean: The Curse of the Black Pearl", "Adventure, Fantasy, Action",
     "A roguish pirate captain teams up with a blacksmith to rescue a governor's daughter from a crew of cursed undead sailors.",
     8.1, 2003, "Pirates of the Caribbean: The Curse of the Black Pearl"),

    ("The Conjuring", "Horror, Mystery, Thriller",
     "Paranormal investigators Ed and Lorraine Warren help a family terrorised by a dark presence in their secluded farmhouse.",
     7.5, 2013, "The Conjuring"),

    ("Annabelle", "Horror, Mystery, Thriller",
     "A young couple's vintage porcelain doll becomes the vessel for a malevolent supernatural entity that stalks their home.",
     5.4, 2014, "Annabelle (film)"),

    ("A Quiet Place", "Horror, Thriller, Sci-Fi",
     "A family must live in total silence to hide from blind alien creatures that hunt every sound they make.",
     7.5, 2018, "A Quiet Place (film)"),

    ("Joker", "Crime, Drama, Thriller",
     "A failed comedian in a decaying city spirals into madness and violence, becoming the criminal icon known as the Joker.",
     8.4, 2019, "Joker (2019 film)"),

    ("Forrest Gump", "Drama, Romance",
     "A kind-hearted man with a low IQ witnesses and unwittingly shapes decades of American history while loving one woman.",
     8.8, 1994, "Forrest Gump"),

    ("Gladiator", "Action, Drama, Adventure",
     "A betrayed Roman general is enslaved and rises through the gladiatorial arena to avenge his murdered family.",
     8.5, 2000, "Gladiator (2000 film)"),

    ("The Prestige", "Drama, Mystery, Thriller",
     "Two rival Victorian stage magicians destroy each other in an obsessive competition to perform the perfect illusion.",
     8.5, 2006, "The Prestige (film)"),

    ("Shutter Island", "Mystery, Thriller, Drama",
     "A US Marshal investigating a patient's disappearance at a remote psychiatric hospital begins to doubt his own sanity.",
     8.2, 2010, "Shutter Island (film)"),

    ("Avatar", "Sci-Fi, Adventure, Action",
     "A paralysed marine sent to the moon Pandora in an alien body is torn between his orders and the tribe he grows to love.",
     7.9, 2009, "Avatar (2009 film)"),

    ("Black Panther", "Action, Adventure, Sci-Fi",
     "The new king of the hidden African nation of Wakanda must defend his throne and his people from a vengeful challenger.",
     7.3, 2018, "Black Panther (film)"),

    ("Doctor Strange", "Fantasy, Action, Adventure",
     "An arrogant neurosurgeon loses the use of his hands and is trained in the mystic arts to defend reality itself.",
     7.5, 2016, "Doctor Strange (2016 film)"),

    ("Thor", "Action, Fantasy, Adventure",
     "An arrogant Norse god is stripped of his power and banished to Earth, where he learns humility and true heroism.",
     7.0, 2011, "Thor (film)"),

    ("Captain America: The First Avenger", "Action, Adventure, Sci-Fi",
     "A frail young volunteer is transformed into a super soldier and becomes America's symbol of hope during World War II.",
     6.9, 2011, "Captain America: The First Avenger"),

    ("Guardians of the Galaxy", "Sci-Fi, Adventure, Comedy",
     "A band of misfit outlaws reluctantly unite to keep a powerful orb out of the hands of a fanatical alien warlord.",
     8.0, 2014, "Guardians of the Galaxy (film)"),

    ("Deadpool", "Action, Comedy, Adventure",
     "A wisecracking mercenary gains accelerated healing powers through a brutal experiment and hunts the man who ruined his life.",
     8.0, 2016, "Deadpool (film)"),

    ("Black Widow", "Action, Thriller, Adventure",
     "A former Russian assassin confronts the dark secrets of her past and the spy programme that created her.",
     6.7, 2021, "Black Widow (2021 film)"),

    ("Wonder Woman", "Action, Fantasy, Adventure",
     "An Amazon princess leaves her hidden island to fight alongside humans in the First World War and stop a god of war.",
     7.4, 2017, "Wonder Woman (2017 film)"),

    ("Man of Steel", "Action, Sci-Fi, Adventure",
     "A young man raised on Earth discovers he is an alien with extraordinary powers and must defend his adopted world.",
     7.1, 2013, "Man of Steel (film)"),

    ("Aquaman", "Action, Fantasy, Adventure",
     "The half-human heir to the underwater kingdom of Atlantis must claim his birthright to stop a war against the surface world.",
     6.8, 2018, "Aquaman (film)"),

    ("Batman Begins", "Action, Crime, Drama",
     "After years of training abroad, Bruce Wayne returns to Gotham City and becomes a masked symbol of justice and fear.",
     8.2, 2005, "Batman Begins"),

    ("The Dark Knight Rises", "Action, Crime, Drama",
     "Eight years after vanishing, Batman returns to save Gotham from Bane, a brutal revolutionary who breaks both city and hero.",
     8.4, 2012, "The Dark Knight Rises"),

    ("Dune", "Sci-Fi, Adventure, Drama",
     "The heir of a noble house travels to a lethal desert planet to protect the most valuable resource in the known universe.",
     8.0, 2021, "Dune (2021 film)"),

    ("Dune: Part Two", "Sci-Fi, Adventure, Drama",
     "A young exiled duke unites with the desert people of Arrakis to wage a holy war against the house that destroyed his family.",
     8.5, 2024, "Dune: Part Two"),

    ("Tenet", "Sci-Fi, Action, Thriller",
     "A secret agent learns to manipulate the flow of time in a mission to prevent a war worse than nuclear annihilation.",
     7.3, 2020, "Tenet (film)"),

    ("Edge of Tomorrow", "Sci-Fi, Action, Adventure",
     "A soldier relives the same day of a losing alien war over and over, growing deadlier with every brutal death.",
     7.9, 2014, "Edge of Tomorrow"),

    ("Ready Player One", "Sci-Fi, Adventure, Action",
     "A teenager hunts a fortune hidden inside a sprawling virtual reality world before a ruthless corporation can claim it.",
     7.4, 2018, "Ready Player One (film)"),

    ("The Martian", "Sci-Fi, Drama, Adventure",
     "An astronaut left behind on Mars uses science, humour and sheer stubbornness to survive until a rescue can reach him.",
     8.0, 2015, "The Martian (film)"),

    ("Gravity", "Sci-Fi, Thriller, Drama",
     "Two astronauts are left adrift in orbit after debris destroys their shuttle and must fight to reach safety.",
     7.7, 2013, "Gravity (2013 film)"),

    ("The Shawshank Redemption", "Drama, Crime",
     "A banker wrongly convicted of murder forms a lifelong friendship in prison and quietly engineers his own redemption.",
     9.3, 1994, "The Shawshank Redemption"),

    ("The Godfather", "Crime, Drama",
     "The ageing patriarch of a New York crime dynasty hands control of his empire to his reluctant youngest son.",
     9.2, 1972, "The Godfather"),

    ("Fight Club", "Drama, Thriller",
     "An insomniac office worker and a reckless soap salesman start an underground fight club that spirals into anarchy.",
     8.8, 1999, "Fight Club"),

    ("The Wolf of Wall Street", "Crime, Drama, Comedy",
     "A New York stockbroker builds a fortune through fraud and excess before federal agents close in on his empire.",
     8.2, 2013, "The Wolf of Wall Street (2013 film)"),

    ("Whiplash", "Drama, Music",
     "A young jazz drummer is pushed to the edge of sanity by an abusive conservatory instructor obsessed with greatness.",
     8.5, 2014, "Whiplash (2014 film)"),

    ("La La Land", "Romance, Music, Drama",
     "A struggling actress and a jazz pianist fall in love in Los Angeles while chasing careers that pull them apart.",
     8.0, 2016, "La La Land"),

    ("The Hangover", "Comedy",
     "Three friends wake with no memory of a wild Las Vegas bachelor party and must retrace the night to find the missing groom.",
     7.7, 2009, "The Hangover"),

    ("Home Alone", "Comedy, Family, Adventure",
     "An eight-year-old boy accidentally left behind at Christmas defends his house from two bumbling burglars.",
     7.7, 1990, "Home Alone"),

    ("The Conjuring 2", "Horror, Mystery, Thriller",
     "The Warrens travel to London to help a single mother and her daughters tormented by a violent poltergeist.",
     7.3, 2016, "The Conjuring 2"),

    ("Pulp Fiction", "Crime, Drama, Thriller",
     "The lives of two hitmen, a boxer and a gangster's wife intertwine across four interlocking tales of violence and dark comedy.",
     8.9, 1994, "Pulp Fiction"),

    ("Goodfellas", "Crime, Drama, Biography",
     "A young man rises through the ranks of the New York mafia and watches his glamorous criminal life collapse into paranoia.",
     8.7, 1990, "Goodfellas"),

    ("The Departed", "Crime, Thriller, Drama",
     "An undercover cop and a mole inside the police race to expose each other inside the Boston Irish mob.",
     8.5, 2006, "The Departed"),

    ("Se7en", "Crime, Mystery, Thriller",
     "Two detectives hunt a meticulous serial killer who stages his murders around the seven deadly sins.",
     8.6, 1995, "Seven (1995 film)"),

    ("The Silence of the Lambs", "Crime, Thriller, Horror",
     "A young FBI trainee seeks the help of an imprisoned cannibal psychiatrist to catch another active serial killer.",
     8.6, 1991, "The Silence of the Lambs (film)"),

    ("Parasite", "Drama, Thriller, Comedy",
     "A poor family cons its way into the household of a wealthy clan, until a hidden secret turns the arrangement deadly.",
     8.5, 2019, "Parasite (2019 film)"),

    ("Schindler's List", "Drama, History, Biography",
     "A German industrialist gradually risks everything to save more than a thousand Jewish refugees during the Holocaust.",
     9.0, 1993, "Schindler's List"),

    ("Saving Private Ryan", "Drama, War, Action",
     "After the D-Day landings, a squad of soldiers is sent behind enemy lines to bring one paratrooper safely home.",
     8.6, 1998, "Saving Private Ryan"),

    ("The Green Mile", "Drama, Fantasy, Crime",
     "Guards on a 1930s death row meet a towering inmate whose gentle nature conceals a miraculous healing gift.",
     8.6, 1999, "The Green Mile (film)"),

    ("Django Unchained", "Western, Drama, Action",
     "A freed slave partners with a bounty hunter to rescue his wife from a brutal Mississippi plantation owner.",
     8.5, 2012, "Django Unchained"),

    ("Inglourious Basterds", "War, Drama, Adventure",
     "A squad of Jewish-American soldiers and a vengeful cinema owner plot to end the Nazi regime in occupied France.",
     8.4, 2009, "Inglourious Basterds"),

    ("The Lord of the Rings: The Fellowship of the Ring", "Fantasy, Adventure, Drama",
     "A hobbit inherits a ring of terrible power and sets out with eight companions to destroy it before darkness spreads.",
     8.9, 2001, "The Lord of the Rings: The Fellowship of the Ring"),

    ("The Lord of the Rings: The Two Towers", "Fantasy, Adventure, Drama",
     "The broken fellowship fights on separate fronts as the ring bearer edges closer to Mordor with a treacherous guide.",
     8.8, 2002, "The Lord of the Rings: The Two Towers"),

    ("The Lord of the Rings: The Return of the King", "Fantasy, Adventure, Drama",
     "The armies of men make a final desperate stand while two hobbits carry the ring to the fires of Mount Doom.",
     9.0, 2003, "The Lord of the Rings: The Return of the King"),

    ("The Hobbit: An Unexpected Journey", "Fantasy, Adventure, Family",
     "A home-loving hobbit is swept into a quest with thirteen dwarves to reclaim a mountain kingdom from a dragon.",
     7.8, 2012, "The Hobbit: An Unexpected Journey"),

    ("Star Wars: A New Hope", "Sci-Fi, Adventure, Fantasy",
     "A farm boy joins a rebellion against a galactic empire and discovers his destiny as a wielder of the Force.",
     8.6, 1977, "Star Wars (film)"),

    ("The Empire Strikes Back", "Sci-Fi, Adventure, Fantasy",
     "The rebels are scattered by the empire while a young Jedi trains with a master and learns a devastating truth.",
     8.7, 1980, "The Empire Strikes Back"),

    ("Star Wars: The Force Awakens", "Sci-Fi, Adventure, Action",
     "A scavenger and a runaway soldier are drawn into a galactic conflict as a new order rises from the empire's ashes.",
     7.8, 2015, "Star Wars: The Force Awakens"),

    ("Back to the Future", "Sci-Fi, Comedy, Adventure",
     "A teenager is sent thirty years into the past by a homemade time machine and must repair his own future.",
     8.5, 1985, "Back to the Future"),

    ("Terminator 2: Judgment Day", "Sci-Fi, Action, Thriller",
     "A reprogrammed cyborg protects a boy destined to lead humanity from a shapeshifting assassin sent to kill him.",
     8.6, 1991, "Terminator 2: Judgment Day"),

    ("Alien", "Sci-Fi, Horror, Thriller",
     "The crew of a commercial spacecraft is hunted one by one by a perfectly evolved extraterrestrial predator.",
     8.5, 1979, "Alien (film)"),

    ("Blade Runner 2049", "Sci-Fi, Drama, Mystery",
     "A replicant detective uncovers a buried secret that could shatter the fragile order between humans and machines.",
     8.0, 2017, "Blade Runner 2049"),

    ("E.T. the Extra-Terrestrial", "Sci-Fi, Family, Adventure",
     "A lonely boy befriends a stranded alien and helps it escape government scientists to return home.",
     7.9, 1982, "E.T. the Extra-Terrestrial"),

    ("Jaws", "Thriller, Adventure, Horror",
     "A police chief, a marine biologist and a grizzled fisherman hunt an enormous great white shark terrorising a resort town.",
     8.1, 1975, "Jaws (film)"),

    ("Jurassic Park", "Adventure, Sci-Fi, Thriller",
     "Scientists touring a park of cloned dinosaurs are hunted when the security systems fail during a tropical storm.",
     8.2, 1993, "Jurassic Park (film)"),

    ("Raiders of the Lost Ark", "Adventure, Action, Fantasy",
     "A globetrotting archaeologist races Nazi agents to recover the Ark of the Covenant before its power is unleashed.",
     8.4, 1981, "Raiders of the Lost Ark"),

    ("The Lion King", "Animation, Family, Drama",
     "A young lion prince flees his kingdom after his father's murder and must return to claim his rightful place.",
     8.5, 1994, "The Lion King"),

    ("Toy Story", "Animation, Family, Comedy",
     "A cowboy doll's place as favourite toy is threatened when a flashy space ranger action figure arrives.",
     8.3, 1995, "Toy Story"),

    ("Finding Nemo", "Animation, Family, Adventure",
     "An anxious clownfish crosses the ocean with a forgetful companion to rescue his captured son.",
     8.2, 2003, "Finding Nemo"),

    ("Up", "Animation, Family, Adventure",
     "A grieving widower flies his house to South America with balloons and an accidental young stowaway.",
     8.3, 2009, "Up (2009 film)"),

    ("Inside Out", "Animation, Family, Comedy",
     "The five emotions inside a young girl's mind struggle to guide her through an unsettling move to a new city.",
     8.1, 2015, "Inside Out (2015 film)"),

    ("Coco", "Animation, Family, Fantasy",
     "A boy who dreams of music is transported to the Land of the Dead and uncovers his family's hidden history.",
     8.4, 2017, "Coco (2017 film)"),

    ("WALL-E", "Animation, Sci-Fi, Family",
     "A lonely waste-collecting robot on an abandoned Earth follows the probe he loves across the galaxy.",
     8.4, 2008, "WALL-E"),

    ("Spider-Man: Into the Spider-Verse", "Animation, Action, Adventure",
     "A Brooklyn teenager becomes Spider-Man and teams with heroes from parallel dimensions to save the multiverse.",
     8.4, 2018, "Spider-Man: Into the Spider-Verse"),

    ("Spider-Man: No Way Home", "Action, Adventure, Fantasy",
     "A botched spell tears open the multiverse and brings Spider-Man face to face with villains from other realities.",
     8.2, 2021, "Spider-Man: No Way Home"),

    ("Avengers: Infinity War", "Action, Adventure, Sci-Fi",
     "The Avengers and their allies make a desperate stand against Thanos, a titan seeking the six Infinity Stones.",
     8.4, 2018, "Avengers: Infinity War"),

    ("Avengers: Endgame", "Action, Adventure, Drama",
     "The surviving heroes attempt one impossible last mission through time to undo the loss of half the universe.",
     8.4, 2019, "Avengers: Endgame"),

    ("Thor: Ragnarok", "Action, Comedy, Fantasy",
     "Stranded on a gladiator planet without his hammer, Thor races to stop the goddess of death from destroying Asgard.",
     7.9, 2017, "Thor: Ragnarok"),

    ("Logan", "Action, Drama, Sci-Fi",
     "An ageing, weary Wolverine shelters an ailing Professor X and protects a young mutant girl hunted across the country.",
     8.1, 2017, "Logan (film)"),

    ("The Batman", "Action, Crime, Mystery",
     "In his second year of crimefighting, Batman tracks a sadistic serial killer exposing corruption at Gotham's core.",
     7.8, 2022, "The Batman (film)"),

    ("Oppenheimer", "Drama, History, Biography",
     "The physicist who led the Manhattan Project confronts the moral weight of the weapon he brought into the world.",
     8.3, 2023, "Oppenheimer (film)"),

    ("Barbie", "Comedy, Adventure, Fantasy",
     "A doll living in a perfect plastic world travels to the real one and confronts what it means to be human.",
     6.8, 2023, "Barbie (film)"),

    ("Top Gun: Maverick", "Action, Drama, Adventure",
     "A veteran navy pilot trains a squad of elite graduates for a near-impossible mission while facing his own past.",
     8.2, 2022, "Top Gun: Maverick"),

    ("John Wick", "Action, Thriller, Crime",
     "A retired hitman returns to the criminal underworld to hunt the gangsters who destroyed the last piece of his old life.",
     7.4, 2014, "John Wick"),

    ("Mad Max: Fury Road", "Action, Adventure, Sci-Fi",
     "A drifter and a rebel commander flee a tyrant across a post-apocalyptic desert in a relentless vehicular war.",
     8.1, 2015, "Mad Max: Fury Road"),

    ("The Grand Budapest Hotel", "Comedy, Drama, Adventure",
     "A legendary concierge and his loyal lobby boy are swept into a murder mystery over a priceless stolen painting.",
     8.1, 2014, "The Grand Budapest Hotel"),

    ("Get Out", "Horror, Mystery, Thriller",
     "A young man visits his girlfriend's family estate and uncovers a disturbing secret beneath their relentless hospitality.",
     7.8, 2017, "Get Out"),

    ("Hereditary", "Horror, Drama, Mystery",
     "After the death of her secretive mother, a woman's family unravels as a terrifying inheritance reveals itself.",
     7.3, 2018, "Hereditary (film)"),

    ("It", "Horror, Thriller",
     "A group of bullied children band together to face a shapeshifting entity that feeds on the fears of their small town.",
     7.3, 2017, "It (2017 film)"),

    ("3 Idiots", "Comedy, Drama",
     "Two friends search for their brilliant, rebellious college classmate and revisit the engineering years that changed them.",
     8.4, 2009, "3 Idiots"),

    ("Dangal", "Drama, Sport, Biography",
     "A former wrestler trains his two daughters against fierce social opposition to become India's champion wrestlers.",
     8.3, 2016, "Dangal (film)"),

    ("RRR", "Action, Drama, Adventure",
     "Two revolutionaries in colonial India forge an unbreakable friendship before their opposing missions collide.",
     7.8, 2022, "RRR (film)"),

    ("Baahubali: The Beginning", "Action, Fantasy, Adventure",
     "A young man raised in a remote village discovers his royal bloodline and the war that cost his father a kingdom.",
     8.0, 2015, "Baahubali: The Beginning"),

    ("PK", "Comedy, Drama, Sci-Fi",
     "A stranded alien wanders India asking innocent questions that expose the contradictions of faith and society.",
     8.1, 2014, "PK (film)"),

    ("Sholay", "Action, Adventure, Drama",
     "A retired policeman hires two small-time crooks to capture the ruthless bandit who destroyed his family.",
     8.1, 1975, "Sholay"),

    ("Gully Boy", "Drama, Music",
     "A young man from a Mumbai slum finds his voice as a street rapper and fights to escape the life he was born into.",
     7.9, 2019, "Gully Boy"),

    ("Drishyam", "Crime, Drama, Thriller",
     "An ordinary cable operator uses everything he has learned from films to shield his family from a murder investigation.",
     8.2, 2015, "Drishyam (2015 film)"),
]
