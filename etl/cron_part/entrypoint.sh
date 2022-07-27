#!/bin/bash
sh /etl/checker.sh >> log.txt 2>&1 && cron -f 