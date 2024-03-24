# Command
D://Project//Python//python-flask-microservices//sqlacodegen.exe mysql://root:database_password@127.0.0.1:36693/shippingrecord > models.py


```
python-flask-microservices
├─ .gitignore
├─ email
│  ├─ application.py
│  ├─ controllers
│  │  └─ email
│  │     ├─ email.py
│  │     └─ __init__.py
│  ├─ Dockerfile
│  ├─ extensions.py
│  ├─ requirements.txt
│  ├─ server.py
│  ├─ service
│  │  └─ email
│  │     ├─ email_service.py
│  │     └─ __init__.py
│  ├─ settings.py
│  ├─ utils
│  │  ├─ email_template.html
│  │  └─ helper.py
│  └─ __init__.py
├─ inventory
│  ├─ application.py
│  ├─ controllers
│  │  ├─ inventory
│  │  │  ├─ inventory.py
│  │  │  └─ __init__.py
│  │  └─ mq
│  │     ├─ mq.py
│  │     └─ __init__.py
│  ├─ Dockerfile
│  ├─ extensions.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ server.py
│  ├─ service
│  │  ├─ inventory
│  │  │  ├─ inventory_service.py
│  │  │  └─ __init__.py
│  │  ├─ mq_consumer
│  │  │  ├─ mq_consumer_service.py
│  │  │  └─ __init__.py
│  │  └─ mq_product
│  │     ├─ mq_producer_service.py
│  │     └─ __init__.py
│  ├─ settings.py
│  ├─ utils
│  │  └─ helper.py
│  └─ __init__.py
├─ README.md
├─ requirements.txt
├─ shipping
│  ├─ application.py
│  ├─ controllers
│  │  ├─ mq
│  │  │  ├─ mq.py
│  │  │  └─ __init__.py
│  │  └─ shipping_record
│  │     ├─ shipping_record.py
│  │     └─ __init__.py
│  ├─ Dockerfile
│  ├─ extensions.py
│  ├─ models.py
│  ├─ requirements.txt
│  ├─ server.py
│  ├─ service
│  │  ├─ mq_consumer
│  │  │  ├─ mq_consumer_service.py
│  │  │  └─ __init__.py
│  │  ├─ mq_product
│  │  │  ├─ mq_producer_service.py
│  │  │  └─ __init__.py
│  │  └─ shipping_record
│  │     ├─ shipping_record_service.py
│  │     └─ __init__.py
│  ├─ settings.py
│  ├─ utils
│  │  └─ helper.py
│  └─ __init__.py
├─ sqlacodegen.exe
└─ virtual.bat

```