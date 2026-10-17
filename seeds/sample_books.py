"""
Seed dataset for BookWise Atelier.
Contains 36 diverse, high-quality sample books spanning 15 genres, multiple languages,
page counts, and durations.
"""

SAMPLE_BOOKS = [
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "description": "The riveting tale of Kvothe, an orphaned boy gifted with magic and musical genius who grows to become the most notorious wizard, musician, and scholar his world has ever known.",
        "genres": ["Fantasy", "Adventure", "Fiction"],
        "language": "English",
        "publication_year": 2007,
        "age_suitability": "Young Adult",
        "estimated_duration": 45,
        "keywords": ["magic", "university", "music", "legend", "quest", "mystery", "sympathy"],
        "rating": 4.8,
        "isbn": "978-0756404741",
        "cover_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&q=80&w=600",
        "page_count": 662
    },
    {
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "description": "Private journal entries of the Roman Emperor Marcus Aurelius detailing Stoic philosophy, personal resilience, duty, ethics, and clarity in the face of adversity and leadership.",
        "genres": ["Philosophy", "History", "Biography"],
        "language": "English",
        "publication_year": 180,
        "age_suitability": "Adult",
        "estimated_duration": 25,
        "keywords": ["stoicism", "resilience", "wisdom", "duty", "mind", "philosophy", "ethics", "calm"],
        "rating": 4.7,
        "isbn": "978-0140449334",
        "cover_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&q=80&w=600",
        "page_count": 254
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family in a sweeping galactic struggle over the universe's most precious spice resource.",
        "genres": ["Science Fiction", "Adventure", "Philosophy"],
        "language": "English",
        "publication_year": 1965,
        "age_suitability": "Adult",
        "estimated_duration": 40,
        "keywords": ["desert", "spice", "ecology", "prophecy", "empire", "space", "power", "politics"],
        "rating": 4.7,
        "isbn": "978-0441172719",
        "cover_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=600",
        "page_count": 688
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "The sparkling romantic clash between the opinionated Elizabeth Bennet and her proud aristocratic beau, Mr. Fitzwilliam Darcy, in Georgian England.",
        "genres": ["Romance", "Fiction", "History"],
        "language": "English",
        "publication_year": 1813,
        "age_suitability": "All Ages",
        "estimated_duration": 30,
        "keywords": ["love", "wit", "society", "marriage", "family", "class", "england", "dialogue"],
        "rating": 4.6,
        "isbn": "978-0141439518",
        "cover_url": "https://images.unsplash.com/photo-1476275466078-4007374efbbe?auto=format&fit=crop&q=80&w=600",
        "page_count": 432
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "description": "Alicia Berenson’s life is seemingly perfect. One evening she shoots her husband five times in the face, and then never speaks another word. Psychotherapist Theo Faber attempts to unravel her silence.",
        "genres": ["Mystery", "Thriller", "Fiction"],
        "language": "English",
        "publication_year": 2019,
        "age_suitability": "Adult",
        "estimated_duration": 25,
        "keywords": ["psychological", "twist", "murder", "silence", "therapy", "secrets", "suspense"],
        "rating": 4.5,
        "isbn": "978-1250301696",
        "cover_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&q=80&w=600",
        "page_count": 336
    },
    {
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "description": "Based on more than forty interviews with Jobs conducted over two years, this is the definitive biography of the creative entrepreneur whose passion for perfection revolutionized six industries.",
        "genres": ["Biography", "Technology", "History"],
        "language": "English",
        "publication_year": 2011,
        "age_suitability": "Adult",
        "estimated_duration": 35,
        "keywords": ["innovation", "apple", "design", "leadership", "technology", "entrepreneurship", "creativity"],
        "rating": 4.6,
        "isbn": "978-1451648539",
        "cover_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&q=80&w=600",
        "page_count": 656
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "description": "A comprehensive, practical guide on how to change your habits and get 1% better every day through tiny behavioral adjustments, environment design, and identity shifts.",
        "genres": ["Self-Help", "Education", "Philosophy"],
        "language": "English",
        "publication_year": 2018,
        "age_suitability": "All Ages",
        "estimated_duration": 20,
        "keywords": ["habits", "productivity", "growth", "discipline", "mindset", "systems", "psychology"],
        "rating": 4.8,
        "isbn": "978-0735211292",
        "cover_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&q=80&w=600",
        "page_count": 320
    },
    {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "description": "A deep architectural dive into the fundamental principles, algorithms, and trade-offs behind modern distributed data systems, storage engines, and reliability.",
        "genres": ["Technology", "Education"],
        "language": "English",
        "publication_year": 2017,
        "age_suitability": "Adult",
        "estimated_duration": 45,
        "keywords": ["distributed systems", "database", "architecture", "scalability", "replication", "consensus", "software"],
        "rating": 4.9,
        "isbn": "978-1449373320",
        "cover_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&q=80&w=600",
        "page_count": 616
    },
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "description": "From a renowned historian comes a groundbreaking narrative of humanity’s creation and evolution, exploring how biology and history have defined us and enhanced our understanding of what it means to be human.",
        "genres": ["History", "Philosophy", "Education"],
        "language": "English",
        "publication_year": 2014,
        "age_suitability": "Adult",
        "estimated_duration": 30,
        "keywords": ["evolution", "anthropology", "civilization", "society", "agriculture", "cognitive", "future"],
        "rating": 4.7,
        "isbn": "978-0062316097",
        "cover_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&q=80&w=600",
        "page_count": 464
    },
    {
        "title": "The Little Prince",
        "author": "Antoine de Saint-Exupéry",
        "description": "A poetic tale of a young prince who visits various planets in space, including Earth, addressing themes of loneliness, friendship, love, and loss with touching simplicity.",
        "genres": ["Children's Literature", "Philosophy", "Fiction"],
        "language": "French",
        "publication_year": 1943,
        "age_suitability": "All Ages",
        "estimated_duration": 15,
        "keywords": ["friendship", "rose", "fox", "stars", "imagination", "heart", "poetic", "innocence"],
        "rating": 4.8,
        "isbn": "978-0156012195",
        "cover_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&q=80&w=600",
        "page_count": 96
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "description": "Bilbo Baggins, a hobbit enjoying a comfortable, unambitious life, is whisked away on an unexpected journey by the wizard Gandalf and thirteen dwarves to reclaim their treasure from Smaug.",
        "genres": ["Fantasy", "Adventure", "Children's Literature"],
        "language": "English",
        "publication_year": 1937,
        "age_suitability": "All Ages",
        "estimated_duration": 30,
        "keywords": ["hobbit", "dragon", "treasure", "journey", "middle-earth", "ring", "dwarves", "adventure"],
        "rating": 4.8,
        "isbn": "978-0547928227",
        "cover_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&q=80&w=600",
        "page_count": 310
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "description": "An orphaned eleven-year-old boy discovers he is a wizard and attends Hogwarts School of Witchcraft and Wizardry, where he discovers his family's past and confronts dark forces.",
        "genres": ["Fantasy", "Young Adult", "Adventure"],
        "language": "English",
        "publication_year": 1997,
        "age_suitability": "Young Adult",
        "estimated_duration": 30,
        "keywords": ["hogwarts", "magic", "wizards", "friendship", "school", "spells", "mystery"],
        "rating": 4.9,
        "isbn": "978-0590353427",
        "cover_url": "https://images.unsplash.com/photo-1532012164546-f432f2e3777f?auto=format&fit=crop&q=80&w=600",
        "page_count": 309
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "description": "Winston Smith struggles with his inner rebellion against the totalitarian regime of the Party and its omnipresent leader, Big Brother, in a harrowing dystopia of surveillance and mind control.",
        "genres": ["Fiction", "Science Fiction", "Philosophy"],
        "language": "English",
        "publication_year": 1949,
        "age_suitability": "Adult",
        "estimated_duration": 25,
        "keywords": ["dystopia", "surveillance", "totalitarianism", "freedom", "thoughtcrime", "truth", "politics"],
        "rating": 4.7,
        "isbn": "978-0451524935",
        "cover_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&q=80&w=600",
        "page_count": 328
    },
    {
        "title": "Sherlock Holmes: The Hound of the Baskervilles",
        "author": "Arthur Conan Doyle",
        "description": "The world’s most celebrated detective investigates the mysterious death of Sir Charles Baskerville and the legend of a demonic spectral hound roaming Dartmoor.",
        "genres": ["Mystery", "Thriller", "Fiction"],
        "language": "English",
        "publication_year": 1902,
        "age_suitability": "All Ages",
        "estimated_duration": 25,
        "keywords": ["detective", "deduction", "moor", "hound", "clues", "fog", "london", "investigation"],
        "rating": 4.6,
        "isbn": "978-0141034300",
        "cover_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&q=80&w=600",
        "page_count": 256
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "description": "Santiago, an Andalusian shepherd boy, travels from his homeland in Spain to the Egyptian desert in search of a treasure buried near the Pyramids, learning to listen to his heart and the Soul of the World.",
        "genres": ["Fiction", "Philosophy", "Adventure"],
        "language": "Spanish",
        "publication_year": 1988,
        "age_suitability": "All Ages",
        "estimated_duration": 20,
        "keywords": ["destiny", "dreams", "journey", "treasure", "spirituality", "desert", "omen", "wisdom"],
        "rating": 4.6,
        "isbn": "978-0062315007",
        "cover_url": "https://images.unsplash.com/photo-1507842229451-7f01be7fe802?auto=format&fit=crop&q=80&w=600",
        "page_count": 208
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees. A timeless handbook of agile software craftsmanship and best engineering practices.",
        "genres": ["Technology", "Education"],
        "language": "English",
        "publication_year": 2008,
        "age_suitability": "Adult",
        "estimated_duration": 30,
        "keywords": ["programming", "refactoring", "software engineering", "design patterns", "architecture", "craftsmanship"],
        "rating": 4.5,
        "isbn": "978-0132350884",
        "cover_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&q=80&w=600",
        "page_count": 464
    },
    {
        "title": "The Song of Achilles",
        "author": "Madeline Miller",
        "description": "A breathtaking retelling of the Trojan War and the deep, profound love between the golden hero Achilles and the awkward young prince Patroclus.",
        "genres": ["Romance", "Fantasy", "History", "Fiction"],
        "language": "English",
        "publication_year": 2011,
        "age_suitability": "Young Adult",
        "estimated_duration": 30,
        "keywords": ["greek mythology", "troy", "love", "achilles", "war", "destiny", "tragedy", "gods"],
        "rating": 4.8,
        "isbn": "978-0062060624",
        "cover_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&q=80&w=600",
        "page_count": 416
    },
    {
        "title": "Circe",
        "author": "Madeline Miller",
        "description": "In the house of Helios, god of the sun, a daughter is born. Circe turns to witchcraft and discovers her power to transform mortals into monsters and tame wild beasts on her solitary island.",
        "genres": ["Fantasy", "Fiction", "Adventure"],
        "language": "English",
        "publication_year": 2018,
        "age_suitability": "Adult",
        "estimated_duration": 30,
        "keywords": ["witchcraft", "island", "mythology", "sorcery", "empowerment", "solitude", "gods"],
        "rating": 4.7,
        "isbn": "978-0316556347",
        "cover_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=600",
        "page_count": 393
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "description": "An unforgettable memoir about a young girl who, kept out of school by her survivalist family in rural Idaho, leaves home at seventeen to educate herself, ultimately earning a PhD from Cambridge.",
        "genres": ["Biography", "Education", "History"],
        "language": "English",
        "publication_year": 2018,
        "age_suitability": "Adult",
        "estimated_duration": 30,
        "keywords": ["memoir", "family", "education", "resilience", "idaho", "growth", "triumph"],
        "rating": 4.7,
        "isbn": "978-0399590504",
        "cover_url": "https://images.unsplash.com/photo-1491841573634-28140fc7ced7?auto=format&fit=crop&q=80&w=600",
        "page_count": 352
    },
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "description": "Ryland Grace is the sole survivor on a desperate, last-chance mission to save humanity from an extinction-level solar crisis. With the clock ticking and light-years from Earth, he must use science to solve the impossible.",
        "genres": ["Science Fiction", "Adventure", "Technology"],
        "language": "English",
        "publication_year": 2021,
        "age_suitability": "Young Adult",
        "estimated_duration": 35,
        "keywords": ["space", "aliens", "science", "survival", "engineering", "humor", "friendship", "stars"],
        "rating": 4.9,
        "isbn": "978-0593135204",
        "cover_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=600",
        "page_count": 496
    },
    {
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "description": "A Pulitzer Prize-winning examination of the environmental and geographical factors that shaped the modern world and why Eurasian civilizations survived and conquered others.",
        "genres": ["History", "Education", "Philosophy"],
        "language": "English",
        "publication_year": 1997,
        "age_suitability": "Adult",
        "estimated_duration": 40,
        "keywords": ["civilization", "geography", "history", "agriculture", "technology", "sociology"],
        "rating": 4.5,
        "isbn": "978-0393317558",
        "cover_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&q=80&w=600",
        "page_count": 480
    },
    {
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "description": "Between life and death there is a library where the shelves go on forever. Nora Seed gets the chance to undo her regrets and see how her life would have changed had she made different choices.",
        "genres": ["Fiction", "Fantasy", "Philosophy"],
        "language": "English",
        "publication_year": 2020,
        "age_suitability": "Young Adult",
        "estimated_duration": 25,
        "keywords": ["regret", "parallel lives", "library", "hope", "mental health", "choices", "meaning"],
        "rating": 4.4,
        "isbn": "978-0525559474",
        "cover_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&q=80&w=600",
        "page_count": 304
    },
    {
        "title": "And Then There Were None",
        "author": "Agatha Christie",
        "description": "Ten strangers are lured to an isolated island mansion off the Devon coast. During dinner, a phonograph record accuses each of murder. One by one, the guests are killed in accordance with a nursery rhyme.",
        "genres": ["Mystery", "Thriller"],
        "language": "English",
        "publication_year": 1939,
        "age_suitability": "Young Adult",
        "estimated_duration": 20,
        "keywords": ["island", "murder", "locked room", "clues", "whodunit", "agatha christie", "secrets"],
        "rating": 4.8,
        "isbn": "978-0062073488",
        "cover_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&q=80&w=600",
        "page_count": 272
    },
    {
        "title": "Man's Search for Meaning",
        "author": "Viktor E. Frankl",
        "description": "Psychiatrist Viktor Frankl’s memoir of his time in Nazi concentration camps and his development of logotherapy, arguing that the primary human drive is the discovery and pursuit of what we personally find meaningful.",
        "genres": ["Philosophy", "Biography", "Self-Help"],
        "language": "German",
        "publication_year": 1946,
        "age_suitability": "Adult",
        "estimated_duration": 20,
        "keywords": ["meaning", "logotherapy", "psychology", "holocaust", "resilience", "purpose", "hope"],
        "rating": 4.9,
        "isbn": "978-0807014295",
        "cover_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&q=80&w=600",
        "page_count": 165
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "description": "Rules for focused success in a distracted world. Newport argues that the ability to focus without distraction on cognitively demanding tasks is becoming increasingly rare and valuable.",
        "genres": ["Self-Help", "Technology", "Education"],
        "language": "English",
        "publication_year": 2016,
        "age_suitability": "All Ages",
        "estimated_duration": 25,
        "keywords": ["focus", "productivity", "distraction", "discipline", "work", "habits", "concentration"],
        "rating": 4.5,
        "isbn": "978-1455586691",
        "cover_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&q=80&w=600",
        "page_count": 296
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A portrait of the Jazz Age on Long Island, narrating the mysterious millionaire Jay Gatsby and his quixotic passion and obsession for the beautiful former debutante Daisy Buchanan.",
        "genres": ["Fiction", "Romance", "History"],
        "language": "English",
        "publication_year": 1925,
        "age_suitability": "Young Adult",
        "estimated_duration": 20,
        "keywords": ["wealth", "jazz age", "obsession", "tragedy", "love", "american dream", "parties"],
        "rating": 4.4,
        "isbn": "978-0743273565",
        "cover_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&q=80&w=600",
        "page_count": 180
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "description": "The seminal cyberpunk masterpiece that coined the term cyberspace, following Case, a washed-up computer hacker hired by a mysterious employer for one ultimate cyber-heist.",
        "genres": ["Science Fiction", "Technology", "Thriller"],
        "language": "English",
        "publication_year": 1984,
        "age_suitability": "Mature",
        "estimated_duration": 30,
        "keywords": ["cyberpunk", "hacker", "ai", "matrix", "cyberspace", "dystopia", "neon", "virtual reality"],
        "rating": 4.5,
        "isbn": "978-0441569595",
        "cover_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&q=80&w=600",
        "page_count": 271
    },
    {
        "title": "The Road",
        "author": "Cormac McCarthy",
        "description": "A father and his young son walk alone through burned post-apocalyptic America, moving toward the coast in a bleak, devastating, yet profoundly tender story of survival and love.",
        "genres": ["Fiction", "Thriller", "Adventure"],
        "language": "English",
        "publication_year": 2006,
        "age_suitability": "Mature",
        "estimated_duration": 25,
        "keywords": ["post-apocalyptic", "survival", "father", "son", "fire", "journey", "devastation", "love"],
        "rating": 4.6,
        "isbn": "978-0307387899",
        "cover_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=600",
        "page_count": 287
    },
    {
        "title": "Becoming",
        "author": "Michelle Obama",
        "description": "An intimate, powerful, and inspiring memoir by the former First Lady of the United States, chronicling the experiences that have shaped her from the South Side of Chicago to the White House.",
        "genres": ["Biography", "History", "Self-Help"],
        "language": "English",
        "publication_year": 2018,
        "age_suitability": "All Ages",
        "estimated_duration": 30,
        "keywords": ["memoir", "leadership", "white house", "courage", "inspiration", "family", "education"],
        "rating": 4.8,
        "isbn": "978-1524763138",
        "cover_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=600",
        "page_count": 448
    },
    {
        "title": "The Pragmatic Programmer",
        "author": "David Thomas, Andrew Hunt",
        "description": "One of the most significant books in computing, offering timeless career advice, architectural guidelines, and professional tips for software engineers striving for excellence.",
        "genres": ["Technology", "Education"],
        "language": "English",
        "publication_year": 1999,
        "age_suitability": "All Ages",
        "estimated_duration": 30,
        "keywords": ["software", "engineering", "craftsmanship", "pragmatism", "testing", "career", "automation"],
        "rating": 4.8,
        "isbn": "978-0135957059",
        "cover_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&q=80&w=600",
        "page_count": 352
    },
    {
        "title": "The Book Thief",
        "author": "Markus Zusak",
        "description": "Narrated by Death, this touching novel follows Liesel Meminger, a young foster girl living outside Munich in 1939 who steals books to share with her neighbors and the Jewish man hidden in her basement.",
        "genres": ["History", "Young Adult", "Fiction"],
        "language": "English",
        "publication_year": 2005,
        "age_suitability": "Young Adult",
        "estimated_duration": 35,
        "keywords": ["wwii", "germany", "books", "words", "death", "courage", "friendship", "kindness"],
        "rating": 4.8,
        "isbn": "978-0375842207",
        "cover_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&q=80&w=600",
        "page_count": 552
    },
    {
        "title": "Norwegian Wood",
        "author": "Haruki Murakami",
        "description": "A nostalgic story of loss, sexuality, and blooming young adulthood in 1960s Tokyo, centered around Toru Watanabe and his devotion to a beautiful troubled young woman.",
        "genres": ["Fiction", "Romance", "Philosophy"],
        "language": "Japanese",
        "publication_year": 1987,
        "age_suitability": "Mature",
        "estimated_duration": 25,
        "keywords": ["tokyo", "music", "memory", "nostalgia", "grief", "love", "youth", "melancholy"],
        "rating": 4.5,
        "isbn": "978-0375704024",
        "cover_url": "https://images.unsplash.com/photo-1476275466078-4007374efbbe?auto=format&fit=crop&q=80&w=600",
        "page_count": 296
    },
    {
        "title": "The Da Vinci Code",
        "author": "Dan Brown",
        "description": "While in Paris, Harvard symbologist Robert Langdon is awakened in the night by a phone call: the elderly curator of the Louvre has been murdered inside the museum, leaving a bizarre trail of symbols.",
        "genres": ["Mystery", "Thriller", "Adventure"],
        "language": "English",
        "publication_year": 2003,
        "age_suitability": "Adult",
        "estimated_duration": 25,
        "keywords": ["paris", "symbols", "secret society", "grail", "conspiracy", "puzzles", "art", "thriller"],
        "rating": 4.3,
        "isbn": "978-0307474278",
        "cover_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&q=80&w=600",
        "page_count": 489
    },
    {
        "title": "Charlotte's Web",
        "author": "E.B. White",
        "description": "The timeless, tender tale of a little girl named Fern who loved a little pig named Wilbur, and of Wilbur's dear friend Charlotte A. Cavatica, a beautiful large grey spider who saves his life.",
        "genres": ["Children's Literature", "Fiction"],
        "language": "English",
        "publication_year": 1952,
        "age_suitability": "All Ages",
        "estimated_duration": 15,
        "keywords": ["friendship", "barn", "spider", "kindness", "loyalty", "animal", "childhood"],
        "rating": 4.7,
        "isbn": "978-0061124952",
        "cover_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&q=80&w=600",
        "page_count": 184
    },
    {
        "title": "Klara and the Sun",
        "author": "Kazuo Ishiguro",
        "description": "From Nobel laureate Kazuo Ishiguro comes the magnificent story of Klara, an Artificial Friend with outstanding observational qualities, who watches the behavior of those who come in to browse.",
        "genres": ["Science Fiction", "Philosophy", "Fiction"],
        "language": "English",
        "publication_year": 2021,
        "age_suitability": "Adult",
        "estimated_duration": 25,
        "keywords": ["artificial intelligence", "love", "humanity", "sun", "innocence", "future", "devotion"],
        "rating": 4.4,
        "isbn": "978-0593318171",
        "cover_url": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&q=80&w=600",
        "page_count": 303
    },
    {
        "title": "Don Quixote",
        "author": "Miguel de Cervantes",
        "description": "The epic comic and philosophical journey of Alonso Quixano, a nobleman who reads so many chivalric romances that he loses his mind and sets out to revive chivalry as Don Quixote de la Mancha.",
        "genres": ["Adventure", "Fiction", "Philosophy"],
        "language": "Spanish",
        "publication_year": 1605,
        "age_suitability": "Adult",
        "estimated_duration": 50,
        "keywords": ["chivalry", "windmills", "quest", "humor", "sancho panza", "knights", "classic", "spain"],
        "rating": 4.6,
        "isbn": "978-0060934347",
        "cover_url": "https://images.unsplash.com/photo-1507842229451-7f01be7fe802?auto=format&fit=crop&q=80&w=600",
        "page_count": 992
    }
]


def seed_database(db_instance):
    """Inserts sample books into the catalogue if empty, and provisions admin if credentials configured."""
    import os
    from app.models.book import Book
    from app.models.user import User
    from app.models.preference import UserPreference

    # Create admin user only if explicitly configured via environment variables
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@bookwise.atelier').strip()
    admin_password = os.environ.get('ADMIN_PASSWORD')

    if admin_email and admin_password and admin_password.strip():
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_name = os.environ.get('ADMIN_NAME', 'Atelier Curator').strip()
            admin_user = User(
                name=admin_name,
                email=admin_email,
                role='admin'
            )
            admin_user.set_password(admin_password.strip())
            db_instance.session.add(admin_user)
            db_instance.session.flush()

            pref = UserPreference(
                user_id=admin_user.id,
                preferred_genres=['Philosophy', 'History', 'Fiction'],
                preferred_languages=['English'],
                age_preference='Adult',
                preferred_duration=30,
                interest_keywords=['wisdom', 'books', 'ideas'],
                onboarding_completed=True,
                theme_preference='light'
            )
            db_instance.session.add(pref)

    # Insert books
    added_count = 0
    for book_data in SAMPLE_BOOKS:
        existing = Book.query.filter_by(title=book_data['title'], author=book_data['author']).first()
        if not existing:
            book = Book(**book_data)
            db_instance.session.add(book)
            added_count += 1

    db_instance.session.commit()
    return added_count
