set pagination off
set logging file gdb.txt
set logging on
f 4

set print elements 0

p carp.mts_mgr_.first_block_
p pctx.comm_sz
p pctx.carp->oob_buffer_.buf_.size()

p carp->range_min_
p carp->range_max_

p carp.options_.rtp_pvtcnt[1]

p carp->rank_counts_
p carp->rank_bins_

set $ipx=0
set $end=$3

while $ipx < $end
  p carp->oob_buffer_->buf_[$ipx].indexed_prop
  set $ipx = $ipx + 1
end


quit
