from PySide6.QtGui import QClipboard


def calc_row(archive, sieve, columnOrRow, virgula):
    clipboard = QClipboard()
    sieve_list = []
    row_data = {
        'A:': [], 'B:': [], 'C:': [], 'D:': [],
        'E:': [], 'F:': [], 'G:': [], 'H:': [],
        'I:': [], 'J:': [], 'K:': [], 'L:': [],
        'M:': [], 'N:': [], 'O:': [], 'P:': [],
        'Q:': [], 'R:': [], 'S:': [], 'T:': [],
        'U:': [], 'V:': [], 'X:': [], 'Z:': [],
        'Y:': [], 'W:': [], 'date': None}
    index_list = ['A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'X:', 'Z:', 'Y:', 'W:'] 
    index_list_number = ['0:', '5:', '10:', '15:', '20:', '25:', '30:', '35:', '40:', '45:', '50:', '55:', '60:', '65:', '70:', '75:', '80:', '85:', '90:', '95:', '100:', '105:', '110:', '115:', '120:', '125:', '130:', '135:', '140:', '145:', '150:', '155:', '160:', '165:', '170:', '175:', '180:', '185:', '190:', '195:', '200:', '205:', '210:', '215:', '220:', '225:', '230:', '235:', '240:', '245:', '250:', '255:', '260:', '265:', '270:', '275:', '280:', '285:', '290:', '295:', '300:', '305:', '310:', '315:', '320:', '325:', '330:', '335:', '340:', '345:', '350:', '355:', '360:', '365:', '370:', '375:', '380:', '385:', '390:', '395:', '400:', '405:', '410:', '415:', '420:', '425:', '430:', '435:', '440:', '445:', '450:', '455:', '460:', '465:', '470:', '475:', '480:', '485:', '490:', '495:', '500:', '505:', '510:', '515:', '520:', '525:', '530:', '535:', '540:', '545:', '550:', '555:', '560:', '565:', '570:', '575:', '580:', '585:', '590:', '595:', '600:', '605:', '610:', '615:', '620:', '625:', '630:', '635:', '640:', '645:', '650:', '655:', '660:', '665:', '670:', '675:', '680:', '685:', '690:', '695:', '700:', '705:', '710:', '715:', '720:', '725:', '730:', '735:', '740:', '745:', '750:', '755:', '760:', '765:', '770:', '775:', '780:', '785:', '790:', '795:', '800:', '805:', '810:', '815:', '820:', '825:', '830:', '835:', '840:', '845:', '850:', '855:', '860:', '865:', '870:', '875:', '880:', '885:', '890:', '895:', '900:', '905:', '910:', '915:', '920:', '925:', '930:', '935:', '940:', '945:', '950:', '955:', '960:', '965:', '970:', '975:', '980:', '985:', '990:', '995:', '1000:', '1005:', '1010:', '1015:', '1020:', '1025:', '1030:', '1035:', '1040:', '1045:', '1050:', '1055:', '1060:', '1065:', '1070:', '1075:', '1080:', '1085:', '1090:', '1095:', '1100:', '1105:', '1110:', '1115:', '1120:', '1125:', '1130:', '1135:', '1140:', '1145:', '1150:', '1155:', '1160:', '1165:', '1170:', '1175:', '1180:', '1185:', '1190:', '1195:', '1200:', '1205:', '1210:', '1215:', '1220:', '1225:', '1230:', '1235:', '1240:', '1245:', '1250:', '1255:', '1260:', '1265:', '1270:', '1275:', '1280:', '1285:', '1290:', '1295:']
    index_match = None

    full_item = None
    for i in sieve:
        if 'FULL' in i:
            temp = i.split('-')
            full_item = temp[0]
        else:
            sieve_list.append(i.split())

    for i in archive:
        
        if "File" in i:
            i  = i.replace('C:\\', '')
        temp = i.split()
        if len(temp) == 3:
            if 'Start' == temp[0] and 'Date:' == temp[1]:
                row_data['date'] = temp[2]

        if len(temp) > 1:
            if temp[0] in index_list:
                index_match = temp[0]
        elif temp == []:
            continue
        elif temp[0][0:2] in index_list:
            index_match = temp[0][0:2]
        

        for ii in temp:
            if ii in index_list:
                continue
            elif ii in index_list_number:
                continue
            
            for iii in index_list:
                if index_match == iii:
                    row_data[iii].append(ii)

    #print(c)
    data = []
    for i in sieve_list:
        try:
            if i != []:
                temp = i[0].split('-')
                if virgula:
                    data.append(row_data[f"{temp[0]}:"][int(temp[1])].replace('.', ','))
                else:
                    data.append(row_data[f"{temp[0]}:"][int(temp[1])])
        except IndexError:
            return 'Index Incorreto'
    if full_item != None:
        temp = str(row_data['date'])
        for i in row_data[f'{full_item}:']:
            if virgula:
                i = i.replace('.', ',')
            temp += f'\t{str(i)}'
        result = temp
        # clipboard.setText(temp)
        # copy(temp)
    else:
        if columnOrRow == True:
            # data.insert(0,row_data['date'])
            # result = DataFrame(data)
            # result = result.transpose()
            temp = str(row_data['date'])
            for i in data:
                temp += f'\t{str(i)}'
            result = temp
            # copy(result)
            # clipboard.setText(result)
        else:
            temp = str(row_data['date'])
            for i in data:
                temp += f'\n{str(i)}'
            result = temp
            # copy(result)
            # clipboard.setText(result)
    

    # Resetando todas as variáveis
    archive.seek(0)
    sieve.seek(0)
    sieve_list = []
    row_data = {
        'A:': [], 'B:': [], 'C:': [], 'D:': [],
        'E:': [], 'F:': [], 'G:': [], 'H:': [],
        'I:': [], 'J:': [], 'K:': [], 'L:': [],
        'M:': [], 'N:': [], 'O:': [], 'P:': [],
        'Q:': [], 'R:': [], 'S:': [], 'T:': [],
        'U:': [], 'V:': [], 'X:': [], 'Z:': [],
        'Y:': [], 'W:': [], 'date': None}
    index_list = 'A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'X:', 'Y:', 'W:', 'Z:' 
    index_list_number = ['0:', '5:', '10:', '15:', '20:', '25:', '30:', '35:', '40:', '45:', '50:', '55:', '60:', '65:', '70:', '75:', '80:', '85:', '90:', '95:', '100:', '105:', '110:', '115:', '120:', '125:', '130:', '135:', '140:', '145:', '150:', '155:', '160:', '165:', '170:', '175:', '180:', '185:', '190:', '195:', '200:', '205:', '210:', '215:', '220:', '225:', '230:', '235:', '240:', '245:', '250:', '255:', '260:', '265:', '270:', '275:', '280:', '285:', '290:', '295:']
    index_match = ''
    return result

def calc(archive, sieve, columnOrRow, virgula):
    clipboard = QClipboard()
    data = calc_row(archive, sieve, columnOrRow, virgula)
    
    try:
        clipboard.setText(data)
        return "Done"
    except:
        return "Error"
    