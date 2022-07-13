# test-brownie
Test brownie framework

## venv

Activate the environment
```bash
python -m venv venv
source venv/bin/activate
```

Install packages in that environment:
```bash
pip install -r requirements.txt
```
or
```bash
pip install eth-brownie
```

Deactivate environment
```bash
deactivate
```

## Compile, deploy, test....
Compile:
```bash
brownie compile
```

Deploy (development):
```bash
brownie run scripts/deploy.py
```

Deploy (Rinkeby):
```bash
brownie run scripts/deploy.py --network rinkeby
```

Test:
```bash
brownie test
```

List networks:
```bash
brownie networks list
```