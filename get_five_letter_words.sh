#!/bin/bash

cat /usr/share/dict/words | grep -Eow "\w{5}" > 5_let_words
