import argparse
from pickle import load

def main() -> None:
  p = argparse.ArgumentParser(description="...")
  p.add_argument('-b', '--backup-filename', help='Binary backup input filename', required=True)
  p.add_argument('-t', '--textual-filename', help='Textual backup output filename', required=True)
  args = p.parse_args()

  with open(args.backup_filename, 'rb') as fd:
    model = load(fd)
  
  with open(args.textual_filename, 'w') as fd:
    ...

if __name__ == '__main__':
  main()