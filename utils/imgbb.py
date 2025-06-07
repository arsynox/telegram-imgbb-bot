import requests
import base64
from typing import Optional, Dict, Any
import config

class ImgBBUploader:
    def __init__(self):
        self.servers = config.IMGBB_SERVERS
    
    async def upload_image(self, image_data: bytes, server: str = 'server_1') -> Optional[Dict[Any, Any]]:
        """Upload image to ImgBB using specified server with different API keys"""
        try:
            # Get server configuration
            server_config = self.servers.get(server)
            if not server_config:
                return {'success': False, 'error': 'Invalid server selected'}
            
            # Convert image to base64
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare upload data with server-specific API key and expiration
            upload_data = {
                'key': server_config['api_key'],
                'image': image_b64,
                'expiration': server_config['expiration']  # Different expiration for each server
            }
            
            # Upload image
            response = requests.post(server_config['url'], data=upload_data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('success'):
                # Calculate expiration info
                expiration_info = self._get_expiration_info(server_config['expiration'])
                
                return {
                    'success': True,
                    'url': result['data']['url'],
                    'delete_url': result['data']['delete_url'],
                    'display_url': result['data']['display_url'],
                    'size': result['data']['size'],
                    'title': result['data']['title'],
                    'server_name': server_config['name'],
                    'expiration_info': expiration_info,
                    'server_icon': server_config['icon']
                }
            else:
                return {'success': False, 'error': 'Upload failed'}
                
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f'Network error: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def _get_expiration_info(self, expiration_seconds: int) -> str:
        """Get human-readable expiration information"""
        if expiration_seconds == 0:
            return "Permanent (Never expires)"
        elif expiration_seconds == 2592000:  # 1 month
            return "1 Month (Auto-delete)"
        elif expiration_seconds == 15552000:  # 6 months
            return "6 Months (Auto-delete)"
        else:
            days = expiration_seconds // 86400
            return f"{days} Days (Auto-delete)"
    
    def get_server_info(self, server: str) -> Dict[str, Any]:
        """Get detailed server information"""
        server_config = self.servers.get(server, {})
        return {
            'name': server_config.get('name', 'Unknown'),
            'description': server_config.get('description', 'No description'),
            'icon': server_config.get('icon', '📁'),
            'expiration': server_config.get('expiration', 0)
        }
