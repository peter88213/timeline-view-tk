"""Helper module for ID generation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class IdGenerator:

    @classmethod
    def new_id(cls, elements, prefix=''):
        """Return an unused ID for a new element.
        
        Positional arguments:
            elements -- list or dictionary containing all existing IDs
        """
        i = 1
        while f'{prefix}{i}' in elements:
            i += 1
        return f'{prefix}{i}'

