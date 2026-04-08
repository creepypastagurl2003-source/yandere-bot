import discord
from discord.ext import commands
from discord import app_commands
from typing import List

PINK  = 0xffb6c1
RED   = 0x8b0000
DARK  = 0x1a0010
GOLD  = 0xffd700
TEAL  = 0x2e8b8b

CHARACTERS = {
    # ── PROTAGONIST ───────────────────────────────────────────────────────────
    "ayano aishi": {
        "name": "Ayano Aishi",
        "alias": "Yandere-chan",
        "category": "Protagonist",
        "role": "Student — 2nd Year",
        "personality": "Stoic, emotionless, obsessive, calculating, devoted",
        "description": (
            "The protagonist of Yandere Simulator. Born without the ability to feel emotions, "
            "Ayano's hollow world changed the moment she bumped into her Senpai. Now she feels "
            "*something* — and she will stalk, manipulate, frame, and eliminate anyone who dares "
            "get in the way of her love."
        ),
        "color": RED,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/c2/Ayano_Aishi_%28current%29.png/revision/latest?cb=20230706165639",
    },

    # ── SENPAIS ───────────────────────────────────────────────────────────────
    "taro yamada": {
        "name": "Taro Yamada",
        "alias": "Senpai (Male)",
        "category": "Senpai",
        "role": "Student — 3rd Year",
        "personality": "Kind, gentle, oblivious, dense, empathetic",
        "description": (
            "The default male Senpai. A quietly popular student admired for his warmth. "
            "He is completely unaware of the dangerous obsession directed at him and simply "
            "tries to be kind to everyone — which only makes things worse."
        ),
        "color": PINK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/a/aa/Taro_Yamada_%28Illustration%29.png/revision/latest?cb=20211012163824",
    },
    "taeko yamada": {
        "name": "Taeko Yamada",
        "alias": "Senpai (Female)",
        "category": "Senpai",
        "role": "Student — 3rd Year",
        "personality": "Kind, gentle, oblivious, dense, empathetic",
        "description": (
            "The female counterpart Senpai available in gender-swap mode. "
            "Just as kind, oblivious, and warmly regarded as her male counterpart — "
            "and just as completely unaware of what is watching her."
        ),
        "color": PINK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/cf/Taeko_Yamada_%28Illustration%29.png/revision/latest?cb=20211015041053",
    },

    # ── RIVALS ────────────────────────────────────────────────────────────────
    "osana najimi": {
        "name": "Osana Najimi",
        "alias": "Rival 1 — The Childhood Friend",
        "category": "Rival",
        "role": "Student — 3rd Year",
        "personality": "Tsundere, stubborn, sharp-tongued, secretly caring",
        "description": (
            "The first rival and Senpai's childhood friend. She constantly argues with him "
            "and denies her obvious feelings with classic tsundere outbursts — yet she is the "
            "first to defend him. Despite her rough exterior, she is genuinely kind-hearted."
        ),
        "color": 0xff6347,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/d/d0/Osana_Najimi_%28Illustration%29.png/revision/latest?cb=20211015042645",
    },
    "amai odayaka": {
        "name": "Amai Odayaka",
        "alias": "Rival 2 — The Sweetie",
        "category": "Rival",
        "role": "Student — 2nd Year / Cooking Club President",
        "personality": "Warm, nurturing, empathetic, universally beloved",
        "description": (
            "The second rival and president of the Cooking Club. She is adored by virtually "
            "everyone at Akademi for her gentle nature and homemade treats. She bonded with "
            "Senpai through shared lunches and quiet kindness."
        ),
        "color": 0xffb347,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/7/7c/Amai_Odayaka_%28Illustration%29.png/revision/latest?cb=20211014163116",
    },
    "kizana sunobu": {
        "name": "Kizana Sunobu",
        "alias": "Rival 3 — The Drama Queen",
        "category": "Rival",
        "role": "Student — 2nd Year / Drama Club President",
        "personality": "Theatrical, arrogant, self-important, secretly insecure",
        "description": (
            "The third rival and president of the Drama Club. She acts as though every moment "
            "of her life is a performance and considers herself the star of every scene. "
            "Beneath the dramatic flair lies a girl who simply wants to be truly seen."
        ),
        "color": 0x9b59b6,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/d/d9/KizanaSunobu-Reputation.png/revision/latest?cb=20250112233927",
    },
    "oka ruto": {
        "name": "Oka Ruto",
        "alias": "Rival 4 — The Occult Girl",
        "category": "Rival",
        "role": "Student — 2nd Year / Occult Club President",
        "personality": "Paranoid, mysterious, shy, perceptive, superstitious",
        "description": (
            "The fourth rival and leader of the Occult Club. She is deeply paranoid about "
            "supernatural forces lurking in the school — and may not be entirely wrong. "
            "She is one of the few students who senses that something is deeply wrong with Ayano."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/6f/Oka_Ruto_%28Illustration%29.png/revision/latest?cb=20160928214903",
    },
    "oshizu": {
        "name": "Oshizu",
        "alias": "Rival 5 — The Ghost",
        "category": "Rival",
        "role": "Supernatural Entity / Ghost",
        "personality": "Playful, mischievous, lonely, curious, childlike",
        "description": (
            "The fifth rival. A ghost who haunts Akademi High and developed feelings for "
            "Senpai after he interacted with her without fear. She is playful but profoundly "
            "lonely — she has been invisible and forgotten for far too long."
        ),
        "color": 0xc8a2c8,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/f/f4/1980sLogo.png/revision/latest?cb=20200101000000",
    },
    "muja kina": {
        "name": "Muja Kina",
        "alias": "Rival 6 — The Nurse",
        "category": "Rival",
        "role": "Substitute School Nurse",
        "personality": "Clumsy, caring, accident-prone, sincere, warm",
        "description": (
            "The sixth rival. A substitute school nurse who is endearingly clumsy but "
            "genuinely devoted to helping students. She met Senpai while treating an injury "
            "and her sincere care for him turned into something more."
        ),
        "color": 0xff9eb5,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/e9/Muja_Kina_%28current%29.png/revision/latest?cb=20240503001806",
    },
    "mida rana": {
        "name": "Mida Rana",
        "alias": "Rival 7 — The Teacher",
        "category": "Rival",
        "role": "Substitute Teacher",
        "personality": "Seductive, manipulative, cunning, shameless, calculated",
        "description": (
            "The seventh rival. A substitute teacher who deliberately uses her charm and "
            "authority to get close to Senpai. She is fully aware of exactly what she is "
            "doing and shows absolutely no remorse."
        ),
        "color": RED,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/e2/Mida_Rana_%28current%29.png/revision/latest?cb=20240503001815",
    },
    "osoro shidesu": {
        "name": "Osoro Shidesu",
        "alias": "Rival 8 — The Delinquent",
        "category": "Rival",
        "role": "Student / Delinquent Leader",
        "personality": "Aggressive, fiercely loyal, feared, secretly soft-hearted",
        "description": (
            "The eighth rival and leader of the school's delinquent gang. Feared by nearly "
            "every student at Akademi, she rules the back of the school through intimidation. "
            "Yet Senpai somehow reached the gentle side she keeps hidden from everyone else."
        ),
        "color": 0x333333,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/95/Osoro_Shidesu_%28Illustration%29.png/revision/latest?cb=20211015202510",
    },
    "hanako yamada": {
        "name": "Hanako Yamada",
        "alias": "Rival 9 — The Little Sister",
        "category": "Rival",
        "role": "Student — 1st Year / Senpai's Younger Sister",
        "personality": "Cheerful, clingy, innocent, overprotective of her brother",
        "description": (
            "The ninth rival and Senpai's adorable but fiercely attached younger sister. "
            "She becomes a rival not out of romantic intent but simply because her natural "
            "closeness to her brother is impossible to separate. She loves him unconditionally."
        ),
        "color": 0xff69b4,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/31/Hanako_Yamada_%28current%29.png/revision/latest?cb=20240503001838",
    },
    "megami saikou": {
        "name": "Megami Saikou",
        "alias": "Rival 10 — The Student Council President",
        "category": "Rival",
        "role": "Student / Student Council President",
        "personality": "Perfectionist, commanding, brilliant, deeply suspicious",
        "description": (
            "The tenth and final rival. Heir to the Saikou Corporation and the most capable "
            "person at Akademi by every measure. She has sensed for some time that something "
            "is dangerously wrong at the school — and she intends to find out what."
        ),
        "color": 0x4169e1,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/2/29/MegamiSaikou-Reputation.png/revision/latest?cb=20250112234053",
    },

    # ── AISHI FAMILY ─────────────────────────────────────────────────────────
    "ryoba aishi": {
        "name": "Ryoba Aishi",
        "alias": "Ayano's Mother / 1980s Yandere-chan",
        "category": "Aishi Family",
        "role": "Family Member (Mother) / 1980s Protagonist",
        "personality": "Obsessive, charming, ruthless, manipulative, possessive",
        "description": (
            "Ayano's mother and the protagonist of the 1980s mode. She eliminated ten rivals "
            "to claim the man she loved and raised Ayano with the same emotional void she "
            "herself carries. She passed the Yandere curse down through blood."
        ),
        "color": RED,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },
    "jokichi yudasei": {
        "name": "Jokichi Yudasei",
        "alias": "Ayano's Father",
        "category": "Aishi Family",
        "role": "Family Member (Father) / 1980s Senpai",
        "personality": "Traumatized, submissive, loving, broken, hollow",
        "description": (
            "Ayano's father and the Senpai of the 1980s story. He was the unwitting target of "
            "Ryoba's obsession and was 'won' by her after she eliminated every rival. Years of "
            "living beside her have left him deeply traumatized and entirely under her control."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/eb/Jokichi_Yudasei_%28current%29.png/revision/latest?cb=20250202044625",
    },
    "grandma aishi": {
        "name": "Grandma Aishi",
        "alias": "Ayano's Grandmother",
        "category": "Aishi Family",
        "role": "Family Member (Grandmother)",
        "personality": "Cold, mysterious, calculating, ancient malice",
        "description": (
            "Ayano's grandmother and the origin of the Aishi family's Yandere bloodline. "
            "Very little is known about her. She passed the emotional emptiness and obsessive "
            "nature through generations — a curse disguised as a gift."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },

    # ── STUDENT COUNCIL ───────────────────────────────────────────────────────
    "aoi ryugoku": {
        "name": "Aoi Ryugoku",
        "alias": "Student Council Vice President",
        "category": "Student Council",
        "role": "Student / Student Council Vice President",
        "personality": "Strict, disciplined, firm, intimidating, fair",
        "description": (
            "The vice president of the Student Council. She is no-nonsense and entirely "
            "dedicated to upholding order at Akademi. She will not be intimidated or swayed "
            "by anything short of absolute authority."
        ),
        "color": 0x4169e1,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/d/d8/Aoi_Ryugoku_%28Illustration%29.png/revision/latest?cb=20211123041524",
    },
    "kuroko kamenaga": {
        "name": "Kuroko Kamenaga",
        "alias": "Student Council Member",
        "category": "Student Council",
        "role": "Student / Student Council Member",
        "personality": "Sharp, observant, cold, vigilant",
        "description": (
            "A Student Council member with a keen eye for rule violations. She surveys "
            "the school with quiet intensity and misses very little. Getting past her "
            "requires either perfect behavior or perfect deception."
        ),
        "color": 0x4169e1,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/7/7e/Kuroko_Kamenaga_%28Illustration%29.png/revision/latest?cb=20211123041512",
    },
    "akane toriyasu": {
        "name": "Akane Toriyasu",
        "alias": "Student Council Member",
        "category": "Student Council",
        "role": "Student / Student Council Member",
        "personality": "Cheerful surface, strict underneath, deceptively firm",
        "description": (
            "A Student Council member who seems approachable at first glance. "
            "Her cheerful demeanor disappears the moment school rules are broken — "
            "she takes her duties every bit as seriously as her fellow council members."
        ),
        "color": 0x4169e1,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/c3/Akane_Toriyasu_%28Illustration%29.png/revision/latest?cb=20211123041536",
    },
    "shiromi torayoshi": {
        "name": "Shiromi Torayoshi",
        "alias": "Student Council Member",
        "category": "Student Council",
        "role": "Student / Student Council Member",
        "personality": "Unpredictable, cheerful, unsettling, playful, erratic",
        "description": (
            "The most unpredictable member of the Student Council. Her constant smile "
            "and erratic, almost playful behavior make her impossible to read. "
            "She is cheerful in a way that feels just slightly wrong."
        ),
        "color": 0x4169e1,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/0/0e/Shiromi_Torayoshi_%28Illustration%29.png/revision/latest?cb=20211123041449",
    },

    # ── STAFF ─────────────────────────────────────────────────────────────────
    "genka kunahito": {
        "name": "Genka Kunahito",
        "alias": "The School Counselor",
        "category": "Staff",
        "role": "Student Counselor",
        "personality": "Stern, strict, fair, perceptive, no-nonsense",
        "description": (
            "The school counselor at Akademi High. She handles student discipline with "
            "absolute seriousness. Students with declining sanity or suspicious behavior "
            "may find themselves called to her office — which is never a good sign."
        ),
        "color": 0x8b6914,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/4/4e/Genka_Kunahito_%28current%29.png/revision/latest?cb=20230403135416",
    },
    "kocho shuyona": {
        "name": "Kocho Shuyona",
        "alias": "The Headmaster",
        "category": "Staff",
        "role": "School Headmaster",
        "personality": "Authoritative, secretive, pragmatic, untouchable",
        "description": (
            "The headmaster of Akademi High. He runs the school with absolute authority "
            "and has deep, murky ties to the Saikou Corporation. His decisions about the "
            "school are final, and his past is carefully hidden."
        ),
        "color": 0x8b6914,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/6b/Kocho_Shuyona_202X_%28current%29.png/revision/latest?cb=20230403135417",
    },
    "kaho kanon": {
        "name": "Kaho Kanon",
        "alias": "The Librarian",
        "category": "Staff",
        "role": "School Librarian",
        "personality": "Quiet, bookish, reserved, gentle",
        "description": (
            "The school librarian. She keeps the library in perfect order and prefers "
            "the company of books to people. She is rarely involved in the chaos of "
            "Akademi's student life — by choice."
        ),
        "color": 0x8b6914,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/4/41/Kaho_Kanokogi_%28current%29.png/revision/latest?cb=20250127204841",
    },

    # ── NOTABLE STUDENTS ──────────────────────────────────────────────────────
    "info-chan": {
        "name": "Info-chan",
        "alias": "The Info Broker",
        "category": "Notable Students",
        "role": "Student / Underground Information Broker",
        "personality": "Cunning, amoral, secretive, calculating, unknown motives",
        "description": (
            "A mysterious student who operates a secret information brokering service from "
            "the photography club room. She provides Ayano with intelligence, favors, and "
            "tools — for a price. Her true identity and endgame remain completely unknown."
        ),
        "color": RED,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/a/a4/Info-chan_%28current%29.png/revision/latest?cb=20230403135417",
    },
    "raibaru fumetsu": {
        "name": "Raibaru Fumetsu",
        "alias": "Osana's Bodyguard",
        "category": "Notable Students",
        "role": "Student — 3rd Year / Osana's Best Friend & Bodyguard",
        "personality": "Fiercely loyal, physically imposing, warm to allies",
        "description": (
            "Osana's inseparable best friend and unofficial bodyguard. A former martial arts "
            "champion of Japan who retired from competition to simply be Osana's friend. "
            "She is virtually impossible to eliminate directly — she must be separated first."
        ),
        "color": 0xe74c3c,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/d/d1/Raibaru_Fumetsu_%28Illustration%29.png/revision/latest?cb=20250629120236",
    },
    "kokona haruka": {
        "name": "Kokona Haruka",
        "alias": "Original Test Rival",
        "category": "Notable Students",
        "role": "Student — 2nd Year / Drama Club Member",
        "personality": "Sweet, resilient, troubled, dignified",
        "description": (
            "A drama club member who served as the original test rival before Osana was "
            "fully implemented. She carries a quiet sadness — her home life involves debt "
            "and hardship — but she holds herself with remarkable dignity despite it all."
        ),
        "color": PINK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/d/d9/Kokona_Haruka_%28Illustration%29.png/revision/latest?cb=20250518035436",
    },
    "saki miyu": {
        "name": "Saki Miyu",
        "alias": "Kokona's Best Friend",
        "category": "Notable Students",
        "role": "Student — 2nd Year",
        "personality": "Friendly, gossipy, loyal, cheerful",
        "description": (
            "Kokona's best friend and a fellow drama club member. She is sociable, a bit "
            "of a gossip, and genuinely devoted to Kokona. You'll often find the two of "
            "them chatting near the rooftop."
        ),
        "color": PINK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/0/0f/Saki_Miyu_%28Illustration%29.png/revision/latest?cb=20250909083144",
    },
    "musume ronshaku": {
        "name": "Musume Ronshaku",
        "alias": "The Bully Leader",
        "category": "Notable Students",
        "role": "Student — 2nd Year / Bully Leader",
        "personality": "Mean-spirited, entitled, cruel, cowardly when alone",
        "description": (
            "The leader of the school's bullying clique. She is the daughter of a loan shark "
            "who holds debt over Kokona's family, giving her a twisted sense of power. "
            "She is confident in a crowd and spineless without one."
        ),
        "color": 0xc0392b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/f/f6/Daughter-full.png/revision/latest?cb=20220309161645",
    },

    # ── BULLYING CLIQUE ───────────────────────────────────────────────────────
    "hana daidaiyama": {
        "name": "Hana Daidaiyama",
        "alias": "Bully — Musume's Clique",
        "category": "Bullying Clique",
        "role": "Student — 2nd Year / Bully",
        "personality": "Cruel, follower, easily emboldened by numbers",
        "description": (
            "A member of Musume's bullying clique. She draws confidence from the group "
            "around her and uses that safety in numbers to target students she would "
            "never dare approach alone."
        ),
        "color": 0xc0392b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/8/86/Flower-full.png/revision/latest?cb=20220309161647",
    },
    "kashiko murasaki": {
        "name": "Kashiko Murasaki",
        "alias": "Bully — Musume's Clique",
        "category": "Bullying Clique",
        "role": "Student — 2nd Year / Bully",
        "personality": "Snide, calculating, gossip-driven",
        "description": (
            "A member of Musume's clique who specializes in spreading rumors and "
            "whisper campaigns. She prefers psychological cruelty to direct confrontation "
            "and considers herself the most clever of the group."
        ),
        "color": 0xc0392b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/94/Kashiko_Murasaki_%28Illustration%29.png/revision/latest?cb=20220309161648",
    },
    "kokoro momoiro": {
        "name": "Kokoro Momoiro",
        "alias": "Bully — Musume's Clique",
        "category": "Bullying Clique",
        "role": "Student — 2nd Year / Bully",
        "personality": "Shallow, status-obsessed, vain",
        "description": (
            "A member of Musume's clique who is entirely focused on social status "
            "and appearances. She is loyal to Musume primarily because standing beside "
            "her keeps her at the top of the social ladder."
        ),
        "color": 0xc0392b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/3e/Heart-full.png/revision/latest?cb=20220309161639",
    },
    "hoshiko mizudori": {
        "name": "Hoshiko Mizudori",
        "alias": "Bully — Musume's Clique",
        "category": "Bullying Clique",
        "role": "Student — 2nd Year / Bully",
        "personality": "Passive-aggressive, envious, opportunistic",
        "description": (
            "A member of Musume's clique who resents others' happiness and channels "
            "that envy into targeted cruelty. She rarely leads the charge but is always "
            "willing to pile on when someone else starts it."
        ),
        "color": 0xc0392b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/30/Star-full.png/revision/latest?cb=20220309161647",
    },

    # ── DELINQUENTS ───────────────────────────────────────────────────────────
    "umeji kizuguchi": {
        "name": "Umeji Kizuguchi",
        "alias": "Delinquent",
        "category": "Delinquents",
        "role": "Student / Delinquent",
        "personality": "Aggressive, territorial, loyal, hostile to outsiders",
        "description": (
            "One of the male delinquents who rules the back of the school. He is fiercely "
            "loyal to Osoro Shidesu and will aggressively confront anyone who enters "
            "their territory uninvited."
        ),
        "color": 0x333333,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/1/1a/Umeji_Kizuguchi_%28Illustration%29.png/revision/latest?cb=20220414173924",
    },
    "hokuto furugashi": {
        "name": "Hokuto Furugashi",
        "alias": "Delinquent",
        "category": "Delinquents",
        "role": "Student / Delinquent",
        "personality": "Reckless, defiant, street-smart",
        "description": (
            "A delinquent who lingers behind the school with the rest of Osoro's crew. "
            "He has little regard for school rules or authority figures and trusts "
            "almost no one outside the group."
        ),
        "color": 0x333333,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/1/1a/Umeji_Kizuguchi_%28Illustration%29.png/revision/latest?cb=20220414173924",
    },
    "gaku hikitsuri": {
        "name": "Gaku Hikitsuri",
        "alias": "Delinquent",
        "category": "Delinquents",
        "role": "Student / Delinquent",
        "personality": "Menacing, intimidating, disdainful",
        "description": (
            "A delinquent who actively dislikes most students and makes no effort to "
            "hide it. He is part of Osoro's inner circle and takes his role as a "
            "territorial enforcer very seriously."
        ),
        "color": 0x333333,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/6f/Gaku_Hikitsuri_%28Illustration%29.png/revision/latest?cb=20220414173923",
    },
    "hairu ikiyoku": {
        "name": "Hairu Ikiyoku",
        "alias": "Delinquent",
        "category": "Delinquents",
        "role": "Student / Delinquent",
        "personality": "Energetic, rash, impulsive, confrontational",
        "description": (
            "The most impulsive of the delinquent group — he reacts first and thinks "
            "later. He is quick to start confrontations and slower to realize when "
            "he is outmatched."
        ),
        "color": 0x333333,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/6f/Gaku_Hikitsuri_%28Illustration%29.png/revision/latest?cb=20220414173923",
    },
    "dairoku surikizu": {
        "name": "Dairoku Surikizu",
        "alias": "Delinquent",
        "category": "Delinquents",
        "role": "Student / Delinquent",
        "personality": "Brooding, quiet, dangerous when provoked",
        "description": (
            "The quietest of the delinquent group. He rarely speaks but is considered "
            "one of the more physically dangerous members. His silence is not peace — "
            "it's patience."
        ),
        "color": 0x333333,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/32/Mouth-full.png/revision/latest?cb=20220414173924",
    },

    # ── 202X STUDENTS ─────────────────────────────────────────────────────────
    "budo masuta": {
        "name": "Budo Masuta",
        "alias": "Martial Arts Club President",
        "category": "202X Students",
        "role": "Student — 3rd Year / Martial Arts Club President",
        "personality": "Honorable, disciplined, protective, principled",
        "description": (
            "President of the Martial Arts Club and one of the strongest students at "
            "Akademi. He has a deep sense of honor and takes it upon himself to protect "
            "others. He is one of the few students who can physically overpower Ayano."
        ),
        "color": 0x2e8b57,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/5d/Budo_Masuta_%28Illustration%29.png/revision/latest?cb=20181225191832",
    },
    "sho kunin": {
        "name": "Sho Kunin",
        "alias": "Martial Arts Club Member",
        "category": "202X Students",
        "role": "Student / Martial Arts Club",
        "personality": "Focused, eager, loyal to Budo",
        "description": (
            "A dedicated member of the Martial Arts Club who trains hard under Budo's "
            "leadership. He is serious about improvement and has a strong sense of "
            "camaraderie with his fellow club members."
        ),
        "color": 0x2e8b57,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/50/Shokunninnnnnnn.png/revision/latest?cb=20250508070106",
    },
    "juku ren": {
        "name": "Juku Ren",
        "alias": "Martial Arts Club Member",
        "category": "202X Students",
        "role": "Student / Martial Arts Club",
        "personality": "Traditional, disciplined, reserved",
        "description": (
            "A Martial Arts Club member who follows the old traditions of the discipline. "
            "He is reserved and rarely speaks unless necessary — every word he says "
            "is intentional."
        ),
        "color": 0x2e8b57,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/6b/Jukutiny.png/revision/latest?cb=20250508070023",
    },
    "mina rai": {
        "name": "Mina Rai",
        "alias": "Martial Arts Club Member",
        "category": "202X Students",
        "role": "Student / Martial Arts Club",
        "personality": "Energetic, competitive, driven",
        "description": (
            "A fiercely competitive member of the Martial Arts Club. She pushes herself "
            "and everyone around her to improve, and she doesn't believe in half-measures. "
            "She trains harder than almost anyone else in the club."
        ),
        "color": 0x2e8b57,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/5d/Budo_Masuta_%28Illustration%29.png/revision/latest?cb=20181225191832",
    },
    "shima shita": {
        "name": "Shima Shita",
        "alias": "Martial Arts Club Member",
        "category": "202X Students",
        "role": "Student / Martial Arts Club",
        "personality": "Calm, methodical, analytical",
        "description": (
            "A Martial Arts Club member known for his calm, methodical fighting style. "
            "He reads opponents before reacting and prefers control over aggression. "
            "He is the quietest member of the club."
        ),
        "color": 0x2e8b57,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/c0/Shimatiny.png/revision/latest?cb=20250508070230",
    },
    "ryuto ippongo": {
        "name": "Ryuto Ippongo",
        "alias": "Gaming Club President",
        "category": "202X Students",
        "role": "Student / Gaming Club President",
        "personality": "Enthusiastic, geeky, passionate, devoted to Midori",
        "description": (
            "President of the Gaming Club and Midori's devoted boyfriend. He is passionate "
            "about games to an almost obsessive degree and is happiest when surrounded by "
            "fellow enthusiasts in the club room."
        ),
        "color": 0x1e90ff,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/37/Ryutopose26.png/revision/latest?cb=20240502180029",
    },
    "midori gurin": {
        "name": "Midori Gurin",
        "alias": "The Emailer",
        "category": "202X Students",
        "role": "Student / Gaming Club Member",
        "personality": "Bubbly, curious, oblivious, relentlessly cheerful",
        "description": (
            "A Gaming Club member famous for constantly sending questions to anyone who "
            "will listen — including some very inconvenient people. She is endlessly "
            "upbeat and completely unaware of the chaos surrounding her."
        ),
        "color": 0x1e90ff,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/4/4e/Midori_Gurin_%28Illustration%29.png/revision/latest?cb=20220325225018",
    },
    "gema taku": {
        "name": "Gema Taku",
        "alias": "Gaming Club Member",
        "category": "202X Students",
        "role": "Student / Gaming Club Member",
        "personality": "Passionate, opinionated, defensive about gaming",
        "description": (
            "A Gaming Club member who lives and breathes video games. He has strong "
            "opinions about every genre and is not shy about sharing them at length. "
            "He is loyal to his club and his friends within it."
        ),
        "color": 0x1e90ff,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/b/b0/Gema_Taku_%28Illustration%29.png/revision/latest?cb=20211018180508",
    },
    "pippi osu": {
        "name": "Pippi Osu",
        "alias": "Gaming Club Member",
        "category": "202X Students",
        "role": "Student / Gaming Club Member",
        "personality": "Cheerful, energetic, rhythm-obsessed",
        "description": (
            "A Gaming Club member with a particular love for rhythm games. She is "
            "cheerful, social, and known for her remarkable reaction time — a skill "
            "she has transferred from the screen to real life."
        ),
        "color": 0x1e90ff,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/4/4e/Midori_Gurin_%28Illustration%29.png/revision/latest?cb=20220325225018",
    },
    "shin higaku": {
        "name": "Shin Higaku",
        "alias": "Photography Club President",
        "category": "202X Students",
        "role": "Student / Photography Club President",
        "personality": "Observant, quiet, introspective, artistic",
        "description": (
            "President of the Photography Club. He spends his time watching and capturing "
            "the world through a lens rather than participating in it. He notices things "
            "others miss — which makes him someone worth being careful around."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/54/Shinpose25_1.png/revision/latest?cb=20210218180114",
    },
    "yui rio": {
        "name": "Yui Rio",
        "alias": "Art Club President",
        "category": "202X Students",
        "role": "Student / Art Club President",
        "personality": "Creative, peaceful, expressive, sensitive",
        "description": (
            "President of the Art Club. She is gentle and expressive, pouring her "
            "emotions into her paintings. She sees beauty in unexpected places and "
            "approaches the world with a quiet, artistic patience."
        ),
        "color": 0xda70d6,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/0/08/YuiR.png/revision/latest?cb=20160418121048",
    },
    "kuu dere": {
        "name": "Kuu Dere",
        "alias": "Science Club President",
        "category": "202X Students",
        "role": "Student / Science Club President",
        "personality": "Cold, analytical, detached, highly intelligent",
        "description": (
            "President of the Science Club. She approaches everything with clinical "
            "detachment and has little patience for emotion or irrationality. "
            "She is brilliant, precise, and deeply uninterested in social games."
        ),
        "color": 0x00ced1,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/1/1e/Kuureaction.png/revision/latest?cb=20151002101242",
    },
    "mai waifu": {
        "name": "Mai Waifu",
        "alias": "Light Music Club President",
        "category": "202X Students",
        "role": "Student / Light Music Club President",
        "personality": "Cheerful, musical, sociable, warm",
        "description": (
            "President of the Light Music Club. She fills the music room with sound "
            "and the hallways with warmth. She genuinely loves music and the community "
            "her club has built around it."
        ),
        "color": 0xff69b4,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/38/Mai_Waifu_%28Illustration%29.png/revision/latest?cb=20250828194829",
    },
    "supana churu": {
        "name": "Supana Churu",
        "alias": "Occult Club Member",
        "category": "202X Students",
        "role": "Student / Occult Club Member",
        "personality": "Dramatic, enthusiastic, theatrical about the supernatural",
        "description": (
            "A member of the Occult Club who throws herself into every ritual and "
            "investigation with dramatic flair. She believes deeply in everything the "
            "club studies — perhaps more than is healthy."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/a/af/SupanaChuru-Reputation.png/revision/latest?cb=20250112224743",
    },
    "yaku zaishi": {
        "name": "Yaku Zaishi",
        "alias": "Occult Club Member",
        "category": "202X Students",
        "role": "Student / Occult Club Member",
        "personality": "Intense, devout, brooding, secretive",
        "description": (
            "A deeply serious member of the Occult Club who treats every ritual as "
            "sacred. He speaks little about himself but has extensive knowledge of "
            "supernatural lore that unsettles even other club members."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/94/Yaku_Zaishi_%28Illustration%29.png/revision/latest?cb=20250826140314",
    },
    "toga tabara": {
        "name": "Toga Tabara",
        "alias": "Sports Club — Track",
        "category": "202X Students",
        "role": "Student / Sports Club — Track",
        "personality": "Driven, disciplined, quietly competitive",
        "description": (
            "A dedicated track athlete and Sports Club member. He is self-motivated, "
            "trains relentlessly, and carries a quiet competitive fire that he rarely "
            "displays openly."
        ),
        "color": 0xff8c00,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/7/79/Toga_Tabara_%28current%29.png/revision/latest?cb=20230401231347",
    },
    "sakyu basu": {
        "name": "Sakyu Basu",
        "alias": "The Succubus Sister (Elder)",
        "category": "202X Students",
        "role": "Student / Succubus",
        "personality": "Seductive, mysterious, eerily composed",
        "description": (
            "One of two sisters rumored to be actual succubi. Sakyu carries herself "
            "with unsettling poise and has a magnetic effect on those around her. "
            "Whether she is truly supernatural or simply extraordinary is left unclear."
        ),
        "color": 0x8b008b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/b/b4/Sakyu_Basu_%28current%29.png/revision/latest?cb=20260301140911",
    },
    "inkyu basu": {
        "name": "Inkyu Basu",
        "alias": "The Succubus Sister (Younger)",
        "category": "202X Students",
        "role": "Student / Succubus",
        "personality": "Flirtatious, playful, charming, capricious",
        "description": (
            "The younger of the two Basu sisters and equally rumored to be a succubus. "
            "She is more openly playful than her sister and enjoys the effect she has "
            "on people — perhaps too much."
        ),
        "color": 0x8b008b,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/4/4a/Inkyu_Basu_%28Illustration%29.png/revision/latest?cb=20241105235144",
    },

    # ── 1980S CHARACTERS ──────────────────────────────────────────────────────
    "the journalist": {
        "name": "The Journalist",
        "alias": "The Reporter",
        "category": "1980s Mode",
        "role": "Journalist / Narrator",
        "personality": "Determined, suspicious, brave, haunted",
        "description": (
            "A journalist who spent years trying to prove Ryoba Aishi was a murderer. "
            "He is the narrator of Ayano's present-day story — a man who knows the truth "
            "of what the Aishi women are, and has been running from it ever since."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/e9/The_Journalist_%28current%29.png/revision/latest?cb=20220213221846",
    },
    "chojo tekina": {
        "name": "Chojo Tekina",
        "alias": "1980s Student",
        "category": "1980s Mode",
        "role": "Student / 1980s School",
        "personality": "Mysterious, intuitive, perceptive",
        "description": (
            "A mysterious and perceptive student from the 1980s timeline. She seemed to "
            "sense something wrong long before anyone else. In a school full of oblivious "
            "students, that kind of awareness came with its own kind of danger."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/1/18/Chojo_Tekina_%28current%29.png/revision/latest?cb=20250601100834",
    },

    # ── 1980S RIVALS (THE TEN) ────────────────────────────────────────────────
    "riku soma": {
        "name": "Riku Soma",
        "alias": "1980s Rival 1",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Cheerful, popular, openly affectionate",
        "description": (
            "The first rival Ryoba faced. A cheerful and openly affectionate student "
            "who made no secret of her feelings for Senpai. Being forthright and lovable "
            "was not enough to keep her safe from Ryoba's reach."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/2/29/Rikutiny.png/revision/latest?cb=20250508063738",
    },
    "sumire saitozaki": {
        "name": "Sumire Saitozaki",
        "alias": "1980s Rival 2",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Gentle, kind, quietly devoted",
        "description": (
            "The second rival Ryoba faced. A gentle and quietly devoted student who "
            "expressed her feelings for Senpai with sincere warmth. She became an "
            "obstacle the moment Ryoba noticed she existed."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/cd/Sumire_Saitozaki_%28current%29.png/revision/latest?cb=20250518080309",
    },
    "kaguya wakaizumi": {
        "name": "Kaguya Wakaizumi",
        "alias": "1980s Rival 3",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Elegant, composed, admired",
        "description": (
            "The third rival Ryoba faced. An elegant and widely admired student whose "
            "natural grace drew Senpai's attention without effort. Ryoba made sure "
            "that attention would not last."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/8/86/Kaguya_Wakaizumi_%28Illustration%29.png/revision/latest?cb=20211111144900",
    },
    "moeko rakuyona": {
        "name": "Moeko Rakuyona",
        "alias": "1980s Rival 4",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Sweet, earnest, endearingly clumsy",
        "description": (
            "The fourth rival Ryoba faced. A sweet and earnest student whose endearing "
            "clumsiness somehow made her more endearing to Senpai. "
            "Ryoba had no patience for endearing."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/9f/Moeko_Rakuyona_%28Illustration%29.png/revision/latest?cb=20211111145030",
    },
    "honami hodoshima": {
        "name": "Honami Hodoshima",
        "alias": "1980s Rival 5",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Passionate, expressive, warm-hearted",
        "description": (
            "The fifth rival Ryoba faced. A passionate and expressive student who wore "
            "her heart on her sleeve and never hid how she felt about Senpai. "
            "That openness made her an easy target."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/3/30/Honami_Hodoshima_%28Illustration%29.png/revision/latest?cb=20211111145226",
    },
    "sumiko tachibana": {
        "name": "Sumiko Tachibana",
        "alias": "1980s Rival 6",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Reserved, thoughtful, quietly determined",
        "description": (
            "The sixth rival Ryoba faced. A reserved and thoughtful student who expressed "
            "her feelings carefully and only after much consideration. "
            "Careful didn't mean safe."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/8/8d/Sumiko_Tachibana_%28Illustration%29.png/revision/latest?cb=20211111145337",
    },
    "ritsuko chikanari": {
        "name": "Ritsuko Chikanari",
        "alias": "1980s Rival 7",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Bright, sociable, optimistic",
        "description": (
            "The seventh rival Ryoba faced. Bright and optimistic, she made friends "
            "easily and brought warmth into every room she entered. "
            "Ryoba made sure she stopped entering rooms."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/9b/Ritsuko_Chikanari_%28Illustration%29.png/revision/latest?cb=20211111144007",
    },
    "ai doruyashi": {
        "name": "Ai Doruyashi",
        "alias": "1980s Rival 8",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Idealistic, caring, deeply empathetic",
        "description": (
            "The eighth rival Ryoba faced. An idealistic and deeply empathetic student "
            "who genuinely cared about everyone around her — including a Senpai who "
            "didn't realize he was already taken."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/96/Ai_Doruyashi_%28Illustration%29.png/revision/latest?cb=20211111145515",
    },
    "teiko nabatasai": {
        "name": "Teiko Nabatasai",
        "alias": "1980s Rival 9",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Determined, focused, quietly confident",
        "description": (
            "The ninth rival Ryoba faced. Determined and quietly confident, she pursued "
            "what she wanted with steady resolve. Standing in Ryoba's way with resolve "
            "was not enough."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/b/be/Teiko_Nabatasai_%28Illustration%29.png/revision/latest?cb=20211111145719",
    },
    "komako funakoshi": {
        "name": "Komako Funakoshi",
        "alias": "1980s Rival 10",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Radiant, warm, fiercely cherished",
        "description": (
            "The tenth and final rival Ryoba faced. Eliminating her meant the end of "
            "Ryoba's ten-week hunt — and the beginning of Jokichi's lifetime of captivity. "
            "She was the last one standing, and she didn't stand for long."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/a/a0/Komako_Funakoshi_%28Illustration%29.png/revision/latest?cb=20211111145822",
    },
    "chigusa busujima": {
        "name": "Chigusa Busujima",
        "alias": "1980s Rival",
        "category": "1980s Rivals",
        "role": "Student / 1980s Rival",
        "personality": "Mysterious, perceptive, quietly intense",
        "description": (
            "A rival from the 1980s timeline with a quiet intensity that set her apart. "
            "She didn't need to announce her presence — people simply noticed her. "
            "Ryoba noticed her too, and that was that."
        ),
        "color": 0x708090,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/2/28/Chigusa_Busujima_%28Illustration%29.png/revision/latest?cb=20211120154532",
    },
}

CATEGORY_COLORS = {
    "Protagonist":       RED,
    "Senpai":            PINK,
    "Rival":             0xff6347,
    "Aishi Family":      DARK,
    "Student Council":   0x4169e1,
    "Staff":             0x8b6914,
    "Notable Students":  PINK,
    "Bullying Clique":   0xc0392b,
    "Delinquents":       0x333333,
    "202X Students":     0x2e8b57,
    "1980s Mode":        0x708090,
    "1980s Rivals":      0x708090,
}

ALL_NAMES = sorted(CHARACTERS.keys())


class Characters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        current_lower = current.lower()
        matches = [
            app_commands.Choice(name=CHARACTERS[k]["name"], value=k)
            for k in ALL_NAMES
            if current_lower in k or current_lower in CHARACTERS[k]["name"].lower()
               or current_lower in CHARACTERS[k].get("alias", "").lower()
        ]
        return matches[:25]

    @app_commands.command(
        name="character",
        description="Look up a Yandere Simulator character. 👁️"
    )
    @app_commands.describe(name="Character name — start typing to search")
    @app_commands.autocomplete(name=name_autocomplete)
    async def character(self, interaction: discord.Interaction, name: str):
        key = name.lower().strip()
        char = CHARACTERS.get(key)

        if not char:
            close = [
                CHARACTERS[k]["name"] for k in ALL_NAMES
                if key in k or key in CHARACTERS[k]["name"].lower()
            ]
            if close:
                suggestion = "\n".join(f"• {n}" for n in close[:5])
                await interaction.response.send_message(
                    f"👁️ *I don't recognize that name. Did you mean:*\n{suggestion}",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "🔪 *That name isn't in my files. Try the autocomplete to search.*",
                    ephemeral=True
                )
            return

        embed = discord.Embed(
            title=f"👁️ {char['name']}",
            description=char["description"],
            color=char.get("color", PINK),
        )
        embed.add_field(name="📋 Also Known As", value=char.get("alias", "—"), inline=False)
        embed.add_field(name="🎭 Category",       value=char["category"],         inline=True)
        embed.add_field(name="📌 Role",           value=char["role"],             inline=True)
        embed.add_field(name="🌸 Personality",    value=char["personality"],      inline=False)
        embed.set_thumbnail(url=char["image"])
        embed.set_footer(text="Yandere Simulator Character Files 🩸 | Data never lies.")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Characters(bot))
