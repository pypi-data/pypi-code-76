# basic:
#   status: offline
#   label: delivery_time
#   names:
#     file_name: "waybills.csv"
#   paths:
#     file_path: "TEST_ETAE/data/"
#     output_models_path: "TEST_ETAE/output/{task_id}/models/"
#     output_schemas_path: "TEST_ETAE/output/{task_id}/schemas/"
#     output_prediction_path: "TEST_ETAE/output/{task_id}/predictions/"
#     statistic_figs_path: 'TEST_ETAE/output/{task_id}/stat/figs/'
#     statistic_schemas_path: 'TEST_ETAE/output/{task_id}/stat/schemas/'
#     evaluation_schemas_path: 'TEST_ETAE/output/{task_id}/evaluations/schemas/'
#     evaluation_figs_path: 'TEST_ETAE/output/{task_id}/evaluations/figs/'
# layers:
#   ExampleGen:
#   StatisticsGen:
#   SchemaGen:
#     excepts:
#       - order_id
#       - item_name
#       - quantity
#       - cuisines
#       - average_cose
#       - minimum_order
#       - reviews_store
#       - pickup_longitude
#       - pickup_latitude
#       - pickup_geometry
#       - age
#       - marital_status
#       - occupation
#       - monthly_income
#       - educational_qualifications
#       - family_size
#       - pin_code
#       - perference
#       - late_delivery
#       - long_delivery_time
#       - google_maps_accuracy
#       - reviews
#       - dropoff_longitude
#       - dropoff_latitude
#   ExampleValidator:
#     SimpleImputer_cont:
#       params:
#         strategy: median
#       cols:
#         - order_amount
#         - delivery_distance
#         - avg_delivery_time
#         - avg_preparing_time
#         - rating
#         - votes
#         - aoi_period_order_num
#         - aoi_period_driver_num
#     SimpleImputer_cat:
#       params:
#         strategy: most_frequent
#       cols:
#         - aoi
#         - order_time_period
#         - medium
#         - gender
#         - residence_in_busy_location
#         - good_road_condition
#     SimpleImputer_ids:
#       astype: str
#       params:
#         strategy: constant
#         fill_value: unknown
#       cols:
#         - store_id
#         - buyer_id
#         - merchant
#         - cluster_id
#     SimpleImputer_time:
#       params:
#         strategy: constant
#         fill_value: NA
#       cols:
#         order_time
#   Transform:
#     StandardScaler:
#       cols:
#         - order_amount
#         - delivery_distance
#         - avg_delivery_time
#         - avg_preparing_time
#         - rating
#         - votes
#         - aoi_period_order_num
#         - aoi_period_driver_num
#       params:
#     MinMaxScaler:
#       cols:
#         - order_amount
#         - delivery_distance
#         - avg_delivery_time
#         - avg_preparing_time
#         - rating
#         - votes
#         - aoi_period_order_num
#         - aoi_period_driver_num
#       params:
#     LabelEncoder_cat:
#       params:
#       cols:
#         - aoi
#         - order_time_period
#         - medium
#         - gender
#         - residence_in_busy_location
#         - good_road_condition
#     LabelEncoder_ids:
#       params:
#       cols:
#         - store_id
#         - buyer_id
#         - merchant
#         - cluster_id
#     timeMapper:
#       params:
#         result_column: time_mark_col
#         time_interval_min: 5
#       cols:
#         - order_time
#   Trainer:
#     mode: single
#     LGBMRegressor:
#       params:
#         alpha: 0.5508436502606852
#         bagging_fraction: 0.7583226301873406
#         bagging_freq: 1
#         colsample_bytree: 0.6716616109822297
#         gamma: 1.2105080426450052
#         learning_rate: 0.1607676711490857
#         max_depth: 11
#         min_child_weight: 0.0002983296107160923
#         min_data_in_leaf: 1
#         num_boost_round: 55
#         num_leaves: 108
#         reg_alpha: 0.09705094039517195
#         reg_lambda: 0.07340442165433923
#         verbose: 0
#   Evaluator:
#     mean_squared_log_error:
#       mode: schema
#       params:
#         multioutput: raw_values
#   Loader:
#   Pusher:
#     format: "{name}_{dt}.pkl"
#   Predictor:
#     format: "{name}_{dt}.csv"