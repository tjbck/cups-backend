# Cups Backend

## Deployment

To deploy the backend on your local server, you must first install redis for user session management. 

We recommend that you use docker for your redis installation.

```
docker run -d -p 6379:6379 --restart always --name redis redis redis-server --requirepass "YOUR_PASSWORD" --save 60 1 --loglevel warning 
```