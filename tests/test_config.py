import unittest
import tempfile
import os

from peft import LoraConfig, PromptEncoderConfig, PrefixTuningConfig, PromptTuningConfig

class PeftConfigMixin:
    all_config_classes = (
        LoraConfig,
        PromptEncoderConfig,
        PrefixTuningConfig,
        PromptTuningConfig,
    )


class PeftConfigTester(unittest.TestCase, PeftConfigMixin):
    def test_methods(self):
        r"""
        Test if all configs have the expected methods. Here we test
        - to_dict
        - save_pretrained
        - from_pretrained
        - from_json_file
        """
        # test if all configs have the expected methods
        for config_class in self.all_config_classes:
            config = config_class()
            self.assertTrue(hasattr(config, "to_dict"))
            self.assertTrue(hasattr(config, "save_pretrained"))
            self.assertTrue(hasattr(config, "from_pretrained"))
            self.assertTrue(hasattr(config, "from_json_file"))


    def test_save_pretrained(self):
        r"""
        Test if the config is correctly saved and loaded using 
        - save_pretrained
        """
        for config_class in self.all_config_classes:
            config = config_class()
            with tempfile.TemporaryDirectory() as tmp_dirname:
                config.save_pretrained(tmp_dirname)

                config_from_pretrained = config_class.from_pretrained(tmp_dirname)
                self.assertEqual(config.to_dict(), config_from_pretrained.to_dict())
    
    def test_from_json_file(self):
        for config_class in self.all_config_classes:
            config = config_class()
            with tempfile.TemporaryDirectory() as tmp_dirname:
                config.save_pretrained(tmp_dirname)

                config_from_json = config_class.from_json_file(os.path.join(tmp_dirname, "adapter_config.json"))
                self.assertEqual(config.to_dict(), config_from_json)
    

    def test_to_dict(self):
        r"""
        Test if the config can be correctly converted to a dict using:
        - to_dict 
        - __dict__
        """
        for config_class in self.all_config_classes:
            config = config_class()
            self.assertEqual(config.to_dict(), config.__dict__)
            self.assertTrue(isinstance(config.to_dict(), dict))

    
    def test_set_attributes(self):
        # manually set attributes and check if they are correctly written
        for config_class in self.all_config_classes:
            config = config_class(peft_type="test")

            # save pretrained
            with tempfile.TemporaryDirectory() as tmp_dirname:
                config.save_pretrained(tmp_dirname)

                config_from_pretrained = config_class.from_pretrained(tmp_dirname)
                self.assertEqual(config.to_dict(), config_from_pretrained.to_dict())