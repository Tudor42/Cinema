from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models.query import QuerySet
from selenium.webdriver import Chrome
from datetime import date, time
from django.db.models import Count
from .serializers import RezervareSerializer
from .models import Film, CardClient, Rezervare


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = Chrome(executable_path="chromedriver.exe")
        sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def get_elem(self, path):
        print(path)
        loop = True
        while loop:
            try:
                elem = self.selenium.find_element_by_xpath(path)
                loop = False
            except Exception:
                continue
        return elem

    def add_client(self, nume, prenume, CNP, data_nasterii,
                   data_inregistrarii):
        self.go_to_table("cards")
        buttonCreate = self.get_elem("/html/body/div/div/div[2]/div[3]/"
                                     "div[1]/button[1]")
        buttonCreate.click()
        numefield = self.get_elem("/html/body/div[2]/div/div[1]/div/div/div[2]"
                                  "/form/div[1]/input")
        numefield.send_keys(nume)
        prenumefield = self.get_elem("/html/body/div[2]/div/div[1]/div/"
                                     "div/div[2]/form/div[2]/input")
        prenumefield.send_keys(prenume)
        CNPfield = self.get_elem("/html/body/div[2]/div/div[1]"
                                 "/div/div/div[2]/form/div[3]/"
                                 "input")
        CNPfield.send_keys(CNP)
        nasterefield = self.get_elem("/html/body/div[2]/div/div[1]"
                                     "/div/div/div[2]/form/div[4]/"
                                     "div/input[1]")
        nasterefield.send_keys(data_nasterii)
        inregistrarfield = self.get_elem("/html/body/div[2]/div/div[1]"
                                         "/div/div/div[2"
                                         "]/form/div[5]/"
                                         "div/input[1]")
        inregistrarfield.send_keys(data_inregistrarii)
        punctefield = self.get_elem("/html/body/div[2]/div/div[1]"
                                    "/div/div/div[2]/form/div[6]/"
                                    "input")
        punctefield.send_keys("0")
        send_button = self.get_elem("/html/body/div[2]/div/"
                                    "div[1]/div/div/div[2]/form"
                                    "/button")
        send_button.click()

    def add_film(self, titlu, an, pret):
        self.go_to_table("films")
        buttonCreate = self.get_elem("/html/body/div/div/div[2]/div[3]/"
                                     "div[1]/button[1]")
        buttonCreate.click()
        titlufield = self.get_elem("/html/body/div[2]/div/div[1]/div/"
                                   "div/div[2]/form/div[1]/input")
        titlufield.send_keys(titlu)
        year = self.get_elem("/html/body/div[2]/div/div[1]/div"
                             "/div/div[2]/form/div[2]/input")
        year.send_keys(an)
        pretfield = self.get_elem("/html/body/div[2]/div/div[1]/div"
                                  "/div/div[2]/form/div[3]/input")
        pretfield.send_keys(pret)
        send_button = self.get_elem("/html/body/div[2]/div/div[1]/div/div"
                                    "/div[2]/form/button")
        send_button.click()

    def go_to_table(self, table):
        if table == "films":
            elem = self.selenium.find_element_by_xpath("/html/body/div"
                                                       "/div/div/nav/div/"
                                                       "ul/li[1]/a")
        if table == "cards":
            elem = self.selenium.find_element_by_xpath("/html/body/div"
                                                       "/div/div/nav/div/"
                                                       "ul/li[3]/a")
        if table == "bookings":
            elem = self.selenium.find_element_by_xpath("/html/body/div"
                                                       "/div/div/nav/div/"
                                                       "ul/li[2]/a")
        elem.click()
        sleep(1)

    def check_table(self, table, expected_len=None, go_to_table=True,
                    query=None):
        if(go_to_table):
            self.go_to_table(table)
        if table == "films":
            table = self.selenium.find_element_by_xpath("/html/body/div/div"
                                                        "/div[2]/div[2]/div/"
                                                        "table/tbody")
            if query is None:
                objs = Film.objects.all()
            else:
                objs = query
            if expected_len is not None:
                if expected_len == 0:
                    self.assertEqual("Ops, no one here yet", table.
                                     find_element_by_css_selector('tr').text)
                    return
                else:
                    self.assertEqual(expected_len,
                                     len(table.
                                         find_elements_by_css_selector('tr')))
            for row, elem in \
                    zip(table.find_elements_by_css_selector('tr'), objs):
                cells = row.find_elements_by_css_selector('td')
                self.assertEqual(cells[1].text, elem.titlu)
                self.assertEqual(cells[2].text, str(elem.an_aparitie))
                self.assertEqual(cells[3].text, str(elem.pret))

        if table == "cards":
            table = self.selenium.find_element_by_xpath("/html/body/div/div"
                                                        "/div[2]/div[2]/div/"
                                                        "table/tbody")
            if query is None:
                objs = CardClient.objects.all()
            else:
                objs = query
            if expected_len is not None:
                if expected_len == 0:
                    self.assertEqual("Ops, no one here yet", table.
                                     find_element_by_css_selector('tr').text)
                    return
                else:
                    self.assertEqual(expected_len,
                                     len(table.
                                         find_elements_by_css_selector('tr')))
            for row, elem in \
                    zip(table.find_elements_by_css_selector('tr'), objs):
                cells = row.find_elements_by_css_selector('td')
                self.assertEqual(cells[1].text, elem.nume)
                self.assertEqual(cells[2].text, elem.prenume)
                self.assertEqual(cells[3].text, str(elem.CNP))

        if table == "bookings":
            table = self.selenium.find_element_by_xpath("/html/body/div/div"
                                                        "/div[2]/div[2]/div/"
                                                        "table/tbody")
            if query is None:
                objs = Rezervare.objects.all()
            else:
                objs = query
            if expected_len is not None:
                if expected_len == 0:
                    self.assertEqual("Ops, no one here yet", table.
                                     find_element_by_css_selector('tr').text)
                    return
                else:
                    self.assertEqual(expected_len,
                                     len(table.
                                         find_elements_by_css_selector('tr')))
            for row, elem in \
                    zip(table.find_elements_by_css_selector('tr'), objs):
                cells = row.find_elements_by_css_selector('td')
                rezervare = Rezervare.objects.get(id=int(cells[0].text))
                serializer_data = RezervareSerializer(rezervare).data
                self.assertEqual(cells[1].text,
                                 ' '.join(serializer_data['str_film'].
                                          split()[:-1]))
                self.assertEqual(cells[2].text,
                                 ' '.join(serializer_data['str_client'].
                                          split()[:-1]))

    def generate_random(self):
        self.go_to_table("films")
        field = self.get_elem("/html/body/div/div/div[2]/"
                              "div[3]/div[2]/div/input")
        field.send_keys("10")
        generate = self.get_elem("/html/body/div/div/div"
                                 "[2]/div[3]/div[2]/div/button")
        generate.click()
        sleep(1)

    def test_add_film(self):
        self.selenium.get('%s' % (self.live_server_url))
        elem = self.get_elem("/html/body/div/div/div/nav/div/"
                             "ul/li[1]/a")
        elem.click()
        self.check_table("films")
        self.add_film("MA", "2002", "30")
        self.check_table("films")
        self.add_film("LL", "2000", "2")
        self.check_table("films")
        sleep(1)

    def test_undo_redo(self):
        self.go_to_table('films')
        undo = self.get_elem("/html/body/div/div/div[2]/div[4]/button[1]")
        undo.click()
        sleep(1)
        self.add_film("MA", "2002", "30")
        self.check_table("films")
        sleep(2)
        undo = self.get_elem("/html/body/div/div/div[2]/div[4]/button[1]")
        undo.click()
        self.add_client("MON", "CARLEON", "1234567890123", "20.12.2000",
                        "21.01.1999")
        self.check_table("cards")
        self.check_table("bookings")
        self.check_table("films")
        redo = self.get_elem("/html/body/div/div/div[2]/div[4]/button[2]")
        redo.click()
        self.generate_random()
        sleep(2)
        self.check_table("films", 10)
        undo = self.get_elem("/html/body/div/div/div[2]/div[4]/button[1]")
        undo.click()
        sleep(1)
        self.check_table("films", 0)
        self.add_client("ON", "MOR", "1234767890123", "20.12.2000",
                        "21.01.1999")
        self.check_table("films", 0)
        redo = self.get_elem("/html/body/div/div/div[2]/div[4]/button[2]")
        redo.click()
        self.check_table("films", 0)

    def test_generate_random(self):
        self.check_table("films", 0)
        self.generate_random()
        sleep(1)
        self.check_table("films", 10)

    def test_bookings_functionalitati(self):
        film = Film(
            id=3,
            titlu="The Shawshank Redemption",
            an_aparitie=1994,
            pret=50,
            in_program=False,
        )
        film.save()
        client = CardClient(
            id=1,
            nume="Caan",
            prenume="James",
            CNP="2313451263421",
            data_nasterii=date(2000, 12, 2),
            data_inregistrarii=date(2021, 2, 13),
            puncte=0,
        )
        client.save()
        rezervare = Rezervare(
            id=1,
            id_film=film,
            id_card_client=client,
            data=date(2022, 3, 12),
            ora=time(12, 00),
        )
        rezervare2 = Rezervare(
            id=2,
            id_film=film,
            id_card_client=client,
            data=date(2022, 5, 12),
            ora=time(13, 00),
        )
        rezervare3 = Rezervare(
            id=3,
            id_film=film,
            id_card_client=client,
            data=date(2022, 5, 12),
            ora=time(12, 1),
        )
        rezervare2.save()
        rezervare.save()
        rezervare3.save()
        self.check_table('films', 1)
        self.check_table('cards', 1)
        self.check_table('bookings', 3)

        date_gte = self.get_elem('//*[@id="di5"]')
        date_gte.send_keys("04122022")
        date_lte = self.get_elem('//*[@id="di6"]')
        date_lte.send_keys("04122022")
        delete = self.get_elem('/html/body/div/div/div[2]/div[4]/'
                               'div/div/button')
        delete.click()
        self.check_table('bookings', 3)
        date_gte = self.get_elem('//*[@id="di5"]')
        date_gte.send_keys("03122022")
        date_lte = self.get_elem('//*[@id="di6"]')
        date_lte.send_keys("03122022")
        delete = self.get_elem('/html/body/div/div/div[2]/div[4]/div'
                               '/div/button')
        delete.click()
        self.check_table('bookings', 2)

        time_gte = self.get_elem('/html/body/div/div/div[2]/div[5]'
                                 '/div/div/input[1]')
        time_gte.send_keys('1200AM')
        time_lte = self.get_elem('/html/body/div/div/div[2]/div[5]'
                                 '/div/div/input[2]')
        time_lte.send_keys('1200AM')
        sleep(1)
        self.get_elem('/html/body/div/div/div[2]/div[5]'
                      '/div/div/button').click()
        self.check_table('bookings', 0, False)
        self.check_table('bookings', 2)
        time_gte = self.get_elem('/html/body/div/div/div[2]/div[5]'
                                 '/div/div/input[1]')
        time_gte.send_keys('1201PM')
        time_lte = self.get_elem('/html/body/div/div/div[2]/div[5]'
                                 '/div/div/input[2]')
        time_lte.send_keys('1201PM')
        sleep(1)
        self.get_elem('/html/body/div/div/div[2]/div[5]'
                      '/div/div/button').click()
        query = Rezervare.objects.filter(
            ora__gte="12:01",
            ora__lte="12:01"
        )
        self.check_table('bookings', 1, False, query)
        film.delete()
        self.check_table('bookings', 0)

    def test_add_points(self):
        client1 = CardClient(
            id=1,
            nume="Caan",
            prenume="James",
            CNP="2313451263421",
            data_nasterii=date(2000, 12, 2),
            data_inregistrarii=date(2021, 2, 13),
            puncte=0,
        )
        client1.save()
        client2 = CardClient(
            id=2,
            nume="Can",
            prenume="Jam",
            CNP="1313451263421",
            data_nasterii=date(2000, 12, 3),
            data_inregistrarii=date(2021, 2, 13),
            puncte=0,
        )
        client2.save()

        self.go_to_table('cards')
        self.get_elem('//*[@id="di7"]').send_keys(12012000)
        self.get_elem('//*[@id="di8"]').send_keys(12012000)
        self.get_elem('/html/body/div/div/div[2]'
                      '/div[4]/div/div/div[3]/input').send_keys('12')
        self.get_elem('/html/body/div/div/div[2]'
                      '/div[4]/div/div/div[3]/button').click()
        for obj in CardClient.objects.all():
            self.assertEqual(obj.puncte, 0)

        self.check_table('cards', 2)

        self.go_to_table('cards')
        self.get_elem('//*[@id="di7"]').send_keys(12032000)
        self.get_elem('//*[@id="di8"]').send_keys(12032000)
        self.get_elem('/html/body/div/div/div[2]'
                      '/div[4]/div/div/div[3]/input').send_keys('12')
        self.get_elem('/html/body/div/div/div[2]'
                      '/div[4]/div/div/div[3]/button').click()
        objs = CardClient.objects.all()
        self.assertEqual(objs[0].puncte, 0)
        self.assertEqual(objs[1].puncte, 12)
        self.check_table('cards', 2)

    def test_sort_num_points(self):
        client1 = CardClient(
            id=1,
            nume="Caan",
            prenume="James",
            CNP="2313451263421",
            data_nasterii=date(2000, 12, 2),
            data_inregistrarii=date(2021, 2, 13),
            puncte=0,
        )
        client1.save()
        client2 = CardClient(
            id=2,
            nume="Can",
            prenume="Jam",
            CNP="1313451263421",
            data_nasterii=date(2000, 12, 3),
            data_inregistrarii=date(2021, 2, 13),
            puncte=15,
        )
        client2.save()
        client3 = CardClient(
            id=3,
            nume="Can",
            prenume="J",
            CNP="1313251263421",
            data_nasterii=date(2000, 12, 3),
            data_inregistrarii=date(2021, 2, 13),
            puncte=2,
        )
        client3.save()
        query = CardClient.objects.order_by("-puncte")
        self.check_table('cards')
        self.get_elem('/html/body/div/div/div[2]/div[3]/div/button[2]').click()
        print('in')
        self.check_table('cards', 3, False, query)
        print('out')

    def test_sort_num_bookings(self):
        film1 = Film(
            id=1,
            titlu="The Redemption",
            an_aparitie=1994,
            pret=50,
            in_program=False,
        )
        film1.save()
        film2 = Film(
            id=2,
            titlu="The Shawshank",
            an_aparitie=1994,
            pret=50,
            in_program=False,
        )
        film2.save()
        film3 = Film(
            id=3,
            titlu="The",
            an_aparitie=1994,
            pret=50,
            in_program=False,
        )
        film3.save()
        rezervare = Rezervare(
            id=1,
            id_film=film2,
            data=date(2022, 3, 12),
            ora=time(12, 00),
        )
        rezervare2 = Rezervare(
            id=2,
            id_film=film3,
            data=date(2022, 5, 12),
            ora=time(13, 00),
        )
        rezervare3 = Rezervare(
            id=3,
            id_film=film3,
            data=date(2022, 5, 12),
            ora=time(12, 1),
        )
        rezervare.save()
        rezervare2.save()
        rezervare3.save()
        self.go_to_table('films')
        self.get_elem('/html/body/div/div/div[2]'
                      '/div[3]/div[1]/button[2]').click()
        query = \
            Film.objects.annotate(Count('rezervare')).\
            order_by("-rezervare__count")
        self.check_table('films', 3, False, query)
