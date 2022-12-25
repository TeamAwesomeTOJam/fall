import os

from fall import settings
from fall.main import main


settings.ROOT = os.path.dirname(__file__)
settings.RES = os.path.join(settings.ROOT, 'res')
main()