from backend.scanner import ClamAVScanner
import sys 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    scanner = ClamAVScanner()
    output = scanner.run_scan(directory_path)
    print(output)