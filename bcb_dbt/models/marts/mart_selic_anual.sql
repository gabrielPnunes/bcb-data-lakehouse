select
    ano,
    media_selic,
    case
        when media_selic >= 12 then 'Alta'
        when media_selic >= 8  then 'Moderada'
        else 'Baixa'
    end as classificacao_selic
from {{ ref('stg_selic_anual') }}
order by ano