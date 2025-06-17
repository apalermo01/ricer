#!/usr/bin/env bash

if [[ ! -d ~/.config/ricer ]]; then
    mkdir ~/.config/ricer 
fi

cp ./config/ricer.yml ~/.config/ricer/ricer.yml
cp ./config/ricer-global.yml ~/.config/ricer/ricer-global.yml

