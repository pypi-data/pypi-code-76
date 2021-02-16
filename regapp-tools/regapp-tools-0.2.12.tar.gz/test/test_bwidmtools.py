import unittest


class BWidmMethods(unittest.TestCase):
    from regapp_tools.parse_args import args
    from regapp_tools.bwidmtools import external_id_from_subiss, get_username_from_external_id  

    def test_external_id_from_subiss_offline(self):
        subiss = 'test-offline'
        expected = 'hdf_marcus'
        self.assertEqual(BWidmMethods.external_id_from_subiss(sub_iss=subiss), expected)

    def test_username_from_subiss_test_id(self):
        subiss = 'test-id'
        expected = '6c611e2a-2c1c-487f-9948-c058a36c8f0e@https%3A%2F%2Flogin.helmholtz-data-federation.de%2Foauth2'
        self.assertEqual(BWidmMethods.external_id_from_subiss(sub_iss=subiss), expected)
        external_id = expected
        expected = 'hdf_newmarcus22'
        self.assertEqual(BWidmMethods.get_username_from_external_id(external_id), expected)

    def test_username_from_subiss_test_marcus(self):
        subiss = 'test-marcus'
        expected = '6c611e2a-2c1c-487f-9948-c058a36c8f0e@https%3A%2F%2Flogin.helmholtz-data-federation.de%2Foauth2'
        self.assertEqual(BWidmMethods.external_id_from_subiss(sub_iss=subiss), expected)
        external_id = expected
        expected = 'hdf_newmarcus22'
        self.assertEqual(BWidmMethods.get_username_from_external_id(external_id), expected)

    def test_username_from_subiss_test_borja(self):
        subiss = 'test-borja'
        expected = '309ed509-c56a-4894-b163-5993bd08cbc2@https%3A%2F%2Flogin.helmholtz-data-federation.de%2Foauth2'
        self.assertEqual(BWidmMethods.external_id_from_subiss(sub_iss=subiss), expected)
        external_id = expected
        expected = 'hdf_zr5094'
        self.assertEqual(BWidmMethods.get_username_from_external_id(external_id), expected)

    def test_username_from_subiss_test_egi(self):
        subiss = 'f4454db724ea2bb46b849aa045717c19d1659414dc5123144deca5d6e2d77746@egi.eu@https://aai.egi.eu/oidc/'
        expected = 'f4454db724ea2bb46b849aa045717c19d1659414dc5123144deca5d6e2d77746%40egi.eu@https%3A%2F%2Faai.egi.eu%2Foidc%2F'
        self.assertEqual(BWidmMethods.external_id_from_subiss(sub_iss=subiss), expected)
        external_id = expected
        expected = 'hdf_bestebansanchis'
        self.assertEqual(BWidmMethods.get_username_from_external_id(external_id), expected) 


if __name__ == '__main__':
    unittest.main()
