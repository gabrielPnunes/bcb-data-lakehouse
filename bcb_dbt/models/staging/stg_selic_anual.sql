select
    ano,
    round(cast(media_selic as numeric), 2) as media_selic
from {{ source('gold', 'gold_selic_anual') }}