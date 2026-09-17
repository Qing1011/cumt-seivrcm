# Contact matrices

The contact-matrix data are organized by state:

- `6_california/contact_matrix/`
- `37_north_carolina/contact_matrix/`

The matrices represent synthetic daily contacts by race/ethnicity in household,
school, community, and workplace settings. They were developed using methods from
[Mistry et al. (2021)](https://www.nature.com/articles/s41467-020-20544-y) and
[Aleta et al. (2022)](https://www.pnas.org/doi/full/10.1073/pnas.2112182119).

Each state directory contains:

- `household_*.csv`
- `school_*.csv`
- `community_*.csv`
- `workplace_pandemic_*.csv`
- `workplace_prepandemic_*.csv`
- `full_matrix_pandemic_*.csv`
- `full_matrix_prepandemic_*.csv`

Columns represent the race/ethnicity of the individual and rows represent the
race/ethnicity of the contact. Each column sums to the average number of daily
contacts for an individual in that racial/ethnic group. Contacts are not weighted
by duration or intensity.

The full matrices combine the setting-specific layers:

```text
pre-pandemic = p1 × school + p2 × workplace_prepandemic + community + household
pandemic     = p2 × workplace_pandemic + community + household
```

Here, `p1` is the proportion of the population aged 5–17 and `p2` is the
proportion participating in the workforce. The model pipeline uses the supplied
full pandemic matrices and normalizes them in `notebook/01_contact_matrix.ipynb`.
