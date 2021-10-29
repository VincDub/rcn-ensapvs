import yaml
import os

sources_yaml = yaml.safe_load(open("sources.yaml","r",encoding="utf-8"))

liste_sections_html = []

for logiciel,sources in sources_yaml.items():
    repertoire_logiciel = str.casefold(logiciel)

    if not os.path.isdir(repertoire_logiciel):
        os.mkdir(repertoire_logiciel)

    liste_sections_html.append("""<h1 id="titre">%s</h1>"""%logiciel)

    for section,contenu in sources.items():

        id_section = str.casefold(section).replace(" ","_")

        liste_sous_sections_html = []
        sous_sections_html = []
        for sous_section,liste_tutos in contenu.items():
            id_sous_section = str.casefold(sous_section).replace(" ","_")
            liste_sous_sections_html.append(
                """<li src="%s/%s.html#%s" onclick="afficher(this)">%s</li>"""%(repertoire_logiciel,id_section,id_sous_section,sous_section))

            liste_tutos_html = []
            for suffixe_url,resume in liste_tutos.items():

                liste_resume_html = ["""<li>%s</li>"""%r for r in resume]
                
                if not suffixe_url.startswith("http"):
                    url_complet = "https://www.youtube.com/embed/%s"%suffixe_url
                else:
                    url_complet = suffixe_url

                liste_tutos_html.append("""
                <div class="tuto">
                    <iframe src="%s"></iframe>
                    <ul>
                        %s
                    </ul>
                </div>\n"""%(url_complet,"\n".join(liste_resume_html)))

            sous_sections_html.append("""
            <div id="%s" class="ctn">
            <h1>%s</h1>
            %s
            </div>\n
            """%(id_sous_section,sous_section,"\n".join(liste_tutos_html)))


        liste_sections_html.append("""
        <h2>%s</h2>
        <ul>
            %s
        </ul>\n
        """%(section,"\n".join(liste_sous_sections_html)))    

        fichier_section_html = """
        </head>
            <link rel="stylesheet" href="../style.css">
        </head>
        <body id="section">
        %s
        </body>
        """%"\n".join(sous_sections_html)

        with open("%s/%s.html"%(repertoire_logiciel,id_section),"w",encoding="utf-8") as fichier_section:
            fichier_section.write(fichier_section_html)
            fichier_section.close()


index_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <script type="text/javascript" src="pages.js"></script>
    <title>Ressources Revit</title>
</head>
<body>
    <div id="fond">
        <div id="banniere">
            %s
        </div>
            <iframe id="contenu" src="placeholder.html" frameborder="0"></iframe>
        </div>
    </div>
</body>
</html>
"""%"\n".join(liste_sections_html)

with open("index.html","w",encoding="utf-8") as index:
        index.write(index_html)
        index.close()

