# diffenv

Generator script for comparing different environments (GitHub repo and Docker image)


# Requireonment

- MacOS
- `docker-compose` is enabled

# download

You only need to download diffenv.py

```
curl -O https://raw.githubusercontent.com/urahiroshi/diffenv/master/diffenv.py
```

# example

- When comparing `/dist` of `yarn build` between Node.js 6 and 8 (on your GITHUB_ORG/GITHUB_PROJ repository)

```bash
# generate Makefile and docker-compose.yml to current directory
python diffenv.py --repo $GITHUB_ORG/$GITHUB_PROJ --command "yarn && yarn build" --compare dist --a-image node:6 --a-branch master --b-image node:8 --b-branch master
# download source files
make setup
# execute command and compare directory
make abdiff
```

# tips

If you changed `Alice` directory and want to make same change to `Bob` directory, you can use `make atob` command.
(`make btoa` is reverse command (Bob => Alice))
