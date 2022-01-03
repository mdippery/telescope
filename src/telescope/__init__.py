import datetime
import os.path
from importlib.metadata import version


__author__ = "Michael Dippery <michael@monkey-robot.com>"
__version__ = version("aws-telescope")
__date__ = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.dirname(__file__))).date()
__credits__ = f"""
Copyright (C) 2022 {__author__}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
""".strip()
