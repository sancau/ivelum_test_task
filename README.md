### Test task for http://ivelum.com
- a simple http proxy server that modifies page content
### Usage:
```bash
git clone https://github.com/sancau/ivelum_test_task
cd ivelum_test_task
```
#### Using Docker:
```bash
docker build -t ivelum_test_task .
docker run -p 8080:8080 -it --rm ivelum_test_task
```
#### Localy:
```bash
pip install -r requirements.txt
cd src
python proxyhttp.py
```

#### Optionally CLI accepts arguments:
- --host (default is localhost) 
- --port (default is 8080) 
- --target (the domain to proxy from, default is https://habrahabr.ru)

##### Python 3.5+
