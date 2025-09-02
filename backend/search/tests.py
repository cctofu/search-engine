from django.test import TestCase, Client

# Create your tests here.

class MainTests(TestCase):
    def setUp(self):
        pass

    def search(self,query):
        payload = {"query":query}
        return self.client.post(
            "/api/search",
            data=payload,
            content_type="application/json",
        )
    
    def autocomplete(self,short_query):
        return self.client.get(f"/api/autocomplete/{short_query}",context_type = "appliciation/json")
    
    def details(self,claim_texts):
        payload = {"claim_texts":claim_texts}
        return self.client.post(
            "/api/details",
            data=payload,
            content_type="application/json",
        )

    def test_query(self):
        res = self.search("A new method for data processing")
        self.assertEqual(res.json()["code"], 0)
        self.assertEqual(res.status_code, 200)

    def test_autocomplete(self):
        res = self.autocomplete("A new method for")
        self.assertEqual(res.json()["code"], 0)
        self.assertEqual(res.status_code, 200)

    def test_details(self):
        res = self.details(['1 . A data processing system including an information processing device and an information display device, wherein the information processing device includes: a data registration part configured to register a plurality of pieces of data acquired by a predetermined data acquisition device as data handled by the data processing system in a state where each piece of the data and at least one type of accompanying information of each piece of the data are associated with each other; a registration data holder that holds data registered by the data registration part; a data tree creator configured to group the plurality of pieces of data held in the registration data holder by using the accompanying information of an optionally selected type so that pieces of the data having a common piece of the accompanying information belong to a same group, and to create a data tree virtually indicating a state in which the plurality of pieces of data are distributed into groups; and an information display part configured to display a data tree created by the data tree creator on the information display device.', '2 . The data processing system according to claim 1 , wherein the data registration part is configured to perform registration of the plurality of pieces of data in a state where a plurality of types of the accompanying information are associated with each of the plurality of pieces of data, and the data tree creator is configured, in a case where a plurality of types of the accompanying information are set to be used for the grouping, to create the data tree having a hierarchical structure in which the accompanying information of a type that is higher in priority order set in advance for each type of the accompanying information is located on a higher layer.', '3 . The data processing system according to claim 2 , wherein the information processing device is configured so that the priority order is optionally changeable.', '4 . The data processing system according to claim 1 , wherein the data is an image of cell culture or a numerical value acquired by analysis of the image, and the accompanying information includes at least one of a passage number and a number of culture days.', '5 . The data processing system according to claim 1 , wherein the data is a numerical value acquired by analysis, and the information processing device further includes a graph creator that creates a graph having a first axis and a second axis based on a structure of the data tree created by the data tree creator, wherein the first axis indicates each numerical value of the plurality of pieces of data, and the second axis indicates at least one piece of the accompanying information used for the grouping based on a structure of the data tree created by the data tree creator.', '6 . A data processing method comprising: a registration step of registering a plurality of pieces of data acquired by a predetermined data acquisition device in a state where the data and at least one type of accompanying information of each piece of the data are associated with each other; a tree creation step of grouping the plurality of pieces of data registered in the registration step by using the accompanying information of an optionally selected type so that pieces of the data having a common piece of the accompanying information belong to a same group, and creating a data tree virtually indicating a state in which the plurality of pieces of data are distributed into groups; and a display step of displaying a data tree created in the tree creation step on a predetermined information display device.', '7 . The data processing method according to claim 6 , wherein in the registration step, a plurality of types of the accompanying information are registered in association with each of the plurality of pieces of data, and in the tree creation step, the data tree having a hierarchical structure in which the accompanying information of a type that is higher in priority order set in advance for each type of the accompanying information is located on a higher layer is created.', '8 . The data processing method according to claim 7 , further comprising an order changing step of changing the priority order.', '9 . The data processing method according to claim 6 , further comprising a graph creation step of creating, in a case where the data is a numerical value acquired by analysis, a graph having a first axis and a second axis based on a structure of the data tree created in the tree creation step, wherein the first axis indicates each numerical value of the plurality of pieces of data, and the second axis indicates at least one piece of the accompanying information used for the grouping.', '10 . A computer program configured to execute the data processing method according to claim 6 by being applied to an information processing device.'])
        self.assertEqual(res.json()["code"], 0)
        self.assertEqual(res.status_code, 200)
        print(res.json())