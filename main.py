import db
from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
import random
import string
from datetime import date, datetime
from weasyprint import HTML
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import tempfile

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))


# Page d'accueil - redirection vers employé ou propriétaire
@app.route('/', methods=['GET', 'POST'])
@app.route('/accueil', methods=['GET', 'POST'])
def accueil():
    if request.method == "POST":
        # si c'est un proprio on va vers la page proprio sinon employé
        if request.form.get('mode') == 'prop':
            return redirect(url_for('propconnex'))
        else:
            return redirect(url_for('emp'))
    return render_template('accueil.html')


# Connexion des employés (vétérinaires)
@app.route('/emp', methods=['GET', 'POST'])
def emp():
    erreur = None
    if request.method == "POST":
        loginn = request.form.get("login")
        mdps = request.form.get("mdp")

        with db.connect() as conn:
            with conn.cursor() as cur:
                # chercher l'employé avec son login
                cur.execute('SELECT * FROM employes WHERE loginn=%s', (loginn,))
                empl = cur.fetchone()

                if empl is None:
                    return render_template('connexemp.html', erreur="Identifiants incorrects.")

                # vérifier le mot de passe
                if bcrypt.check_password_hash(empl.mdp, mdps):
                    # mettre les infos dans la session
                    session['loginn'] = loginn
                    session['mat'] = empl.matricule
                    session['idcentre'] = empl.idcentre
                    return redirect(url_for('pageemp'))
                else:
                    return render_template('connexemp.html', erreur="Mot de passe incorrect.")

    return render_template('connexemp.html')


# Page principale de l'employé avec ses animaux
@app.route('/pageemp')
def pageemp():
    # vérif si connecté
    if 'mat' not in session:
        return redirect(url_for('emp'))

    with db.connect() as conn:
        with conn.cursor() as cur:
            # récup les infos de l'employé
            cur.execute('SELECT * FROM employes WHERE matricule=%s', (session['mat'],))
            result = cur.fetchone()

            # si pas de centre affecté
            if not result.idcentre:
                return render_template('pageemp.html', res=result, animaux=[], centre=None, ville=None, dirigeant=None)

            # récup infos du centre
            cur.execute('SELECT * FROM centre WHERE idcentre=%s', (result.idcentre,))
            centre = cur.fetchone()

            # récup le dirigeant du centre
            cur.execute('SELECT * FROM employes WHERE matricule=%s', (centre.matricule,))
            dirigeant = cur.fetchone()

            # récup la ville du centre
            cur.execute('SELECT * FROM ville WHERE idville=%s', (centre.idville,))
            ville = cur.fetchone()

            # récup tous les animaux du centre
            cur.execute('''
                SELECT a.ida, a.nom, a.espece, a.age, a.sexe, a.signedist,
                       p.nom AS nom_pro, p.prenom AS prenom_pro
                FROM animal a
                JOIN inscrit i ON i.ida = a.ida
                JOIN propri p ON p.idpro = a.idpro
                WHERE i.idcentre = %s
                ORDER BY a.espece, a.nom
            ''', (result.idcentre,))
            animaux = cur.fetchall()

            return render_template('pageemp.html',
                res=result, centre=centre, ville=ville,
                dirigeant=dirigeant, animaux=animaux)


# Fiche détaillée d'un animal pour le vétérinaire
@app.route('/animal/<ida>')
def ficheanimalemp(ida):
    if 'mat' not in session:
        return redirect(url_for('emp'))

    with db.connect() as conn:
        with conn.cursor() as cur:
            # récup l'animal
            cur.execute('SELECT * FROM animal WHERE ida=%s', (ida,))
            animal = cur.fetchone()
            if animal is None:
                return redirect(url_for('pageemp'))

            # récup le propriétaire
            cur.execute('SELECT * FROM propri WHERE idpro=%s', (animal.idpro,))
            propri = cur.fetchone()

            # récup tous les soins de cet animal
            cur.execute('''
                SELECT o.dateop, o.nature, o.historique, e.prenom, e.nom AS nom_emp
                FROM opere o
                JOIN employes e ON e.matricule = o.matricule
                WHERE o.ida = %s
                ORDER BY o.dateop DESC
            ''', (ida,))
            soins = cur.fetchall()

    return render_template('ficheanimalemp.html', animal=animal, propri=propri, soins=soins)


# Ajouter un nouveau soin pour un animal
@app.route('/soin/ajouter', methods=['POST'])
def ajouter_soin():
    if 'mat' not in session:
        return redirect(url_for('emp'))

    ida = request.form.get('ida')
    nature = request.form.get('nature')
    historique = request.form.get('historique')
    idcentre = session.get('idcentre')

    with db.connect() as conn:
        with conn.cursor() as cur:
            # ajouter le soin avec la date d'aujourd'hui
            cur.execute('''
                INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (idcentre, ida, matricule)
                DO UPDATE SET
                    dateop = EXCLUDED.dateop,
                    nature = EXCLUDED.nature,
                    historique = opere.historique || E'\n--- ' || EXCLUDED.dateop::text || ' ---\n' || EXCLUDED.historique
            ''', (idcentre, ida, session['mat'], date.today(), nature, historique))

    return redirect(url_for('ficheanimalemp', ida=ida))


# Enregistrer un nouvel animal dans la base
@app.route('/animal/ajouter', methods=['GET', 'POST'])
def ajouter_animal():
    if 'mat' not in session:
        return redirect(url_for('emp'))

    # vérif que l'employé a un centre
    if not session.get('idcentre'):
        return redirect(url_for('pageemp'))

    if request.method == "POST":
        nom = request.form.get('nom')
        espece = request.form.get('espece')
        age = request.form.get('age')
        sexe = request.form.get('sexe')
        signedist = request.form.get('signedist')
        idpro = request.form.get('idpro')
        inscrire_centre = request.form.get('inscrire_centre')

        # vérif que les champs obligatoires sont remplis
        if not nom or not espece or not sexe or not idpro:
            with db.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT idpro, nom, prenom, tel, mail FROM propri ORDER BY nom, prenom')
                    proprietaires = cur.fetchall()
            return render_template('ajout_animal.html', 
                proprietaires=proprietaires,
                erreur="Veuillez remplir tous les champs obligatoires.")

        with db.connect() as conn:
            with conn.cursor() as cur:
                # générer un ID aléatoire unique pour l'animal
                while True:
                    ida = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    cur.execute('SELECT 1 FROM animal WHERE ida=%s', (ida,))
                    if cur.fetchone() is None:
                        break

                # insérer l'animal en base
                cur.execute("""
                    INSERT INTO animal (ida, nom, espece, age, sexe, signedist, idpro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (ida, nom, espece, age if age else None, sexe, signedist, idpro))

                # inscrire l'animal dans le centre si demandé
                if inscrire_centre and session.get('idcentre'):
                    cur.execute("""
                        INSERT INTO inscrit (idcentre, ida)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (session['idcentre'], ida))

        return render_template('ajout_animal.html',
            proprietaires=[],
            succes=True,
            ida_cree=ida)

    # afficher le formulaire avec la liste des proprios
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT idpro, nom, prenom, tel, mail FROM propri ORDER BY nom, prenom')
            proprietaires = cur.fetchall()

    return render_template('ajout_animal.html', proprietaires=proprietaires)


# Créer un compte propriétaire
@app.route('/creer/proprietaire', methods=['GET', 'POST'])
def creer_proprietaire():
    if request.method == "POST":
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        tel = request.form.get('tel')
        mail = request.form.get('mail')
        adresse = request.form.get('adresse')

        # vérif que tout est rempli
        if not nom or not prenom or not tel or not mail or not adresse:
            return render_template('creation_proprietaire.html', 
                erreur="Veuillez remplir tous les champs obligatoires.")

        # vérif que le tel a 10 chiffres
        if not tel.isdigit() or len(tel) != 10:
            return render_template('creation_proprietaire.html',
                erreur="Le numéro de téléphone doit contenir exactement 10 chiffres.")

        with db.connect() as conn:
            with conn.cursor() as cur:
                # vérif si mail ou tel existe déjà
                cur.execute('SELECT 1 FROM propri WHERE mail=%s OR tel=%s', (mail, tel))
                if cur.fetchone():
                    return render_template('creation_proprietaire.html',
                        erreur="Un compte existe déjà avec cet email ou numéro de téléphone.")

                # générer un ID unique (P + 9 chiffres)
                while True:
                    idpro = 'P' + ''.join(random.choices(string.digits, k=9))
                    cur.execute('SELECT 1 FROM propri WHERE idpro=%s', (idpro,))
                    if cur.fetchone() is None:
                        break

                # créer le compte
                cur.execute("""
                    INSERT INTO propri (idpro, nom, prenom, tel, mail, adresse)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (idpro, nom, prenom, tel, mail, adresse))

        return render_template('succes_proprietaire.html',
            idpro=idpro, nom=nom, prenom=prenom, mail=mail, tel=tel)

    return render_template('creation_proprietaire.html')


# Créer un compte employé (vétérinaire)
@app.route('/creer', methods=['GET', 'POST'])
def creeruncompte():
    if request.method == "POST":
        prenom = request.form.get("prenom")
        nom = request.form.get("nom")
        adresse = request.form.get("adresse")
        tel = request.form.get("tel")
        naissance = request.form.get("naissance")
        numsec = request.form.get("numsec")
        loginn = request.form.get("loginn")
        mdp = request.form.get("mdp")
        idcentre_raw = request.form.get("idcentre")
        idcentre = int(idcentre_raw) if idcentre_raw else 0
        # hasher le mot de passe pour la sécurité
        mdphashed = bcrypt.generate_password_hash(mdp).decode('utf-8')

        with db.connect() as conn:
            with conn.cursor() as cur:
                # générer un matricule unique (1 lettre + 4 chiffres)
                while True:
                    lettre = random.choice(string.ascii_lowercase)
                    chiffres = ''.join(random.choices(string.digits, k=4))
                    matricule = lettre + chiffres
                    cur.execute('SELECT 1 FROM employes WHERE matricule=%s', (matricule,))
                    if cur.fetchone() is None:
                        break

                # créer le compte employé
                cur.execute("""
                    INSERT INTO employes
                    (matricule, prenom, nom, adresse, tel, naissance, numsec, loginn, mdp, idcentre)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (matricule, prenom, nom, adresse, tel, naissance, numsec, loginn, mdphashed, idcentre))

        return render_template('succes_creation.html', matricule=matricule, prenom=prenom)

    # afficher le formulaire avec la liste des centres
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT idcentre, nomcentre FROM centre ORDER BY nomcentre')
            centres = cur.fetchall()
    return render_template('creation.html', centres=centres)


# Connexion propriétaire
@app.route('/connexionprop', methods=['GET', 'POST'])
def propconnex():
    if request.method == "POST":
        email = request.form.get("username")
        num = request.form.get("numero")
        ida = request.form.get("id_animal")

        with db.connect() as conn:
            with conn.cursor() as cur:
                # vérif email et tel
                cur.execute('SELECT * FROM propri WHERE mail=%s AND tel=%s', (email, num))
                propri = cur.fetchone()

                if propri is None:
                    return render_template('connexprop.html', erreur="Propriétaire introuvable, veuillez recommencer.")

                # vérif que l'animal existe et appartient bien au proprio
                cur.execute('SELECT * FROM animal WHERE idpro=%s AND ida=%s', (propri.idpro, ida))
                anim = cur.fetchone()

                if anim is None:
                    return render_template('connexprop.html', erreur="Animal introuvable, veuillez recommencer.")

                # mettre les infos dans la session
                session['id'] = propri.idpro
                session['email'] = email
                session['num'] = num
                session['ida'] = ida

                return redirect(url_for('pageprop'))

    return render_template('connexprop.html')


# Page principale du propriétaire avec son animal
@app.route('/pageprop')
def pageprop():
    if 'ida' not in session:
        return redirect(url_for('propconnex'))

    with db.connect() as conn:
        with conn.cursor() as cur:
            # récup l'animal
            cur.execute('SELECT * FROM animal WHERE ida=%s', (session['ida'],))
            anim = cur.fetchone()

            # récup les centres où l'animal est inscrit
            cur.execute('''
                SELECT c.nomcentre, c.adresse, c.matricule
                FROM inscrit i
                JOIN centre c ON c.idcentre = i.idcentre
                WHERE i.ida = %s
            ''', (session['ida'],))
            centresoins = cur.fetchall()

            # récup le dirigeant du centre
            dirigeant = None
            if centresoins:
                cur.execute('SELECT * FROM employes WHERE matricule=%s', (centresoins[0].matricule,))
                dirigeant = cur.fetchone()

            # récup l'historique des soins
            cur.execute('''
                SELECT o.dateop, o.nature, o.historique, e.prenom, e.nom AS nom_emp, c.nomcentre
                FROM opere o
                JOIN employes e ON e.matricule = o.matricule
                JOIN centre c ON c.idcentre = o.idcentre
                WHERE o.ida = %s
                ORDER BY o.dateop DESC
            ''', (session['ida'],))
            soins = cur.fetchall()

            return render_template('pageprop.html', anim=anim,
                centresoins=centresoins, dirigeant=dirigeant, soins=soins)


# Modifier les infos de l'animal (proprio seulement)
@app.route('/changer', methods=['GET', 'POST'])
def modif():
    if 'ida' not in session:
        return redirect(url_for('propconnex'))

    if request.method == "POST":
        col = request.form.get("tochange")
        valeur = request.form.get("valeur")

        with db.connect() as conn:
            with conn.cursor() as cur:
                # modifier selon le champ choisi
                if col == 'nom':
                    cur.execute("UPDATE animal SET nom=%s WHERE ida=%s", (valeur, session['ida']))
                elif col == 'age':
                    cur.execute("UPDATE animal SET age=%s WHERE ida=%s", (valeur, session['ida']))
                elif col == 'signedist':
                    cur.execute("UPDATE animal SET signedist=%s WHERE ida=%s", (valeur, session['ida']))

        return redirect(url_for('pageprop'))

    return render_template('modifications.html')


# Générer le PDF de la fiche de l'animal
@app.route('/pdf')
def pdf():
    if 'ida' not in session or 'id' not in session:
        return redirect(url_for('propconnex'))

    with db.connect() as conn:
        with conn.cursor() as cur:
            # récup l'animal
            cur.execute('SELECT * FROM animal WHERE ida=%s', (session['ida'],))
            anim = cur.fetchone()
            if anim is None:
                return redirect(url_for('propconnex'))

            # récup le proprio
            cur.execute('SELECT nom, prenom, tel, mail FROM propri WHERE idpro=%s', (session['id'],))
            prop = cur.fetchone()

            # récup les centres
            cur.execute('''
                SELECT c.nomcentre, c.adresse, c.tel, c.specialite
                FROM inscrit i JOIN centre c ON c.idcentre = i.idcentre
                WHERE i.ida = %s
            ''', (session['ida'],))
            centresoins = cur.fetchall()

            # récup le dirigeant
            dirigeant = None
            if centresoins:
                cur.execute('''
                    SELECT e.*, c.matricule as mat_centre
                    FROM centre c
                    JOIN employes e ON e.matricule = c.matricule
                    JOIN inscrit i ON i.idcentre = c.idcentre
                    WHERE i.ida = %s
                    LIMIT 1
                ''', (session['ida'],))
                dirigeant = cur.fetchone()

            # récup l'historique complet
            cur.execute('''
                SELECT o.dateop, o.nature, o.historique, 
                       e.prenom, e.nom AS nom_emp, c.nomcentre
                FROM opere o
                JOIN employes e ON e.matricule = o.matricule
                JOIN centre c ON c.idcentre = o.idcentre
                WHERE o.ida = %s
                ORDER BY o.dateop DESC
            ''', (session['ida'],))
            soins = cur.fetchall()

    # générer le HTML du PDF
    html_content = render_template(
        'fichepdf.html',
        anim=[anim],
        prop=prop,
        centresoins=centresoins,
        dirigeant=[dirigeant] if dirigeant else None,
        soins=soins,
        date_generation=datetime.now().strftime("%d/%m/%Y à %H:%M")
    )

    # créer le PDF dans un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', mode='wb') as tmp_file:
        pdf_path = tmp_file.name
        HTML(string=html_content, base_url=request.url_root).write_pdf(tmp_file)

    # nom du fichier à télécharger
    filename = f"fiche_{anim.nom or 'animal'}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


# Déconnexion (employé ou proprio)
@app.route('/deconnecter')
def deconnecter():
    session.clear()
    return redirect(url_for('accueil'))


# Page invité pour voir les centres
@app.route('/invite')
def inv():
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT nomcentre, codepostale FROM centre, ville WHERE centre.idville = ville.idville')
            liste = cur.fetchall()
            return render_template('invite.html', liste=liste)


# Détails d'un centre spécifique
@app.route("/invite/<codepostale>/<nomcentre>")
def info(codepostale, nomcentre):
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT adresse, tel, specialite, codepostale, nomcentre, centre.idcentre
                FROM centre
                JOIN ville ON centre.idville = ville.idville
                WHERE codepostale=%s AND nomcentre=%s
            """, (codepostale, nomcentre))
            res = cur.fetchall()
    return render_template('infocentre.html', res=res, elt=codepostale, l=len(res), nom=nomcentre)


if __name__ == '__main__':
    app.run(debug=True)