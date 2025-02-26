# Clean the resale data by renaming flat_type and flat_model items to avoid capital and - problems
def clean_data(resale):
    #
    resale.insert(0, "year", resale["month"].str.split('-').str[0], True)
    #
    resale['remaining_lease'] = (99 + resale['lease_commence_date'].astype(int)) - resale['year'].astype(int)
    # lease_commence_date convert to str type
    resale['lease_commence_date'] = resale['lease_commence_date'].astype(str)
    #
    resale['flat_type'] = resale['flat_type'].replace('MULTI-GENERATION', 'MULTI GENERATION')
    #
    flat_model_replace = {'NEW GENERATION': 'New Generation', 'SIMPLIFIED': 'Simplified', 'STANDARD': 'Standard',
                          'MODEL A-MAISONETTE': 'Model A-Maisonette', 'MULTI GENERATION': 'Multi Generation',
                          'IMPROVED-MAISONETTE': 'Improved-Maisonette', '2-ROOM': '2-room', 'MODEL A': 'Model A',
                          'MAISONETTE': 'Maisonette', 'IMPROVED': 'Improved', 'TERRACE': 'Terrace',
                          'PREMIUM APARTMENT': 'Premium Apartment', 'APARTMENT': 'Apartment'}
    resale['flat_model'] = resale['flat_model'].replace(flat_model_replace)
    return resale