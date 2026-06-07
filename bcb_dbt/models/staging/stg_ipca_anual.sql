select
    ano,
    round(cast(media_ipca as numeric), 2) as media_ipca
from {{ source('gold', 'gold_ipca_anual') }}
