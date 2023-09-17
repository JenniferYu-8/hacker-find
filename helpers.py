import sqlite3

WEIGHT1 = 0.5
WEIGHT2 = 0.3
WEIGHT3 = 0.1
ADJUST_FACTOR = 8

languages = {"Python": 1, "Ruby": 2, "JavaScript": 3, "TypeScript": 4, "CoffeeScript": 5, "Kotlin": 6, "Java": 7, "C#": 8, "Swift": 9, "Objective-C": 10}
specialties = {"Full-Stack": 1, "Front-End": 2, "Back-End": 3, "Mobile-App": 4, "Blockchain": 5, "IoT": 6, "Hardware": 7, "AI": 8, "Data-Science": 9, "Machine-Learning": 10, "Data-Engineer": 11}
comms = {"Low": 1, "Med": 2, "High": 3, "Hardcore": 4}

# The expectations from a search
def compute_expected(lang, spec, exp, commitment):
    return lang + spec * 2 + exp * 3 + commitment * 3


# Add Hacker to database and set their weighted sum
def input_hacker(name, langs, specs, exp, commitment):
    con = sqlite3.connect("hackers.db")
    cur = con.cursor()

    lang1 = languages[langs[0]]
    lang2 = languages[langs[1]]
    lang3 = languages[langs[2]]

    spec1 = specialties[specs[0]]
    spec2 = specialties[specs[1]]
    spec3 = specialties[specs[2]]

    comm = comms[commitment]

    weighted_sum = (lang1 * WEIGHT1 + lang2 * WEIGHT2 + lang3 * WEIGHT3) + (spec1 * WEIGHT1 + spec2 * WEIGHT2 + spec3 * WEIGHT3) * 2 + exp * 3 + comm * 3

    cur.execute("INSERT INTO hackers (name, lang1, lang2, lang3, spec1, spec2, spec3, experience, commitment, sum) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", name, lang1, lang2, lang3, spec1, spec2, spec3, exp, comm, weighted_sum)

    cur.close()
    con.close()

# Find Compatable Hackers
def find_hackers(expected):

    con = sqlite3.connect("hackers.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM hackers WHERE sum BETWEEN ? AND ?", expected - ADJUST_FACTOR, expected + ADJUST_FACTOR)
    results = cur.fetchall()

    cur.close()
    con.close()

    return results

# Let someone add a preference
def add_pref(host_id, pref_id):
    con = sqlite3.connect("hackers.db")
    cur = con.cursor()

    cur.execute("INSERT INTO preferred (host, pref) VALUES (?, ?)", host_id, pref_id)

    cur.close()
    con.close()