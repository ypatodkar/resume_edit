# Node.js Lambda Backend

## Why Node.js?

✅ **No Docker needed** - Works directly on macOS/Windows  
✅ **No grpc issues** - Node.js packages are portable  
✅ **Simpler Lambda deployment** - Just zip and upload  
✅ **Faster cold starts** - Node.js is lightweight  

## Build Lambda Zip

```bash
cd backend-nodejs
npm install
zip -r lambda_deployment.zip . -x "*.git*" "node_modules/.cache/*"
```

That's it! No Docker needed.

## Upload to Lambda

1. Upload `lambda_deployment.zip`
2. Handler: `index.handler`
3. Runtime: `Node.js 18.x` or `Node.js 20.x`
4. Environment: `GEMINI_API_KEY` = your key
5. Timeout: 60s, Memory: 512MB

## Local Testing

```bash
npm install
GEMINI_API_KEY=your-key node index.js
```

## File Size

Node.js version is much smaller (~5-10 MB vs 40 MB Python version)

