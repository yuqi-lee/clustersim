python simulation_one_time.py 7125 --num_servers 5 --cpus 32 --mem 81920 --workload xsbench,xgboost,snappy,redis   --use_shrink --ratios 9:35:23:33 --workload_ratios 100,50,80,50 --remotemem --until 200 --size 200 --max_far 163840
python simulation_one_time.py 8336 --num_servers 5 --cpus 32 --mem 81920 --workload snappy,xgboost,redis   --use_shrink --ratios 28:22:50 --workload_ratios 80,50,60 --remotemem --until 200 --size 200 --max_far 163840
python simulation_one_time.py 8836 --num_servers 5 --cpus 32 --mem 81920 --workload xsbench,pagerank,redis,snappy,xgboost   --use_shrink --ratios 28:16:27:17:12 --workload_ratios 100,100,60,80,50 --remotemem --until 200 --size 200 --max_far 163840
python simulation_one_time.py 9428 --num_servers 5 --cpus 32 --mem 81920 --workload snappy,redis,xgboost   --use_shrink --ratios 28:51:21 --workload_ratios 80,60,50 --remotemem --until 200 --size 200 --max_far 163840