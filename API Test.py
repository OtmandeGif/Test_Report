import youtrack
import requests
from youtrack import *
from youtrack.connection import Connection as YouTrack

yt = YouTrack('https://youtrack.interne.urgotech.xyz', token='perm:bWNvcXVlcnk=.NDktNQ==.glnCuKTPiNpRWOZ6eh39KCckGYvMpo')

card=yt.getIssue('NIOS-108')
print(type(card.Swimlane)==list)


