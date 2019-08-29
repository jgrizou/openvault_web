#!/bin/bash

# brew install rsync on MacOS if rsync does not recognize --info=progress2 option

rsync -az --info=progress2 --info=name0 --stats jgrizou@openvault.jgrizou.com:/home/jgrizou/workspace/openvault_web/server/logs .
