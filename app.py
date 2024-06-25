from sqlite3 import IntegrityError
from flask import Flask, flash, render_template, request, redirect, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_donnees.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin.admin@Admin-isi.utm.tn' and password == 'admin':
           
           
            session['admin'] = True
            return redirect(url_for('index'))
        else:
            session.pop('admin', None) 
            if "@etudiant-isi.utm.tn" in username:
                nom_prenom = username.split('@')[0].split('.')
                if len(nom_prenom) == 2:
                    nom = nom_prenom[0]
                    prenom = nom_prenom[1]
                    etudiant = Etd.query.filter_by(nom=nom, prenom=prenom).first()
                    if etudiant and etudiant.carte_number == password:
                        return redirect(url_for('emploi_du_temps', nom=nom, prenom=prenom))
            
            flash("Nom d'utilisateur ou mot de passe invalide.", "error")
            return render_template('login.html')
    
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))







class Etd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    carte_number = db.Column(db.String(100))
    classe = db.Column(db.String(100))
 
  
  
  

@app.route('/rechercher_etudiant', methods=['POST'])
def rechercher_etudiant():
    nom_recherche = request.json.get('nom_recherche')
    etudiants_trouves = Etd.query.filter_by(nom=nom_recherche).all()
    return jsonify([{
        'nom': etudiant.nom,
        'prenom': etudiant.prenom,
        'contact': etudiant.contact,
        'carte_number': etudiant.carte_number
    } for etudiant in etudiants_trouves])

  
  
  
  

@app.route('/etd', methods=['GET', 'POST'])
def etd():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        contact = request.form['contact']
        carte_number = request.form['carte_number']
        classe = request.form['classe']
        
       
        if Etd.query.filter((Etd.contact == contact) | (Etd.carte_number == carte_number)).first():
            flash('Étudiant non ajouté. Le numéro de carte ou le contact existe déjà.', 'danger')
        else:
            etudiant = Etd(nom=nom, prenom=prenom, contact=contact, carte_number=carte_number, classe=classe)
            db.session.add(etudiant)
            db.session.commit()
            flash('Étudiant ajouté avec succès !', 'success')
    etudiants = Etd.query.all()
    return render_template('etudiant.html', etudiants=etudiants)


@app.route('/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_etudiant(id):
    etudiant = Etd.query.get_or_404(id)
    if request.method == 'POST':
       
        etudiant.nom = request.form['nom']
        etudiant.prenom = request.form['prenom']
        etudiant.contact = request.form['contact']
        etudiant.carte_number = request.form['carte_number']
        
        db.session.commit()
        flash('Étudiant modifié avec succès !', 'success')
        return redirect(url_for('etd'))
    return render_template('modifier_etudiant.html', etudiant=etudiant)



@app.route('/delete/<int:id>', methods=['POST'])
def delete_etudiant(id):
    etudiant = Etd.query.get_or_404(id)
    db.session.delete(etudiant)
    db.session.commit()
    flash('Étudiant supprimé avec succès !', 'success')
    return redirect(url_for('etd'))

@app.route('/chercher_emploi', methods=['POST'])
def chercher_emploi():
    if 'classe' not in request.form:
        return "Classe non spécifiée", 400
    
    classe = request.form['classe']
    
    
    emploi_seances = []
    if classe:
        emploi_seances = Seance.query.filter_by(classe=classe).all()
    else:
        emploi_seances = Seance.query.all()
    
    return render_template('emploi_du_temps.html', seances=[], emploi_seances=emploi_seances)








@app.route('/reinitialiser_table', methods=['POST'])
def reinitialiser_table():
    
    toutes_les_seances = Seance.query.all()
    return render_template('emploi_du_temps.html', seances=toutes_les_seances)


@app.route('/supprimer_seance', methods=['POST'])
def supprimer_seance():
   
    data = request.get_json()
    seance_id = data.get('id')
    
    
    seance = Seance.query.get(seance_id)
    
 
    if seance:
        
        db.session.delete(seance)
        db.session.commit()
       
        return jsonify({'message': 'Séance supprimée avec succès.'}), 200
    else:
       
        return jsonify({'message': 'Séance non trouvée.'}), 404









@app.route('/chercher_seances', methods=['POST'])
def chercher_seances():
    classe = request.form['classe']
    matiere = request.form.get('matiere')
    
 
    seances = []
    if classe and matiere:
        seances = Seance.query.filter_by(classe=classe, matiere=matiere).all()
    elif classe:
        seances = Seance.query.filter_by(classe=classe).all()
    else:
        seances = Seance.query.all()
    
    return render_template('emploi_du_temps.html', seances=seances, emploi_seances=[])















@app.route('/supprimer_enseignant', methods=['POST'])
def supprimer_enseignant():
    matricule = request.form['matricule']
    # Fetch the teacher from the database based on the matricule
    enseignant = Enseignant.query.filter_by(matricule=matricule).first()
    
    # Check if the teacher exists
    if enseignant:
        # Delete the teacher's record from the database
        db.session.delete(enseignant)
        db.session.commit()
        return jsonify({'message': 'Enseignant supprimé avec succès.'}), 200
    else:
        return jsonify({'message': "Enseignant non trouvé."}), 404





@app.route('/modifier_enseignant', methods=['POST'])
def modifier_enseignant():
    matricule = request.form['matricule']
    enseignant = Enseignant.query.filter_by(matricule=matricule).first()
    
    if enseignant:
        enseignant.nom = request.form['nom']
        enseignant.contact = request.form['contact']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return jsonify({'message': "Enseignant non trouvé."}), 404



@app.route('/chercher_enseignant', methods=['POST'])
def chercher_enseignant():
    nom_enseignant = request.json.get('nom')  
    
    enseignant_trouve = chercher_enseignant_dans_bd(nom_enseignant)
    
    
    if enseignant_trouve:
        return jsonify({'message': 'Enseignant trouvé.'}), 200
    else:
        return jsonify({'message': "Enseignant non trouvé."}), 404

def chercher_enseignant_dans_bd(nom_enseignant):

    enseignant_trouve = Enseignant.query.filter_by(nom=nom_enseignant).first()
    
    
    if enseignant_trouve:
        return True
    else:
        return False



class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)

class Seance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classe = db.Column(db.String(10), nullable=False)
    matiere = db.Column(db.String(100), nullable=False)
    jour = db.Column(db.String(10), nullable=False)
    heure = db.Column(db.String(20), nullable=False)
    nom_enseignant = db.Column(db.String(100), nullable=False)
    contact_enseignant = db.Column(db.String(20), nullable=False)

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/index')
def index():
    enseignants = Enseignant.query.all()
    seances = Seance.query.all()
    return render_template('index.html', enseignants=enseignants, seances=seances)





@app.route('/emploi_du_temps')
def emploi_du_temps():
    seances = Seance.query.all()
    return render_template('emploi_du_temps.html', seances=seances)

@app.route('/enregistrer_enseignant', methods=['POST'])
def enregistrer_enseignant():
    matricule = request.form['matricule']
    nom = request.form['nom']
    contact = request.form['contact']
    
    
    existing_enseignant = Enseignant.query.filter_by(matricule=matricule).first()
    if existing_enseignant:
        return "Error: Teacher with matricule {} already exists.".format(matricule)
    
    nouvel_enseignant = Enseignant(matricule=matricule, nom=nom, contact=contact)
    db.session.add(nouvel_enseignant)
    db.session.commit()
    
    if nouvel_enseignant.id:
        print("Enseignant enregistré avec succès !")
    else:
        print("Erreur lors de l'enregistrement de l'enseignant.")
    
    return redirect(url_for('index'))



@app.route('/enregistrer_seance', methods=['POST'])
def enregistrer_seance():
    classe = request.form['classe']
    matiere = request.form['matiere']
    jour = request.form['jour']
    heure = request.form['heure']
    matricule_enseignant = request.form['matricule-enseignant']
    
    enseignant = Enseignant.query.filter_by(matricule=matricule_enseignant).first()
    
    if enseignant:
        nouvelle_seance = Seance(
            classe=classe,
            matiere=matiere,
            jour=jour,
            heure=heure,
            nom_enseignant=enseignant.nom,
            contact_enseignant=enseignant.contact
        )
        db.session.add(nouvelle_seance)
        db.session.commit()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
         db.create_all()
         
    app.secret_key = 'votre_clé_secrète'
    app.run(debug=True,  host='0.0.0.0')
