# import os
#
# import django
# from django.core.exceptions import ImproperlyConfigured
# from django.test import TestCase, override_settings
#
# from ai.services.custom_scrubber import AbstractScrubbingService
#
#
# class AbstractScrubbingServiceTest(TestCase):
#
#     def setUp(self):
#         # TODO this will not for because of not loaded apps. Needs to be fixed at some point...
#
#         self.service = AbstractScrubbingService()
#
#     @override_settings(DEBUG=False)
#     def test_scrubber_debug_mode_needs_to_be_active(self):
#         self.assertEqual(self.service.process(), False)
#
#     @override_settings(DEBUG=True, INSTALLED_APPS=[])
#     def test_scrubber_needs_to_be_installed(self):
#         self.assertEqual(self.service.process(), False)
