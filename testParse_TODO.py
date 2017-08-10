import unittest
import parse_TODO as pT
import datetime
import os

filename = "test-"
comment_wildcard = {
    'c': '//',
    'py': '#'
}

def createTestFile(filetype):
    f = open(filename + filetype + "." + filetype, "w+")
    c = comment_wildcard[filetype];
    data = c + " TODO Titulo\n" + \
           c + " Esta tarjeta es una prueba de un TODO\n" + \
           c + " - Esto mola\n" + \
           c + " - Eso tambien\n" + \
           c + "\n\n" + \
           c + " TODO\n" + \
           c + " Esta tarjeta tiene un titulo auto generado\n\n" + \
           c + " TODO\n\n" + \
           c + " Este comentario y el de arriba no se tienen que subir"

    f.write(data);
    f.close();

def deleteTestFile(filetype):
    os.remove(filename + filetype + "." + filetype)

def checkIdInTodoComment(filetype,id_,line):
    f = open(filename + filetype + "." + filetype, "r")
    data = f.read().split('\n')
    f.close()
    if len(data[line].split(' - '))>1:
        if data[line].split(' - ')[1].strip() == id_:
            return True
        else:
            return False
    else:
        return False

class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def test_searchAllCardsOnFile(self):
        for key, value in comment_wildcard.items():
            createTestFile(key)
            obt_cards = pT.searchAllCardsOnFile(filename + key + '.' + key)
            test_cards = [
                pT.Trello_card(name = "Titulo",
                    desc = "Esta tarjeta es una prueba de un TODO\n- Esto mola\n- Eso tambien",
                    line = 0),
                pT.Trello_card(name = "TODO - " + datetime.datetime.now().strftime("%Y-%m-%d"),
                    desc = "Esta tarjeta tiene un titulo auto generado",
                    line = 6)
            ]
            deleteTestFile(key)
            self.assertEqual(test_cards,obt_cards)

    def test_addIdTodoComment(self):
        for key, value in comment_wildcard.items():
            createTestFile(key)
            codefilename = filename + key + '.' + key
            card = pT.Trello_card(name = "Titulo",
                    desc = "Esta tarjeta es una prueba de un TODO\n- Esto mola\n- Eso tambien",
                    line = 0,
                    t_id = "123456789" )
            pT.add_id_TODO_comment(codefilename,card)
            assert(checkIdInTodoComment(key,"123456789",0))




if __name__ == '__main__':
    unittest.main()
