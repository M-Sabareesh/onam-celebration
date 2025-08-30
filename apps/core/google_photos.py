"""
Google Photos integration stub - disabled in production
"""

class GooglePhotosService:
    def __init__(self):
        self.enabled = False
    
    def authenticate(self):
        return False
    
    def upload_photo(self, photo_path, album_id=None):
        return None
    
    def create_album(self, title, description=""):
        return None
    
    def get_photos(self, album_id=None):
        return []
    
    def is_authenticated(self):
        return False

# Global instance
google_photos_service = GooglePhotosService()

def get_google_photos_service():
    return google_photos_service
