#!/bin/bash

whois $1 | grep abuse-mailbox | awk '{print $2}' | uniq | xargs echo
whois $1 | grep phone | awk '{print $2}' | uniq | xargs echo
#echo -e "$1"; whois $1 | grep abuse-mailbox | grep -v "abuse-mailbox" | awk '{print $2}'
