import os
import requests
import datetime
import random
import pathlib
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

missed_messages_counter = 0
# is_rms_received = False

# AgACAgIAAxkBAANMYqjfumTDg4lXzvHm27bMhpRz6S4AArvBMRvC9EhJi1dwavnm2ngBAAMCAANzAAMkBA

photo_id_list = ['AgACAgIAAxkBAANhYqodH2whZO86cV8POITnQug7jV8AAje8MRvC9FBJr_UAAeIRrV1mAQADAgADcwADJAQ','AgACAgIAAxkBAANiYqodH2Mg_CgWAAFmsAn5_FPK-YbeAAI4vDEbwvRQSZ2PBQj1U_ylAQADAgADcwADJAQ','AgACAgIAAxkBAANjYqodPATftDDi-MaKAw3RWlFbgvYAAjm8MRvC9FBJL7lw2B1lHVMBAAMCAANzAAMkBA','AgACAgIAAxkBAANkYqodPLgWyHV91Uvm96-RNCetP0YAAju8MRvC9FBJInXXH_1QxFABAAMCAANzAAMkBA','AgACAgIAAxkBAANlYqodPCLt4P_kfictVbCAN5u7eIsAAjy8MRvC9FBJ1QABD6IOJK5WAQADAgADcwADJAQ','AgACAgIAAxkBAANmYqodPNA9uvQelG23dAYtzHHn9u4AAj28MRvC9FBJcHrWZqQH89kBAAMCAANzAAMkBA','AgACAgIAAxkBAANnYqodPH9uHeuG73TbscN0uDL85voAAj68MRvC9FBJlJuJRbNaxocBAAMCAANzAAMkBA','AgACAgIAAxkBAANoYqodPPMph2CPfHEuyJW5k0EHHnoAAj-8MRvC9FBJ_Qi2nDjh37EBAAMCAANzAAMkBA','AgACAgIAAxkBAANpYqodPJjaXfoNKA_U4EHGuJexsCgAAkC8MRvC9FBJEXK8atr9o0IBAAMCAANzAAMkBA','AgACAgIAAxkBAANqYqodPLScYW5A3m6MPsv0LEb9FQcAAkG8MRvC9FBJ5C-SQVV1GBoBAAMCAANzAAMkBA','AgACAgIAAxkBAANrYqodPGacm2oIcrbhktqPrfEsVgADSbwxG8L0UEk70HV-2e45VwEAAwIAA3MAAyQE','AgACAgIAAxkBAANsYqodPCIQbimq1ggpmIa9_Ek7vn8AAkq8MRvC9FBJd_PfxiDX4HMBAAMCAANzAAMkBA','AgACAgIAAxkBAANtYqodTbutw4agOBI_peQCBRqQ1SgAAku8MRvC9FBJDWuaY0KISIYBAAMCAANzAAMkBA','AgACAgIAAxkBAANuYqodTd5LlYnP3vRey5ebHhb5BzIAAky8MRvC9FBJwAPQDy6Rjz0BAAMCAANzAAMkBA','AgACAgIAAxkBAANvYqodTYF2HEudWPA1bm-VCWLmiFoAAk28MRvC9FBJuyYqSZQqm6ABAAMCAANzAAMkBA','AgACAgIAAxkBAANwYqodTekUvLySO4MtqOfd2LWLIPIAAk68MRvC9FBJrCIiZ8y_09gBAAMCAANzAAMkBA','AgACAgIAAxkBAANxYqodTUr5uHbiMchxr_CyQ7YizfYAAk-8MRvC9FBJcmpctKft_kIBAAMCAANzAAMkBA','AgACAgIAAxkBAANyYqodTQ_xm0JnLQYJtwE9ZR3sElgAAlC8MRvC9FBJSpgiNUVCrD0BAAMCAANzAAMkBA','AgACAgIAAxkBAANzYqodTUNomYHh33KT7_40VahYtUAAAlG8MRvC9FBJ_UH_e2oMM64BAAMCAANzAAMkBA','AgACAgIAAxkBAAN0YqodTRTaOwTGmjV5ja2taOMcWEcAAlK8MRvC9FBJHjCLDCeXUMgBAAMCAANzAAMkBA','AgACAgIAAxkBAAN1YqodTdalgVpUgEc74dJqoGHC0hQAAlO8MRvC9FBJ630PYq1mFa4BAAMCAANzAAMkBA','AgACAgIAAxkBAAN2YqodTV9LPNdSLU9r6g-24mMUwcMAAlS8MRvC9FBJhzglExsMGTMBAAMCAANzAAMkBA','AgACAgIAAxkBAAN3YqodV9GM3ixMZXZZxwhyFWL5UWIAAlW8MRvC9FBJYGeNVai4vQIBAAMCAANzAAMkBA','AgACAgIAAxkBAAN4YqodVzSPXHTel3_lMrlDebDIwosAAla8MRvC9FBJS95FVBhvmkABAAMCAANzAAMkBA','AgACAgIAAxkBAAN5YqodV1n1Jnqk1ytAHIgMFFe5a48AAle8MRvC9FBJnyNopNevIgkBAAMCAANzAAMkBA','AgACAgIAAxkBAAN6YqodV-iwMU1grHVlVPO0RUr9RzUAAli8MRvC9FBJgkwBWRVCaToBAAMCAANzAAMkBA','AgACAgIAAxkBAAN7YqodV9Nn6_YMVCRIUGb-Qoqoi1gAAlm8MRvC9FBJ_Mx6gNDNbIYBAAMCAANzAAMkBA','AgACAgIAAxkBAAN8YqodV_BK5KXw4Hrzo_8WhsasGhEAAlq8MRvC9FBJ9v_USUYIu5QBAAMCAANzAAMkBA','AgACAgIAAxkBAAN9YqodV_f_NYlo4-by1YnVasch4h8AAlu8MRvC9FBJULSUp_5uZC0BAAMCAANzAAMkBA','AgACAgIAAxkBAAN-YqodVzNUO6hbw8oYCHGa2cxUEX4AAly8MRvC9FBJYClcEAerWWABAAMCAANzAAMkBA','AgACAgIAAxkBAAN_YqodV_TvfJOG5GboI8FSMuLWvgwAAl28MRvC9FBJcO_E3_FAmSYBAAMCAANzAAMkBA','AgACAgIAAxkBAAOAYqodVyzr8g4yOUHRTsGhoTFWIJEAAl68MRvC9FBJM_XGfGKA5ysBAAMCAANzAAMkBA','AgACAgIAAxkBAAOBYqodY8QYvx1D_x4uvOHGP1tBF9EAAl-8MRvC9FBJf1x8hxdD2qkBAAMCAANzAAMkBA','AgACAgIAAxkBAAOCYqodY1rOyf0nGUvPbTvSYwHx_yIAAmC8MRvC9FBJLrHn8AbKAa0BAAMCAANzAAMkBA','AgACAgIAAxkBAAODYqodYxnMFcVhYLYbqy5Gv_ripQMAAmG8MRvC9FBJGxHSjlQReEkBAAMCAANzAAMkBA','AgACAgIAAxkBAAOEYqodYzK5F8en1m0vl9Rqf8glUHwAAmK8MRvC9FBJT3IIKcDeEZABAAMCAANzAAMkBA','AgACAgIAAxkBAAOFYqodYymuNSBpHchnXpYkWBKn0AYAAmO8MRvC9FBJFEk-azM4AVABAAMCAANzAAMkBA','AgACAgIAAxkBAAOGYqodY39l0Aqk9Rk7zrrycKq4Ib4AAmS8MRvC9FBJium_snmgBtcBAAMCAANzAAMkBA','AgACAgIAAxkBAAOHYqodY0rv7ClV38hmr3MmHDMXD7AAAmW8MRvC9FBJKIHDRqFJnSoBAAMCAANzAAMkBA','AgACAgIAAxkBAAOIYqodY1wz7MCoYGKVZufWDbmub8wAAma8MRvC9FBJkHu67OUmmxkBAAMCAANzAAMkBA','AgACAgIAAxkBAAOJYqodY8XudDeUlp_-lDxpM2oF0ogAAme8MRvC9FBJDBKTzXXQ_kABAAMCAANzAAMkBA','AgACAgIAAxkBAAOKYqodYze_s3HJJeP7IWuFDKiRu5QAAmi8MRvC9FBJ5Vf0oDnWUuUBAAMCAANzAAMkBA','AgACAgIAAxkBAAOLYqodeh4srTaFlzvH23LH3QHVniYAAmm8MRvC9FBJSXrTx8HAos8BAAMCAANzAAMkBA','AgACAgIAAxkBAAOMYqodejZ8QFcYa0Efsj1YRs0_Wq4AAmq8MRvC9FBJ61HZ_oCAvCMBAAMCAANzAAMkBA','AgACAgIAAxkBAAONYqodehSkN6NgD7LlwlVyJfLBaiYAAmu8MRvC9FBJ8zr6lBU__n0BAAMCAANzAAMkBA','AgACAgIAAxkBAAOOYqodetS4Mv6z4v34uSYFjTPcJfMAAmy8MRvC9FBJawABkUNdjRq8AQADAgADcwADJAQ','AgACAgIAAxkBAAOPYqoderqSa7kwbCscFuUv1IFC-rUAAm28MRvC9FBJ9QaL_KCeBTkBAAMCAANzAAMkBA','AgACAgIAAxkBAAOQYqodejSERQEKnx6b3lz1rrrAQl8AAm68MRvC9FBJvqcNGR42JFwBAAMCAANzAAMkBA','AgACAgIAAxkBAAORYqodejy882MQ-C4veUd6vyLJn0sAAm-8MRvC9FBJefCeGftgujkBAAMCAANzAAMkBA','AgACAgIAAxkBAAOSYqodepaDokGwJ8rzHiMPBMdusSMAAnC8MRvC9FBJZFs9phy1DjwBAAMCAANzAAMkBA','AgACAgIAAxkBAAOTYqoderA4Iki4M7zF1ZigW9iw5IoAAnG8MRvC9FBJpQcVBa6uYbwBAAMCAANzAAMkBA','AgACAgIAAxkBAAOUYqodegQscmQ0TiGrgQwSXiYXl14AAnK8MRvC9FBJjNhNceoLlCABAAMCAANzAAMkBA','AgACAgIAAxkBAAOVYqodgj8mRvXSqDEv3kTyRqvHmtcAAnO8MRvC9FBJvi3T1rluSH0BAAMCAANzAAMkBA','AgACAgIAAxkBAAOWYqodgiXMqJpKkIJFPf6iFzuxmzQAAnS8MRvC9FBJljhBPKQw-ZQBAAMCAANzAAMkBA','AgACAgIAAxkBAAOXYqodgso8Qvb-7PTiK4AkKhY_f_0AAnW8MRvC9FBJHjU80nvDICUBAAMCAANzAAMkBA','AgACAgIAAxkBAAOYYqodgoKlULHSOI-J4G31Ixl-mwIAAna8MRvC9FBJXNu8qrcc_XIBAAMCAANzAAMkBA','AgACAgIAAxkBAAOZYqodgv-n0cQngxkxskvxog98aIQAAne8MRvC9FBJqz7uNHjrKP4BAAMCAANzAAMkBA','AgACAgIAAxkBAAOaYqodgqwe466tTH0oF3C9_Ny8PRwAAni8MRvC9FBJ0xhiolmve0QBAAMCAANzAAMkBA','AgACAgIAAxkBAAObYqodggX1qcDBLrC-hq4MIYd3C_UAAnm8MRvC9FBJZcSRDPQAAU7sAQADAgADcwADJAQ','AgACAgIAAxkBAAOcYqodgm0YMrps1WL61H5Nr6eFeMkAAnq8MRvC9FBJV-8iT9quXxwBAAMCAANzAAMkBA','AgACAgIAAxkBAAOdYqodgrMxLbHrQ7sd4tHMJC4yMhQAAnu8MRvC9FBJP_PA0xyJeLsBAAMCAANzAAMkBA','AgACAgIAAxkBAAOeYqodghK2bhTmWeaWecAMigQKZfsAAny8MRvC9FBJTTW6yjdm5ikBAAMCAANzAAMkBA','AgACAgIAAxkBAAOfYqodj_9eYCJLb6a8uhKmnUwvmroAAn28MRvC9FBJeFwOJQ5TGasBAAMCAANzAAMkBA','AgACAgIAAxkBAAOgYqodj6dhc0aNMtDoIGX7mHNT7-gAAn68MRvC9FBJD5MGPTmf4g0BAAMCAANzAAMkBA','AgACAgIAAxkBAAOhYqodj8ngeqNANcLptIH7_cGmZAMAAn-8MRvC9FBJzXpa4sjpqvEBAAMCAANzAAMkBA','AgACAgIAAxkBAAOiYqodj106wSwVN01SnIhwI3oxMBIAAoC8MRvC9FBJbJXRSdPAm_gBAAMCAANzAAMkBA','AgACAgIAAxkBAAOjYqodj7hy7kP5sQ0EJwmawR-4ow4AAoG8MRvC9FBJ5GlF6s3LauQBAAMCAANzAAMkBA','AgACAgIAAxkBAAOkYqodj8A3y21vUrG2tR7B63nAlycAAoK8MRvC9FBJbYnV6bDwM2QBAAMCAANzAAMkBA','AgACAgIAAxkBAAOlYqodj5NI0FcCmmJEd9WAnRjZ9A4AAoO8MRvC9FBJ02Ufv-QU6sgBAAMCAANzAAMkBA','AgACAgIAAxkBAAOmYqodj7FemHgwYeQxY0UOWdTUQcEAAoS8MRvC9FBJ-0SW0DFJN4wBAAMCAANzAAMkBA','AgACAgIAAxkBAAOnYqodj7xjZlseSSgp9WRbs9OZiBUAAoW8MRvC9FBJfNr8caSOOg0BAAMCAANzAAMkBA','AgACAgIAAxkBAAOoYqodj40TQiPjpLE4gS12Pdr0SfYAAoa8MRvC9FBJJwfu7JAUggsBAAMCAANzAAMkBA','AgACAgIAAxkBAAOpYqodme6nvzpaV4ozvahr9pKsQlwAAoe8MRvC9FBJm9q3Ar8-sAIBAAMCAANzAAMkBA','AgACAgIAAxkBAAOqYqodmbTyexRxFxFliF_7fWIP6aIAAoi8MRvC9FBJSmKuBMWXbDwBAAMCAANzAAMkBA','AgACAgIAAxkBAAOrYqodmX1J-Ty_yh9MRIXdetzqsZoAAom8MRvC9FBJN1BGiboy6ygBAAMCAANzAAMkBA','AgACAgIAAxkBAAOsYqodmRSaIwU8k3brGiRCWocbXYsAAoq8MRvC9FBJc_eKEQABJB6AAQADAgADcwADJAQ','AgACAgIAAxkBAAOtYqodmadxZgn9pFcEQ-u1RZCB7AkAAou8MRvC9FBJxjcjjr_H1FkBAAMCAANzAAMkBA','AgACAgIAAxkBAAOuYqodmWRJk2otahj-oNxvQOhTtqwAAoy8MRvC9FBJKj_mMqA2r7MBAAMCAANzAAMkBA','AgACAgIAAxkBAAOvYqodmYJZlkvarlTa4Dwpjc7BsPgAAo28MRvC9FBJDHqP1K5f38oBAAMCAANzAAMkBA','AgACAgIAAxkBAAOwYqodmXs9bw8OHwABquUUKMm9FhhVAAKOvDEbwvRQSQABzO7oFIAb8AEAAwIAA3MAAyQE','AgACAgIAAxkBAAOxYqodmXpoRZYL4fKGejng8BqOpVAAAo-8MRvC9FBJusUrUu3_4MUBAAMCAANzAAMkBA','AgACAgIAAxkBAAOyYqodmetoL17boc1JpfLJLfkrzrMAApC8MRvC9FBJzfl4glckP9oBAAMCAANzAAMkBA','AgACAgIAAxkBAAOzYqodpGXFD04whYuI8UAMvfIeNqAAApG8MRvC9FBJ3wnixYZcx5EBAAMCAANzAAMkBA','AgACAgIAAxkBAAO0YqodpNW2gcvVQ9f04eJSX6kRYMUAApK8MRvC9FBJDrpARuKXN3wBAAMCAANzAAMkBA','AgACAgIAAxkBAAO1YqodpCcOCxEw0gb4lQ6h4sWtK3UAApO8MRvC9FBJJWcO0sBFlO0BAAMCAANzAAMkBA','AgACAgIAAxkBAAO2YqodpE4UglnDtWVpsQ2HXl4yvnsAApS8MRvC9FBJh86bkSIWgcUBAAMCAANzAAMkBA','AgACAgIAAxkBAAO3YqodpHibE8knCD4WpQG4q4Ly92kAApW8MRvC9FBJ34TLKAUqdesBAAMCAANzAAMkBA','AgACAgIAAxkBAAO4YqodpG4tuDpEC75VA33fVSlGiusAApa8MRvC9FBJkzinosj7enMBAAMCAANzAAMkBA','AgACAgIAAxkBAAO5YqodpDIeyfeID5j7Ik18jVFaTkEAApe8MRvC9FBJhquwUSJNK7gBAAMCAANzAAMkBA','AgACAgIAAxkBAAO6YqodpPlqo6w_gXIq6DK7-6GROioAApi8MRvC9FBJ8bv5yiPGNT0BAAMCAANzAAMkBA','AgACAgIAAxkBAAO7YqodpCVKhRQaa2RiEGow1upGRBcAApq8MRvC9FBJGuIWt5JhA3YBAAMCAANzAAMkBA','AgACAgIAAxkBAAO8YqodpJsk4n_XF-0NaTbiP-MjPDAAApu8MRvC9FBJwqAl8QuH_T4BAAMCAANzAAMkBA','AgACAgIAAxkBAAO9Yqodq-e5qKQwT_7lEggjyPg-A18AApy8MRvC9FBJfmRk8jGLSNcBAAMCAANzAAMkBA','AgACAgIAAxkBAAO-YqodqwiMT5c_sTuXtzZbJ2lW9CsAAp28MRvC9FBJAXELhRYoztABAAMCAANzAAMkBA','AgACAgIAAxkBAAO_Yqodqxyh67dAmTI16Br8Ef5pdq8AAp68MRvC9FBJOFJfvlgX20IBAAMCAANzAAMkBA','AgACAgIAAxkBAAPAYqodq9aJiGobwnV6iUX8oxxhmUwAAp-8MRvC9FBJ02P7toDjrx8BAAMCAANzAAMkBA','AgACAgIAAxkBAAPBYqodq9ql7bcgVfZvk0YvEVMZ9SAAAqC8MRvC9FBJgjLtf7y6mNgBAAMCAANzAAMkBA','AgACAgIAAxkBAAPCYqodqwyaM8xjfAoN0zPrI99HNBsAAqG8MRvC9FBJ4bcpg01FcZcBAAMCAANzAAMkBA','AgACAgIAAxkBAAPDYqodq1u2TM7Uwn9eV1Rcsi8ZfvIAAqK8MRvC9FBJMAyN8vx6aMoBAAMCAANzAAMkBA','AgACAgIAAxkBAAPEYqodq6JqGupOX_D9YbpcMlfL1F8AAqO8MRvC9FBJCYGbwpss-bYBAAMCAANzAAMkBA','AgACAgIAAxkBAAPFYqodq7C9EUo4vN82mhBtgvG9IjEAAqS8MRvC9FBJv0u7Vt4alz8BAAMCAANzAAMkBA','AgACAgIAAxkBAAPGYqodq-ZVAAEoGtQN_WakJh6JCwchAAKlvDEbwvRQSU94EHp1Df5-AQADAgADcwADJAQ','AgACAgIAAxkBAAPHYqodsg6CxPt-VTRkegYAAXBDiiAEAAKmvDEbwvRQScY0-yps3ZJJAQADAgADcwADJAQ','AgACAgIAAxkBAAPIYqodsowVTJNiTrOiQng9NHqEqogAAqe8MRvC9FBJRrry3roSbmkBAAMCAANzAAMkBA','AgACAgIAAxkBAAPJYqodsoNANBUPCnGpFPIpdQm-UKMAAqi8MRvC9FBJCvOHzxvNJvwBAAMCAANzAAMkBA','AgACAgIAAxkBAAPKYqodsj9Y-aQUt9eAyw89jMQJ94AAAqm8MRvC9FBJZBRlk5YT880BAAMCAANzAAMkBA','AgACAgIAAxkBAAPLYqodsmU1l6B22Y3xK-0RnLkTPKMAAqu8MRvC9FBJ4WcDFfj2LzYBAAMCAANzAAMkBA','AgACAgIAAxkBAAPMYqodstKDljsT5OJIHDIJ6N1iXscAAqq8MRvC9FBJJt5HjYFBTGQBAAMCAANzAAMkBA','AgACAgIAAxkBAAPNYqodsoBkHAER5Xm0PlKu1s5yqW0AAqy8MRvC9FBJ8PeeXOvbeVoBAAMCAANzAAMkBA','AgACAgIAAxkBAAPOYqodso8Tb3hGmAsQ61ZmUGgLrqUAAq28MRvC9FBJ_WWwBIRB0gEBAAMCAANzAAMkBA','AgACAgIAAxkBAAPPYqodss1VAmHxc-1Ud9H7-HclxuIAAq68MRvC9FBJPd3A-IDI_S4BAAMCAANzAAMkBA','AgACAgIAAxkBAAPQYqodsr-sjiYrq9L_Oo14LmiXhE0AAq-8MRvC9FBJ8I0HJUxO-XgBAAMCAANzAAMkBA','AgACAgIAAxkBAAPRYqodwBvrhS38HcOod4_sNljXpoEAArC8MRvC9FBJL5ul7TIJg3ABAAMCAANzAAMkBA','AgACAgIAAxkBAAPSYqodwIRuCNq-7lRKcCU5n6MV3IkAArG8MRvC9FBJ05Hgh1T4g7UBAAMCAANzAAMkBA','AgACAgIAAxkBAAPTYqodwIB7WrdUNBI-3y5AUR5KOr0AArK8MRvC9FBJ3HX9gUveheEBAAMCAANzAAMkBA','AgACAgIAAxkBAAPUYqodwLaEC25rVmTS4fh8uQMzs_AAArO8MRvC9FBJY5Yn47gAAeYKAQADAgADcwADJAQ','AgACAgIAAxkBAAPVYqodwHjQa067Qv3Ff4YM298hVywAArS8MRvC9FBJJMqgrInfSicBAAMCAANzAAMkBA','AgACAgIAAxkBAAPWYqodwHysQ9R1XsRSkEaw90UIutoAArW8MRvC9FBJ23q3kRl5LUYBAAMCAANzAAMkBA','AgACAgIAAxkBAAPXYqodwAF2r-vO54NmNcl11nXt3OcAAnvAMRt4MlBJoPJ7yAwCYbkBAAMCAANzAAMkBA','AgACAgIAAxkBAAPYYqodwFl20CAeJYQZNzmGWoYpj0MAAra8MRvC9FBJ073mgj9TCZYBAAMCAANzAAMkBA','AgACAgIAAxkBAAPZYqodwE2zO9islf_gA3LwPEN6OfQAAre8MRvC9FBJ3tYxQLDx9ikBAAMCAANzAAMkBA','AgACAgIAAxkBAAPaYqodwEOHpZc4vVuJAAGcv3LmxJGsAAK4vDEbwvRQSeFxyB7c8X59AQADAgADcwADJAQ','AgACAgIAAxkBAAPbYqodx_oY42BitZt09OuMrQfUiJQAArm8MRvC9FBJIQQUr76UFjoBAAMCAANzAAMkBA','AgACAgIAAxkBAAPcYqodx3GgHs1fn75xNmoAARIO90NOAAK6vDEbwvRQSexXmX2wfl0xAQADAgADcwADJAQ','AgACAgIAAxkBAAPdYqodx8O-sKCcOTk7ERKnCv6x1CcAAru8MRvC9FBJ7a7xEIlveMsBAAMCAANzAAMkBA','AgACAgIAAxkBAAPeYqodx30RJ9dPasjc4Z8VhAWbLrEAAry8MRvC9FBJv8_vf4st3D0BAAMCAANzAAMkBA','AgACAgIAAxkBAAPfYqodxzQTbUoY8fE_hUOLJBEKJMcAAr28MRvC9FBJKtrdJJuB_BABAAMCAANzAAMkBA','AgACAgIAAxkBAAPgYqodx23flbeUCJ0h00U4Eg65IdcAAr68MRvC9FBJzfIAAdY-Ala7AQADAgADcwADJAQ','AgACAgIAAxkBAAPhYqodxxQxYMjvz5QGj6U77GdwSjMAAr-8MRvC9FBJ6cggHE7SDvkBAAMCAANzAAMkBA','AgACAgIAAxkBAAPiYqodx-D4vsgdJL3FZrn66-_K2PcAAsG8MRvC9FBJ42msRuw1WyMBAAMCAANzAAMkBA','AgACAgIAAxkBAAPjYqodxwpaXmSwtsaU0FscIjYvhjAAAsC8MRvC9FBJxkXb-2d8KlEBAAMCAANzAAMkBA','AgACAgIAAxkBAAPkYqodx7NZzATPPc6CKHJ1nGceRPwAAsK8MRvC9FBJ8nn09tgEvCEBAAMCAANzAAMkBA','AgACAgIAAxkBAAPlYqod0gNffba2nHEgDLb_7CxAda0AAsO8MRvC9FBJNBrnqtz1o24BAAMCAANzAAMkBA','AgACAgIAAxkBAAPmYqod0n3MBZKoA4NBSP2rQVAtzXwAAsS8MRvC9FBJ3PO8JzZ03AEBAAMCAANzAAMkBA','AgACAgIAAxkBAAPnYqod0h1TbAbzO4GRUJCQHBfqqmYAAsW8MRvC9FBJtUTQoPuV5tQBAAMCAANzAAMkBA','AgACAgIAAxkBAAPoYqod0htuE3owJE8jDsqpTKdECl8AAsa8MRvC9FBJvMnaql3uspwBAAMCAANzAAMkBA','AgACAgIAAxkBAAPpYqod0shSy6eE4qT09m44sQPfYE0AAse8MRvC9FBJFCRdTb3QxhwBAAMCAANzAAMkBA','AgACAgIAAxkBAAPqYqod0qmYO4x9THSslyDJwMxBxgYAAsi8MRvC9FBJDgkCvVSUXwwBAAMCAANzAAMkBA','AgACAgIAAxkBAAPrYqod0k1AbeTZ6X8zMz30gRsXcxMAAsm8MRvC9FBJuHEZ2VrsJVIBAAMCAANzAAMkBA','AgACAgIAAxkBAAPsYqod0nf6JgWc1m2M44p6D0Mp_pUAAsq8MRvC9FBJnplj1-GfuH4BAAMCAANzAAMkBA','AgACAgIAAxkBAAPtYqod0uCD9-rfW1Q1xb1sd0EV5EEAAsu8MRvC9FBJJ_dcUdJo8y0BAAMCAANzAAMkBA','AgACAgIAAxkBAAPuYqod0nt4xa-Gk2Oa75EUYfgxjO0AAsy8MRvC9FBJOSDh6koXz6UBAAMCAANzAAMkBA','AgACAgIAAxkBAAPvYqod0k-rvPnxCEw9TG61L-fnkLMAAs28MRvC9FBJ3ZUrEpUBLyYBAAMCAANzAAMkBA','AgACAgIAAxkBAAPwYqod0u67Q8ai6XrmixxB5PlZ8SUAAs68MRvC9FBJgjTIuzdEUdQBAAMCAANzAAMkBA']



def send_cat(update: Update, context: CallbackContext) -> None:
    global missed_messages_counter
    print(update.message.date)
    print(datetime.datetime.now(datetime.timezone.utc))
    print(missed_messages_counter)
    print((update.message.date - datetime.datetime.now(datetime.timezone.utc)))
    if (datetime.datetime.now(datetime.timezone.utc) - update.message.date) > datetime.timedelta(minutes=5) :
        missed_messages_counter += 1
        print("Counted")
        return
    if missed_messages_counter == 1:
        # update.message.chat.send_message(f"Missed one cat :<")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Missed one cat :<")
    elif missed_messages_counter > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Missed {missed_messages_counter} cats :<")
        # update.message.chat.send_message(f"Missed {missed_messages_counter} cats :<")

    missed_messages_counter = 0

    request_url = 'https://api.thecatapi.com/v1/images/search'

    headers = {'x-api-key': os.getenv("CATAPI_KEY")}
    r = requests.get(request_url, headers=headers)
    print(r.text)
    rj = r.json()
    cat_img_url = rj[0]['url']
    if 'breeds' in rj[0]:
        if len(rj[0]['breeds']) > 0:
            if 'description' in rj[0]['breeds'][0]:


                print('description')
                update.message.reply_photo(cat_img_url, caption=rj[0]['breeds'][0]['description'][:1024])
                return

        update.message.reply_photo(cat_img_url)

# def toggle_rms_receiver(update: Update, context: CallbackContext) -> None:
#     global is_rms_received
#     is_rms_received = not is_rms_received
#     if is_rms_received:
#         context.bot.send_message(update.message.chat_id, "Send the images!")
#         return
#     context.bot.send_message(update.message.chat_id, "Don't send the images!")


def send_rms(update: Update, context: CallbackContext) -> None:
    print(update.message.date)
    print(datetime.datetime.now(datetime.timezone.utc))
    print((update.message.date - datetime.datetime.now(datetime.timezone.utc)))
    if (datetime.datetime.now(datetime.timezone.utc) - update.message.date) > datetime.timedelta(minutes=5) :
        missed_messages_counter += 1
        print("Counted")
        return


    update.message.reply_photo(random.choice(photo_id_list))


# def save_photo_id(update: Update, context: CallbackContext) -> None:
#     global is_rms_received
#     if is_rms_received:
#         with open('photoids.txt', 'a') as id_file:
#             print(update.message.photo[0].file_id, file=id_file)


def help_command(update: Update, context: CallbackContext) -> None:
    htext = '''
Welcome
Send /cat to get a cat'''
    update.message.reply_text(htext)


def main():
    updater = Updater(os.getenv("TOKEN"))

    PORT = os.environ.get('PORT')
    NAME = "l8doku-telegram-bot2"
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", help_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("cat", send_cat))
    dispatcher.add_handler(CommandHandler("cat2", send_cat))
    dispatcher.add_handler(CommandHandler("cat3", send_cat))
    dispatcher.add_handler(CommandHandler("rms", send_rms))
    # dispatcher.add_handler(CommandHandler("toggle_rms", toggle_rms_receiver))
    # dispatcher.add_handler(CommandHandler("toggle_rms", toggle_rms_receiver))
    
    # dispatcher.add_handler(MessageHandler(Filters.photo, save_photo_id))
    
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=f"https://{NAME}.herokuapp.com/{os.getenv("TOKEN")}")

    updater.idle()


if __name__ == '__main__':
    main()