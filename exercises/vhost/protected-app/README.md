# Copyable protected-project application

This dependency-free WSGI example demonstrates the RCC application contract without exposing production details.

```bash
python3 -m unittest -v
RCC_DEMO_MODE=1 python3 app.py
```

Production requirements:

- run behind the governed RCC reverse proxy;
- bind the backend only to the approved application network/interface;
- accept identity headers only from the proxy;
- require the expected `project_<name>` group in the app as well as at the proxy;
- use a production WSGI server and a dedicated non-login service account;
- use a narrowly scoped database account;
- never accept a filesystem path from a request;
- do not enable demo mode in production.
