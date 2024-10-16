import time
from functools import wraps

def profiling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 시작 시간
        result = func(*args, **kwargs)  # 함수 실행
        end_time = time.time()  # 끝 시간
        elapsed_time = end_time - start_time  # 경과 시간 계산
        print(f"'{func.__name__}' 함수 실행 시간: {elapsed_time:.6f}초")
        return result
    return wrapper
