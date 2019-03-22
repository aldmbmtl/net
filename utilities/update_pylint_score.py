import os
import re
from subprocess import PIPE, Popen

ROOT = os.path.abspath(__file__ + '/../../')
reg_ex = re.compile(r'at ([0-9].+)/10 ')

process = Popen(
    'pylint net',
    shell=True,
    stdout=PIPE,
    stderr=PIPE,
    cwd=ROOT
)


report = str(process.stdout.read(), 'ascii')
score = reg_ex.search(report).groups()[0]
print(report)

with open(os.path.join(ROOT, 'score.txt'), 'w') as score_file:
    score_file.write(report)

readme = os.path.join(ROOT, 'README.rst')
with open(readme, 'r') as README:
    content = README.read()

result = re.sub(r'pybadge/badges/(.+)\.svg', 'pybadge/badges/{0}.svg'.format(score), content)
with open(readme, 'w') as README:
    README.write(result)

