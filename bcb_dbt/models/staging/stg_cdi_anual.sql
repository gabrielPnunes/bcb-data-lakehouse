select
    ano,
    round(cast(media_cdi as numeric), 2) as media_cdi
from {{ source('gold', 'gold_cdi_anual') }}
