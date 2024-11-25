#!/bin/bash

#Beet import automation
#---

#define global variables
ARTIST="artist_name"

#run the beets import command
docker exec -it beets beet import --group-albums "/music/${ARTIST}"