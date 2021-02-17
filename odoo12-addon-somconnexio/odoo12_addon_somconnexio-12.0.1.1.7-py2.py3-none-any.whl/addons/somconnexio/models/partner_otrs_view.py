from odoo import models, tools


class PartnerOTRSView(models.Model):
    _name = 'partner.otrs.view'
    _auto = False

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
                %s
            )
        ''' % (
            self._table, self._query()
        ))

    def _query(self):
        return '''
            SELECT DISTINCT ON (partner.id)
                partner.ref AS customerid,
                partner.ref AS partner_id,
                COALESCE(partner.firstname, '-'::character varying) AS first_name,
                COALESCE(partner.lastname, '-'::character varying) AS name,
                partner.cooperator_register_number::character varying AS partner_number,
                partner.effective_date AS date_partner,
                partner.cooperator_end_date AS date_partner_end,
                CASE
                    WHEN partner.active = true THEN 1
                    WHEN partner.active = false THEN 2
                    ELSE NULL::integer
                END AS active,
                partner.birthdate_date AS birthday,
                CASE
                    WHEN partner.is_company = true THEN 'organization'
                    ELSE 'person'
                END AS party_type,
                'eu_vat' AS identifier_type,
                partner.vat AS identifier_code,
                partner.email AS email,
                CASE
                    WHEN partner.lang::text = 'ca_ES'::text THEN 'ca'::character varying
                    WHEN partner.lang::text = 'es_ES'::text THEN 'es'::character varying
                    ELSE NULL::character varying
                END AS language,
                partner.street AS address,
                partner.city AS city,
                partner.zip AS zip,
                upper(country.code) AS country_code,
                country.name AS country,
                upper(country.code) || '-' || upper(state.code) AS subdivision_code,
                state.name AS subdivision
            FROM res_partner partner
            LEFT JOIN res_country country ON partner.country_id = country.id
            LEFT JOIN res_country_state state ON partner.state_id = state.id
            WHERE partner.parent_id IS NULL AND partner.ref IS NOT NULL
            ORDER BY partner.id
        '''
