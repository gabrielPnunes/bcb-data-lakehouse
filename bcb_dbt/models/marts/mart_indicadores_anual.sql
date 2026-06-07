select
    s.ano,
    s.media_selic,
    i.media_ipca,
    c.media_cdi,
    ca.media_cambio,
    ca.max_cambio,
    ca.min_cambio,
    round(s.media_selic - i.media_ipca, 2) as taxa_real,
    case
        when s.media_selic >= 12 then 'Alta'
        when s.media_selic >= 8  then 'Moderada'
        else 'Baixa'
    end as classificacao_selic
from {{ ref('stg_selic_anual') }}       s
left join {{ ref('stg_ipca_anual') }}   i  on s.ano = i.ano
left join {{ ref('stg_cdi_anual') }}    c  on s.ano = c.ano
left join {{ ref('stg_cambio_anual') }} ca on s.ano = ca.ano
order by s.ano
