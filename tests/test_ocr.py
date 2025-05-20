import unittest
import os
from PIL import Image
import pytesseract
from utils.helpers import save_json, load_json
from utils.config import OCR_DIR

class TestOCR(unittest.TestCase):
    def setUp(self):
        # Create test image
        self.test_image = Image.new('RGB', (100, 100), color='white')
        self.test_image_path = os.path.join(OCR_DIR, 'test_image.png')
        self.test_image.save(self.test_image_path)
        
    def tearDown(self):
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
    
    def test_ocr_processing(self):
        # Test OCR processing
        text = pytesseract.image_to_string(self.test_image)
        self.assertIsInstance(text, str)
    
    def test_ocr_results_saving(self):
        # Test saving OCR results
        test_results = {
            'timestamp': str(datetime.now(pytz.UTC)),
            'filename': 'test_image.png',
            'text': 'Test OCR text',
            'confidence': 0.85
        }
        save_json('data/test_ocr_results.json', test_results)
        
        # Verify results were saved
        loaded_results = load_json('data/test_ocr_results.json')
        self.assertEqual(loaded_results['filename'], test_results['filename'])

if __name__ == '__main__':
    unittest.main()
