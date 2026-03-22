import subprocess
import os

WORDS = [
    "Apple", "Book", "Day", "Dead", "Die", "Finger", "Give", "Glass", 
    "Gold", "Hand", "Head", "Moon", "Night", "Old", "Snow", "Stone", 
    "Two", "Who", "Sun", "Water"
]

LANGUAGES = [
    "Latin", "Sardinian", "Dalmatian", "Aromanian", "Gascon", "Catalan", 
    "French", "Italian", "Spanish", "Portuguese", "Romanian", "Romansh", 
    "Walloon", "Aragonese", "Asturian", "Lombard", "Occitan", "Sicilian", 
    "Venetian", "Picard", "Piedmontese", "Mirandese", "Haitian"
]

DATA = {
    "Apple": ["Malum", "Mela", "Miela", "Mearã", "Poma", "Poma", "Pomme", "Mela", "Manzana", "Maçã", "Măr", "Mail", "Peme", "Mazana", "Mazana", "Pomm", "Poma", "Pumu", "Pomo", "Ponme", "Pom", "Maçana", "Ponm"],
    "Book": ["Liber", "Lìberu", "Libro", "Cati", "Libe", "Llibre", "Livre", "Libro", "Libro", "Livro", "Carte", "Cudesch", "Live", "Libro", "Llibru", "Libro", "Libre", "Libbru", "Libro", "Libe", "Lìber", "Lhibro", "Liv"],
    "Day": ["Dies", "Die", "Dii", "Dzuã", "Dia", "Dia", "Jour", "Giorno", "Día", "Dia", "Zi", "Di", "Djoû", "Día", "Día", "Dì", "Jorn", "Jornu", "Dì", "Djou", "Dì", "Dien", "Jou"],
    "Dead": ["Mortuus", "Mortu", "Muart", "Mortu", "Mort", "Mort", "Mort", "Morto", "Muerto", "Morto", "Mort", "Mort", "Moirt", "Muerto", "Muertu", "Mort", "Mòrt", "Mortu", "Morto", "Mort", "Mòrt", "Muorto", "Mouri"],
    "Die": ["Mori", "Mòrrere", "Morar", "Moredz", "Morir", "Morir", "Mourir", "Morire", "Morir", "Morrer", "Muri", "Morir", "Mori", "Morir", "Morrer", "Morì", "Morir", "Mòriri", "Morir", "Mourir", "Meure", "Morrir", "Mouri"],
    "Finger": ["Digitus", "Dìdidu", "Dit", "Dzidit", "Det", "Dit", "Doigt", "Dito", "Dedo", "Dedo", "Deget", "Det", "Doet", "Dido", "Dedu", "Dii", "Det", "Jìditu", "Dèo", "Doét", "Dì", "Dedo", "Dwèt"],
    "Give": ["Dare", "Dare", "Dar", "Dau", "Dar", "Donar", "Donner", "Dare", "Dar", "Dar", "Da", "Dar", "Dner", "Dar", "Dar", "Dà", "Donar", "Dari", "Dar", "Donner", "Dè", "Dar", "Bayo"],
    "Glass": ["Vitrum", "Bidru", "Vitro", "Yilii", "Veire", "Vidre", "Verre", "Vetro", "Vidrio", "Vidro", "Sticlă", "Vider", "Vere", "Veire", "Vidru", "Veder", "Veire", "Vitru", "Vero", "Vèr", "Véder", "Bídrio", "Vè"],
    "Gold": ["Aurum", "Oru", "Iaur", "Auru", "Aur", "Or", "Or", "Oro", "Oro", "Ouro", "Aur", "Aur", "Ôr", "Oro", "Oru", "Or", "Aur", "Oru", "Oro", "Or", "Òr", "Ouro", "Lò"],
    "Hand": ["Manus", "Manu", "Muan", "Mânã", "Man", "Mà", "Main", "Mano", "Mano", "Mão", "Mână", "Maun", "Mwin", "Man", "Mano", "Man", "Man", "Manu", "Man", "Main", "Man", "Mano", "Men"],
    "Head": ["Caput", "Conca", "Cup", "Cap", "Cap", "Cap", "Tête", "Testa", "Cabeza", "Cabeça", "Cap", "Tgau", "Tiesse", "Cabo", "Cabeza", "Coo", "Cap", "Testa", "Cao", "Tête", "Cra", "Cabeça", "Tèt"],
    "Moon": ["Luna", "Luna", "Loina", "Lunã", "Lua", "Lluna", "Lune", "Luna", "Luna", "Lua", "Lună", "Glina", "Lune", "Luna", "Lluna", "Luna", "Luna", "Luna", "Luna", "Leune", "Lun-a", "Lhuna", "Lalin"],
    "Night": ["Nox", "Note", "Nuat", "Noapti", "Nueit", "Nit", "Nuit", "Notte", "Noche", "Noite", "Noapte", "Notg", "Nute", "Nueit", "Nueche", "Notch", "Nuèch", "Notti", "Note", "Nuit", "Neuit", "Nuite", "Nwit"],
    "Old": ["Vetus", "Betzu", "Viec", "Veclju", "Vielh", "Vell", "Vieux", "Vecchio", "Viejo", "Velho", "Vechi", "Vegl", "Vî", "Viello", "Vieyu", "Vegg", "Vièlh", "Vecchiu", "Vecio", "Viu", "Vej", "Bielho", "Vye"],
    "Snow": ["Nix", "Nie", "Nai", "Neauã", "Nèu", "Neu", "Neige", "Neve", "Nieve", "Neve", "Zăpadă", "Naiv", "Nive", "Nieu", "Nieve", "Nev", "Nèu", "Nivi", "Neve", "Niche", "Fiòca", "Niebe", "Nèj"],
    "Stone": ["Petra", "Pera", "Pitra", "Chiatra", "Pèira", "Pedra", "Pierre", "Pietra", "Piedra", "Pedra", "Piatră", "Crap", "Pire", "Piedra", "Piedra", "Pria", "Pèira", "Petra", "Piera", "Pièrre", "Pera", "Piedra", "Wòch"],
    "Two": ["Duo", "Duos", "Doi", "Doi", "Dus", "Dos", "Deux", "Due", "Dos", "Dois", "Doi", "Dus", "Deus", "Dos", "Dos", "Du", "Dos", "Dui", "Do", "Deus", "Doi", "Dous", "De"],
    "Who": ["Quis", "Chie", "Cui", "Cari", "Qui", "Qui", "Qui", "Chi", "Quién", "Quem", "Cine", "Tgi", "Kî", "Quí", "Quien", "Chi", "Quau", "Cui", "Chi", "Qui", "Chi", "Quien", "Ki"],
    "Sun": ["Sol", "Sole", "Saul", "Soari", "Sorelh", "Sol", "Soleil", "Sole", "Sol", "Sol", "Soare", "Sulegl", "Solea", "Sol", "Sol", "Sol", "Solelh", "Suli", "Sołe", "Solé", "Sol", "Sol", "Solèy"],
    "Water": ["Aqua", "Abba", "Acu", "Apã", "Aiga", "Aigua", "Eau", "Acqua", "Agua", "Água", "Apă", "Aua", "Aiwe", "Auga", "Agua", "Acqua", "Aiga", "Acqua", "Acua", "Iau", "Eva", "Auga", "Dlo"]
}

def main():
    print("Generating TeX with full linguistic data...")
    tex_file = 'docs/grammar/latin_word_zoo.tex'
    
    with open(tex_file, 'w') as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage[margin=0.2in, landscape]{geometry}\n") # Landscape and smaller margins to fit everything
        f.write("\\usepackage{booktabs}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage[utf8]{inputenc}\n")
        f.write("\\begin{document}\n")
        f.write("\\title{Latin Word Zoo: Comparative Romance Vocabulary}\n")
        f.write("\\date{}\n")
        f.write("\\maketitle\n")
        f.write("\\noindent A comparison of 20 common words across 22 varied Romance languages (plus Haitian Kreyol). Generated via expert linguistic data.\\\\[1em]\n")
        
        f.write("\\begin{table}[h!]\n")
        f.write("\\centering\n")
        f.write("\\resizebox{\\textwidth}{!}{\n")
        f.write("\\begin{tabular}{l" + "l" * len(LANGUAGES) + "}\n")
        f.write("\\toprule\n")
        
        f.write("\\textbf{English} & " + " & ".join(f"\\textbf{{{l}}}" for l in LANGUAGES) + " \\\\\n")
        f.write("\\midrule\n")
        
        for w in WORDS:
            row = [w] + DATA[w]
            f.write(" & ".join(row) + " \\\\\n")
            
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("}\n")
        f.write("\\end{table}\n")
        f.write("\\end{document}\n")
        
    print(f"Compiling {tex_file}...")
    
    pdflatex_path = "pdflatex"
    if os.path.exists("/Library/TeX/texbin/pdflatex"):
        pdflatex_path = "/Library/TeX/texbin/pdflatex"
        
    subprocess.run([pdflatex_path, "-output-directory=docs/grammar", tex_file], stdout=subprocess.DEVNULL)
    print("PDF generated at docs/grammar/latin_word_zoo.pdf")

if __name__ == '__main__':
    main()
