select
    year_of_birth as birth_year,
    count(distinct person_id) as patient_count
from {{ source('omop', 'person') }}
group by year_of_birth
