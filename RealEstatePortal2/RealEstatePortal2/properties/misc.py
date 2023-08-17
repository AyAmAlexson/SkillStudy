PROP_DIVISION_CHOICES = [
    ('QL', 'Residential Lease'),
    ('QC', 'Commercial Lease'),
    ('ZH', 'Property Sales'),
]

PROP_DIVISION_REFERENCE = {
    'QL': 'Residential Lease',
    'QC': 'Commercial Lease',
    'ZH': 'Sales',
    'All': 'All',
}


rented = 'RE'
available = 'AV'
soon = 'SO'
to_call = 'TC'

PROP_STATUSES = [
    (rented, 'Rented'),
    (available, 'Available'),
    (soon, 'Coming soon'),
    (to_call, 'To call'),
]

residential = 'QL'
commercial = 'QC'
sales = 'ZH'

PROP_DIVISION = [
    (residential, 'Residential'),
    (commercial, 'Commercial'),
    (sales, 'Sales'),
]



LOCATION_CHOICES = [
    ('Luqa','Luqa'),
    ('Kirkop','Kirkop'),
    ('Safi', 'Safi'),
    ('Sliema', 'Sliema'),
    ('Gzira', 'Gzira'),
    ('Birkirkara', 'Birkirkara'),
    ('Swieqi', 'Swieqi'),
    ('Pieta', 'Pieta'),
    ("Ta' Xbiex", "Ta' Xbiex"),
    ('Pembroke', 'Pembroke'),
    ('St. Julians', 'St. Julians'),
    ('Valletta', 'Valletta'),
    ('Balzan', 'Balzan'),
    ('Pieta', 'Pieta'),
    ('Santa Venera','Santa Venera'),
    ('Zebbug', 'Zebbug'),
    ('Attard', 'Attard'),
    ('San Gwann', 'San Gwann'),
    ('Ta l-ibragg', 'Ta l-ibragg'),
    ('Paola', 'Paola'),
    ('Kappara', 'Kappara'),
    ('Naxxar', 'Naxxar'),
    ('Mosta', 'Mosta'),
    ('Bugibba', 'Bugibba'),
    ("St. Paul's Bay", "St. Paul's Bay"),
    ('Qawra', 'Qawra'),
    ('Xemxija', 'Xemxija'),
    ('Bahar ic-Caghaq', 'Bahar ic-Caghaq'),
    ('Mgarr', 'Mgarr'),
    ('Mellieha', 'Mellieha'),
    ('Gharghur', 'Gharghur'),
    ('Burmarrad', 'Burmarrad'),
    ('Madliena', 'Madliena'),
    ('Kalkara', 'Kalkara'),
    ('Marsaskala', 'Marsaskala'),
    ('Zejtun', 'Zejtun'),
    ('Fgura', 'Fgura'),
    ('Isla', 'Isla'),
    ("St. Julian's","St. Julian's"),
    ('Zabbar', 'Zabbar'),
    ('Ghaxaq', 'Ghaxaq'),
    ('Xghajra', 'Xghajra'),
    ('Dingli', 'Dingli'),
    ('Rabat', 'Rabat'),
    ('Zurrieq', 'Zurrieq'),
    ('Gudja', 'Gudja'),
]

AREAS_LIST= {
    'Luqa': 'Airport',
    'Kirkop': 'Airport',
    'Safi': 'Airport',
    'Sliema': 'Central',
    'Gzira': 'Central',
    'Birkirkara': 'Central',
    'Swieqi': 'Central',
    'Pieta': 'Central',
    "Ta' Xbiex":'Central',
    'Pembroke': 'Central',
    'St. Julians': 'Central',
    'Valletta': 'Central',
    'Balzan': 'Central',
    'Msida': 'Central',
    'Santa Venera': 'Central',
    'Zebbug': 'Central',
    'Attard': 'Central',
    'San Gwann': 'Central',
    "Ta' l - ibragg":'Central',
    'Paola': 'Central',
    'Kappara': 'Central',
    'Naxxar': 'North',
    'Mosta': 'North',
    'Bugibba': 'North',
    "St. Paul's Bay":'North',
    'Qawra':'North',
    'Xemxija': 'North',
    'Bahar ic-Caghaq': 'North',
    'Mgarr': 'North',
    'Mellieha': 'North',
    'Gharghur': 'North',
    'Burmarrad': 'North',
    'Madliena': 'North',
    'Kalkara': 'South',
    'Marsaskala': 'South',
    'Zejtun': 'South',
    'Fgura': 'South',
    'Isla': 'South',
    'Zabbar': 'South',
    'Ghaxaq': 'Airport',
    'Xghajra': 'South',
    'Dingli': 'West',
    'Rabat': 'West',
    'Zurrieq': 'West',
    'Gudja': 'Airport',
}

AREAS_CHOICES = [
    ('Airport', 'Airport'),
    ('North', 'North'),
    ('Central', 'Central'),
    ('South', 'South'),
    ('West', 'West'),
]