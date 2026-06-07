select
    ano,
    round(cast(media_cambio as numeric), 4) as media_cambio,
    round(cast(max_cambio   as numeric), 4) as max_cambio,
    round(cast(min_cambio   as numeric), 4) as min_cambio
from {{ source('gold', 'gold_cambio_anual') }}
