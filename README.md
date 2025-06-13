# Douyin View Tracker 🎵

A Python web application with an HTML frontend that tracks real-time view counts for Douyin (Chinese TikTok) videos using the TikHub API. **Now updated with improved TikHub API demo patterns!**

## Features

- 🎯 **Real-time View Tracking**: Monitor view counts, likes, comments, and shares in real-time
- 👤 **User Search**: Search for Douyin users and browse their video collections
- 📊 **Beautiful Dashboard**: Modern, responsive web interface with live statistics
- 🔄 **Auto-refresh**: Automatic updates every 30 seconds during tracking
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- ✨ **New**: Enhanced API client following TikHub official demo patterns
- 🛡️ **Robust Error Handling**: Improved error handling and response formatting
- 🔧 **Health Check**: Built-in API health monitoring endpoint

## Prerequisites

- Python 3.7 or higher
- TikHub API key (get it from [https://api.tikhub.io/](https://api.tikhub.io/))

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd douyin_view_python
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**:
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env and add your TikHub API key
   # Get your API key from: https://api.tikhub.io/
   nano .env
   ```

4. **Test your API connection**:
   ```bash
   python test_api.py
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser**:
   - Web Interface: [http://localhost:5000](http://localhost:5000)
   - Health Check: [http://localhost:5000/api/health](http://localhost:5000/api/health)

## What's New in v2.0

### Improved TikHub API Integration

The application has been completely refactored to follow the official TikHub API demo patterns:

- **Enhanced API Client**: New `TikHubAPIClient` class with proper error handling
- **Better Response Format**: Standardized API responses with success/error handling
- **Comprehensive Video Data**: Extract video URLs, cover images, music info, and more
- **User Profile Data**: Full user information including follower counts and avatar URLs
- **Robust Error Handling**: Proper HTTP status code handling and error messages
- **Health Monitoring**: Built-in health check endpoint for monitoring API status

### API Endpoints

#### Health Check
```
GET /api/health
```

#### Search User
```
POST /api/search_user
{
  "sec_user_id": "MS4wLjABAAAAhZxp015xL6y5KVIccX0xERirhZMEteLvl5lCM6XaiOk"
}
```

#### Get User Videos
```
POST /api/get_user_videos
{
  "user_id": "user123",
  "max_cursor": 0,
  "count": 20
}
```

#### Get Video Information
```
POST /api/get_video_info
{
  "video_url": "https://v.douyin.com/xxxxx/"
}
```

#### Track Video
```
POST /api/track_video
{
  "video_url": "https://v.douyin.com/xxxxx/"
}
```

## Testing

### Basic API Test
```bash
python test_api.py
```

This will test:
- API connection and authentication
- Video data fetching
- User data fetching (optional)

### Interactive Testing
The test script now provides interactive prompts:
1. Tests API connection automatically
2. Prompts for a Douyin video URL (or uses default)
3. Optionally prompts for user ID testing
4. Provides detailed feedback and next steps

## TikHub API Features

This application leverages the following TikHub API endpoints:

- **User Details**: `/api/v1/douyin/app/v3/handler_user_profile`
- **User Videos**: `/api/v1/douyin/app/v3/fetch_user_post_videos`
- **Video Info**: `/api/v1/douyin/app/v3/fetch_one_video`

All endpoints follow the official TikHub demo implementation patterns with:
- Proper device parameters (`device_id`, `iid`)
- Bearer token authentication
- Comprehensive error handling
- Structured response formatting
- **Updated**: Now uses `sec_user_id` parameter for user profile fetching

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# TikHub API Configuration
TIKHUB_API_KEY=your_tikhub_api_key_here

# Optional: Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### API Key Setup

1. Visit [TikHub.io](https://api.tikhub.io/)
2. Create an account and log in
3. Go to API Keys section
4. Generate a new API key with appropriate scopes
5. Copy the key to your `.env` file

## Troubleshooting

### Common Issues

1. **API Key Not Found**:
   ```
   ❌ ERROR: TIKHUB_API_KEY not found in environment variables
   ```
   - Ensure your `.env` file exists and contains the API key
   - Restart the application after adding the API key

2. **Authentication Failed**:
   ```
   ❌ Authentication failed - check your API key
   ```
   - Verify your API key is correct
   - Check if the API key has the required scopes
   - Ensure the API key hasn't expired

3. **Rate Limit Exceeded**:
   ```
   ❌ Rate limit exceeded - please try again later
   ```
   - Wait a few moments before making more requests
   - Consider upgrading your TikHub plan for higher rate limits

4. **Video URL Invalid**:
   - Ensure you're using valid Douyin video URLs
   - Supported formats: `https://v.douyin.com/xxxxx/`, `https://www.douyin.com/video/xxxxx`

### Debug Mode

Run with debug output:
```bash
FLASK_DEBUG=True python app.py
```

### Health Check

Monitor API status:
```bash
curl http://localhost:5000/api/health
```

## Quick Start Script

Use the provided quick start script:
```bash
chmod +x run.sh
./run.sh
```

This script will:
1. Check for `.env` file and create if needed
2. Set up virtual environment
3. Install dependencies
4. Run the application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes with `python test_api.py`
4. Ensure all tests pass
5. Submit a pull request

## Support

- **TikHub Documentation**: [https://api.tikhub.io/docs](https://api.tikhub.io/docs)
- **TikHub Discord**: [Discord Community](https://discord.gg/tikhub)
- **Issues**: Open an issue on GitHub

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **TikHub.io** for providing the comprehensive Douyin API
- **TikHub API Demo** for implementation patterns and best practices
- **Flask** and **PyWebIO** for the web framework
- **HTTPX** for async HTTP client capabilities

---

**🎯 Start tracking your Douyin videos today!**