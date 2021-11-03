#!/bin/sh

sh lib/quartet_count.sh $1 | perl lib/summarize_quartets_stdin.pl > $2
