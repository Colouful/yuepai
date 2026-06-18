#!/bin/bash
cd /var/www/yuepai-admin/ruoyi-fastapi-backend
mv /usr/local/lib/python3.11/site-packages/utils.py /usr/local/lib/python3.11/site-packages/utils.py.hidden 2>/dev/null
python3 -m uvicorn run:app --host 0.0.0.0 --port 8001 --no-access-log
mv /usr/local/lib/python3.11/site-packages/utils.py.hidden /usr/local/lib/python3.11/site-packages/utils.py 2>/dev/null
