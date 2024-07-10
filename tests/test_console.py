import unittest
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from io import StringIO
from unittest.mock import patch

class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Tear down test environment."""
        storage._FileStorage__objects = {}

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_parameters(self, mock_stdout):
        """Test create command with parameters."""
        cmd = HBNBCommand()
        cmd.onecmd('create BaseModel name="My_little_house" age=30 height=1.75')
        
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) > 0)
        
        instance_id = output
        instance = storage.all()[f'BaseModel.{instance_id}']
        
        self.assertEqual(instance.name, "My little house")
        self.assertEqual(instance.age, 30)
        self.assertEqual(instance.height, 1.75)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_invalid_parameters(self, mock_stdout):
        """Test create command with invalid parameters."""
        cmd = HBNBCommand()
        cmd.onecmd('create BaseModel name="My_little_house" age=thirty height=1.75')
        
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) > 0)
        
        instance_id = output
        instance = storage.all()[f'BaseModel.{instance_id}']
        
        self.assertEqual(instance.name, "My little house")
        self.assertFalse(hasattr(instance, 'age'))
        self.assertEqual(instance.height, 1.75)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_no_class_name(self, mock_stdout):
        """Test create command with no class name."""
        cmd = HBNBCommand()
        cmd.onecmd('create')
        self.assertEqual(mock_stdout.getvalue().strip(), "** class name missing **")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_with_nonexistent_class(self, mock_stdout):
        """Test create command with a nonexistent class name."""
        cmd = HBNBCommand()
        cmd.onecmd('create NonExistentClass name="Test"')
        self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

if __name__ == '__main__':
    unittest.main()
