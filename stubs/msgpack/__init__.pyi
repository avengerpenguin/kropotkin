from typing import Dict, List, Union

def packb(o: Union[Dict, List, int, float, str]) -> bytes: ...
def unpackb(b: bytes) -> Union[Dict, List, int, float, str]: ...