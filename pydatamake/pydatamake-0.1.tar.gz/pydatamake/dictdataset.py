import random

arg_dict = ['class', 'sex', 'name', 'phone', 'add', 'hobby', 'field']

class_dicts = ['0class0', '0class1', '0class2', '0class3', '0class4', '0class5', '0class6', '0class7', '0class8',
               '0class9', '1class0', '1class1', '1class2', '1class3', '1class4', '1class5', '1class6', '1class7',
               '1class8', '1class9', '2class0', '2class1', '2class2', '2class3', '2class4', '2class5', '2class6',
               '2class7', '2class8', '2class9', '3class0', '3class1', '3class2', '3class3', '3class4', '3class5',
               '3class6', '3class7', '3class8', '3class9', '4class0', '4class1', '4class2', '4class3', '4class4',
               '4class5', '4class6', '4class7', '4class8', '4class9', '5class0', '5class1', '5class2', '5class3',
               '5class4', '5class5', '5class6', '5class7', '5class8', '5class9', '6class0', '6class1', '6class2',
               '6class3', '6class4', '6class5', '6class6', '6class7', '6class8', '6class9', '7class0', '7class1',
               '7class2', '7class3', '7class4', '7class5', '7class6', '7class7', '7class8', '7class9', '8class0',
               '8class1', '8class2', '8class3', '8class4', '8class5', '8class6', '8class7', '8class8', '8class9',
               '9class0', '9class1', '9class2', '9class3', '9class4', '9class5', '9class6', '9class7', '9class8',
               '9class9']

sex_dicts = ['male', 'famale']

phone_dicts = ['1891886963', '18968541327', '18920735878', '18980927811', '18991494640', '18952197830', '18949999487',
               '18999806657', '1891357981', '18992645657', '1893142086', '18951537365', '1892546197', '18932277946',
               '18964269455', '18921134614', '18950859765', '18931445992', '18949107422', '18910299189', '18991234529',
               '18912252539', '18975053048', '18982124117', '18965006792', '1893171167', '18950577965', '18973567022',
               '18937045533', '18957401226', '18929138653', '18938229908', '18928714399', '18978165559', '18965376533',
               '1898127230', '1895618819', '18990307400', '18911883876', '18927734876', '18933873275', '18985785088',
               '18928298014', '1893748621', '18971916875', '18932339678', '1897973315', '18922508562', '18915935549',
               '189460672', '18915206597', '18972974934', '18971624346', '18990527488', '18939049827', '1895357788',
               '18973388958', '18924729005', '18996385837', '18960466351', '18947802373', '18918196788', '1894001866',
               '18981578095', '18977776568', '18970652961', '18920765320', '18982891783', '18917595408', '18924562868',
               '18959951689', '18969506427', '18927554018', '18921631097', '18911306064', '18911705963', '18999152502',
               '18916644390', '18910528241', '18922896585', '18961655627', '18923496178', '18946765246', '18918224050',
               '18993077413', '18961122978', '18929478529', '18923507267', '1898679651', '18942969424', '18913564068',
               '18972894238', '1896894178', '18982868205', '1898574475', '18992213886', '1893286216', '18945716904',
               '1892612459', '18965149778']

# for i in range(10):
#     for o in range(10):
#         phone_dicts.append(str(189) + str(random.randint(0000, 9999)) + str(random.randint(0000, 9999)))
xingshi_dict = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davis', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                'Rodriguez', 'Wilson', 'Garcia']
num_dict = ['A', 'D', 'Q', 'W', 'R', 'T', 'U', 'P', 'O', 'L', 'K', 'N', 'B', 'Z', 'X']
name_dict = ['Vincent', 'Charles', 'Mark', 'Bill', 'William', 'Jseph', 'James', 'Henry', 'Gary', 'Martin', 'Ulrica',
             'Quella', 'Lilith']
names_dict = ['Wilson.D.Mark', 'Taylor.N.William', 'Jones.O.Charles', 'Garcia.W.Jseph', 'Taylor.D.Henry',
              'Thomas.P.Bill', 'Garcia.O.Bill', 'Taylor.X.Martin', 'Jones.U.Ulrica', 'Jones.K.Charles',
              'Rodriguez.Z.Gary', 'Garcia.W.Charles', 'Thomas.Q.Mark', 'Rodriguez.N.Mark', 'Johnson.R.Mark',
              'Williams.T.Quella', 'Thomas.O.William', 'Jones.Q.Henry', 'Thomas.O.Martin', 'Evans.O.Vincent',
              'Johnson.X.Henry', 'Wilson.K.Mark', 'Johnson.Q.Ulrica', 'Rodriguez.A.Ulrica', 'Wilson.R.Quella',
              'Wilson.R.Ulrica', 'Brown.P.Mark', 'Williams.O.William', 'Rodriguez.X.Vincent', 'Wilson.A.Gary',
              'Rodriguez.Q.Vincent', 'Taylor.L.Quella', 'Garcia.L.Jseph', 'Smith.P.James', 'Thomas.D.Vincent',
              'Davis.B.William', 'Evans.B.Bill', 'Thomas.P.Charles', 'Jones.A.Vincent', 'Johnson.R.Martin',
              'Jones.X.Bill', 'Williams.X.Ulrica', 'Taylor.N.Bill', 'Rodriguez.X.William', 'Johnson.L.Vincent',
              'Brown.T.Vincent', 'Jones.D.William', 'Garcia.Q.Quella', 'Evans.B.Martin', 'Brown.A.Charles',
              'Smith.D.Quella', 'Johnson.Z.Henry', 'Evans.D.Ulrica', 'Williams.N.William', 'Wilson.U.Vincent',
              'Wilson.X.Martin', 'Garcia.O.Mark', 'Thomas.O.William', 'Wilson.X.Ulrica', 'Williams.B.Gary',
              'Rodriguez.D.Gary', 'Rodriguez.T.James', 'Evans.N.Jseph', 'Wilson.U.William', 'Davis.B.Gary',
              'Wilson.R.Jseph', 'Brown.K.Ulrica', 'Jones.W.Bill', 'Evans.R.Ulrica', 'Brown.U.Martin',
              'Johnson.L.Ulrica', 'Brown.W.Mark', 'Davis.X.James', 'Garcia.D.James', 'Evans.X.William',
              'Taylor.O.Quella', 'Wilson.W.Jseph', 'Jones.Q.Henry', 'Jones.K.Lilith', 'Jones.Z.James',
              'Davis.T.William', 'Rodriguez.R.Jseph', 'Johnson.X.Mark', 'Davis.N.Quella', 'Evans.L.Lilith',
              'Garcia.K.Bill', 'Wilson.O.Mark', 'Wilson.Q.Martin', 'Wilson.D.James', 'Smith.T.Quella', 'Davis.R.James',
              'Wilson.Q.Ulrica', 'Davis.L.Quella', 'Johnson.W.Vincent', 'Wilson.U.James', 'Davis.B.Vincent',
              'Brown.U.William', 'Wilson.U.Charles', 'Davis.Z.Henry', 'Wilson.N.Mark']

# for i in range(0, 100):
#     names_dict.append(random.choice(xingshi_dict) + '.' + random.choice(num_dict) + '.' + random.choice(name_dict))

