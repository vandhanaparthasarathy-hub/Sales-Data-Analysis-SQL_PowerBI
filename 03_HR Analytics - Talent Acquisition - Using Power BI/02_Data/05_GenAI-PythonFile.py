"""
=============================================================
  TechCorp SaaS — Talent Acquisition Dataset Generator
  Run in Google Colab or locally with Python 3.8+
  No external libraries needed — only built-in modules
=============================================================
"""

import csv, random, copy, math, os
from datetime import date, timedelta
from collections import defaultdict, Counter

random.seed(2025)

# ── OUTPUT FOLDER ─────────────────────────────────────────────────────────────
OUTPUT_DIR = "/content" if os.path.exists("/content") else "."
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Files will be saved to: {OUTPUT_DIR}")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — CANDIDATE POOL
# ═════════════════════════════════════════════════════════════════════════════
MALE_FIRST = [
    "James","Michael","David","Daniel","Matthew","Christopher","Andrew","Joshua","Ryan","Nathan",
    "Kevin","Brian","Justin","Eric","Jonathan","Raj","Arjun","Vikram","Rohan","Kiran",
    "Mohammed","Omar","Hassan","Tariq","Yusuf","Wei","Jian","Ming","Hao","Chen",
    "Carlos","Miguel","Diego","Luis","Alejandro","Kwame","Kofi","Chidi","Emeka","Tobias",
    "Luca","Marco","Giovanni","Felix","Stefan","Kenji","Hiroshi","Takeshi","Daiki","Samuel",
    "Benjamin","Alexander","William","Henry","Ethan","Logan","Mason","Aiden","Jackson","Tyler",
    "Noah","Liam","Oliver","Elijah","James","Oscar","Leo","Harry","George","Charlie",
    "Adrian","Marcus","Julian","Xavier","Isaac","Gabriel","Sebastian","Dominic","Victor","Theo",
    "Rahul","Sanjay","Aditya","Karan","Nikhil","Amit","Suresh","Deepak","Arun","Vivek",
    "Ibrahim","Khalid","Bilal","Zayd","Amir","Sami","Faisal","Karim","Rashid","Nasser",
    "Jie","Feng","Bo","Yong","Lei","Tao","Zhi","Jun","Peng","Xin",
    "Andres","Javier","Rodrigo","Fernando","Emilio","Pablo","Mateo","Sergio","Ricardo","Enrique",
    "Kwesi","Kojo","Sekou","Femi","Ade","Obi","Chike","Uche","Nnamdi","Ikenna",
    "Matteo","Enzo","Lorenzo","Adriano","Rocco","Dario","Massimo","Nico","Salvatore","Vito",
    "Ryo","Sho","Kaito","Yuto","Sota","Ren","Haruto","Riku","Yuki","Sora"
]
FEMALE_FIRST = [
    "Sarah","Emily","Jessica","Ashley","Amanda","Stephanie","Melissa","Nicole","Jennifer","Elizabeth",
    "Priya","Ananya","Divya","Shruti","Kavya","Fatima","Aisha","Zara","Nadia","Layla",
    "Wei","Ling","Mei","Xiu","Yan","Sofia","Isabella","Valentina","Camila","Lucia",
    "Amara","Ngozi","Adaeze","Chioma","Yetunde","Emma","Olivia","Ava","Mia","Charlotte",
    "Yuki","Sakura","Hana","Nami","Aoi","Anna","Maria","Elena","Katarina","Ingrid",
    "Zoe","Chloe","Grace","Hannah","Lily","Sophia","Natalie","Victoria","Claire","Amber",
    "Isla","Poppy","Freya","Willow","Luna","Aurora","Cleo","Nora","Sienna","Ada",
    "Rebecca","Samantha","Lauren","Megan","Rachel","Kayla","Alyssa","Brianna","Danielle","Michelle",
    "Neha","Pooja","Anjali","Meera","Ritu","Sunita","Deepika","Aarti","Isha","Radhika",
    "Yasmin","Sara","Noor","Hala","Rania","Salma","Dina","Mariam","Lubna","Amina",
    "Jing","Hui","Fang","Ting","Xue","Yun","Rui","Hong","Qing","Lan",
    "Gabriela","Daniela","Andrea","Paola","Carmen","Rosa","Alejandra","Ximena","Renata","Julieta",
    "Amaka","Adaeze","Chiamaka","Ifeoma","Nkechi","Folake","Titi","Bisi","Yewande","Aduke",
    "Giulia","Chiara","Francesca","Alessandra","Bianca","Serena","Federica","Ilaria","Martina","Silvia",
    "Mei","Rin","Yui","Airi","Mio","Kokoro","Rio","Koharu","Ichika","Yuina"
]
NB_FIRST = [
    "Alex","Jordan","Taylor","Morgan","Riley","Casey","Quinn","Avery","Reese","Skyler",
    "Drew","Sage","River","Phoenix","Rowan","Finley","Blair","Emery","Hayden","Lennon",
    "Charlie","Frankie","Remy","Devon","Ellis","Sawyer","Kai","Bellamy","Justice","Sutton",
    "Marlowe","Wren","Shiloh","August","Dakota","Peyton","Sloane","Micah","Salem","Story"
]
LAST_BY_ETH = {
    "White":     ["Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Wilson","Taylor",
                  "Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Walker","Hall","Allen","Young",
                  "King","Wright","Scott","Baker","Adams","Nelson","Carter","Mitchell","Roberts","Phillips"],
    "Asian":     ["Patel","Sharma","Singh","Kumar","Tanaka","Yamamoto","Nakamura","Kim","Park","Lee",
                  "Chen","Wang","Liu","Zhang","Nguyen","Tran","Le","Pham","Ho","Sato",
                  "Gupta","Reddy","Iyer","Choi","Yoon","Suzuki","Kobayashi","Watanabe","Huang","Xu"],
    "Black":     ["Okafor","Diallo","Mensah","Osei","Asante","Robinson","Washington","Jefferson","Coleman",
                  "Brooks","Griffin","Hayes","Foster","Reed","Banks","Jenkins","Perry","Patterson","Morgan","Okonkwo",
                  "Adeyemi","Balogun","Eze","Nwosu","Abubakar","Freeman","Boateng","Owusu","Appiah","Kamau"],
    "Hispanic":  ["Garcia","Rodriguez","Martinez","Lopez","Hernandez","Gonzalez","Perez","Sanchez",
                  "Ramirez","Torres","Flores","Rivera","Gomez","Diaz","Cruz","Reyes","Morales","Ortiz","Gutierrez","Chavez",
                  "Vargas","Castillo","Jimenez","Mendoza","Romero","Aguilar","Delgado","Guerrero","Medina","Vega"],
    "Mixed":     ["Andrews","Bailey","Campbell","Douglas","Edwards","Fleming","Graham","Hamilton",
                  "Irving","Jensen","Kennedy","Lambert","Murray","Nelson","Owen","Pierce","Russell","Sullivan","Turner","Whitmore",
                  "Ashford","Bennett","Copeland","Ellison","Grady","Holbrook","Lockhart","Prescott","Sinclair","Wallis"],
    "Other":     ["Ivanova","Petrov","Kowalski","Nowak","Müller","Schmidt","Rossi","Ferrari","Andersen",
                  "Larsen","Al-Amin","Fontaine","Dupont","Leclerc","Ito","Watanabe","Hashimoto","Kobayashi","Nakagawa","Bergstrom",
                  "Novak","Horvat","Dvorak","Berg","Lindqvist","Haas","Weber","Moreau","Girard","Karlsson"],
    "Prefer not to say": ["Taylor","Morgan","Riley","Jordan","Casey","Parker","Avery","Blake","Cameron","Finley",
                           "Reese","Sawyer","Sutton","Marlow","Ellis","Devon","Kai","Emerson","Rowan","Sage"],
}
ETHNICITIES = ["White","Asian","Black","Hispanic","Mixed","Other","Prefer not to say"]
ETH_W       = [0.35, 0.22, 0.13, 0.13, 0.08, 0.05, 0.04]
GENDERS     = ["Male","Female","Non-binary"]
GEN_W       = [0.50, 0.44, 0.06]

def wchoice(choices, weights):
    t = sum(weights); r = random.uniform(0, t); c = 0
    for x, w in zip(choices, weights):
        c += w
        if r <= c: return x
    return choices[-1]

LEVEL_AGE = {
    "Junior":   (22, 29),
    "Mid":      (26, 35),
    "Senior":   (30, 42),
    "Lead":     (34, 46),
    "Manager":  (36, 50),
    "Director": (40, 56),
}

def gen_dob(level):
    lo, hi = LEVEL_AGE[level]
    age    = random.randint(lo, hi)
    ref    = date(2023, 6, 15)
    return ref - timedelta(days=age * 365 + random.randint(0, 364))

# ── SCALE KNOB #1 — bigger candidate pool to support more applications ────────
N_CANDIDATES = 3200
print(f"\nBuilding candidate pool ({N_CANDIDATES} candidates)...")
CAND_POOL = []
for i in range(N_CANDIDATES):
    eth   = wchoice(ETHNICITIES, ETH_W)
    gen   = wchoice(GENDERS, GEN_W)
    last  = random.choice(LAST_BY_ETH[eth])
    first = random.choice(
        MALE_FIRST if gen == "Male" else
        FEMALE_FIRST if gen == "Female" else NB_FIRST
    )
    CAND_POOL.append({
        "CandidateID":   f"CND{i+1:04d}",
        "CandidateName": f"{first} {last}",
        "Gender":        gen,
        "Ethnicity":     eth,
        "Email":         f"{first.lower()}.{last.lower()}{random.randint(1,99)}@email.com",
    })
print(f"  Done — {len(CAND_POOL)} candidates created")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — SALARY & REFERENCE DATA
# ═════════════════════════════════════════════════════════════════════════════
SAL = {
    "Engineering":     {"Junior":(65,80),"Mid":(90,115),"Senior":(130,155),"Lead":(155,180),"Manager":(170,195),"Director":(200,230)},
    "Sales":           {"Junior":(50,65),"Mid":(70,88), "Senior":(90,115), "Lead":(112,135),"Manager":(128,150),"Director":(160,185)},
    "Marketing":       {"Junior":(46,60),"Mid":(63,80), "Senior":(85,108), "Lead":(105,128),"Manager":(118,140),"Director":(150,175)},
    "Product":         {"Junior":(70,85),"Mid":(98,118),"Senior":(135,160),"Lead":(158,182),"Manager":(172,198),"Director":(205,235)},
    "Customer Success":{"Junior":(44,58),"Mid":(60,75), "Senior":(78,98),  "Lead":(92,115), "Manager":(108,130),"Director":(138,160)},
    "HR":              {"Junior":(42,56),"Mid":(57,72), "Senior":(73,92),  "Lead":(87,108), "Manager":(102,125),"Director":(132,155)},
}
SAL = {dept: {lvl: (lo*1000, hi*1000) for lvl,(lo,hi) in levels.items()} for dept,levels in SAL.items()}

REF_BONUS = {"Junior":1000,"Mid":1500,"Senior":2500,"Lead":3500,"Manager":4000,"Director":5000}

TTH_BASE = {
    "Engineering":55,"Sales":28,"Marketing":35,
    "Product":45,"Customer Success":30,"HR":25
}

STAGES    = ["Applied","Screened","Interviewed","Offered","Hired"]
STAGE_ORD = {s: i+1 for i, s in enumerate(STAGES)}
STAGE_IDS = {"Applied":"STG01","Screened":"STG02","Interviewed":"STG03",
             "Offered":"STG04","Hired":"STG05"}

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — JOB CATALOGUE (chronological JobID order)
# ═════════════════════════════════════════════════════════════════════════════
def quarterly_post_date(year, quarter, job_type="normal"):
    q_starts = {1:date(year,1,1), 2:date(year,4,1), 3:date(year,7,1), 4:date(year,10,1)}
    q_ends   = {1:date(year,3,28),2:date(year,6,28),3:date(year,9,28),4:date(year,12,20)}
    qs = q_starts[quarter]
    if job_type == "director": offset = random.randint(1, 10)
    else:
        r = random.random()
        if r < 0.40:   offset = random.randint(1, 14)
        elif r < 0.75: offset = random.randint(15, 42)
        elif r < 0.95: offset = random.randint(43, 78)
        else:          offset = random.randint(20, 55)
    return min(qs + timedelta(days=offset), q_ends[quarter])

RAW_JOBS = [
    # 2023 Q1
    {"Dept":"Engineering","Title":"Junior Software Engineer","Level":"Junior","HM":"HM001","Pos":7,"PostQ":(2023,1),"Type":"normal"},
    {"Dept":"Engineering","Title":"Software Engineer","Level":"Mid","HM":"HM001","Pos":8,"PostQ":(2023,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Development Rep","Level":"Junior","HM":"HM004","Pos":8,"PostQ":(2023,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Account Executive","Level":"Mid","HM":"HM004","Pos":7,"PostQ":(2023,1),"Type":"normal"},
    {"Dept":"HR","Title":"HR Coordinator","Level":"Junior","HM":"HM012","Pos":3,"PostQ":(2023,1),"Type":"normal"},
    {"Dept":"Marketing","Title":"Marketing Analyst","Level":"Junior","HM":"HM006","Pos":3,"PostQ":(2023,1),"Type":"normal"},
    # 2023 Q2
    {"Dept":"Engineering","Title":"Senior Software Engineer","Level":"Senior","HM":"HM001","Pos":5,"PostQ":(2023,2),"Type":"normal"},
    {"Dept":"Engineering","Title":"DevOps Engineer","Level":"Mid","HM":"HM001","Pos":5,"PostQ":(2023,2),"Type":"normal"},
    {"Dept":"Marketing","Title":"Marketing Coordinator","Level":"Junior","HM":"HM006","Pos":4,"PostQ":(2023,2),"Type":"normal"},
    {"Dept":"Product","Title":"Associate Product Manager","Level":"Junior","HM":"HM008","Pos":4,"PostQ":(2023,2),"Type":"normal"},
    {"Dept":"HR","Title":"Recruiter","Level":"Mid","HM":"HM012","Pos":3,"PostQ":(2023,2),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Support Specialist","Level":"Junior","HM":"HM010","Pos":3,"PostQ":(2023,2),"Type":"normal"},
    # 2023 Q3
    {"Dept":"Engineering","Title":"QA Engineer","Level":"Mid","HM":"HM001","Pos":4,"PostQ":(2023,3),"Type":"normal"},
    {"Dept":"Sales","Title":"Senior Account Executive","Level":"Senior","HM":"HM004","Pos":4,"PostQ":(2023,3),"Type":"normal"},
    {"Dept":"Marketing","Title":"Content Strategist","Level":"Mid","HM":"HM006","Pos":3,"PostQ":(2023,3),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Customer Success Associate","Level":"Junior","HM":"HM010","Pos":6,"PostQ":(2023,3),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Customer Success Manager","Level":"Mid","HM":"HM010","Pos":5,"PostQ":(2023,3),"Type":"normal"},
    {"Dept":"Engineering","Title":"Backend Engineer","Level":"Mid","HM":"HM002","Pos":4,"PostQ":(2023,3),"Type":"normal"},
    # 2023 Q4
    {"Dept":"Engineering","Title":"Staff Engineer","Level":"Lead","HM":"HM002","Pos":3,"PostQ":(2023,4),"Type":"normal"},
    {"Dept":"Product","Title":"Product Manager","Level":"Mid","HM":"HM008","Pos":5,"PostQ":(2023,4),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Manager","Level":"Manager","HM":"HM005","Pos":3,"PostQ":(2023,4),"Type":"normal"},
    {"Dept":"Engineering","Title":"Engineering Director","Level":"Director","HM":"HM003","Pos":1,"PostQ":(2023,4),"Type":"director"},
    {"Dept":"HR","Title":"HR Business Partner","Level":"Mid","HM":"HM012","Pos":3,"PostQ":(2023,4),"Type":"normal"},
    # 2024 Q1
    {"Dept":"Engineering","Title":"Senior DevOps Engineer","Level":"Senior","HM":"HM002","Pos":3,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Product","Title":"Senior Product Manager","Level":"Senior","HM":"HM008","Pos":3,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Marketing","Title":"Growth Marketer","Level":"Senior","HM":"HM006","Pos":3,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Senior CSM","Level":"Senior","HM":"HM010","Pos":3,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Solutions Engineer","Level":"Senior","HM":"HM004","Pos":3,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Engineering","Title":"Frontend Engineer","Level":"Mid","HM":"HM001","Pos":4,"PostQ":(2024,1),"Type":"normal"},
    # 2024 Q2
    {"Dept":"Engineering","Title":"Engineering Manager","Level":"Manager","HM":"HM002","Pos":2,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"Product","Title":"Product Designer","Level":"Mid","HM":"HM008","Pos":3,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"Marketing","Title":"Performance Marketing Manager","Level":"Manager","HM":"HM007","Pos":2,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"HR","Title":"Senior Recruiter","Level":"Senior","HM":"HM012","Pos":2,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"Sales","Title":"Account Executive","Level":"Mid","HM":"HM004","Pos":5,"PostQ":(2024,2),"Type":"normal"},
    # 2024 Q3
    {"Dept":"Product","Title":"Principal Product Manager","Level":"Lead","HM":"HM009","Pos":2,"PostQ":(2024,3),"Type":"normal"},
    {"Dept":"Customer Success","Title":"CS Team Lead","Level":"Lead","HM":"HM011","Pos":2,"PostQ":(2024,3),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Director","Level":"Director","HM":"HM005","Pos":1,"PostQ":(2024,3),"Type":"director"},
    {"Dept":"Engineering","Title":"Software Engineer","Level":"Mid","HM":"HM001","Pos":5,"PostQ":(2024,3),"Type":"normal"},
    # 2024 Q4
    {"Dept":"Marketing","Title":"Brand Director","Level":"Director","HM":"HM007","Pos":1,"PostQ":(2024,4),"Type":"director"},
    {"Dept":"HR","Title":"Recruiter","Level":"Mid","HM":"HM012","Pos":2,"PostQ":(2024,4),"Type":"normal"},
    # 2025 Q1
    {"Dept":"Engineering","Title":"Senior Software Engineer","Level":"Senior","HM":"HM001","Pos":4,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Product","Title":"UX Researcher","Level":"Senior","HM":"HM009","Pos":2,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Development Rep","Level":"Junior","HM":"HM004","Pos":6,"PostQ":(2025,1),"Type":"normal"},
    # 2025 Q2
    {"Dept":"Customer Success","Title":"VP Customer Success","Level":"Director","HM":"HM003","Pos":1,"PostQ":(2025,2),"Type":"director"},
    {"Dept":"HR","Title":"Senior HRBP","Level":"Senior","HM":"HM012","Pos":2,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"Engineering","Title":"QA Engineer","Level":"Mid","HM":"HM001","Pos":3,"PostQ":(2025,2),"Type":"normal"},
    # 2025 Q3
    {"Dept":"Engineering","Title":"L&D Specialist","Level":"Mid","HM":"HM012","Pos":2,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Product","Title":"Product Manager","Level":"Mid","HM":"HM008","Pos":3,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Sales","Title":"Account Executive","Level":"Mid","HM":"HM004","Pos":4,"PostQ":(2025,3),"Type":"normal"},
    # 2025 Q4
    {"Dept":"Customer Success","Title":"Customer Success Associate","Level":"Junior","HM":"HM010","Pos":3,"PostQ":(2025,4),"Type":"normal"},
    # 2026 Q1 — in-progress
    {"Dept":"Product","Title":"VP of Product","Level":"Director","HM":"HM003","Pos":1,"PostQ":(2026,1),"Type":"director"},
    {"Dept":"Engineering","Title":"CHRO","Level":"Director","HM":"HM003","Pos":1,"PostQ":(2026,1),"Type":"director"},
    {"Dept":"Engineering","Title":"Backend Engineer","Level":"Mid","HM":"HM002","Pos":3,"PostQ":(2026,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Account Executive","Level":"Mid","HM":"HM004","Pos":3,"PostQ":(2026,1),"Type":"normal"},

    # ── EXTRA POSTINGS — ramps up overall hiring volume year over year ───────
    # 2024 (+11 jobs)
    {"Dept":"Engineering","Title":"Platform Engineer","Level":"Mid","HM":"HM001","Pos":3,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Development Rep","Level":"Junior","HM":"HM004","Pos":4,"PostQ":(2024,1),"Type":"normal"},
    {"Dept":"Marketing","Title":"Content Marketing Manager","Level":"Mid","HM":"HM006","Pos":2,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"Product","Title":"Product Analyst","Level":"Junior","HM":"HM008","Pos":3,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"HR","Title":"HR Generalist","Level":"Junior","HM":"HM012","Pos":2,"PostQ":(2024,2),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Customer Success Associate","Level":"Junior","HM":"HM010","Pos":4,"PostQ":(2024,3),"Type":"normal"},
    {"Dept":"Sales","Title":"Account Executive","Level":"Mid","HM":"HM004","Pos":3,"PostQ":(2024,3),"Type":"normal"},
    {"Dept":"Engineering","Title":"Site Reliability Engineer","Level":"Senior","HM":"HM002","Pos":2,"PostQ":(2024,3),"Type":"normal"},
    {"Dept":"Product","Title":"Associate Product Manager","Level":"Junior","HM":"HM008","Pos":3,"PostQ":(2024,4),"Type":"normal"},
    {"Dept":"Marketing","Title":"Marketing Analyst","Level":"Junior","HM":"HM006","Pos":2,"PostQ":(2024,4),"Type":"normal"},
    {"Dept":"HR","Title":"Talent Sourcer","Level":"Junior","HM":"HM012","Pos":2,"PostQ":(2024,4),"Type":"normal"},

    # 2025 (+24 jobs)
    {"Dept":"Engineering","Title":"Software Engineer II","Level":"Mid","HM":"HM001","Pos":4,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Enterprise Account Executive","Level":"Senior","HM":"HM004","Pos":3,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Marketing","Title":"Demand Generation Manager","Level":"Mid","HM":"HM006","Pos":2,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Product","Title":"Product Designer","Level":"Mid","HM":"HM008","Pos":2,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Onboarding Specialist","Level":"Junior","HM":"HM010","Pos":3,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"HR","Title":"People Operations Analyst","Level":"Junior","HM":"HM012","Pos":2,"PostQ":(2025,1),"Type":"normal"},
    {"Dept":"Engineering","Title":"Data Engineer","Level":"Mid","HM":"HM002","Pos":3,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Development Rep","Level":"Junior","HM":"HM004","Pos":4,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"Marketing","Title":"Brand Marketing Specialist","Level":"Mid","HM":"HM006","Pos":2,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"Product","Title":"Product Manager","Level":"Mid","HM":"HM009","Pos":2,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Customer Success Manager","Level":"Mid","HM":"HM011","Pos":2,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"HR","Title":"Recruiter","Level":"Mid","HM":"HM012","Pos":2,"PostQ":(2025,2),"Type":"normal"},
    {"Dept":"Engineering","Title":"Frontend Engineer","Level":"Mid","HM":"HM001","Pos":4,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Sales","Title":"Account Executive","Level":"Mid","HM":"HM004","Pos":3,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Marketing","Title":"SEO Specialist","Level":"Junior","HM":"HM006","Pos":2,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Product","Title":"Technical Program Manager","Level":"Senior","HM":"HM009","Pos":2,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Support Specialist","Level":"Junior","HM":"HM010","Pos":3,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"HR","Title":"Compensation Analyst","Level":"Mid","HM":"HM012","Pos":2,"PostQ":(2025,3),"Type":"normal"},
    {"Dept":"Engineering","Title":"Backend Engineer","Level":"Mid","HM":"HM002","Pos":4,"PostQ":(2025,4),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Manager","Level":"Manager","HM":"HM005","Pos":2,"PostQ":(2025,4),"Type":"normal"},
    {"Dept":"Marketing","Title":"Marketing Coordinator","Level":"Junior","HM":"HM006","Pos":2,"PostQ":(2025,4),"Type":"normal"},
    {"Dept":"Product","Title":"Associate Product Manager","Level":"Junior","HM":"HM008","Pos":2,"PostQ":(2025,4),"Type":"normal"},
    {"Dept":"HR","Title":"HR Business Partner","Level":"Mid","HM":"HM012","Pos":2,"PostQ":(2025,4),"Type":"normal"},
    {"Dept":"Engineering","Title":"QA Engineer","Level":"Mid","HM":"HM001","Pos":3,"PostQ":(2025,4),"Type":"normal"},

    # 2026 Q1 (+5 jobs — pace exceeds 2025 quarterly average)
    {"Dept":"Engineering","Title":"Senior Backend Engineer","Level":"Senior","HM":"HM002","Pos":3,"PostQ":(2026,1),"Type":"normal"},
    {"Dept":"Sales","Title":"Sales Development Rep","Level":"Junior","HM":"HM004","Pos":4,"PostQ":(2026,1),"Type":"normal"},
    {"Dept":"Marketing","Title":"Growth Marketer","Level":"Mid","HM":"HM006","Pos":2,"PostQ":(2026,1),"Type":"normal"},
    {"Dept":"Product","Title":"Product Designer","Level":"Mid","HM":"HM008","Pos":2,"PostQ":(2026,1),"Type":"normal"},
    {"Dept":"Customer Success","Title":"Customer Success Associate","Level":"Junior","HM":"HM010","Pos":3,"PostQ":(2026,1),"Type":"normal"},
]

for j in RAW_JOBS:
    yr, q = j["PostQ"]
    j["JobPostedDate"] = quarterly_post_date(yr, q, j["Type"])

RAW_JOBS.sort(key=lambda x: x["JobPostedDate"])
JOB_CATALOGUE = []
for idx, j in enumerate(RAW_JOBS):
    dept  = j["Dept"]
    level = j["Level"]
    lo, hi = SAL[dept][level]
    mid    = (lo + hi) / 2
    j["JobID"]             = f"JOB{idx+1:03d}"
    j["BudgetPerPosition"] = round(mid * random.uniform(0.93, 1.07), -2)
    JOB_CATALOGUE.append(j)

JOB_MAP = {j["JobID"]: j for j in JOB_CATALOGUE}
TOTAL_POSITIONS = sum(j["Pos"] for j in JOB_CATALOGUE)
print(f"\nJob catalogue: {len(JOB_CATALOGUE)} jobs | {TOTAL_POSITIONS} total positions")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3b — HIRE DISTRIBUTION PLAN (spreads StartDates across years)
# ═════════════════════════════════════════════════════════════════════════════
# Target number of hires (StartDate quarter) per Department x Quarter.
# Consumed as a budget while assigning hire quarters below; once a
# dept/quarter cell is exhausted, later hires fall back to a weighted
# random pick among still-valid quarters so nothing gets stuck.
_HIRE_PLAN_RAW = {
    ("Customer Success","2023-Q1"):2, ("Engineering","2023-Q1"):17, ("HR","2023-Q1"):3,
    ("Marketing","2023-Q1"):3, ("Product","2023-Q1"):2, ("Sales","2023-Q1"):17,
    ("Customer Success","2023-Q2"):3, ("Engineering","2023-Q2"):11, ("HR","2023-Q2"):3,
    ("Marketing","2023-Q2"):4, ("Product","2023-Q2"):4, ("Sales","2023-Q2"):0,
    ("Customer Success","2023-Q3"):12, ("Engineering","2023-Q3"):9, ("HR","2023-Q3"):1,
    ("Marketing","2023-Q3"):3, ("Product","2023-Q3"):0, ("Sales","2023-Q3"):4,
    ("Customer Success","2023-Q4"):0, ("Engineering","2023-Q4"):4, ("HR","2023-Q4"):3,
    ("Marketing","2023-Q4"):0, ("Product","2023-Q4"):6, ("Sales","2023-Q4"):3,
    ("Customer Success","2024-Q1"):3, ("Engineering","2024-Q1"):8, ("HR","2024-Q1"):0,
    ("Marketing","2024-Q1"):3, ("Product","2024-Q1"):3, ("Sales","2024-Q1"):3,
    ("Customer Success","2024-Q2"):0, ("Engineering","2024-Q2"):2, ("HR","2024-Q2"):2,
    ("Marketing","2024-Q2"):2, ("Product","2024-Q2"):3, ("Sales","2024-Q2"):6,
    ("Customer Success","2024-Q3"):2, ("Engineering","2024-Q3"):6, ("HR","2024-Q3"):1,
    ("Marketing","2024-Q3"):0, ("Product","2024-Q3"):2, ("Sales","2024-Q3"):1,
    ("Customer Success","2024-Q4"):0, ("Engineering","2024-Q4"):1, ("HR","2024-Q4"):2,
    ("Marketing","2024-Q4"):1, ("Product","2024-Q4"):0, ("Sales","2024-Q4"):2,
    ("Customer Success","2025-Q1"):0, ("Engineering","2025-Q1"):4, ("HR","2025-Q1"):0,
    ("Marketing","2025-Q1"):0, ("Product","2025-Q1"):2, ("Sales","2025-Q1"):7,
    ("Customer Success","2025-Q2"):1, ("Engineering","2025-Q2"):3, ("HR","2025-Q2"):2,
    ("Marketing","2025-Q2"):0, ("Product","2025-Q2"):1, ("Sales","2025-Q2"):0,
    ("Customer Success","2025-Q3"):1, ("Engineering","2025-Q3"):2, ("HR","2025-Q3"):1,
    ("Marketing","2025-Q3"):2, ("Product","2025-Q3"):3, ("Sales","2025-Q3"):4,
    ("Customer Success","2025-Q4"):3, ("Engineering","2025-Q4"):2, ("HR","2025-Q4"):0,
    ("Marketing","2025-Q4"):0, ("Product","2025-Q4"):1, ("Sales","2025-Q4"):2,
    ("Customer Success","2026-Q1"):0, ("Engineering","2026-Q1"):4, ("HR","2026-Q1"):2,
    ("Marketing","2026-Q1"):0, ("Product","2026-Q1"):1, ("Sales","2026-Q1"):3,
}
HIRE_PLAN = defaultdict(lambda: defaultdict(int))
for (_dept, _qtr), _cnt in _HIRE_PLAN_RAW.items():
    HIRE_PLAN[_dept][_qtr] = _cnt

ALL_QUARTERS_ORDERED = []
for _yr in [2023, 2024, 2025, 2026]:
    for _q in [1, 2, 3, 4]:
        if _yr == 2026 and _q > 1:
            break
        ALL_QUARTERS_ORDERED.append(f"{_yr}-Q{_q}")

def quarter_bounds(qstr):
    yr_s, q_s = qstr.split("-Q")
    yr, qn = int(yr_s), int(q_s)
    starts = {1: date(yr,1,1), 2: date(yr,4,1), 3: date(yr,7,1), 4: date(yr,10,1)}
    ends   = {1: date(yr,3,31),2: date(yr,6,30),3: date(yr,9,30),4: date(yr,12,31)}
    return starts[qn], ends[qn]

def fill_window(post_yr):
    """Return (window_end_date) per the posted-year -> fill-by rule."""
    if post_yr == 2023:
        return date(2024, 3, 31)          # fill by Q1 2024
    elif post_yr == 2024:
        return date(2025, 6, 30)          # fill by Q2 2025
    else:
        return date(2026, 4, 15)          # fill by start of Q2 2026 (2025 & 2026 postings)

def pick_hire_quarter(dept, posted, window_end):
    """Pick a target hire (StartDate) quarter for this dept, respecting the
    posting date and the fill window, consuming budget from HIRE_PLAN."""
    candidates = []
    for qtr in ALL_QUARTERS_ORDERED:
        q_start, q_end = quarter_bounds(qtr)
        if q_end < posted + timedelta(days=25):   # need some minimal pipeline runway
            continue
        if q_start > window_end:
            continue
        candidates.append(qtr)
    if not candidates:
        candidates = [f"{window_end.year}-Q{(window_end.month-1)//3+1}"]

    weighted = [(q, HIRE_PLAN[dept].get(q, 0)) for q in candidates]
    total_w = sum(w for _, w in weighted)
    if total_w > 0:
        r = random.uniform(0, total_w)
        c = 0
        for q, w in weighted:
            c += w
            if r <= c:
                chosen = q
                break
        else:
            chosen = weighted[-1][0]
    else:
        chosen = random.choice(candidates)

    HIRE_PLAN[dept][chosen] = max(0, HIRE_PLAN[dept].get(chosen, 0) - 1)
    return chosen

def target_hire_date(dept, posted, window_end):
    qtr = pick_hire_quarter(dept, posted, window_end)
    q_start, q_end = quarter_bounds(qtr)
    lo = max(q_start, posted + timedelta(days=25))
    hi = min(q_end, window_end)
    if lo >= hi:
        hi = lo + timedelta(days=1)
    return rdate(lo, hi)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — HIRING MANAGERS & RECRUITERS
# ═════════════════════════════════════════════════════════════════════════════
HM_MASTER = {
    "HM001":{"HiringManagerName":"Sarah Mitchell","HiringManagerTitle":"Engineering Lead","HiringManagerDept":"Engineering","HiringManagerEmail":"s.mitchell@techcorp.io"},
    "HM002":{"HiringManagerName":"David Park","HiringManagerTitle":"Senior Engineering Lead","HiringManagerDept":"Engineering","HiringManagerEmail":"d.park@techcorp.io"},
    "HM003":{"HiringManagerName":"James Whitfield","HiringManagerTitle":"CTO","HiringManagerDept":"Executive","HiringManagerEmail":"j.whitfield@techcorp.io"},
    "HM004":{"HiringManagerName":"Lisa Nguyen","HiringManagerTitle":"Sales Lead","HiringManagerDept":"Sales","HiringManagerEmail":"l.nguyen@techcorp.io"},
    "HM005":{"HiringManagerName":"Tom Hargreaves","HiringManagerTitle":"VP of Sales","HiringManagerDept":"Sales","HiringManagerEmail":"t.hargreaves@techcorp.io"},
    "HM006":{"HiringManagerName":"Priya Sharma","HiringManagerTitle":"Marketing Lead","HiringManagerDept":"Marketing","HiringManagerEmail":"p.sharma@techcorp.io"},
    "HM007":{"HiringManagerName":"Raj Kapoor","HiringManagerTitle":"VP of Marketing","HiringManagerDept":"Marketing","HiringManagerEmail":"r.kapoor@techcorp.io"},
    "HM008":{"HiringManagerName":"Kenji Tanaka","HiringManagerTitle":"Product Lead","HiringManagerDept":"Product","HiringManagerEmail":"k.tanaka@techcorp.io"},
    "HM009":{"HiringManagerName":"Anya Ivanova","HiringManagerTitle":"Senior Product Lead","HiringManagerDept":"Product","HiringManagerEmail":"a.ivanova@techcorp.io"},
    "HM010":{"HiringManagerName":"Maria Lopez","HiringManagerTitle":"CS Lead","HiringManagerDept":"Customer Success","HiringManagerEmail":"m.lopez@techcorp.io"},
    "HM011":{"HiringManagerName":"Ben Okafor","HiringManagerTitle":"Senior CS Lead","HiringManagerDept":"Customer Success","HiringManagerEmail":"b.okafor@techcorp.io"},
    "HM012":{"HiringManagerName":"Claire Fontaine","HiringManagerTitle":"HR Lead","HiringManagerDept":"HR","HiringManagerEmail":"c.fontaine@techcorp.io"},
}
DEPT_RECS = {
    "Engineering":      ["REC001","REC002","REC007","REC011","REC012"],
    "Sales":            ["REC003","REC008","REC012"],
    "Marketing":        ["REC004","REC012"],
    "Product":          ["REC005","REC009","REC012"],
    "Customer Success": ["REC006","REC012"],
    "HR":               ["REC010","REC012"],
}
REC_MASTER = {
    "REC001":{"RecruiterName":"Jordan Blake","RecruiterRole":"Technical Recruiter","RecruiterDept":"Engineering","RecruiterEmail":"jordan.blake@techcorp.io","JoinDate":"2021-03-15","EndDate":"","Status":"Active"},
    "REC002":{"RecruiterName":"Amara Diallo","RecruiterRole":"Technical Recruiter","RecruiterDept":"Engineering","RecruiterEmail":"amara.diallo@techcorp.io","JoinDate":"2020-07-01","EndDate":"","Status":"Active"},
    "REC003":{"RecruiterName":"Sam Kowalski","RecruiterRole":"Sales Recruiter","RecruiterDept":"Sales","RecruiterEmail":"sam.kowalski@techcorp.io","JoinDate":"2021-01-10","EndDate":"","Status":"Active"},
    "REC004":{"RecruiterName":"Olivia Chen","RecruiterRole":"Marketing Recruiter","RecruiterDept":"Marketing","RecruiterEmail":"olivia.chen@techcorp.io","JoinDate":"2022-05-20","EndDate":"","Status":"Active"},
    "REC005":{"RecruiterName":"Marcus Webb","RecruiterRole":"Product Recruiter","RecruiterDept":"Product","RecruiterEmail":"marcus.webb@techcorp.io","JoinDate":"2021-09-01","EndDate":"","Status":"Active"},
    "REC006":{"RecruiterName":"Nina Patel","RecruiterRole":"CS Recruiter","RecruiterDept":"Customer Success","RecruiterEmail":"nina.patel@techcorp.io","JoinDate":"2022-02-14","EndDate":"","Status":"Active"},
    "REC007":{"RecruiterName":"Ethan Ross","RecruiterRole":"Senior Recruiter","RecruiterDept":"Engineering","RecruiterEmail":"ethan.ross@techcorp.io","JoinDate":"2020-11-01","EndDate":"","Status":"Active"},
    "REC008":{"RecruiterName":"Fatima Al-Amin","RecruiterRole":"Senior Recruiter","RecruiterDept":"Sales","RecruiterEmail":"fatima.alamin@techcorp.io","JoinDate":"2021-06-15","EndDate":"","Status":"Active"},
    "REC009":{"RecruiterName":"Leo Andersen","RecruiterRole":"Senior Recruiter","RecruiterDept":"Product","RecruiterEmail":"leo.andersen@techcorp.io","JoinDate":"2020-08-20","EndDate":"","Status":"Active"},
    "REC010":{"RecruiterName":"Chiara Russo","RecruiterRole":"HR Recruiter","RecruiterDept":"HR","RecruiterEmail":"chiara.russo@techcorp.io","JoinDate":"2021-04-01","EndDate":"2024-06-16","Status":"Inactive"},
    "REC011":{"RecruiterName":"Daniel Kim","RecruiterRole":"Lead Recruiter","RecruiterDept":"Engineering","RecruiterEmail":"daniel.kim@techcorp.io","JoinDate":"2020-09-10","EndDate":"2024-09-20","Status":"Inactive"},
    "REC012":{"RecruiterName":"Sophia Turner","RecruiterRole":"Recruitment Manager","RecruiterDept":"All","RecruiterEmail":"sophia.turner@techcorp.io","JoinDate":"2020-01-15","EndDate":"","Status":"Active"},
}

def get_recruiter(dept, app_date_str):
    eligible = [r for r in DEPT_RECS.get(dept, ["REC012"])
                if not (REC_MASTER[r]["EndDate"] and app_date_str > REC_MASTER[r]["EndDate"])]
    return random.choice(eligible) if eligible else "REC012"

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — SOURCES
# ═════════════════════════════════════════════════════════════════════════════
SOURCES     = ["LinkedIn","Job Board","Agency","Career Site","GitHub","Indeed","Referral"]
SOURCE_MAP  = {
    "LinkedIn":    ("SRC01","Digital",  0.13),
    "Job Board":   ("SRC02","Digital",  0.09),
    "Agency":      ("SRC03","Agency",   0.16),
    "Career Site": ("SRC04","Digital",  0.11),
    "GitHub":      ("SRC05","Digital",  0.20),
    "Indeed":      ("SRC06","Digital",  0.08),
    "Referral":    ("SRC07","Referral", 0.30),
}
SRC_WEIGHTS = [0.20, 0.11, 0.09, 0.10, 0.12, 0.10, 0.28]

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 6 — HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════
def fmt(d):
    return d.isoformat() if d else ""

def rdate(s, e):
    if s >= e: return s
    return s + timedelta(days=random.randint(0, (e - s).days))

def get_pre_offer_stage(source, dept, app_date):
    q = SOURCE_MAP[source][2]
    if app_date.month in [10, 11, 12]: q *= 0.75
    if dept == "Engineering":
        s_rate = min(q * 2.0, 0.82)
        i_rate = q * 1.3
    else:
        s_rate = min(q * 2.5, 0.88)
        i_rate = q * 1.7
    r = random.random()
    if r > s_rate: return "Applied"
    if r > i_rate: return "Screened"
    return "Interviewed"

def get_dates(app_d, stage, dept):
    tth = max(10, TTH_BASE[dept] + random.randint(-8, 12))
    sd = id_ = od = std = None
    o = STAGE_ORD[stage]
    if o >= 2: sd  = app_d + timedelta(days=random.randint(3, 10))
    if o >= 3: id_ = (sd or app_d) + timedelta(days=random.randint(5, 18))
    if o >= 4: od  = (id_ or app_d) + timedelta(days=random.randint(3, 10))
    if o >= 5: std = (od or app_d) + timedelta(days=random.randint(14, 45))
    return sd, id_, od, std, tth

def make_row(app_id, cand, job, src, app_d, stage, sd, id_, od, std, tth, dob,
             post_closure_error=False, closure_note="", slot_num=None):
    dept  = job["Dept"]
    level = job["Level"]
    hm    = HM_MASTER[job["HM"]]
    sid, stype, _ = SOURCE_MAP[src]
    rec_id = get_recruiter(dept, fmt(app_d))
    rec    = REC_MASTER[rec_id]
    slot_id = f"{job['JobID']}-{slot_num}" if slot_num is not None else f"{job['JobID']}-0"

    sal = bv = ref_bonus = ""
    if stage in ["Offered", "Hired"]:
        lo, hi  = SAL[dept][level]
        offered = round(random.uniform(lo, hi), -2)
        if random.random() < 0.20:
            offered = round(job["BudgetPerPosition"] * random.uniform(1.02, 1.12), -2)
        sal = offered
        bv  = round(float(sal) - job["BudgetPerPosition"], 2)
    if src == "Referral" and stage == "Hired":
        ref_bonus = REF_BONUS[level]

    return {
        "ApplicationID":       f"APP{app_id}",
        "CandidateID":         cand["CandidateID"],
        "CandidateName":       cand["CandidateName"],
        "Gender":              cand["Gender"],
        "Ethnicity":           cand["Ethnicity"],
        "DateOfBirth":         fmt(dob),
        "Email":               cand["Email"],
        "JobID":               job["JobID"],
        "PositionSlotID":      slot_id,
        "Department":          dept,
        "JobTitle":            job["Title"],
        "JobLevel":            level,
        "NumberOfPositions":   job["Pos"],
        "BudgetPerPosition":   job["BudgetPerPosition"],
        "JobPostedDate":       fmt(job["JobPostedDate"]),
        "HiringManagerID":     job["HM"],
        "HiringManagerName":   hm["HiringManagerName"],
        "HiringManagerTitle":  hm["HiringManagerTitle"],
        "HiringManagerDept":   hm["HiringManagerDept"],
        "HiringManagerEmail":  hm["HiringManagerEmail"],
        "SourceID":            sid,
        "SourceName":          src,
        "SourceType":          stype,
        "RecruiterID":         rec_id,
        "RecruiterName":       rec["RecruiterName"],
        "RecruiterRole":       rec["RecruiterRole"],
        "RecruiterDept":       rec["RecruiterDept"],
        "RecruiterEmail":      rec["RecruiterEmail"],
        "RecruiterJoinDate":   rec["JoinDate"],
        "RecruiterEndDate":    rec["EndDate"],
        "RecruiterStatus":     rec["Status"],
        "ApplicationDate":     fmt(app_d),
        "ScreenDate":          fmt(sd),
        "InterviewDate":       fmt(id_),
        "OfferDate":           fmt(od),
        "StartDate":           fmt(std),
        "StageID":             STAGE_IDS.get(stage, ""),
        "HireStage":           stage,
        "StageOrder":          STAGE_ORD.get(stage, ""),
        "SalaryOffered":       sal,
        "BudgetVariance":      bv,
        "AvgDaysToHire":       tth if stage == "Hired" else "",
        "ReferralBonus":       ref_bonus,
        "PostingClosureError": "Yes" if post_closure_error else "No",
        "ClosureErrorNote":    closure_note,
        "JobStatus":           "",   # backfilled in Section 7b
        "PositionsFilled":     "",   # backfilled in Section 7b
        "JobClosedDate":       "",   # backfilled in Section 7b
    }

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 7 — MAIN APPLICATION GENERATION
# ═════════════════════════════════════════════════════════════════════════════
print(f"\nGenerating applications...")

hired_candidates = set()
CAND_DOB         = {}
all_rows         = []
app_id           = 1000

closure_error_jobs    = set()
MAX_CLOSURE_PER_JOB   = 2
first_two_2023_jobs   = [j["JobID"] for j in JOB_CATALOGUE if j["JobPostedDate"].year == 2023][:2]
for jid in first_two_2023_jobs:
    closure_error_jobs.add(jid)

first_hire_date_per_job = {}

for job_idx, job in enumerate(JOB_CATALOGUE):
    jid       = job["JobID"]
    dept      = job["Dept"]
    level     = job["Level"]
    n_pos     = job["Pos"]
    posted    = job["JobPostedDate"]
    post_yr   = posted.year

    # ── Posted-vs-filled logic (spreads hires across years) ──────────────────
    window_end = fill_window(post_yr)
    if post_yr <= 2024:
        fill_target = n_pos                              # fully filled
    elif post_yr == 2025:
        fill_target = max(1, round(n_pos * 0.60))         # 60% filled
    else:
        fill_target = round(n_pos * random.uniform(0.30, 0.35))  # 30-35% filled

    for slot in range(n_pos):
        is_filled  = slot < fill_target
        app_start  = posted + timedelta(days=2)

        if is_filled:
            slot_target_hire = target_hire_date(dept, posted, window_end)
            app_end = slot_target_hire - timedelta(days=random.randint(45, 65))
            app_end = max(app_end, app_start + timedelta(days=14))
            app_cap = min(app_end, slot_target_hire - timedelta(days=1))
            app_cap = max(app_cap, app_start)
        else:
            slot_target_hire = None
            app_cap = date(2026, 3, 20)

        # ── SCALE KNOB #2 — bigger pipeline per position (was 10-18) ─────────
        pipeline_size = random.randint(20, 34)
        app_dates     = sorted([rdate(app_start, app_cap)
                                for _ in range(pipeline_size)])

        for idx, app_d in enumerate(app_dates):
            pool = [c for c in CAND_POOL if c["CandidateID"] not in hired_candidates]
            if not pool: break
            cand = random.choice(pool)
            cid  = cand["CandidateID"]

            if cid not in CAND_DOB:
                CAND_DOB[cid] = gen_dob(level)
            dob = CAND_DOB[cid]

            src = wchoice(SOURCES, SRC_WEIGHTS)

            is_last = (idx == len(app_dates) - 1)

            if is_filled and is_last:
                stage = "Hired"
            elif is_filled and idx >= len(app_dates) - 3:
                if idx == len(app_dates) - 2 and random.random() < 0.03:
                    stage = "Offered"
                else:
                    stage = get_pre_offer_stage(src, dept, app_d)
            else:
                pre = get_pre_offer_stage(src, dept, app_d)
                if pre == "Interviewed" and random.random() < 0.01:
                    stage = "Offered"
                else:
                    stage = pre

            sd, id_, od, std, tth = get_dates(app_d, stage, dept)

            if stage == "Hired" and slot_target_hire is not None:
                # Pin the StartDate to the quarter chosen by the hire plan,
                # keeping it consistent with the offer date that precedes it.
                floor_date = (od + timedelta(days=14)) if od else (app_d + timedelta(days=14))
                std = max(slot_target_hire, floor_date)
                tth = max(10, (std - app_d).days)

            row = make_row(app_id, cand, job, src, app_d, stage,
                          sd, id_, od, std, tth, dob, slot_num=slot + 1)
            all_rows.append(row)
            app_id += 1

            if stage == "Hired":
                hired_candidates.add(cid)
                if jid not in first_hire_date_per_job:
                    first_hire_date_per_job[jid] = std or app_d + timedelta(days=30)

        if not is_filled:
            # ── SCALE KNOB #3 — more in-progress stragglers (was 3-7) ────────
            for _ in range(random.randint(6, 12)):
                pool = [c for c in CAND_POOL if c["CandidateID"] not in hired_candidates]
                if not pool: break
                cand  = random.choice(pool)
                cid   = cand["CandidateID"]
                if cid not in CAND_DOB: CAND_DOB[cid] = gen_dob(level)
                dob   = CAND_DOB[cid]
                app_d = rdate(max(posted + timedelta(days=5), date(2025, 6, 1)), date(2026, 3, 20))
                src   = wchoice(SOURCES, SRC_WEIGHTS)
                stage = get_pre_offer_stage(src, dept, app_d)
                sd, id_, od, std, tth = get_dates(app_d, stage, dept)
                row = make_row(app_id, cand, job, src, app_d, stage, sd, id_, od, std, tth, dob,
                              slot_num=slot + 1)
                all_rows.append(row)
                app_id += 1

    if jid in closure_error_jobs and jid in first_hire_date_per_job:
        fhd  = first_hire_date_per_job[jid]
        note = "ATS auto-close not configured — manual process gap Jan-Mar 2023"
        for _ in range(MAX_CLOSURE_PER_JOB):
            pool = [c for c in CAND_POOL if c["CandidateID"] not in hired_candidates]
            if not pool: break
            cand  = random.choice(pool)
            cid   = cand["CandidateID"]
            if cid not in CAND_DOB: CAND_DOB[cid] = gen_dob(level)
            dob   = CAND_DOB[cid]
            app_d = fhd + timedelta(days=random.randint(3, 18))
            if app_d > date(2023, 3, 31): app_d = date(2023, 3, 20)
            src   = wchoice(SOURCES, SRC_WEIGHTS)
            stage = "Applied"
            sd, id_, od, std, tth = get_dates(app_d, stage, dept)
            row   = make_row(app_id, cand, job, src, app_d, stage, sd, id_, od, std, tth, dob,
                            post_closure_error=True, closure_note=note, slot_num="late")
            all_rows.append(row)
            app_id += 1

    if (job_idx + 1) % 10 == 0:
        print(f"  Processed {job_idx+1}/{len(JOB_CATALOGUE)} jobs | {len(all_rows)} rows so far")

print(f"  Generation complete: {len(all_rows)} clean rows")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 7b — BACKFILL JOB FILL-STATUS (PositionsFilled / JobStatus / JobClosedDate)
# ═════════════════════════════════════════════════════════════════════════════
print(f"\nBackfilling job fill-status...")
job_hire_dates = defaultdict(list)   # JobID -> sorted list of StartDates for Hired rows
for r in all_rows:
    if r["HireStage"] == "Hired" and r["StartDate"]:
        job_hire_dates[r["JobID"]].append(r["StartDate"])

for jid, dates in job_hire_dates.items():
    dates.sort()

for r in all_rows:
    jid       = r["JobID"]
    n_pos     = JOB_MAP[jid]["Pos"]
    filled    = len(job_hire_dates.get(jid, []))
    r["PositionsFilled"] = filled
    if filled == 0:
        r["JobStatus"]     = "Open"
        r["JobClosedDate"] = ""
    elif filled < n_pos:
        r["JobStatus"]     = "Partially Filled"
        r["JobClosedDate"] = ""
    else:
        r["JobStatus"]     = "Filled"
        r["JobClosedDate"] = job_hire_dates[jid][-1]   # date the last position was filled

n_filled   = sum(1 for j in JOB_CATALOGUE if len(job_hire_dates.get(j["JobID"], [])) >= j["Pos"])
n_partial  = sum(1 for j in JOB_CATALOGUE if 0 < len(job_hire_dates.get(j["JobID"], [])) < j["Pos"])
n_open     = len(JOB_CATALOGUE) - n_filled - n_partial
print(f"  Jobs Filled: {n_filled} | Partially Filled: {n_partial} | Open: {n_open}")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 8 — INJECT DIRTY DATA (~2.5%)
# ═════════════════════════════════════════════════════════════════════════════
print(f"\nInjecting dirty data...")
n_dirty      = max(40, len(all_rows) // 40)
dirty_indices= random.sample(range(len(all_rows)), min(n_dirty, len(all_rows)))
dirty_rows   = []

for idx in dirty_indices:
    row = copy.deepcopy(all_rows[idx])
    err = random.choice([
        "duplicate","null_stage","null_gender","null_appdate",
        "dept_casing","invalid_stage","salary_wrong_stage",
        "date_inversion","invalid_gender","future_date"
    ])
    if err == "duplicate":
        dirty_rows.append((idx + 1, copy.deepcopy(all_rows[idx])))
    elif err == "null_stage":
        row["HireStage"] = ""; row["StageOrder"] = ""; row["StageID"] = ""
        dirty_rows.append((idx, row))
    elif err == "null_gender":
        row["Gender"] = ""
        dirty_rows.append((idx, row))
    elif err == "null_appdate":
        row["ApplicationDate"] = ""
        dirty_rows.append((idx, row))
    elif err == "dept_casing":
        row["Department"] = random.choice([row["Department"].upper(), row["Department"].lower()])
        dirty_rows.append((idx, row))
    elif err == "invalid_stage":
        row["HireStage"] = random.choice(["Shortlisted","In Review","Pending","rejected","HIRED"])
        row["StageOrder"] = ""; row["StageID"] = ""
        dirty_rows.append((idx, row))
    elif err == "salary_wrong_stage":
        if row["HireStage"] not in ["Offered","Hired"]:
            row["SalaryOffered"] = random.randint(50, 200) * 1000
        dirty_rows.append((idx, row))
    elif err == "date_inversion":
        try:
            ad = date.fromisoformat(row["ApplicationDate"])
            row["ScreenDate"] = (ad - timedelta(days=random.randint(1,10))).isoformat()
        except: pass
        dirty_rows.append((idx, row))
    elif err == "invalid_gender":
        row["Gender"] = random.choice(["M","F","male","FEMALE"])
        dirty_rows.append((idx, row))
    elif err == "future_date":
        row["ApplicationDate"] = (date(2027,1,1)+timedelta(days=random.randint(0,200))).isoformat()
        dirty_rows.append((idx, row))

final_rows = list(all_rows)
for ins, drow in sorted(dirty_rows, key=lambda x: x[0]):
    final_rows.insert(min(ins, len(final_rows)), drow)

print(f"  Dirty rows injected: {len(dirty_rows)} | Total rows: {len(final_rows)}")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 9 — HEADCOUNT PLAN
# ═════════════════════════════════════════════════════════════════════════════
print(f"\nBuilding HeadcountPlan...")
dept_qtr_positions = defaultdict(lambda: defaultdict(int))
for job in JOB_CATALOGUE:
    yr, q = job["PostQ"]
    qtr   = f"{yr}-Q{q}"
    dept_qtr_positions[job["Dept"]][qtr] += job["Pos"]

all_quarters = []
for yr in [2023, 2024, 2025, 2026]:
    for q in [1,2,3,4]:
        if yr == 2026 and q > 1: break
        all_quarters.append(f"{yr}-Q{q}")

hcp_rows = []
DEPTS = ["Engineering","Sales","Marketing","Product","Customer Success","HR"]
for dept in DEPTS:
    for qtr in all_quarters:
        actual  = dept_qtr_positions[dept].get(qtr, 0)
        target  = max(0, round(actual * 1.12)) if actual > 0 else 0
        if target == 0 and random.random() < 0.3:
            target = random.randint(1, 2)
        hcp_rows.append({"Department":dept,"Quarter":qtr,"TargetHires":target})

with open(f"{OUTPUT_DIR}/HeadcountPlan.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["Department","Quarter","TargetHires"])
    w.writeheader(); w.writerows(hcp_rows)

total_target = sum(r["TargetHires"] for r in hcp_rows)
print(f"  HeadcountPlan: {len(hcp_rows)} rows | Total target hires: {total_target}")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 10 — SOURCE COSTS (no referral, YoY growth, realistic spikes)
# ═════════════════════════════════════════════════════════════════════════════
print(f"\nBuilding SourceCosts...")
SC_CONFIG = {
    "LinkedIn":    {"base":7800,  "yoy":0.08,"spikes":{2023:[3],    2024:[3,9],  2025:[3]},   "spike_pct":0.45},
    "Job Board":   {"base":2800,  "yoy":0.05,"spikes":{2023:[6],    2024:[],     2025:[6]},   "spike_pct":0.43},
    "Agency":      {"base":14000, "yoy":0.10,"spikes":{2023:[9],    2024:[9],    2025:[2,9]}, "spike_pct":0.43},
    "Career Site": {"base":750,   "yoy":0.03,"spikes":{},                                     "spike_pct":0},
    "GitHub":      {"base":1100,  "yoy":0.06,"spikes":{2024:[1],    2025:[1]},                "spike_pct":0.73},
    "Indeed":      {"base":2400,  "yoy":0.05,"spikes":{2023:[11],   2025:[11]},               "spike_pct":0.42},
}
sc_rows = []
cur = date(2023,1,1)
while cur <= date(2026,3,1):
    mo_str = cur.strftime("%Y-%m")
    yr, mo = cur.year, cur.month
    for src, cfg in SC_CONFIG.items():
        mult  = (1 + cfg["yoy"]) ** (yr - 2023)
        base  = round(cfg["base"] * mult, -2)
        spike = round(base * cfg["spike_pct"], -2) if mo in cfg.get("spikes",{}).get(yr,[]) else 0
        sc_rows.append({"SourceName":src,"Month":mo_str,"Year":yr,
                        "BaseCost":int(base),"SpikeCost":int(spike),
                        "MonthlyCost":int(base+spike),"IsSpike":"Yes" if spike>0 else "No"})
    cur = date(cur.year+1,1,1) if cur.month==12 else date(cur.year,cur.month+1,1)

with open(f"{OUTPUT_DIR}/SourceCosts.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["SourceName","Month","Year","BaseCost","SpikeCost","MonthlyCost","IsSpike"])
    w.writeheader(); w.writerows(sc_rows)
print(f"  SourceCosts: {len(sc_rows)} rows")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 11 — WRITE HiringData_Flat (single file — split later in Power BI)
# ═════════════════════════════════════════════════════════════════════════════
print(f"\nWriting HiringData_Flat.csv...")
fields = list(final_rows[0].keys())
with open(f"{OUTPUT_DIR}/HiringData_Flat.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(final_rows)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 12 — SUMMARY REPORT
# ═════════════════════════════════════════════════════════════════════════════
stage_c  = Counter(r["HireStage"] for r in all_rows)
offered  = stage_c["Offered"] + stage_c["Hired"]
hired    = stage_c["Hired"]

print(f"""
{'='*55}
  GENERATION COMPLETE
{'='*55}
  HiringData_Flat.csv : {len(final_rows):>6} rows | {len(fields)} columns
  HeadcountPlan.csv   : {len(hcp_rows):>6} rows
  SourceCosts.csv     : {len(sc_rows):>6} rows

  Candidate pool      : {len(CAND_POOL)} candidates
  Unique candidates   : {len(set(r['CandidateID'] for r in all_rows))}
  Hired (pool exits)  : {len(hired_candidates)}
  Dirty rows injected : {len(dirty_rows)}

  FUNNEL (clean rows)
  {'─'*30}""")
for s in STAGES:
    print(f"  {s:15s}: {stage_c.get(s,0):>5}")

print(f"""
  Offer acceptance    : {hired}/{offered} = {round(hired/offered*100,1) if offered else 0}%
  Closure errors      : {sum(1 for r in all_rows if r['PostingClosureError']=='Yes')} rows (JOB001+JOB002 only)
  HeadcountPlan total : {total_target} target hires

  JOB POSTING DATES
  {'─'*30}
  Earliest posting    : {min(j['JobPostedDate'] for j in JOB_CATALOGUE)}
  Latest posting      : {max(j['JobPostedDate'] for j in JOB_CATALOGUE)}
  2023 jobs           : {sum(1 for j in JOB_CATALOGUE if j['JobPostedDate'].year==2023)}
  2024 jobs           : {sum(1 for j in JOB_CATALOGUE if j['JobPostedDate'].year==2024)}
  2025 jobs           : {sum(1 for j in JOB_CATALOGUE if j['JobPostedDate'].year==2025)}
  2026 jobs           : {sum(1 for j in JOB_CATALOGUE if j['JobPostedDate'].year==2026)}

  FILES SAVED TO: {OUTPUT_DIR}
{'='*55}
""")
