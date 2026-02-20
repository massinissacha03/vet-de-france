-- Base de données VetDeFrance
-- Pour tester la connexion, les mots de passe des employés sont :
--    jean.dupont@vetparis.fr   → dupont123
--    sophie.martin@vetparis.fr → martin456
--    pierre.leroy@vetlyon.fr   → leroy789
--    emma.bernard@vetlyon.fr   → bernard01
--    lucas.petit@vetmarseille.fr → petit234
--    clara.simon@vetmarseille.fr → simon567

-- supprimer les tables si elles existent déjà
DROP TABLE IF EXISTS inscrit CASCADE;
DROP TABLE IF EXISTS opere CASCADE;
DROP TABLE IF EXISTS ordonnance CASCADE;
DROP TABLE IF EXISTS possedspe CASCADE;
DROP TABLE IF EXISTS animal CASCADE;
DROP TABLE IF EXISTS propri CASCADE;
DROP TABLE IF EXISTS historique CASCADE;
DROP TABLE IF EXISTS centre CASCADE;
DROP TABLE IF EXISTS employes CASCADE;
DROP TABLE IF EXISTS specialite CASCADE;
DROP TABLE IF EXISTS ville CASCADE;


-- création des tables

CREATE TABLE employes(
    matricule char(5),
    nom varchar(1000),
    prenom varchar(1000),
    adresse varchar(70),
    tel char(10),
    naissance date,
    numsec char(13),
    embauche date,
    loginn varchar(1000) UNIQUE,
    mdp varchar(1000),
    idcentre int,
    CONSTRAINT matriculePK PRIMARY KEY (matricule)
);

CREATE TABLE specialite(
    idspe varchar(10),
    nom varchar(1000),
    CONSTRAINT idspecialitePK PRIMARY KEY (idspe)
);

CREATE TABLE propri(
    idpro char(10) PRIMARY KEY,
    nom varchar(1000),
    prenom varchar(1000),
    tel char(10),
    adresse varchar(1000),
    mail varchar(1000)
);

CREATE TABLE ville(
    idville char(2) PRIMARY KEY,
    nomville varchar(20),
    codepostale char(5)
);

CREATE TABLE centre(
    idcentre SERIAL PRIMARY KEY,
    nomcentre varchar(1000),
    adresse text,
    tel varchar(10),
    matricule char(5),
    specialite varchar(1000),
    idville char(2)
);

CREATE TABLE possedspe(
    idspe varchar(10),
    matricule char(5),
    PRIMARY KEY(idspe, matricule)
);

CREATE TABLE inscrit(
    ida char(5),
    idcentre int,
    PRIMARY KEY(ida, idcentre)
);

CREATE TABLE animal(
    ida char(5) PRIMARY KEY,
    espece varchar(1000),
    nom varchar(1000),
    age int,
    sexe char(1),
    signedist varchar(1000),
    idpro char(10)
);

CREATE TABLE opere(
    idcentre int,
    ida char(5),
    matricule char(5),
    dateop date,
    nature text,
    historique text,
    PRIMARY KEY (idcentre, ida, matricule)
);

CREATE TABLE ordonnance(
    idpro char(10),
    matricule char(5),
    nompro varchar(1000),
    nomemp varchar(1000),
    dateord date,
    medoc text,
    PRIMARY KEY (idpro, matricule)
);


-- Insertion des villes

INSERT INTO ville (idville, nomville, codepostale) VALUES ('01', 'Paris',     '75001');
INSERT INTO ville (idville, nomville, codepostale) VALUES ('02', 'Lyon',      '69001');
INSERT INTO ville (idville, nomville, codepostale) VALUES ('03', 'Marseille', '13001');


-- Insertion des employés (vétérinaires)
-- (idcentre sera mis à jour après insertion des centres)

INSERT INTO employes (matricule, prenom, nom, adresse, tel, naissance, numsec, embauche, loginn, mdp, idcentre)
VALUES ('j0001','Jean','DUPONT','12 Rue de Rivoli - 75001 - Paris','0612111111','1985-03-14','1850335011114','2018-09-01','jean.dupont@vetparis.fr','$2b$04$eM89Cr4SKsnIvq4NqvuucOc.A2/i8IhuChe7D6CRnu2UYwYLC37g6',1);

INSERT INTO employes (matricule, prenom, nom, adresse, tel, naissance, numsec, embauche, loginn, mdp, idcentre)
VALUES ('j0002','Sophie','MARTIN','8 Avenue de l''Opéra - 75001 - Paris','0623222222','1990-07-22','2900735021115','2020-01-15','sophie.martin@vetparis.fr','$2b$04$Zb.l7SUeuT8foZjgJP4ZIubO6DzpipMrQQ3.5FEXaclbwhFbNc4oS',1);

INSERT INTO employes (matricule, prenom, nom, adresse, tel, naissance, numsec, embauche, loginn, mdp, idcentre)
VALUES ('j0003','Pierre','LEROY','45 Rue de la République - 69001 - Lyon','0634333333','1982-11-05','1821169031116','2015-04-10','pierre.leroy@vetlyon.fr','$2b$04$5yRSIjIr98aidpH5N.FWve.YjYh1CdlNnTh4UH44f8WIS9QyBJwKO',2);

INSERT INTO employes (matricule, prenom, nom, adresse, tel, naissance, numsec, embauche, loginn, mdp, idcentre)
VALUES ('j0004','Emma','BERNARD','3 Place Bellecour - 69001 - Lyon','0645444444','1994-02-18','2940269041117','2021-06-01','emma.bernard@vetlyon.fr','$2b$04$04Xh8cbbQColz97LteWfH.AEL2FI4ukvWjUUwSnhuzbLjwSCUR8SC',2);

INSERT INTO employes (matricule, prenom, nom, adresse, tel, naissance, numsec, embauche, loginn, mdp, idcentre)
VALUES ('j0005','Lucas','PETIT','22 Rue Paradis - 13001 - Marseille','0656555555','1988-09-30','1880913051118','2017-02-20','lucas.petit@vetmarseille.fr','$2b$04$jISlhclKpg5gshDpnEo8K..M/ZeO02gSJ6.Dc4E9LuYhRafShXXKq',3);

INSERT INTO employes (matricule, prenom, nom, adresse, tel, naissance, numsec, embauche, loginn, mdp, idcentre)
VALUES ('j0006','Clara','SIMON','15 Boulevard Longchamp - 13001 - Marseille','0667666666','1992-12-01','2921213061119','2022-03-10','clara.simon@vetmarseille.fr','$2b$04$aIKLNQiTXbNIsiSD6s43b.CMUL5Z2Y9.QKR7.6P81EHz0kng3slA.',3);


-- Insertion des centres vétérinaires

INSERT INTO centre (nomcentre, adresse, tel, matricule, specialite, idville)
VALUES ('Clinique du Parc', '12 Rue de Rivoli', '0140111111', 'j0001', 'Médecine générale', '01');

INSERT INTO centre (nomcentre, adresse, tel, matricule, specialite, idville)
VALUES ('Cabinet Vétérinaire Lyon', '45 Rue de la République', '0472222222', 'j0003', 'Chirurgie des petits animaux', '02');

INSERT INTO centre (nomcentre, adresse, tel, matricule, specialite, idville)
VALUES ('Vétérinaire Marseille Sud', '22 Rue Paradis', '0491333333', 'j0005', 'Cardiologie', '03');


-- Insertion des propriétaires d'animaux

INSERT INTO propri (idpro, nom, prenom, tel, adresse, mail)
VALUES ('p0001','MARTIN','Marie','0612345678','5 Rue des Fleurs - 75001 - Paris','marie.martin@mail.com');

INSERT INTO propri (idpro, nom, prenom, tel, adresse, mail)
VALUES ('p0002','LAMBERT','Paul','0623456789','18 Avenue Victor Hugo - 69001 - Lyon','paul.lambert@mail.com');

INSERT INTO propri (idpro, nom, prenom, tel, adresse, mail)
VALUES ('p0003','THOMAS','Julie','0634567890','32 Allée des Roses - 13001 - Marseille','julie.thomas@mail.com');

INSERT INTO propri (idpro, nom, prenom, tel, adresse, mail)
VALUES ('p0004','GARCIA','Nicolas','0645678901','7 Impasse du Moulin - 75001 - Paris','nicolas.garcia@mail.com');

INSERT INTO propri (idpro, nom, prenom, tel, adresse, mail)
VALUES ('p0005','ROUX','Camille','0656789012','11 Boulevard des Capucines - 69001 - Lyon','camille.roux@mail.com');


-- Insertion des animaux

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0001','Chat','Mimi',3,'f','Pelage blanc, yeux bleus','p0001');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0002','Chien','Rex',5,'m','Tache noire autour de l''oeil droit','p0001');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0003','Chat','Léo',2,'m','Oreille gauche légèrement abîmée','p0002');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0004','Chien','Luna',4,'f','Porte un collier rouge','p0003');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0005','Chat','Nala',1,'f','Très câline, ronronne beaucoup','p0003');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0006','Chien','Max',7,'m','Boiterie légère de la patte avant droite','p0004');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0007','Lapin','Floppy',2,'m','Oreilles tombantes, robe grise','p0004');

INSERT INTO animal (ida, espece, nom, age, sexe, signedist, idpro)
VALUES ('a0008','Chien','Bella',3,'f','Cicatrice sur le ventre (opération)','p0005');


-- Inscription des animaux dans les centres
-- centre 1 = Clinique du Parc (Paris)    → a0001, a0002, a0005
-- centre 2 = Cabinet Vet Lyon            → a0003, a0004
-- centre 3 = Vet Marseille Sud           → a0006, a0007, a0008

INSERT INTO inscrit (ida, idcentre) VALUES ('a0001', 1);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0002', 1);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0005', 1);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0003', 2);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0004', 2);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0006', 3);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0007', 3);
INSERT INTO inscrit (ida, idcentre) VALUES ('a0008', 3);


-- Historique des soins effectués

INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
VALUES (1,'a0001','j0001','2024-01-15','Vaccination','Vaccin antirabique administré. Animal en bonne santé générale. Rappel dans 1 an.');

INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
VALUES (1,'a0002','j0002','2024-02-20','Chirurgie dentaire','Extraction d''une dent cassée (canine supérieure droite). Récupération sans complication.');

INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
VALUES (2,'a0003','j0003','2024-03-10','Traitement antiparasitaire','Traitement contre les puces et tiques. Pipette appliquée. Renouveler dans 4 semaines.');

INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
VALUES (2,'a0004','j0004','2024-03-22','Urgence traumatologique','Fracture patte avant gauche suite à une chute. Plâtre posé. Repos strict 6 semaines.');

INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
VALUES (3,'a0006','j0005','2024-04-05','Consultation suivi','Suivi boiterie patte droite. Radiographie effectuée. Arthrose légère diagnostiquée. Anti-inflammatoires prescrits.');

INSERT INTO opere (idcentre, ida, matricule, dateop, nature, historique)
VALUES (3,'a0008','j0006','2024-05-12','Consultation post-opératoire','Contrôle cicatrice post-opératoire. Bonne cicatrisation. Fils retirés. Animal déclaré guéri.');


-- Liste des spécialités vétérinaires

INSERT INTO specialite (idspe, nom) VALUES ('spe01','Médecine générale');
INSERT INTO specialite (idspe, nom) VALUES ('spe02','Chirurgie des petits animaux');
INSERT INTO specialite (idspe, nom) VALUES ('spe03','Cardiologie vétérinaire');
INSERT INTO specialite (idspe, nom) VALUES ('spe04','Dermatologie animale');
INSERT INTO specialite (idspe, nom) VALUES ('spe05','Ophtalmologie vétérinaire');
