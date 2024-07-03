import os
import unittest

from Code.texture_manager import (DMSValidator, InvalidSpriteError,
                                  SpriteValidationError)


class TestTextureFolders(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Sprites'))

    def test_validate_all_dms_folders(self):
        try:
            result = DMSValidator.validate_all_dms(self.base_path)
            self.assertTrue(result)
        
        except (SpriteValidationError, InvalidSpriteError) as e:
            error_message = f"validate_all_dms raised an exception: {e.message}, Path: {e.path}"
            if isinstance(e, InvalidSpriteError):
                if e.missing_files:
                    error_message += f", Missing Files: {e.missing_files}"
                if e.missing_field:
                    error_message += f", Missing Field: {e.missing_field}"
            
            self.fail(error_message)

if __name__ == '__main__':
    unittest.main()
