#!/bin/bash

if [[ ! ${RPEAT} ]] ; then REPEAT=1 ; fi
if [[ ! ${SLEEP} ]] ; then  SLEEP=1 ; fi
if [[ ! ${BATCH_REPEAT} ]] ; then BATCH_REPEAT=10 ; fi
if [[ ! ${BATCH_SLEEP} ]] ; then BATCH_SLEEP=0.5 ; fi

#    parser.add_argument('--timezone', type=str, choices=['local', 'UTC', 'ET', 'BR', 'JP', 'WS', 'AU', 'IT'], default='local', help='timezone for generated timestamp(s)')
 #    parser.add_argument('--enable-timezone-range', type=bool, nargs='?', const=True, default=False, help='whether or not to set timestamp within a "range"')
 #    parser.add_argument('--authentication', type=str, default=None, help='username, password')
 #    parser.add_argument('--timeout', type=float, default=30, help='REST timeout (in seconds)')
 #    parser.add_argument('--topic', type=str, default=None, help='topic for either REST POST or MQTT')

if [[ ! ${TIMEZONE} ]] ; then TIMEZONE=local ; fi
if [[ ! ${ENABLE_TIMEZONE_RANGE} ]] ; then ENABLE_TIMEZONE_RANGE=false ; fi
if [[ ! ${AUTHENTICATION} ]] ; then AUTHENTICATION='' ; fi
if [[ ! ${TIMEOUT} ]] ; then TIMEZONE=30 ; fi
if [[ ! ${PROTOCOL} == put ]] && [[ ! ${PROTOCOL} == print ]] && [[ ! ${PROTOCOL} == file ]] && [[ ! ${TOPIC}]] ; then echo "TOPIC required for protocol: ${PROTOCOL}" ; fi