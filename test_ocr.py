"""
Unit tests for OCR menu detection functionality
"""
import unittest
import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock
from PIL import Image, ImageDraw, ImageFont

# Add the parent directory to the path so we can import the API
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.ocr import app, allowed_file, preprocess_image, detect_language, extract_menu_items, translate_text

class TestOCRFunctionality(unittest.TestCase):
    """Test cases for OCR functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a temporary test image
        self.test_image = self.create_simple_test_image()
    
    def create_simple_test_image(self):
        """Create a simple test image for testing"""
        img = Image.new('RGB', (400, 300), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Add some text to the image
        draw.text((50, 50), "Test Menu", fill='black', font=font)
        draw.text((50, 100), "Pizza - $15.99", fill='black', font=font)
        draw.text((50, 130), "Pasta - $12.99", fill='black', font=font)
        draw.text((50, 160), "Salad - $8.99", fill='black', font=font)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        img.save(temp_file.name, 'JPEG')
        temp_file.close()
        
        return temp_file.name
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_image):
            os.unlink(self.test_image)
    
    def test_allowed_file(self):
        """Test file extension validation"""
        self.assertTrue(allowed_file('test.jpg'))
        self.assertTrue(allowed_file('test.png'))
        self.assertTrue(allowed_file('test.jpeg'))
        self.assertTrue(allowed_file('test.gif'))
        self.assertTrue(allowed_file('test.bmp'))
        self.assertTrue(allowed_file('test.tiff'))
        
        self.assertFalse(allowed_file('test.txt'))
        self.assertFalse(allowed_file('test.pdf'))
        self.assertFalse(allowed_file('test.doc'))
        self.assertFalse(allowed_file('test'))
        self.assertFalse(allowed_file(''))
    
    @patch('api.ocr.cv2')
    def test_preprocess_image(self, mock_cv2):
        """Test image preprocessing"""
        # Mock cv2 functions
        mock_image = MagicMock()
        mock_cv2.cvtColor.return_value = mock_image
        mock_cv2.GaussianBlur.return_value = mock_image
        mock_cv2.adaptiveThreshold.return_value = mock_image
        mock_cv2.morphologyEx.return_value = mock_image
        
        result = preprocess_image(mock_image)
        
        # Verify cv2 functions were called
        mock_cv2.cvtColor.assert_called_once()
        mock_cv2.GaussianBlur.assert_called_once()
        mock_cv2.adaptiveThreshold.assert_called_once()
        mock_cv2.morphologyEx.assert_called_once()
    
    @patch('api.ocr.translator')
    def test_detect_language(self, mock_translator):
        """Test language detection"""
        mock_detection = MagicMock()
        mock_detection.lang = 'en'
        mock_translator.detect.return_value = mock_detection
        
        result = detect_language("Hello world")
        self.assertEqual(result, 'en')
        mock_translator.detect.assert_called_once_with("Hello world")
    
    def test_extract_menu_items(self):
        """Test menu item extraction from text"""
        test_text = """
        APPETIZERS
        Caesar Salad - Fresh romaine lettuce $12.99
        Buffalo Wings - Spicy chicken wings $15.99
        
        MAIN COURSES
        Grilled Salmon - Atlantic salmon $24.99
        Beef Steak - 8oz ribeye steak $28.99
        """
        
        items = extract_menu_items(test_text)
        
        # Should extract menu items
        self.assertGreater(len(items), 0)
        
        # Check if items have expected structure
        for item in items:
            self.assertIn('full_text', item)
    
    @patch('api.ocr.translator')
    def test_translate_text(self, mock_translator):
        """Test text translation"""
        mock_result = MagicMock()
        mock_result.text = "Hola mundo"
        mock_translator.translate.return_value = mock_result
        
        result = translate_text("Hello world", "es")
        self.assertEqual(result, "Hola mundo")
        mock_translator.translate.assert_called_once_with("Hello world", dest="es")
    
    def test_translate_text_english(self):
        """Test that English text is not translated"""
        result = translate_text("Hello world", "en")
        self.assertEqual(result, "Hello world")
    
    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'OCR Menu Detector')
    
    def test_index_endpoint(self):
        """Test index endpoint returns HTML"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OCR Menu Detector', response.data)
        self.assertIn(b'Upload Menu Image', response.data)
    
    def test_ocr_endpoint_no_file(self):
        """Test OCR endpoint with no file"""
        response = self.app.post('/api/ocr')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No file provided')
    
    def test_ocr_endpoint_invalid_file(self):
        """Test OCR endpoint with invalid file type"""
        data = {'file': (open(self.test_image, 'rb'), 'test.txt')}
        response = self.app.post('/api/ocr', data=data)
        self.assertEqual(response.status_code, 400)
        
        result = json.loads(response.data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Invalid file type')
    
    @patch('api.ocr.pytesseract')
    @patch('api.ocr.cv2')
    @patch('api.ocr.detect_language')
    @patch('api.ocr.extract_menu_items')
    def test_ocr_endpoint_success(self, mock_extract, mock_detect, mock_cv2, mock_pytesseract):
        """Test successful OCR processing"""
        # Mock the dependencies
        mock_cv2.imread.return_value = MagicMock()
        mock_cv2.cvtColor.return_value = MagicMock()
        mock_cv2.GaussianBlur.return_value = MagicMock()
        mock_cv2.adaptiveThreshold.return_value = MagicMock()
        mock_cv2.morphologyEx.return_value = MagicMock()
        
        mock_pytesseract.image_to_data.return_value = {
            'conf': ['90', '85', '88'],
            'text': ['Test', 'Menu', 'Item']
        }
        mock_pytesseract.image_to_string.return_value = "Test Menu Item"
        
        mock_detect.return_value = 'en'
        mock_extract.return_value = [
            {'name': 'Test Item', 'price': '$10.99', 'full_text': 'Test Item $10.99'}
        ]
        
        # Test with valid image file
        with open(self.test_image, 'rb') as f:
            data = {
                'file': (f, 'test.jpg'),
                'target_lang': 'en'
            }
            response = self.app.post('/api/ocr', data=data)
        
        self.assertEqual(response.status_code, 200)
        
        result = json.loads(response.data)
        self.assertTrue(result['success'])
        self.assertEqual(result['detected_language'], 'en')
        self.assertIn('menu_items', result)
        self.assertIn('total_items', result)

class TestOCRIntegration(unittest.TestCase):
    """Integration tests for OCR functionality"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_full_ocr_workflow(self):
        """Test the complete OCR workflow with a real image"""
        # This test requires actual OCR libraries to be installed
        # Skip if not available
        try:
            import cv2
            import pytesseract
        except ImportError:
            self.skipTest("OCR libraries not available")
        
        # Use the sample menu image if it exists
        sample_image_path = 'tests/sample_menu.jpg'
        if not os.path.exists(sample_image_path):
            self.skipTest("Sample menu image not found")
        
        with open(sample_image_path, 'rb') as f:
            data = {
                'file': (f, 'sample_menu.jpg'),
                'target_lang': 'en'
            }
            response = self.app.post('/api/ocr', data=data)
        
        # Should return successful response
        self.assertEqual(response.status_code, 200)
        
        result = json.loads(response.data)
        self.assertTrue(result['success'])
        self.assertIn('detected_language', result)
        self.assertIn('menu_items', result)
        self.assertIn('total_items', result)
        self.assertGreater(result['total_items'], 0)

if __name__ == '__main__':
    # Create test images if they don't exist
    if not os.path.exists('tests/sample_menu.jpg'):
        from create_test_image import create_test_menu_image
        create_test_menu_image()
    
    unittest.main()
