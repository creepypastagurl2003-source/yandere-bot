import discord
from discord.ext import commands
from discord import app_commands
from typing import List

PINK  = 0xffb6c1
RED   = 0x8b0000
DARK  = 0x1a0010
SLATE = 0x708090

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

    # ── AISHI FAMILY ──────────────────────────────────────────────────────────
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
    "dozuki aishi": {
        "name": "Dozuki Aishi",
        "alias": "Ayano's Grandmother (Maternal)",
        "category": "Aishi Family",
        "role": "Family Member (Grandmother)",
        "personality": "Cold, calculating, deeply unsettling, matriarchal",
        "description": (
            "One of Ayano's grandmothers and a carrier of the Aishi family curse. "
            "The emotional void and obsessive nature that defines the Aishi bloodline "
            "runs through her. Very little else is known about her."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },
    "kataba aishi": {
        "name": "Kataba Aishi",
        "alias": "Ayano's Great-Grandmother",
        "category": "Aishi Family",
        "role": "Family Member (Great-Grandmother)",
        "personality": "Mysterious, distant, haunting",
        "description": (
            "Ayano's great-grandmother and one of the earliest known carriers of the Aishi "
            "bloodline curse. She shares the same emotional void and obsessive nature that "
            "has been passed down through every generation since."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },
    "torahiko aishi": {
        "name": "Torahiko Aishi",
        "alias": "Ayano's Great-Grandfather",
        "category": "Aishi Family",
        "role": "Family Member (Great-Grandfather)",
        "personality": "Unknown — bound to the Aishi bloodline",
        "description": (
            "Ayano's great-grandfather and Kataba's counterpart. He is part of the oldest "
            "known generation of the Aishi family tree, shrouded in the same mystery "
            "that surrounds the entire lineage."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/eb/Jokichi_Yudasei_%28current%29.png/revision/latest?cb=20250202044625",
    },
    "sueribu aishi": {
        "name": "Sueribu Aishi",
        "alias": "Ayano's Grandfather",
        "category": "Aishi Family",
        "role": "Family Member (Grandfather)",
        "personality": "Unknown — an Aishi through and through",
        "description": (
            "Ayano's grandfather and the link between the great-grandparents' generation "
            "and Ryoba's. He carries the Aishi name and all the weight that comes with it."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/eb/Jokichi_Yudasei_%28current%29.png/revision/latest?cb=20250202044625",
    },
    "azebiki aishi": {
        "name": "Azebiki Aishi",
        "alias": "Aishi Ancestor",
        "category": "Aishi Family",
        "role": "Ancestor",
        "personality": "Unknown — lost to time",
        "description": (
            "An ancestor of the Aishi bloodline. One of the many who came before Ayano, "
            "each passing down the same emotional void and obsessive devotion that defines "
            "every woman in this cursed lineage."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },
    "kugi aishi": {
        "name": "Kugi Aishi",
        "alias": "Aishi Ancestor",
        "category": "Aishi Family",
        "role": "Ancestor",
        "personality": "Unknown — lost to time",
        "description": (
            "An ancestor of the Aishi bloodline. One of the many who came before Ayano, "
            "each passing down the same emotional void and obsessive devotion that defines "
            "every woman in this cursed lineage."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },
    "hiki aishi": {
        "name": "Hiki Aishi",
        "alias": "Aishi Ancestor",
        "category": "Aishi Family",
        "role": "Ancestor",
        "personality": "Unknown — lost to time",
        "description": (
            "An ancestor of the Aishi bloodline. One of the many who came before Ayano, "
            "each passing down the same emotional void and obsessive devotion that defines "
            "every woman in this cursed lineage."
        ),
        "color": DARK,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/6/65/Ryoba_Aishi_%28current%29.png/revision/latest?cb=20220330160121",
    },
    "jokichi yudasei": {
        "name": "Jokichi Yudasei",
        "alias": "Ayano's Father / 1980s Senpai",
        "category": "Aishi Family",
        "role": "Family Member (Father) / 1980s Senpai",
        "personality": "Traumatized, submissive, loving, broken, hollow",
        "description": (
            "Ayano's father and the Senpai of the 1980s story. He was the unwitting target of "
            "Ryoba's obsession and was 'won' by her after she eliminated every rival. Years of "
            "living beside her have left him deeply traumatized and entirely under her control."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/eb/Jokichi_Yudasei_%28current%29.png/revision/latest?cb=20250202044625",
    },

    # ── RIVALS (202X) ─────────────────────────────────────────────────────────
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
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/ce/Oshizu.png/revision/latest",
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

    # ── 1980s RIVALS ──────────────────────────────────────────────────────────
    "sumire saitozaki": {
        "name": "Sumire Saitozaki",
        "alias": "Tutorial Rival — Week 0",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Cheerful, bubbly, sincere",
        "description": (
            "The tutorial rival of the 1980s storyline. Ryoba's first obstacle and the "
            "girl who unknowingly set everything in motion. Warm and sincere in her feelings "
            "for Jokichi — eliminated before she ever got a real chance."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/7/7d/Sumire_Saitozaki_%28Illustration%29.png/revision/latest",
    },
    "kaguya wakaizumi": {
        "name": "Kaguya Wakaizumi",
        "alias": "1980s Rival 1 — Week 1",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Elegant, composed, quietly devoted",
        "description": (
            "The first rival in the 1980s storyline. Elegant and reserved, she admired "
            "Jokichi from a distance — a distance Ryoba made permanent."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/57/Kaguya_Wakaizumi_%28Illustration%29.png/revision/latest",
    },
    "moeko rakuyona": {
        "name": "Moeko Rakuyona",
        "alias": "1980s Rival 2 — Week 2",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Playful, energetic, bold",
        "description": (
            "The second rival in the 1980s storyline. Bold and full of energy, she pursued "
            "Jokichi openly — which made her an early target."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/5e/Moeko_Rakuyona_%28Illustration%29.png/revision/latest",
    },
    "honami hodoshima": {
        "name": "Honami Hodoshima",
        "alias": "1980s Rival 3 — Week 3",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Sweet, artistic, gentle",
        "description": (
            "The third rival in the 1980s storyline. An artistic and gentle soul whose "
            "feelings for Jokichi were quietly genuine — and quietly ended."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/0/0e/Honami_Hodoshima_%28Illustration%29.png/revision/latest",
    },
    "sumiko tachibana": {
        "name": "Sumiko Tachibana",
        "alias": "1980s Rival 4 — Week 4",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Studious, serious, quietly warm",
        "description": (
            "The fourth rival in the 1980s storyline. Serious and studious, she kept her "
            "feelings close — not close enough to survive Ryoba's notice."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/53/Sumiko_Tachibana_%28Illustration%29.png/revision/latest",
    },
    "ritsuko chikanari": {
        "name": "Ritsuko Chikanari",
        "alias": "1980s Rival 5 — Week 5",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Lively, social, outgoing",
        "description": (
            "The fifth rival in the 1980s storyline. Popular and outgoing, her social "
            "connection to Jokichi drew Ryoba's attention immediately."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/a/a8/Ritsuko_Chikanari_%28Illustration%29.png/revision/latest",
    },
    "ai doruyashi": {
        "name": "Ai Doruyashi",
        "alias": "1980s Rival 6 — Week 6",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Shy, sensitive, deeply sincere",
        "description": (
            "The sixth rival in the 1980s storyline. Shy and deeply sincere, she was "
            "perhaps the most innocent of all the rivals. It did not protect her."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/b/b9/Ai_Doruyashi_%28Illustration%29.png/revision/latest",
    },
    "teiko nabatasai": {
        "name": "Teiko Nabatasai",
        "alias": "1980s Rival 7 — Week 7",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Confident, direct, fiercely competitive",
        "description": (
            "The seventh rival in the 1980s storyline. Confident and direct in everything she "
            "did — including pursuing Jokichi. Ryoba found her the most infuriating to deal with."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/e8/Teiko_Nabatasai_%28Illustration%29.png/revision/latest",
    },
    "komako funakoshi": {
        "name": "Komako Funakoshi",
        "alias": "1980s Rival 8 — Week 8",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Calm, composed, quietly determined",
        "description": (
            "The eighth rival in the 1980s storyline. Calm and composed, she was "
            "a formidable obstacle between Ryoba and her Senpai."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/9/98/Komako_Funakoshi_%28Illustration%29.png/revision/latest",
    },
    "chigusa busujima": {
        "name": "Chigusa Busujima",
        "alias": "1980s Rival 9 — Week 9",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Unknown — eliminated before her story could be told",
        "description": (
            "The ninth rival in the 1980s storyline. She developed feelings for Jokichi "
            "and was removed from the picture before anything more could unfold."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/c/c7/Chigusa_Busujima_%28Illustration%29.png/revision/latest",
    },
    "sonoko sakanoue": {
        "name": "Sonoko Sakanoue",
        "alias": "1980s Rival 10 — Week 10",
        "category": "1980s Rivals",
        "role": "Student — 1980s Mode",
        "personality": "Gentle, kind, unknowingly magnetic",
        "description": (
            "The tenth and final rival in the 1980s storyline. The last girl standing "
            "between Ryoba and her Senpai — and the last to fall."
        ),
        "color": SLATE,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/5/55/Sonoko_Sakanoue_%28Illustration%29.png/revision/latest",
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

    # ── NOTABLE STUDENTS ──────────────────────────────────────────────────────
    "info-chan": {
        "name": "Info-chan",
        "alias": "The Info Broker",
        "category": "Students",
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
        "category": "Students",
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
        "category": "Students",
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
        "category": "Students",
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
        "category": "Students",
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
    "budo masuta": {
        "name": "Budo Masuta",
        "alias": "Martial Arts Club President",
        "category": "Students",
        "role": "Student — 2nd Year / Martial Arts Club President",
        "personality": "Honorable, disciplined, earnest, straightforward",
        "description": (
            "The president of the Martial Arts Club and one of the most physically capable "
            "students at Akademi. He is earnest to a fault, deeply principled, and one of "
            "the few students Ayano genuinely cannot manipulate easily."
        ),
        "color": 0xe74c3c,
        "image": "https://static.wikia.nocookie.net/yandere-simulator/images/e/e5/Budo_Masuta_%28Illustration%29.png/revision/latest?cb=20211015202508",
    },
}

CATEGORY_COLORS = {
    "Protagonist":    RED,
    "Senpai":         PINK,
    "Aishi Family":   RED,
    "Rival":          0xff6347,
    "1980s Rivals":   SLATE,
    "Student Council": 0x4169e1,
    "Students":       PINK,
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
