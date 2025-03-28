def shorten_string(input_string: str, total_length: int = 50) -> str:
    """
    문자열을 지정된 길이에 맞춰 앞부분, 중간, 끝부분을 포함한 형식으로 축소합니다.

    Args:
        input_string (str): 축소할 원본 문자열
        total_length (int): 최종 출력할 문자열의 길이 (기본값: 50)

    Returns:
        str: 축소된 문자열
    """
    # 전체 길이가 지정된 최소 길이보다 작으면 그냥 반환
    if len(input_string) <= total_length:
        return input_string

    # 앞부분 20자와 중간의 '...' 그리고 끝부분 20% 부분을 계산
    front_length = 20
    end_length = max(1, int(total_length * 0.2))  # 끝부분은 최소 1자를 보장
    middle_length = total_length - front_length - end_length - 3  # '...' 부분을 제외한 길이 계산

    # 앞부분, 중간, 끝부분을 합쳐서 최종 문자열 만들기
    front = input_string[:front_length]
    middle = "..."
    end = input_string[-end_length:] if len(input_string) > total_length else ""

    return front + middle + end