#!/usr/bin/env python

import argparse
from string import Template

A_NAME='Alice'
B_NAME='Bob'

T_DOCKER_COMPOSE='''
$name:
  image: $image
  volumes:
    - ./$name/src:/src
  command: sh -c "cd /src && $command"
'''

T_MAKEFILE='''
.PHONY: setup
setup:
  mkdir -p $a_name $b_name
	git clone --depth 1 -b $a_branch git@github.com:$repo.git $a_name/src
	git clone --depth 1 -b $b_branch git@github.com:$repo.git $b_name/src

.PHONY: abdiff
abdiff:
	docker-compose up
	find $a_name/src/$compare -type f -exec md5 {} \; > $a_name/_compare.md5
	find $b_name/src/$compare -type f -exec md5 {} \; > $b_name/_compare.md5
	diff $a_name/_compare.md5 $b_name/_compare.md5

.PHONY: adiff
adiff:
	docker-compose up $a_name
	find $a_name/src/$compare -type f -exec md5 {} \; > $a_name/_compare1.md5
	docker-compose up $a_name
	find $a_name/src/$compare -type f -exec md5 {} \; > $a_name/_compare2.md5
	diff $a_name/_compare1.md5 $a_name/_compare2.md5

.PHONY: bdiff
bdiff:
	docker-compose up $b_name
	find $b_name/src/$compare -type f -exec md5 {} \; > $b_name/_compare1.md5
	docker-compose up $b_name
	find $b_name/src/$compare -type f -exec md5 {} \; > $b_name/_compare2.md5
	diff $b_name/_compare1.md5 $b_name/_compare2.md5

.PHONY: atob
atob:
	(cd $a_name/src && git diff > ../repo.diff)
	(cd $b_name/src && patch -N -p 1 < ../../$a_name/repo.diff)

.PHONY: btoa
btoa:
	(cd $b_name/src && git diff > ../repo.diff)
	(cd $a_name/src && patch -N -p 1 < ../../$b_name/repo.diff)
'''

def generate_makefile(a_name, b_name, a_branch, b_branch, repo, compare):
  template = Template(T_MAKEFILE)
  return template.substitute(
    a_name=a_name,
    b_name=b_name,
    a_branch=a_branch,
    b_branch=b_branch,
    repo=repo,
    compare=compare
  )

def generate_docker_compose(a_name, b_name, a_image, b_image, command):
  template = Template(T_DOCKER_COMPOSE)
  a_compose = template.substitute(name=a_name, image=a_image, command=command)
  b_compose = template.substitute(name=b_name, image=b_image, command=command)
  return '\n'.join((a_compose, b_compose))

def main():
  parser = argparse.ArgumentParser(description='tool generator for comparing 2 environments')
  parser.add_argument('--repo', dest='repo', help='git repository', required=True)
  parser.add_argument('--command', dest='command', help='comparing command', required=True)
  parser.add_argument('--compare', dest='compare', help='compared directory', required=True)
  parser.add_argument('--a-image', dest='a_image', help="A's docker image", required=True)
  parser.add_argument('--a-branch', dest='a_branch', help="A's git repository", required=True)
  parser.add_argument('--a-name', dest='a_name', help="A's name", default=A_NAME)
  parser.add_argument('--b-image', dest='b_image', help="B's docker image", required=True)
  parser.add_argument('--b-branch', dest='b_branch', help="B's git repository", required=True)
  parser.add_argument('--b-name', dest='b_name', help="B's name", default=B_NAME)
  args = parser.parse_args()
  with open('Makefile', 'w') as f:
    f.write(generate_makefile(
      a_name=args.a_name,
      b_name=args.b_name,
      a_branch=args.a_branch,
      b_branch=args.b_branch,
      repo=args.repo,
      compare=args.compare
    ))
  with open('docker-compose.yml', 'w') as f:
    f.write(generate_docker_compose(
      a_name=args.a_name,
      b_name=args.b_name,
      a_image=args.a_image,
      b_image=args.b_image,
      command=args.command
    ))

if __name__ == '__main__':
  main()
