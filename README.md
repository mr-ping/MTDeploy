## Features

- Execute git pull command in certain remote sever from local.
- Multiple service support.
- ...

## Requirements

- Python 2.7+ or 3.4+
- 3rd Package:
  - fabric
  - PyYaml

## Useage:

Change the configuration elements in conf.yaml file with your values.

Open your terminal:

```bash
python fabfile.py --serivce=service_price
```

It will pick up the 1st service if no service is pointed.

```bash
python fabfile.py
```

## TODO:

 1. Add exception detecting.
 2. Implement multiple server deployment.
 3. Multiple projects spport.
 4. Package the project ,emit to server and deploy it.
 5. Web Panel.
