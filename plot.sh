#!/bin/sh
# python3 draw.py {plot/hist/bar/scatter} {x 데이터 파일명, 따로 없으면 "False"} {y 데이터 파일명} {x label} {y label} {title} {plot filename} {x 데이터 숫자로 바꿔야 하면, int} {y sort 원하면, "True"} {x label tilt 원하면, "True"}

# python3 draw.py bar data_x_cache_hit_F\&F_GET.txt data_y_cache_hit_F\&F_GET.txt Cache_hit The_number_of_Cache_hit Cache_hit cache_hit_F\&F_GET str True True True
# python3 draw.py bar data_x_cache_hit_F\&F_POST.txt data_y_cache_hit_F\&F_POST.txt Cache_hit The_number_of_Cache_hit Cache_hit cache_hit_F\&F_POST str True True True
# python3 draw.py bar data_x_cache_hit_mediaService_GET.txt data_y_cache_hit_mediaService_GET.txt Cache_hit The_number_of_Cache_hit Cache_hit cache_hit_mediaService_GET str True True True


# python3 draw.py scatter ../webCrawler_try/Data_y.txt ../webCrawler_try/Data_x.txt object_size TTL Object_size_of_TTL ttl_object_size int False False False True
# python3 draw.py plot ../webCrawler_try/Data_x.txt False TTL\(s\) cdf TTL ttl_log int False False False False False True True
python3 draw.py plot ../webCrawler_try/Data_x.txt False TTL\(s\) cdf TTL ttl_log {\"xStringTo\":\"int\",\"cdf\":1000,\"xLog\":\"True\"} 