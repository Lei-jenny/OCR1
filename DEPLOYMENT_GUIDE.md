# 🚀 Deployment Guide - OCR Menu Detector

This guide will help you deploy the OCR Menu Detector to GitHub and Vercel.

## 📁 Files to Upload to GitHub

### ✅ **Required Files (Upload These)**

```
ocr-menu-detector/
├── api/
│   ├── __init__.py          # Makes api a Python package
│   └── ocr.py              # Main Flask application
├── templates/
│   └── index.html          # Frontend interface
├── tests/
│   ├── test_ocr.py         # Unit tests
│   ├── sample_menu.jpg     # Test image
│   └── multilingual_menu.jpg
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
└── DEPLOYMENT_GUIDE.md    # This file
```

### ❌ **Files to Exclude (Don't Upload)**

- `__pycache__/` folders
- `api/ocr_demo.py` (demo version, not needed for production)
- `create_test_image.py` (utility script)
- `deploy.py` (local deployment script)
- `test_api.py` (local testing script)
- `test_tesseract.py` (local testing script)
- `package.json` (not needed for Python-only deployment)
- `static/` (empty folder)

## 🔧 GitHub Upload Steps

### 1. **Initialize Git Repository**
```bash
cd ocr-menu-detector
git init
git add .
git commit -m "Initial commit: OCR Menu Detector"
```

### 2. **Create GitHub Repository**
1. Go to GitHub.com
2. Click "New repository"
3. Name it: `ocr-menu-detector`
4. Make it public (for free Vercel deployment)
5. Don't initialize with README (you already have one)

### 3. **Push to GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/ocr-menu-detector.git
git branch -M main
git push -u origin main
```

## ☁️ Vercel Deployment Steps

### 1. **Connect to Vercel**
1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Import your `ocr-menu-detector` repository

### 2. **Configure Vercel Settings**
- **Framework Preset**: Other
- **Root Directory**: `./` (leave as default)
- **Build Command**: Leave empty (Vercel will auto-detect)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 3. **Environment Variables (Optional)**
If you need to set Tesseract path:
- Go to Project Settings → Environment Variables
- Add: `TESSDATA_PREFIX` = `/opt/render/project/src`

### 4. **Deploy**
Click "Deploy" and wait for the build to complete.

## 🐛 Troubleshooting

### **Common Issues:**

1. **Build Fails on Vercel**
   - Check that `requirements.txt` has all dependencies
   - Ensure `vercel.json` is properly configured
   - Check Vercel build logs for specific errors

2. **Tesseract Not Found**
   - Vercel doesn't support Tesseract OCR by default
   - Consider using a different OCR service for production
   - Or use a custom Docker image with Tesseract

3. **Template Not Found**
   - Ensure `templates/` folder is uploaded
   - Check Flask template configuration in `api/ocr.py`

### **Alternative OCR Solutions for Production:**

1. **Google Cloud Vision API**
2. **AWS Textract**
3. **Azure Computer Vision**
4. **Custom Docker with Tesseract**

## 📋 Pre-Deployment Checklist

- [ ] All required files are in the repository
- [ ] `.gitignore` excludes unnecessary files
- [ ] `requirements.txt` has all dependencies
- [ ] `vercel.json` is properly configured
- [ ] `README.md` has clear instructions
- [ ] Test the application locally first
- [ ] Check that all imports work correctly

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [Flask on Vercel](https://vercel.com/guides/deploying-flask-with-vercel)
- [Python Dependencies on Vercel](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)

## 📞 Support

If you encounter issues:
1. Check Vercel build logs
2. Test locally first
3. Verify all files are uploaded correctly
4. Check the GitHub repository structure
