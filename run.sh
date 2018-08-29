#!/bin/bash

user=${1?No username given}

docker run -it --env-file chat.env --rm rocketchat-delete-user "$user"
