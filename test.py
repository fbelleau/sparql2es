import re
m = re.search('(.*?)[(](.*?)[)]', 'MI:0000(unspecified)')
print(m.group(0), m.group(1), m.group(2))
