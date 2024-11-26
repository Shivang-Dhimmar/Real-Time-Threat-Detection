import pyclamd
import sys
import os

class ClamAVScanner:

    def __init__(self):
        self.connection = pyclamd.ClamdUnixSocket()

    def is_clamd_daemon_running(self):
        try:
            return self.connection.ping() == True
        except pyclamd.ConnectionError:
            return False
        
    def scan_directory(self,directory_path):
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            sys.exit(1)
        try:
            result = self.connection.multiscan_file(directory_path)
            # print(result)
        except Exception as e:
            print(f"Error scanning file: {e}")
            sys.exit(1)
        return result
    
    def format_result(self,result):
        if result:
            messages = []
            for file, (status, name) in result.items():
                if status == 'OK' :
                    messages.append(f"Directory {file} is clean.")
                elif status == 'FOUND':
                    messages.append(f"Virus {name} detected in file {file}!")
                elif status=='ERROR':
                    messages.append(f"Error {name} happened in file {file}!")
                else:
                    messages.append("Unknown Output")
            return "\n".join(messages)
        else:
            return "Directory is empty!"
                


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    scanner = ClamAVScanner()
    output = scanner.run_scan(directory_path)
    print(output)