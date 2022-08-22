#!/usr/bin/env bash

parse_core() {
  rm gdb.txt
  BIN=/users/ankushj/repos/carp-umb-install/mpich-1804-2/bin/range-runner
  CORE_FILE=$1

  gdb -x pivots.gs $BIN $CORE_FILE
}

parse_log_line() {
  LOG=$1
  LINE=$2

  echo $(cat $LOG | egrep '^\$'$LINE' =') | awk -F= '{ print $2 }'
}

parse_log_arr() {
  LOG=$1
  LINE=$2

  echo $(cat $LOG | egrep '^\$'$LINE' =') | awk -F= '{ print $3 }'
}

parse_log_oob() {
  LOG=$1
  OOB_SZ=$2

  cat $LOG | tail -$OOB_SZ | awk -F= '{ print $2 }' | paste -sd, -
}

parse_log() {
  LOG=$1

  FIRSTBLOCK=$(parse_log_line $LOG 1)
  NRANKS=$(parse_log_line $LOG 2)
  OOB_SZ=$(parse_log_line $LOG 3)
  OOB_DATA=$(parse_log_oob $LOG $OOB_SZ)

  RANGE_MIN=$(parse_log_line $LOG 4)
  RANGE_MAX=$(parse_log_line $LOG 5)

  PVTCNT=$(parse_log_line $LOG 6)

  RANK_COUNTS=$(parse_log_arr $LOG 7)
  RANK_BINS=$(parse_log_arr $LOG 8)

  echo "const bool first_block = $FIRSTBLOCK;"
  echo "const int num_ranks = $NRANKS;"
  echo "const float oob_data[] = { $OOB_DATA };"
  echo "const int oob_data_sz = $OOB_SZ;"
  echo ""
  echo "const float range_min = $RANGE_MIN;"
  echo "const float range_max = $RANGE_MAX;"
  echo "const int num_pivots = $PVTCNT;"
  echo ""
  echo "const float rank_bin_counts[] = $RANK_COUNTS;"
  echo ""
  echo "const float rank_bins[] = $RANK_BINS;"
}

gen_test() {
  LOG=$1
  TEST=$2
  parse_log $LOG > temp.cc
  clang-format --style=google temp.cc > $TEST
  rm temp.cc
  cat $TEST
}

parse_core $1
gen_test gdb.txt test.cc
