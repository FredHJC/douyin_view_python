import os
import requests
import json
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import time
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

class TikHubAPIClient:
    """
    TikHub API Client following the official demo implementation patterns
    Based on TikHub-API-Demo structure
    """
    
    def __init__(self, api_key: str = None):
        self.base_url = "https://api.tikhub.io"
        self.api_key = api_key or os.getenv('TIKHUB_API_KEY', '')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'DouyinViewTracker/2.0'
        }
        self.device_params = {
            'device_id': '7318518857994222633',
            'iid': '7318518857994222633'
        }
    
    def _make_request(self, endpoint: str, params: dict = None, method: str = 'GET'):
        """
        Internal method to make API requests with proper error handling
        Following the TikHub demo format
        """
        try:
            url = f"{self.base_url}{endpoint}"
            
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers)
            else:
                response = requests.post(url, headers=headers, json=params)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    return {'success': True, 'data': data.get('data'), 'raw_response': data}
                else:
                    return {'success': False, 'error': data.get('message', 'API returned error')}
            elif response.status_code == 401:
                return {'success': False, 'error': 'Authentication failed - check your API key'}
            elif response.status_code == 429:
                return {'success': False, 'error': 'Rate limit exceeded - please try again later'}
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}: {response.text}'}
                
        except requests.RequestException as e:
            return {'success': False, 'error': f'Network error: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def get_user_info(self, sec_user_id: str):
        """Get user information by sec_user_id"""
        url = f"{self.base_url}/api/v1/douyin/app/v3/handler_user_profile"
        
        params = {
            "sec_user_id": sec_user_id
        }
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200 and data.get('data'):
                    user_data = data['data'].get('user', {})
                    return {
                        'success': True,
                        'data': {
                            'nickname': user_data.get('nickname', ''),
                            'unique_id': user_data.get('unique_id', ''),
                            'sec_uid': user_data.get('sec_uid', ''),
                            'follower_count': user_data.get('follower_count', 0),
                            'following_count': user_data.get('following_count', 0),
                            'total_favorited': user_data.get('total_favorited', 0),
                            'aweme_count': user_data.get('aweme_count', 0),
                            'signature': user_data.get('signature', ''),
                            'ip_location': user_data.get('ip_location', ''),
                            'avatar_url': user_data.get('avatar_larger', {}).get('url_list', [''])[0] if user_data.get('avatar_larger') else ''
                        },
                        'timestamp': datetime.now().isoformat(),
                        'raw_response': data
                    }
                else:
                    return {'success': False, 'error': f"API returned code {data.get('code')} - {data.get('message', 'Unknown error')}"}
            elif response.status_code == 401:
                return {'success': False, 'error': 'Authentication failed - check your API key'}
            elif response.status_code == 429:
                return {'success': False, 'error': 'Rate limit exceeded - please try again later'}
            else:
                return {'success': False, 'error': f'Request failed with status code: {response.status_code}'}
                
        except requests.RequestException as e:
            return {'success': False, 'error': f'Network error: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def get_user_videos(self, user_id: str, max_cursor: int = 0, count: int = 20):
        """Get user's video list"""
        url = f"{self.base_url}/api/v1/douyin/app/v3/fetch_user_post_videos"
        
        params = {
            'user_id': user_id,
            'device_id': '7318518857994222633',
            'iid': '7318518857994222633',
            'max_cursor': max_cursor,
            'count': count
        }
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200 and data.get('data'):
                    videos = data['data'].get('aweme_list', [])
                    processed_videos = []
                    
                    for video in videos:
                        stats = video.get('statistics', {})
                        processed_videos.append({
                            'aweme_id': video.get('aweme_id', ''),
                            'desc': video.get('desc', ''),
                            'create_time': video.get('create_time', 0),
                            'author': {
                                'nickname': video.get('author', {}).get('nickname', ''),
                                'unique_id': video.get('author', {}).get('unique_id', '')
                            },
                            'statistics': {
                                'play_count': stats.get('play_count', 0),
                                'digg_count': stats.get('digg_count', 0),
                                'comment_count': stats.get('comment_count', 0),
                                'share_count': stats.get('share_count', 0)
                            },
                            'video_url': video.get('video', {}).get('play_addr', {}).get('url_list', [''])[0] if video.get('video') else '',
                            'cover_url': video.get('video', {}).get('cover', {}).get('url_list', [''])[0] if video.get('video') else ''
                        })
                    
                    return {
                        'success': True,
                        'data': {
                            'videos': processed_videos,
                            'has_more': data['data'].get('has_more', False),
                            'max_cursor': data['data'].get('max_cursor', 0),
                            'total': len(processed_videos)
                        },
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {'success': False, 'error': f"API returned code {data.get('code')} - {data.get('message', 'Unknown error')}"}
            else:
                return {'success': False, 'error': f'Request failed with status code: {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_video_info(self, video_url: str):
        """
        Get video information and statistics by share URL
        First gets aweme_id from fetch_one_video_by_share_url, then gets accurate stats from fetch_video_statistics
        """
        try:
            # Step 1: Get video details and aweme_id
            url = f"{self.base_url}/api/v1/douyin/app/v3/fetch_one_video_by_share_url"
            params = {
                'share_url': video_url
            }
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code != 200:
                return {'success': False, 'error': f'Request failed with status code: {response.status_code}'}
            
            data = response.json()
            if data.get('code') != 200:
                return {'success': False, 'error': f"API returned code {data.get('code')} - {data.get('message', 'Unknown error')}"}
            
            video_data = data['data'].get('aweme_detail', {})
            aweme_id = video_data.get('aweme_id', '')
            
            if not aweme_id:
                return {'success': False, 'error': 'Could not extract aweme_id from video'}
            
            # Step 2: Get accurate statistics using aweme_id
            stats_url = f"{self.base_url}/api/v1/douyin/app/v3/fetch_video_statistics"
            stats_params = {
                "aweme_ids": aweme_id
            }
            
            stats_response = requests.get(stats_url, params=stats_params, headers=headers)
            
            # Get original statistics from video data
            original_stats = video_data.get('statistics', {})
            
            # Initialize stats with original data
            stats = {
                'play_count': original_stats.get('play_count', 0),
                'digg_count': original_stats.get('digg_count', 0),
                'comment_count': original_stats.get('comment_count', 0),
                'share_count': original_stats.get('share_count', 0),
                'collect_count': original_stats.get('collect_count', 0)
            }
            
            # Try to get more accurate statistics from fetch_video_statistics API
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                if stats_data.get('code') == 200 and stats_data.get('data', {}).get('statistics_list'):
                    video_stats = stats_data['data']['statistics_list'][0]
                    # Update only the fields that are available in the statistics API
                    # Note: fetch_video_statistics doesn't include comment_count, so we keep the original
                    if 'play_count' in video_stats:
                        stats['play_count'] = video_stats['play_count']
                    if 'digg_count' in video_stats:
                        stats['digg_count'] = video_stats['digg_count']
                    if 'share_count' in video_stats:
                        stats['share_count'] = video_stats['share_count']
                    # comment_count and collect_count remain from original data
            
            # Extract other video information
            author = video_data.get('author', {})
            video_info = video_data.get('video', {})
            play_addr = video_info.get('play_addr', {})
            video_urls = play_addr.get('url_list', [])
            
            return {
                'success': True,
                'data': {
                    'aweme_id': aweme_id,
                    'desc': video_data.get('desc', ''),
                    'create_time': video_data.get('create_time', 0),
                    'duration': video_data.get('duration', 0),
                    'author': {
                        'nickname': author.get('nickname', ''),
                        'unique_id': author.get('unique_id', ''),
                        'sec_uid': author.get('sec_uid', ''),
                        'follower_count': author.get('follower_count', 0)
                    },
                    'statistics': stats,
                    'video_urls': video_urls,
                    'cover_url': video_info.get('cover', {}).get('url_list', [''])[0] if video_info.get('cover') else '',
                    'music': {
                        'title': video_data.get('music', {}).get('title', ''),
                        'author': video_data.get('music', {}).get('author', ''),
                        'play_url': video_data.get('music', {}).get('play_url', {}).get('url_list', [''])[0] if video_data.get('music', {}).get('play_url') else ''
                    }
                },
                'timestamp': datetime.now().isoformat(),
                'raw_response': data,
                'statistics_response': stats_response.json() if stats_response.status_code == 200 else None
            }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Initialize API client
api_client = TikHubAPIClient()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/search_user', methods=['POST'])
def search_user():
    """Search for user by sec_user_id"""
    try:
        data = request.get_json()
        sec_user_id = data.get('sec_user_id', '').strip()
        
        if not sec_user_id:
            return jsonify({'success': False, 'error': 'sec_user_id is required'}), 400
        
        result = api_client.get_user_info(sec_user_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_user_videos', methods=['POST'])
def get_user_videos():
    """Get user's video list"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', '').strip()
        max_cursor = data.get('max_cursor', 0)
        count = data.get('count', 20)
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID is required'}), 400
        
        result = api_client.get_user_videos(user_id, max_cursor, count)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_video_info', methods=['POST'])
def get_video_info():
    """Get video information and view count"""
    try:
        data = request.get_json()
        video_url = data.get('video_url', '').strip()
        
        if not video_url:
            return jsonify({'success': False, 'error': 'Video URL is required'}), 400
        
        result = api_client.get_video_info(video_url)
        
        if result['success']:
            # Format the response for frontend compatibility
            video_data = result['data']
            formatted_result = {
                'success': True,
                'timestamp': result['timestamp'],
                'video_info': {
                    'title': video_data['desc'],
                    'author': video_data['author']['nickname'],
                    'view_count': video_data['statistics']['play_count'],
                    'like_count': video_data['statistics']['digg_count'],
                    'comment_count': video_data['statistics']['comment_count'],
                    'share_count': video_data['statistics']['share_count'],
                    'duration': video_data['duration'],
                    'create_time': video_data['create_time'],
                    'cover_url': video_data['cover_url'],
                    'video_urls': video_data['video_urls']
                },
                'raw_data': result
            }
            return jsonify(formatted_result)
        else:
            return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/track_video', methods=['POST'])
def track_video():
    """Start tracking a video's view count"""
    try:
        data = request.get_json()
        video_url = data.get('video_url', '').strip()
        
        if not video_url:
            return jsonify({'success': False, 'error': 'Video URL is required'}), 400
        
        # Get initial video info
        result = api_client.get_video_info(video_url)
        
        if result['success']:
            video_data = result['data']
            tracking_data = {
                'video_url': video_url,
                'aweme_id': video_data['aweme_id'],
                'title': video_data['desc'],
                'author': video_data['author']['nickname'],
                'initial_view_count': video_data['statistics']['play_count'],
                'current_view_count': video_data['statistics']['play_count'],
                'like_count': video_data['statistics']['digg_count'],
                'comment_count': video_data['statistics']['comment_count'],
                'share_count': video_data['statistics']['share_count'],
                'last_updated': datetime.now().isoformat(),
                'tracking_started': datetime.now().isoformat()
            }
            
            return jsonify({
                'success': True,
                'message': 'Video tracking started',
                'data': tracking_data
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch video information'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test API connectivity
        if not api_client.api_key:
            return jsonify({
                'status': 'unhealthy',
                'error': 'API key not configured',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        return jsonify({
            'status': 'healthy',
            'api_configured': bool(api_client.api_key),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('TIKHUB_API_KEY'):
        print("⚠️  Warning: TIKHUB_API_KEY not found in environment variables")
        print("📝 Please create a .env file with your TikHub API key:")
        print("   TIKHUB_API_KEY=your_api_key_here")
        print("🔗 Get your API key from: https://api.tikhub.io/")
    else:
        print("✅ TikHub API key configured successfully")
        print(f"🔑 Using API key: {os.getenv('TIKHUB_API_KEY')[:20]}...")
    
    print("\n🚀 Starting Douyin View Tracker...")
    print("📱 Web interface: http://localhost:5001")
    print("📊 API docs: http://localhost:5001/docs")
    print("🔧 Health check: http://localhost:5001/api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 