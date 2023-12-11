# Generated by Django 4.2.3 on 2023-08-02 20:03

from django.db import migrations


# The MITRE handles the CVE_ID and the Summary
# Syntax:
# > CALL mitre_upsert(%(cve)s, %(created)s, %(updated)s, %(summary)s, %(path)s);
MITRE_SQL = """
CREATE PROCEDURE mitre_upsert(
    cve text,
    created timestamptz,
    updated timestamptz,
    summary text,
    path jsonb
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- add a new CVE or update an existing one
    INSERT INTO opencve_cves (id, created_at, updated_at, cve_id, vendors, cwes, sources, summary, cvss)
    VALUES(uuid_generate_v4(), created, updated, cve, '[]', '[]', path, summary, '{}')
    ON CONFLICT (cve_id) DO
    UPDATE SET
      updated_at = updated,
      summary = EXCLUDED.summary,
      sources = opencve_cves.sources || path;
END;
$$;
"""
MITRE_REVERSE_SQL = """
DROP PROCEDURE mitre_upsert(
    cve text,
    created timestamptz,
    updated timestamptz,
    summary text,
    path jsonb
);"""

# The NVD handles the CVE_ID, the CVSS, the Vendors and the CWEs
# Syntax:
# > CALL nvd_upsert(%(cve)s, %(created)s, %(updated)s, %(cvss)s, %(vendors)s, %(cwes)s, %(path)s);
NVD_SQL = """
CREATE PROCEDURE nvd_upsert(
    cve text,
    created timestamptz,
    updated timestamptz,
    cvss jsonb,
    vendors jsonb,
    cwes jsonb,
    path jsonb
)
LANGUAGE plpgsql
AS $$
DECLARE
   _cwe       text;
   _vendors   text;
   _vendor    text;
   _vendor_id text;
   _product   text;
BEGIN
    -- add a new CVE or update an existing one
    INSERT INTO opencve_cves (id, created_at, updated_at, cve_id, vendors, cwes, sources, cvss)
    VALUES(uuid_generate_v4(), created, updated, cve, vendors, cwes, path, cvss)
    ON CONFLICT (cve_id) DO
    UPDATE SET
      updated_at = updated,
      cvss = EXCLUDED.cvss,
      vendors = EXCLUDED.vendors,
      cwes = EXCLUDED.cwes,
      sources = opencve_cves.sources || path;

    -- add the new CWEs
    FOR _cwe IN SELECT * FROM json_array_elements_text(cwes::json)
    LOOP
      INSERT INTO opencve_cwes (id, created_at, updated_at, cwe_id)
      VALUES(uuid_generate_v4(), NOW(), NOW(), _cwe)
      ON CONFLICT (cwe_id) DO NOTHING;
    END LOOP;

    -- add the new Vendors & Products
    FOR _vendors IN SELECT * FROM json_array_elements_text(vendors::json)
    LOOP
      _vendor := split_part(_vendors, '$PRODUCT$', 1);
      _product := split_part(_vendors, '$PRODUCT$', 2);

      -- insert the vendor
      INSERT INTO opencve_vendors (id, created_at, updated_at, name)
      VALUES(uuid_generate_v4(), NOW(), NOW(), _vendor)
      ON CONFLICT (name) DO NOTHING;

      -- retrieve its ID
      SELECT id INTO _vendor_id FROM opencve_vendors WHERE name = _vendor;

      -- insert the product
      INSERT INTO opencve_products (id, created_at, updated_at, vendor_id, name)
      VALUES(uuid_generate_v4(), NOW(), NOW(), _vendor_id::uuid, _product)
      ON CONFLICT (name, vendor_id) DO NOTHING;
    END LOOP;
END;
$$;
"""
NVD_REVERSE_SQL = """
DROP PROCEDURE nvd_upsert(
    cve text,
    created timestamptz,
    updated timestamptz,
    cvss jsonb,
    vendors jsonb,
    cwes jsonb,
    path jsonb
);"""


class Migration(migrations.Migration):

    dependencies = [
        ('cves', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(sql=NVD_SQL, reverse_sql=NVD_REVERSE_SQL),
        migrations.RunSQL(sql=MITRE_SQL, reverse_sql=MITRE_REVERSE_SQL),
    ]