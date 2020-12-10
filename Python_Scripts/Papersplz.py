test = 'test'

from datetime import datetime

class Inspector:
    def __init__(self):
        self.gloryious_motherland = "Arstotzka"
        self.countries   = "Arstotzka, Antegria, Impor, Kolechia, Obristan, Republia, United Federation".split(', ')
        self.exp_date    = datetime.strptime("1982.11.22", "%Y.%m.%d")
        self.check_missmatch = {
            "ID number",
            "nationality",
            "name",
            "date of birth",
            "SEX",
        }
        self.wanted      = set()
        self.requirments = { country : {
            'Allow'       : False,
            'WorkPerm'    : False,
            'Documents'   : set(),
            'Vaccination' : set()
        } for country in self.countries }
    
    def __str__(self):
        depth = 0; spacer = ' - '; n = '\n'
        string = f"Wanted criminals:\n{spacer+n if len(self.wanted) == 0 else ''}"
        for crim in self.wanted:
            string += f"{spacer}{crim}\n"
        for doc, values in self.requirments.items():
            string += f"{doc}:\n"
            for data_point, data_value in values.items():
                string += f"{(depth+1)*spacer}{data_point:12}: {data_value}\n"
        return string
        
        
    def receive_bulletin(self, bulletin):
        for point in bulletin.split('\n'):
            print(point)
            # ------------------------------- Find relevant countries
            countries = []
            if 'Entrants' in point:
                countries = [country for country in self.countries]
            elif 'Foreigners' in point or 'Workers' in point:
                countries = [country for country in self.countries]
                countries.remove('Arstotzka')
            else:
                countries = [country for country in self.countries if country in point]
            # ------------------------------- Determine point off bulletin
            
            "certificate of vaccination"

            if 'require' in point:
                """
                if 'Workers' in point:
                    for country in self.countries:
                        self.requirments[country]['WorkPerm'] = True
                    continue
                """
                requirement = point.split('require ')[1].split('vaccination')[0].strip()
                for country in countries:
                    vacVdoc = 'Vaccination' if 'vaccination' in point else 'Documents'
                    if 'no longer' in point:
                        try: 
                            self.requirments[country][vacVdoc].remove(requirement)
                            if len(self.requirments[country]['Vaccination']) == 0:
                                try: 
                                    self.requirments[country]['Documents'].remove("certificate of vaccination")
                                except: 
                                    pass
                        except: 
                            pass
                    else:
                        self.requirments[country][vacVdoc].add(requirement)
                        if len(self.requirments[country]['Vaccination']) > 0:
                            self.requirments[country]['Documents'].add("certificate of vaccination")

            elif 'Wanted' in point:
                for crim in point.split(': ')[1].split(', '):
                    self.wanted.add(crim.strip())
            elif 'Allow' in point:
                for country in countries:
                    self.requirments[country]['Allow'] = True
            elif 'Deny'  in point:
                for country in countries:
                    self.requirments[country]['Allow'] = False
        print(self)
        
    def inspect(self, person_data):
        """
        All required documents are present
        There is no conflicting information across the provided documents
        All documents are current (ie. none have expired) 
        -- a document is considered expired if the expiration date is November 22, 1982 or earlier
        The entrant is not a wanted criminal
        If a certificate_of_vaccination is required and provided, 
            it must list the required vaccination
        A "worker" is a foreigner entrant who has WORK listed as their purpose on their access permit
        If entrant is a foreigner, a grant_of_asylum or diplomatic_authorization are acceptable in lieu of an access_permit. In the case where a diplomatic_authorization is used, it must include Arstotzka as one of the list of nations that can be accessed.
        """
        p = Person(self, person_data)
        print(p)
        if   not self.not_wanted(p):
            return p.raised
        elif not self.documents_valid(p):
            return p.raised
        elif not self.not_banned(p):
            return p.raised
        elif not self.carries_all_docs(p):
            return p.raised
        elif not self.document_current(p):
            return p.raised
        elif not self.vaccination_upto_date(p):
            return p.raised
        else:
            if p.nation == self.gloryious_motherland:
                return f'Glory to {self.gloryious_motherland}.'
            else:
                return 'Cause no trouble.'
        
    def carries_all_docs(self, p):
        for each in self.requirments[p.nation]['Documents']:
            if each not in p.properties.keys(): # if a doc is missing
                p.raised = f'Entry denied: missing required {each}.'
                if p.nation != self.gloryious_motherland: # if it is a foreigner other things can affect the rulling
                    if each == "access permit": # if they miss a acces permit there are alternatives
                        if "grant of asylum" in p.properties.keys(): # right to asylum, out_of_date is checked elsewhere
                            continue
                        elif "diplomatic authorization" in p.properties.keys(): # diplomatic paper is alternative
                            if self.gloryious_motherland in p.properties["diplomatic authorization"]['ACCESS']: # if they have acces to the motherland
                                continue # make sure it is not caught under another check
                            else: # they have no acces to the motherlands
                                p.raised = 'Entry denied: invalid diplomatic authorization.'
                    if each == 'work pass':
                        if "diplomatic authorization" in p.properties.keys():
                            continue
                        elif "grant of asylum" in p.properties.keys():
                            continue
                        else:
                            try:
                                if not p.properties["access permit"]["PURPOSE"] == "WORK":
                                    continue
                            except KeyError:
                                continue
                return False
        return True
    
    def documents_valid(self, p):
        for this in p.properties.keys():
            for other in p.properties.keys():
                if other != this:
                    for each in self.check_missmatch:
                        try:
                            if p.properties[this][each] != p.properties[other][each]:
                                p.raised = f'Detainment: {each} mismatch.'
                                return False
                        except: 
                            pass
        return True
    
    def document_current(self, p):
        for document, info in p.properties.items():
            try:
                print(info['EXP'] - self.exp_date)
                if info['EXP'] < self.exp_date:
                    p.raised = f'Entry denied: {document} expired.'
                    return False
            except: pass
        return True

    def not_wanted(self, p):
        last, first = p.name.split(', ')
        if f"{first} {last}" in self.wanted:
            p.raised = 'Detainment: Entrant is a wanted criminal.'
            return False
        return True
    
    def not_banned(self, p):
        if not self.requirments[p.nation]['Allow']:
            p.raised = 'Entry denied: citizen of banned nation.'
            return False
        return True
        
    def vaccination_upto_date(self, p):
        for vacc in self.requirments[p.nation]["Vaccination"]:
            if "certificate of vaccination" in p.properties:
                if vacc not in p.properties["certificate of vaccination"]["VACCINES"]:
                    p.raised = 'Entry denied: missing required vaccination.'
                    return False
        return True
        
        
class Person:
    def __init__(self, inspector, stats):
        self.inspector  = inspector
        self.properties = {}
        self.raised     = None
        self.nation     = 'Arstotzka'
        self.name       = 'None, None'
        for doc, values in stats.items():
            doc = doc.replace('_',' ')
            value_list = values.splitlines()
            self.properties[doc] = {}
            for value in value_list:
                data_point, data_value = value.split(': ')
                if   data_point == 'ID#':
                    data_point = 'ID number'
                if   data_point == 'DOB':
                    data_point = 'date of birth'
                elif data_point == 'EXP':
                    data_value = datetime.strptime(data_value, "%Y.%m.%d")
                elif data_point == 'NATION':
                    data_point = "nationality"
                    self.nation = data_value
                elif data_point == 'NAME':
                    data_point = "name"
                    self.name = data_value
                    
                self.properties[doc][data_point] = data_value
    
    def __str__(self):
        string = ''
        depth = 0; spacer = ' - '
        for doc, values in self.properties.items():
            string += f"{doc}:\n"
            for data_point, data_value in values.items():
                string += f"{(depth+1)*spacer}{data_point:10}: {data_value}\n"
        return string
        
        
""" Entrants require passport
Allow citizens of Arstotzka
Wanted by the State: Damian Maars
Allow citizens of Antegria, Impor, Kolechia, Obristan, Republia, United Federation
Foreigners require access permit
Citizens of Arstotzka require ID card
Allow citizens of Republia, Impor, Kolechia
Allow citizens of United Federation
Allow citizens of Obristan
Foreigners require typhus vaccination
Workers require work pass
Wanted by the State: Erika Klaus
Allow citizens of Antegria
Citizens of United Federation, Republia require cowpox vaccination
Wanted by the State: Sharona Pejic
Deny citizens of Impor, Obristan, Republia, Antegria, United Federation
Wanted by the State: Nikolas Tjell
Allow citizens of Obristan
Entrants require hepatitis B vaccination
Wanted by the State: Yelena Malkova
Allow citizens of United Federation, Impor, Republia
Wanted by the State: Katarina Burke
Deny citizens of Republia, United Federation, Kolechia
Citizens of United Federation, Republia no longer require cowpox vaccination
Wanted by the State: Adam Kerr
Foreigners require polio vaccination
Wanted by the State: Aleksandra Zitna
Wanted by the State: Brenna Evans
Foreigners require tuberculosis vaccination
Foreigners no longer require typhus vaccination
Wanted by the State: Ekaterina Fischer
Allow citizens of Kolechia, Antegria
Wanted by the State: Eva Diaz
Allow citizens of Republia, United Federation
Deny citizens of Kolechia, Impor, Obristan
Entrants no longer require hepatitis B vaccination
Wanted by the State: Gloria Fischer
Allow citizens of Obristan
Foreigners no longer require polio vaccination
Wanted by the State: Agnes Jacobs
Allow citizens of Kolechia, Impor
Entrants require cholera vaccination
Wanted by the State: Ilya Smirnov
Foreigners require tetanus vaccination
Foreigners no longer require tuberculosis vaccination
Wanted by the State: Valentina Ibrahimovic
Foreigners require cowpox vaccination
Wanted by the State: Valentina Hammacher
Deny citizens of Antegria, Impor, Kolechia, United Federation, Republia
Entrants no longer require cholera vaccination
Wanted by the State: Benito Odom
Allow citizens of Antegria, Republia, Impor, Kolechia, United Federation
Wanted by the State: Anya Novak
Deny citizens of United Federation, Kolechia, Republia
Foreigners require hepatitis B vaccination
Wanted by the State: Jonathan Romanowski
Allow citizens of Kolechia, Republia
Deny citizens of Obristan
Citizens of United Federation require HPV vaccination
Wanted by the State: Liliana Jung
Deny citizens of Republia, Antegria, Impor, Kolechia
Wanted by the State: William Michaelson
Allow citizens of Impor, United Federation, Antegria, Kolechia, Republia, Obristan
Foreigners no longer require cowpox vaccination
Wanted by the State: Marina Krug
Entrants require cowpox vaccination
Foreigners no longer require tetanus vaccination
Wanted by the State: Tomasz Dahl
Foreigners no longer require hepatitis B vaccination
Citizens of United Federation no longer require HPV vaccination
Wanted by the State: William Stanislov
Entrants require typhus vaccination
Wanted by the State: Martina Strauss
Wanted by the State: Borek Zitna"""        
        
        
        
#        
