# Quick Start Guide - ANPR System

## 🚀 Getting Started

### Step 1: Backend Setup (Flask)

The backend is already configured with CORS support. Make sure it's running:

```bash
# Navigate to ANPR directory
cd d:\ANPR

# Activate virtual environment (if using one)
venv\Scripts\activate

# Run the Flask server
python app.py
```

The backend should be running on: **http://127.0.0.1:5000**

### Step 2: Frontend Setup (React)

```bash
# Navigate to frontend directory
cd d:\ANPR\frontend

# Install dependencies (first time only)
npm install

# Start the React development server
npm start
```

The frontend will automatically open in your browser at: **http://localhost:3000**

## 📋 Usage

### Home Page
1. Click on the upload area or "Choose Image or Video"
2. Select an image (JPG, PNG) or video (MP4) file
3. Preview will appear automatically
4. Click "Detect Plate" button
5. Wait for processing (loading spinner will show)
6. View results:
   - Detected plate number (in green)
   - Confidence score
   - Processed output image/video

### History Page
1. Click "History" in the navigation bar
2. View all previous detections in a table
3. Click on any thumbnail to view full image
4. Click "Refresh" to update the list

## 🎨 Features

✅ Modern, responsive UI
✅ Real-time loading indicators
✅ Error handling with friendly messages
✅ File preview before detection
✅ Confidence score visualization
✅ Latest records appear first
✅ Mobile-friendly design
✅ Smooth animations

## 🔧 Troubleshooting

### Backend not responding
- Ensure Flask server is running on port 5000
- Check if `flask-cors` is installed: `pip install flask-cors`

### Frontend errors
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### CORS errors
- Verify CORS is enabled in `app.py`
- Check browser console for specific errors

## 📱 Responsive Design

The UI is fully responsive and works on:
- Desktop (1920px+)
- Laptop (1024px - 1920px)
- Tablet (768px - 1024px)
- Mobile (320px - 768px)

## 🎯 API Endpoints

- **POST** `/detect` - Upload file for detection
- **GET** `/history` - Fetch all detection records

## 💡 Tips

- Supported formats: JPG, JPEG, PNG (images), MP4 (videos)
- Best results with clear, well-lit images
- Confidence scores above 80% are highly reliable
- History is stored in `history.json` in the backend

---

**Enjoy using the ANPR System! 🚗✨**
