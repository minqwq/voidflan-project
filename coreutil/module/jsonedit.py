import json
import os
import sys
import re
from typing import Dict, Union

class JsonEditor:
    def __init__(self, 
                 filepath: str | None = None, 
                 save_path: str | None = None):
        """
        Initialize JSON editor
        
        Args:
            filepath: Path to the JSON file to read
            save_path: Path to save the file (if None, use filepath as save location)
        """
        self.filepath = filepath
        self.save_path = save_path or filepath  # Use filepath as save location if not specified
        self.data: Dict = {}
        
    def load(self) -> bool:
        """Load JSON file"""
        if not self.filepath:
            print("No file path specified for reading")
            return False
            
        if not os.path.exists(self.filepath):
            print(f"File does not exist: {self.filepath}")
            # Create new file
            self.data = {}
            return True
            
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except json.JSONDecodeError as e:
            print(f"JSON format error: {e}")
            return False
        except JsonReadFileError as e:
            print(f"Failed to read file: {e}")
            return False
    
    def display(self):
        """Display data in '<name>': '<stat>' format"""
        if not self.data:
            print("No data to display")
            return
            
        for key, value in self.data.items():
            # Determine whether to add quotes based on value type
            if isinstance(value, bool):
                print(f'"{key}": {str(value).lower()}')
            elif isinstance(value, (int, float)):
                print(f'"{key}": {value}')
            else:
                print(f'"{key}": "{value}"')
    
    def process_input(self, input_str: str) -> bool:
        """Process user input"""
        if not input_str.strip():
            return True
            
        parts = input_str.strip().split(' ', 1)
        if len(parts) != 2:
            print("Format error: Use 'name content' format (separated by space)")
            return True
            
        name, stat = parts
        
        # Process stat value
        processed_stat = self._process_stat(stat)
        
        # Update data
        self.data[name] = processed_stat
        print(f"Updated: {name} = {processed_stat}")
        return True
    
    def _process_stat(self, stat: str) -> Union[str, bool, int, float]:
        """Process stat string and return appropriate type value"""
        # Process boolean values
        if stat.lower() == 'true':
            return True
        if stat.lower() == 'false':
            return False
        
        # Process numbers
        try:
            # Try to parse as integer
            if re.match(r'^-?\d+$', stat):
                return int(stat)
            # Try to parse as float
            if re.match(r'^-?\d+\.\d+$', stat):
                return float(stat)
        except ValueError:
            pass
        
        # Return string for other cases
        return stat
    
    def save(self, custom_path: str | None = None) -> bool:
        """
        Save to file
        
        Args:
            custom_path: Custom save path (if None, use save_path set during initialization)
        """
        save_to = custom_path or self.save_path
        if not save_to:
            print("No save path specified")
            return False
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_to), exist_ok=True)
            
            with open(save_to, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"Saved to: {save_to}")
            return True
        except SaveFileError as e:
            print(f"Failed to save: {e}")
            return False
    
    def set_save_path(self, save_path: str):
        """Set save path"""
        self.save_path = save_path
    
    def run(self):
        """Run editor"""
        if not self.filepath:
            self.filepath = input("Enter JSON file path to read: ").strip()
            if not self.save_path:  # If save path not set, use read path
                self.save_path = self.filepath
        
        if not self.load():
            return
        
        print(f"\nReading file: {self.filepath}")
        if self.save_path != self.filepath:
            print(f"Save location: {self.save_path}")
        
        print("\nCurrent content:")
        self.display()
        
        print(
            "\nInput format: name content (e.g., iswin true or name \"John\")"
            "\nEnter 'save' to save and exit"
            "\nEnter 'saveas <path>' to save as"
            "\nEnter 'exit' to exit without saving"
            "\nEnter 'show' to redisplay current content"
            "\nEnter 'clear' to clear all data"
            "\nEnter 'setpath <path>' to set save path"
        )
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'exit':
                    print("Exiting editor")
                    break
                if user_input.lower() == 'save':
                    if self.save():
                        print("Save successful, exiting editor")
                        break
                if user_input.lower().startswith('saveas '):
                    parts = user_input.split(' ', 1)
                    if len(parts) == 2:
                        custom_path = parts[1]
                        if self.save(custom_path):
                            print("Save as successful, exiting editor")
                            break
                elif user_input.lower().startswith('setpath '):
                    parts = user_input.split(' ', 1)
                    if len(parts) == 2:
                        new_path = parts[1]
                        self.set_save_path(new_path)
                        print(f"Save path set to: {new_path}")
                elif user_input.lower() == 'show':
                    self.display()
                elif user_input.lower() == 'clear':
                    self.data = {}
                    print("Data cleared")
                else:
                    self.process_input(user_input)
                    
            except KeyboardInterrupt:
                print("\n\nEditor interrupted")
                save_choice = input("Save changes? (y/n): ").strip().lower()
                if save_choice == 'y':
                    self.save()
                break
            except EOFError:
                print("\n\nEditor ended")
                break


class JsonReadFileError(Exception):
    """ Error occurred during reading json file. """


class SaveFileError(Exception):
    """ Error occurred during saving file. """


def main():
    """Main function, can be run as a module"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JSON Editor')
    parser.add_argument('file', nargs='?', help='JSON file path to read')
    parser.add_argument('--save', '-s', help='File path to save (defaults to read file path)')
    
    args = parser.parse_args()
    
    editor = JsonEditor(args.file, args.save)
    editor.run()


if __name__ == '__main__':
    main()