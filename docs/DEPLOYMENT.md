# 🚀 Deployment Guide - Agentic AI Honeypot System

## Quick Deploy (Development)

```bash
cd "e:\Agentic Honeypot"
pip install -r requirements.txt
python -m src.api
```

Server runs on: `http://localhost:5000`

---

## Production Deployment

### Prerequisites
- Python 3.8+
- PostgreSQL (for production database)
- Redis (for scaling, optional)
- Linux/Unix server (Ubuntu 20.04+ recommended)
- Domain name and SSL certificate

### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip postgresql redis-server nginx

# Create application user
sudo useradd -m -s /bin/bash honeypot
sudo su - honeypot
```

### Step 2: Deploy Application

```bash
# Clone repository (or upload files)
cd /home/honeypot
git clone <repository-url> agentic-honeypot
cd agentic-honeypot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Set permissions
chmod +x src/api.py
```

### Step 3: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit production configuration
nano .env
```

**Update these in .env for production:**
```
FLASK_ENV=production
API_HOST=127.0.0.1  # Don't expose directly
API_PORT=5000
DEBUG=False

# Use PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/honeypot

# Restrict API keys and IPs
AUTHORIZED_IPS=your_server_ip,law_enforcement_ip
API_KEYS=very_secure_production_key

# Security settings
HONEYPOT_EXPOSURE_THRESHOLD=0.7
ENABLE_SAFETY_CHECKS=true
```

### Step 4: Setup Database

```bash
# Create PostgreSQL database
sudo -u postgres psql <<EOF
CREATE DATABASE honeypot;
CREATE USER honeypot_user WITH PASSWORD 'very_secure_password';
GRANT ALL PRIVILEGES ON DATABASE honeypot TO honeypot_user;
EOF
```

### Step 5: Setup Gunicorn (WSGI Server)

```bash
# Install gunicorn
pip install gunicorn

# Create systemd service file
sudo nano /etc/systemd/system/honeypot.service
```

**Content of /etc/systemd/system/honeypot.service:**
```ini
[Unit]
Description=Agentic AI Honeypot System
After=network.target postgresql.service

[Service]
Type=notify
User=honeypot
WorkingDirectory=/home/honeypot/agentic-honeypot
Environment="PATH=/home/honeypot/agentic-honeypot/venv/bin"
EnvironmentFile=/home/honeypot/agentic-honeypot/.env
ExecStart=/home/honeypot/agentic-honeypot/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /home/honeypot/agentic-honeypot/logs/access.log \
    --error-logfile /home/honeypot/agentic-honeypot/logs/error.log \
    src.api:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable honeypot
sudo systemctl start honeypot
```

### Step 6: Setup Nginx Reverse Proxy

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/honeypot
```

**Content of /etc/nginx/sites-available/honeypot:**
```nginx
upstream honeypot_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /home/honeypot/agentic-honeypot/logs/nginx_access.log;
    error_log /home/honeypot/agentic-honeypot/logs/nginx_error.log;
    
    # Proxy settings
    location / {
        proxy_pass http://honeypot_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/honeypot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Setup SSL Certificate

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

### Step 8: Monitoring & Logging

```bash
# View service logs
sudo journalctl -u honeypot -f

# View application logs
tail -f /home/honeypot/agentic-honeypot/logs/error.log

# Monitor system
top  # Check CPU/Memory
df -h  # Check disk space
```

---

## Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create logs directory
RUN mkdir -p logs

# Set environment
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run gunicorn
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", \
     "--timeout", "120", "--access-logfile", "-", \
     "--error-logfile", "-", "src.api:app"]
```

**Docker Compose (docker-compose.yml):**
```yaml
version: '3.8'

services:
  honeypot:
    build: .
    container_name: honeypot-api
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://honeypot:password@db:5432/honeypot
      REDIS_HOST: cache
    depends_on:
      - db
      - cache
    volumes:
      - ./logs:/app/logs
    restart: always

  db:
    image: postgres:13-alpine
    container_name: honeypot-db
    environment:
      POSTGRES_DB: honeypot
      POSTGRES_USER: honeypot
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  cache:
    image: redis:7-alpine
    container_name: honeypot-cache
    restart: always

  nginx:
    image: nginx:alpine
    container_name: honeypot-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - honeypot
    restart: always

volumes:
  postgres_data:
```

**Deploy with Docker:**
```bash
docker-compose up -d
docker-compose logs -f
```

---

## Kubernetes Deployment

**honeypot-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: honeypot-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: honeypot-api
  template:
    metadata:
      labels:
        app: honeypot-api
    spec:
      containers:
      - name: honeypot
        image: your-registry/honeypot:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: honeypot-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: honeypot-api-service
spec:
  selector:
    app: honeypot-api
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: honeypot-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: honeypot-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Deploy:**
```bash
kubectl apply -f honeypot-deployment.yaml
kubectl logs -f deployment/honeypot-api
```

---

## Health Checks & Monitoring

### Application Health Check
```bash
curl -I http://localhost:5000/health
```

### System Monitoring
```bash
# CPU and Memory
watch -n 1 'ps aux | grep honeypot'

# Disk usage
watch -n 1 'df -h'

# Network connections
netstat -tulpn | grep 5000

# Database connections
sudo -u postgres psql -c "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"
```

### Log Aggregation
Consider setting up:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk** for log analysis
- **CloudWatch** if using AWS

---

## Backup & Recovery

### Database Backup
```bash
# Backup
sudo -u postgres pg_dump honeypot > backup.sql

# Restore
sudo -u postgres psql honeypot < backup.sql
```

### Application Backup
```bash
# Tar the application
tar -czf honeypot-backup.tar.gz /home/honeypot/agentic-honeypot

# Upload to S3
aws s3 cp honeypot-backup.tar.gz s3://your-bucket/backups/
```

---

## Security Hardening

### 1. Firewall Configuration
```bash
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 5432/tcp  # PostgreSQL (from specific IPs only)
```

### 2. Fail2Ban (DDoS Protection)
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 3. API Rate Limiting
Implement in production:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/v1/conversation', methods=['POST'])
@limiter.limit("100 per hour")
def create_conversation():
    ...
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
sudo journalctl -u honeypot -n 50

# Verify configuration
python -m py_compile src/api.py
```

### Database Connection Error
```bash
# Test connection
psql -h localhost -U honeypot -d honeypot

# Check PostgreSQL service
sudo systemctl status postgresql
```

### High Memory Usage
```bash
# Restart service
sudo systemctl restart honeypot

# Check for memory leaks
ps aux | grep honeypot | grep -v grep
```

---

## Performance Tuning

### Gunicorn Workers
```bash
# Recommended: (2 * CPU_cores) + 1
# For 4-core server: workers = 9
gunicorn --workers 9 src.api:app
```

### PostgreSQL Connection Pooling
Add PgBouncer:
```bash
sudo apt install pgbouncer
```

### Redis Optimization
```bash
# Increase max connections
redis-cli CONFIG SET maxclients 10000
```

---

## Maintenance Schedule

- **Daily:** Check error logs
- **Weekly:** Monitor disk usage, backup database
- **Monthly:** Update packages, review security logs
- **Quarterly:** Performance analysis, capacity planning

---

**Deployment Version:** 1.0.0  
**Last Updated:** February 3, 2026
