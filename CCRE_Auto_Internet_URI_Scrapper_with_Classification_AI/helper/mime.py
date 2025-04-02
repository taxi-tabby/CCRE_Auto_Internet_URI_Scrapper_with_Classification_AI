import magic

def get_mime_type_from_binary(binary_data: bytes) -> str:
    """
    바이너리 데이터를 입력받아 MIME 타입을 반환합니다.
    
    Args:
        binary_data (bytes): MIME 타입을 확인할 바이너리 데이터.
        
    Returns:
        str: MIME 타입 문자열 (예: 'image/png', 'application/pdf' 등).
             MIME 타입을 확인할 수 없으면 'application/octet-stream' 반환.
    """
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(binary_data)
    except Exception:
        return 'application/octet-stream'
    
    return mime_type if mime_type else 'application/octet-stream'
