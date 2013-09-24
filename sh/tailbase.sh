#!/bin/env sh
#/**
#* @file   tailbase.sh
#* @author alvayang <netyang@gmail.com>, brightown <brightown@gmail.com>
#* @date   Tue Sep 24 14:04:15 2013
#* 
#* @brief  A tail like tool, to view real time data stored in hbase.
#* 
#* 
#*/


ARGC=("$#")
DEBUG=$6

if [ ! $HBASE_BIN ]
then
if [ $4 ]
then
HBASE_BIN=$4
else
HBASE_BIN=/usr/local/hbase/bin
fi
fi

if [ $DEBUG > 0 ]
then
echo $HBASE_BIN
fi


function usage(){
echo "$0 [TimesAgo(minute)] [KeyPrefix] [ValuePart] [HBASE_BIN] [SLEEP SEC] [DEBUG]"
}

if [ ! -f $HBASE_BIN/hbase ]
then
echo "HBASE Not Found"
usage
exit
fi


if [[ "$1" =~ "^[0-9]+$" ]]
then
START_MIN=$1
else
START_MIN=0
fi



if [ $2 ]
then
DATA_PREFIX=$2
else
DATA_PREFIX=""
fi

if [ $3 ]
then
DATA_CHANNEL=$3
else
DATA_CHANNEL=""
fi

if [ $5 ]
then
SLEEP_TIME=$5
else
SLEEP_TIME=5
fi


DATE_START=`date '+%s'`
DATE_START=$((DATE_START-600))
DATE_START=$DATE_START"000"

while [ 1 > 0 ]
do
echo "scan 'coologger_data' ,{FILTER => \"(PrefixFilter('$DATA_PREFIX') AND (QualifierFilter(=,'substring:$DATA_CHANNEL'))\", TIMERANGE=>[$DATE_START, 9999999999999]}" |$HBASE_BIN/hbase shell
TMP_DATE=`date '+%s'`
sleep $SLEEP_TIME
DATE_START=$TMP_DATE"000"
done
