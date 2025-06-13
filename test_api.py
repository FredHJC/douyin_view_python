#!/usr/bin/env python3
"""
Test script to verify TikHub API integration
Based on TikHub API demo patterns
"""

import os
import requests
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TikHubAPIClient:
    """
    TikHub API Client following the demo implementation patterns
    """
    
    def __init__(self, api_key: str = None):
        self.base_url = "https://api.tikhub.io"
        self.api_key = api_key or os.getenv('TIKHUB_API_KEY', '')
        self.test_sec_user_id = os.getenv('TEST_SEC_USER_ID', '')
    
    def test_connection(self):
        """Test basic API connection"""
        if not self.api_key:
            return {
                'success': False,
                'error': 'API key not found. Please set TIKHUB_API_KEY in your .env file'
            }
        
        try:
            # Simple health check endpoint (if available)
            url = f"{self.base_url}/api/v1/douyin/app/v3/handler_user_profile"
            
            params = {
                "sec_user_id": self.test_sec_user_id
            }
            
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(url, params=params, headers=headers)
            print(f'type(response): {type(response)}')
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200 and data.get('data'):
                    return {'success': True, 'message': 'API connection successful'}
                else:
                    return {'success': False, 'error': f"API Error: Code {data.get('code')} - {data.get('message', 'Unknown error')}"}
            elif response.status_code == 401:
                return {'success': False, 'error': 'Authentication failed - invalid API key'}
            elif response.status_code == 429:
                return {'success': False, 'error': 'Rate limit exceeded'}
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}: {response.text}'}
            
        except Exception as e:
            return {'success': False, 'error': f'Connection failed: {str(e)}'}
    
    def fetch_douyin_user_data(self, sec_user_id: str):
        """
        Fetch Douyin user data using TikHub API
        """
        url = "https://api.tikhub.io/api/v1/douyin/app/v3/handler_user_profile"
        
        params = {
            "sec_user_id": sec_user_id
        }
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            print(f"👤 Fetching user data for: {sec_user_id}")
            response = requests.get(url, params=params, headers=headers)
            print(f'type(response): {type(response)}')
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                print(f"📊 API Response code: {data.get('code')}")
                print(f"📊 API Response keys: {list(data.keys())}")
                
                if data.get('code') == 200 and data.get('data'):
                    user_data = data['data'].get('user', {})
                    
                    # Format and display user information
                    print("✅ User data retrieved successfully!")
                    print(f"📱 Nickname: {user_data.get('nickname', 'N/A')}")
                    print(f"🆔 Unique ID: {user_data.get('unique_id', 'N/A')}")
                    print(f"🔒 Sec UID: {user_data.get('sec_uid', 'N/A')}")
                    print(f"👥 Followers: {user_data.get('follower_count', 0):,}")
                    print(f"➕ Following: {user_data.get('following_count', 0):,}")
                    print(f"❤️ Total Likes: {user_data.get('total_favorited', 0):,}")
                    print(f"🎵 Videos: {user_data.get('aweme_count', 0):,}")
                    print(f"📝 Bio: {user_data.get('signature', 'N/A')}")
                    print(f"🌍 IP Location: {user_data.get('ip_location', 'N/A')}")
                    
                    return {
                        'success': True,
                        'data': user_data,
                        'formatted_info': {
                            'nickname': user_data.get('nickname', 'N/A'),
                            'unique_id': user_data.get('unique_id', 'N/A'),
                            'sec_uid': user_data.get('sec_uid', 'N/A'),
                            'followers': user_data.get('follower_count', 0),
                            'following': user_data.get('following_count', 0),
                            'total_likes': user_data.get('total_favorited', 0),
                            'video_count': user_data.get('aweme_count', 0),
                            'signature': user_data.get('signature', 'N/A'),
                            'ip_location': user_data.get('ip_location', 'N/A'),
                            'avatar_url': user_data.get('avatar_larger', {}).get('url_list', [''])[0] if user_data.get('avatar_larger') else ''
                        },
                        'raw_response': data
                    }
                else:
                    error_msg = f"API returned code {data.get('code')} - {data.get('message', 'Unknown error')}"
                    print(f"❌ API Error: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                error_msg = f"Request failed with status code: {response.status_code}"
                print(f"❌ {error_msg}")
                print(f"Response: {response.text}")
                return {'success': False, 'error': error_msg}
                
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}
    
    def fetch_video_statistics(self, video_url: str):
        """
        Fetch video statistics using TikHub API
        First gets aweme_id from fetch_one_video_by_share_url, then gets accurate stats from fetch_video_statistics
        """
        try:
            # Step 1: Get video details and aweme_id
            print(f"🎵 Fetching video data for: {video_url}")
            url = "https://api.tikhub.io/api/v1/douyin/app/v3/fetch_one_video_by_share_url"
            
            params = {
                "share_url": video_url
            }
            
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(url, params=params, headers=headers)
            print(f'type(response): {type(response)}')
            
            # Check if request was successful
            if response.status_code != 200:
                error_msg = f"Request failed with status code: {response.status_code}"
                print(f"❌ {error_msg}")
                return {'success': False, 'error': error_msg}
            
            data = response.json()
            print(f"📊 API Response code: {data.get('code')}")
            print(f"📊 API Response keys: {list(data.keys())}")
            
            if data.get('code') != 200:
                error_msg = f"API returned code {data.get('code')} - {data.get('message', 'Unknown error')}"
                print(f"❌ API Error: {error_msg}")
                return {'success': False, 'error': error_msg}
            
            video_data = data['data'].get('aweme_detail', {})
            aweme_id = video_data.get('aweme_id', '')
            
            if not aweme_id:
                error_msg = "Could not extract aweme_id from video"
                print(f"❌ {error_msg}")
                return {'success': False, 'error': error_msg}
            
            print(f"🆔 Extracted aweme_id: {aweme_id}")
            
            # Step 2: Get accurate statistics using aweme_id
            print(f"📊 Fetching accurate statistics for aweme_id: {aweme_id}")
            stats_url = "https://api.tikhub.io/api/v1/douyin/app/v3/fetch_video_statistics"
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
                print(f"📊 Statistics API Response code: {stats_data.get('code')}")
                
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
                    print("✅ Enhanced statistics retrieved from fetch_video_statistics API!")
                    print(f"📊 Using original comment_count: {original_stats.get('comment_count', 0)}")
                else:
                    print("⚠️ Using statistics from original video data (fetch_video_statistics failed)")
            else:
                print(f"⚠️ Statistics API failed with status {stats_response.status_code}, using original stats")
            
            author = video_data.get('author', {})
            
            # Format and display video information
            print("✅ Video data retrieved successfully!")
            print(f"🎬 Title: {video_data.get('desc', 'N/A')}")
            print(f"👨‍💼 Author: {author.get('nickname', 'N/A')} (@{author.get('unique_id', 'N/A')})")
            print(f"👀 Views: {stats.get('play_count', 0):,}")
            print(f"❤️ Likes: {stats.get('digg_count', 0):,}")
            print(f"💬 Comments: {stats.get('comment_count', 0):,}")
            print(f"📤 Shares: {stats.get('share_count', 0):,}")
            print(f"⭐ Collects: {stats.get('collect_count', 0):,}")
            print(f"⏱️ Duration: {video_data.get('duration', 0) / 1000:.1f}s")
            
            return {
                'success': True,
                'data': video_data,
                'formatted_stats': {
                    'title': video_data.get('desc', 'N/A'),
                    'author': author.get('nickname', 'N/A'),
                    'unique_id': author.get('unique_id', 'N/A'),
                    'views': stats.get('play_count', 0),
                    'likes': stats.get('digg_count', 0),
                    'comments': stats.get('comment_count', 0),
                    'shares': stats.get('share_count', 0),
                    'collects': stats.get('collect_count', 0),
                    'duration': video_data.get('duration', 0),
                    'aweme_id': aweme_id,
                    'create_time': video_data.get('create_time', 0)
                },
                'raw_response': data,
                'statistics_response': stats_response.json() if stats_response.status_code == 200 else None
            }
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ {error_msg}")
            return {'success': False, 'error': error_msg}

def main():
    """Main test function"""
    print("🎵 TikHub API Test Script")
    print("=" * 50)
    
    # Initialize client
    client = TikHubAPIClient()
    
    # Test connection
    print("\n🔌 Testing API Connection...")
    connection_result = client.test_connection()
    if connection_result['success']:
        print(f"✅ {connection_result['message']}")
    else:
        print(f"❌ Connection failed: {connection_result['error']}")
        return
    
    # Test user data fetching  
    print("\n👤 Testing User Data Fetching...")
    test_sec_user_id = input("Enter a Douyin sec_user_id (or press Enter to use default from .env): ").strip()
    if not test_sec_user_id:
        test_sec_user_id = client.test_sec_user_id
        print(f"Using default sec_user_id from .env: {test_sec_user_id}")
    
    user_result = client.fetch_douyin_user_data(test_sec_user_id)
    
    # Test video statistics fetching
    print("\n🎵 Testing Video Statistics Fetching...")
    test_video_url = input("Enter a Douyin video URL (or press Enter to skip): ").strip()
    if test_video_url:
        video_result = client.fetch_video_statistics(test_video_url)
    else:
        print("Skipping video statistics test")
    
    print("\n🎉 Test completed!")
    print("\nTip: Make sure your .env file contains a valid TIKHUB_API_KEY")
    print("Get your API key from: https://api.tikhub.io/")

if __name__ == "__main__":
    main() 