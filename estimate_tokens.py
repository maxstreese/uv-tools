import subprocess
import os
import tiktoken
from collections import defaultdict
from prettytable import PrettyTable

# Get list of all files known to git in the repository
files = subprocess.check_output('git ls-files', shell=True).decode('utf-8').splitlines()

# Group files by extension
files_by_extension = defaultdict(list)
for file_path in files:
    _, ext = os.path.splitext(file_path)
    ext = ext.strip('.').capitalize() if ext else 'No extension'
    files_by_extension[ext].append(file_path)

# Initialize token counter
token_counts = defaultdict(int)
file_counts = defaultdict(int)
encoding = tiktoken.get_encoding('o200k_base')

# Count tokens by extension
for ext, file_list in files_by_extension.items():
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tokens = encoding.encode(content)
                token_counts[ext] += len(tokens)
                file_counts[ext] += 1
        except Exception as e:
            print(f'Error processing {file_path}: {e}')

# Set up pretty table
table = PrettyTable()
table.field_names = ['Extension', 'Files', 'Tokens']
table.align['Extension'] = 'l'
table.align['Files'] = 'r'
table.align['Tokens'] = 'r'

# Add extension rows to table
for ext, count in sorted(token_counts.items(), key=lambda x: x[1], reverse=True):
    table.add_row([ext, file_counts[ext], count])

# Add total row to table
table.add_divider()
table.add_row(['Total', sum(file_counts.values()), sum(token_counts.values())])

# Print table
print(table)
