create table Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    constraint pk_departements primary key (code_departement),
    constraint fk_region foreign key (code_region) references Regions(code_region)
);

create table Regions (
    code_region INTEGER,
    nom_region TEXT,
    constraint pk_regions primary key (code_region)
);

create table Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    constraint pk_mesures primary key (code_departement, date_mesure),
    constraint fk_mesures foreign key (code_departement) references Departements(code_departement)
);

--TODO Q4 Ajouter les créations des nouvelles tables

CREATE TABLE Communes (
    code_commune INTEGER NOT NULL,
    nom_commune TEXT NOT NULL, 
    statut_commune TEXT,
    altitude_Moy INTEGER,
    population_commune INTEGER,
    superficie_commune INTEGER,
    code_canton INTEGER,
    code_departement TEXT NOT NULL,
    code_arrondissement INTEGER,
    CONSTRAINT pk_commune PRIMARY KEY (code_commune),
    CONSTRAINT fk_commune foreign key (code_departement) references Departements(code_departement) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE Isolation (
    id_isolation INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    cout_total_ht FLOAT,
    cout_induit_ht FLOAT,
    annee INTEGER,
    type_logement TEXT,
    annee_construction INTEGER,
    code_departement TEXT,
    code_region INTEGER NOT NULL, 
    poste TEXT,
    isolant TEXT,
    epaisseur INTEGER,
    surface FLOAT,
    CONSTRAINT fk_travaux_dept foreign key (code_departement) references Departements(code_departement) ON DELETE CASCADE ON UPDATE NO ACTION,
    CONSTRAINT fk_travaux_region FOREIGN KEY (code_region) REFERENCES Regions(code_region) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE Chauffage (
    id_chauffage INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    cout_total_ht FLOAT,
    cout_induit_ht FLOAT,
    annee INTEGER,
    type_logement TEXT,
    annee_construction INTEGER,
    code_departement TEXT,
    code_region INTEGER NOT NULL, 
    energie_avt_trav TEXT,
    energie_installe TEXT,
    generateur TEXT, 
    type_chaudiere TEXT,
    CONSTRAINT fk_travaux_dept foreign key (code_departement) references Departements(code_departement),
    CONSTRAINT fk_travaux_region FOREIGN KEY (code_region) REFERENCES Regions(code_region) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE PhotoVoltaique (
    id_photovoltaique INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    cout_total_ht FLOAT,
    cout_induit_ht FLOAT,
    annee INTEGER,
    type_logement TEXT,
    annee_construction INTEGER,
    code_departement TEXT,
    code_region INTEGER NOT NULL, 
    puissance INTEGER,
    type_panneaux TEXT,
    CONSTRAINT fk_travaux_dept foreign key (code_departement) references Departements(code_departement),
    CONSTRAINT fk_travaux_region FOREIGN KEY (code_region) REFERENCES Regions(code_region) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE Travaux (
    departement TEXT NOT NULL,
    travaux TEXT NOT NULL,
    CONSTRAINT pk_travaux PRIMARY KEY (departement, travaux)
);





