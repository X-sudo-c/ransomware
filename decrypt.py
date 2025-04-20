import os
from cryptography.fernet import Fernet

def decrypt_file(filepath, key):
    """Decrypt a single file"""
    try:
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()
        
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Remove .encrypted extension to restore original filename
        original_path = filepath.replace('.encrypted', '')
        with open(original_path, 'wb') as f:
            f.write(decrypted_data)
        
        os.remove(filepath)  # Delete the encrypted version
        print(f"Successfully decrypted: {filepath}")
        return True
    except Exception as e:
        print(f"Failed to decrypt {filepath}: {str(e)}")
        return False

def decrypt_directory(directory, key):
    """Decrypt all .encrypted files in a directory"""
    success_count = 0
    fail_count = 0
    
    for filename in os.listdir(directory):
        if filename.endswith('.encrypted'):
            filepath = os.path.join(directory, filename)
            if decrypt_file(filepath, key):
                success_count += 1
            else:
                fail_count += 1
    
    print(f"\nDecryption complete: {success_count} files decrypted, {fail_count} failures")

if __name__ == "__main__":
    # Replace this with your actual key (as bytes)
    # Example: key = b'Bq9h4Xg4KZcY1y53sJatwW7e8nzr6T2RkLmNp0OvQxM='
    key = input("Enter the decryption key: ").encode()
    
    target_dir = os.getcwd()  # Current working directory
    print(f"Attempting to decrypt files in: {target_dir}")
    
    decrypt_directory(target_dir, key)