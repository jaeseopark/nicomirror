from functools import wraps
from typing import Callable, List, Tuple, Union

def _validate(validations: List[Tuple[Union[str, List[str]], Callable[[str], None]]]):
    def validate(**kwargs):
        for variable_names, assert_func in validations:
            if isinstance(variable_names, str):
                variable_names = [variable_names]

            for variable_name in variable_names:
                assert variable_name in kwargs, f"VARIABLE_NOT_FOUND_IN_KWARGS {variable_name=}"
                assert_func(kwargs[variable_name])

    def inner(func):
        @wraps(func)
        def inner2(*args, **kwargs):
            validate(**kwargs)
            return func(*args, **kwargs)
        return inner2
    return inner

def validate_video_ids(variable_names: Union[str, List[str]]):
    def _validate_video_id(video_id: str):
        # TODO use regex for ID validation
        assert video_id.startswith("sm") or video_id.startswith("nm"), "video_id must start with 'sm' or 'nm'."

    return _validate([(variable_names, _validate_video_id)])

def validate_playlist_ids(variable_names: Union[str, List[str]]):
    def _validate_playlist_id(playlist_id: str):
        assert playlist_id.isdigit(), "playlist_id must be all-numeric."

    return _validate([(variable_names, _validate_playlist_id)])
